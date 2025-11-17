# Importa o módulo socket
from socket import *
import sys  # Necessário para encerrar o programa

# Cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepara o socket do servidor
serverSocket.bind(('', 6789))
serverSocket.listen(1)

while True:
    # Espera uma conexão
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        # Recebe a mensagem do cliente (requisição HTTP)
        message = connectionSocket.recv(1024).decode()

        # Ignora requisições malformadas
        if len(message.split()) < 2:
            connectionSocket.close()
            continue

        filename = message.split()[1]  # Ex: "/index.html"
        f = open(filename[1:], "r")    # Remove o '/' do início
        outputdata = f.read()

        # Envia o cabeçalho de resposta HTTP 200 (OK)
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # Envia o conteúdo do arquivo
        connectionSocket.sendall(outputdata.encode())

        # Fecha a conexão com o cliente
        connectionSocket.close()

    except IOError:
        # Arquivo não encontrado — envia erro 404
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Encerra o programa