# Importa o módulo socket
from socket import *
import sys  # Necessário para encerrar o programa

# Cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepara o socket do servidor
#Fill in start
serverSocket.bind(('', 6789))   # Associa o socket a todas as interfaces locais e porta 6789
serverSocket.listen(1)          # Coloca o servidor em modo de escuta
#Fill in end

print("Servidor pronto! Acesse: http://localhost:6789/index.html")

while True:
    # Estabelece a conexão
    print('Ready to serve...')
    #Fill in start
    connectionSocket, addr = serverSocket.accept()  # Aceita a conexão do cliente
    #Fill in end
    try:
        # Recebe a mensagem do cliente (requisição HTTP)
        #Fill in start
        message = connectionSocket.recv(1024).decode()
        #Fill in end

        filename = message.split()[1]
        f = open(filename[1:])
        #Fill in start
        outputdata = f.read()  # Lê o conteúdo do arquivo
        f.close()
        #Fill in end

        # Envia a linha de status do cabeçalho HTTP
        #Fill in start
        connectionSocket.send(b"HTTP/1.1 200 OK\r\n\r\n")
        #Fill in end

        # Envia o conteúdo do arquivo ao cliente
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # Fecha a conexão com o cliente
        connectionSocket.close()

    except IOError:
        # Envia mensagem de erro 404 se o arquivo não for encontrado
        #Fill in start
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.send(b"<html><body><h1>404 Not Found</h1></body></html>")
        #Fill in end

        # Fecha o socket do cliente
        #Fill in start
        connectionSocket.close()
        #Fill in end

serverSocket.close()
sys.exit()  # Encerra o programa
