# Importa o módulo socket
from socket import *
import sys # Necessário para encerrar o programa

# Cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepara o socket do servidor
serverSocket.bind(('', 6789))       # Associa o socket a todas as interfaces locais e porta 6789
serverSocket.listen(1)              # Coloca o servidor em modo de escuta, aceitando 1 conexão por vez

print("Servidor pronto! Acesse: http://localhost:6789/index.html")

while True:
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()

        # Mostra o que chegou (para debug)
        print("Mensagem recebida:", repr(message))

        # Se a mensagem for vazia ou incompleta, ignora
        if not message or len(message.split()) < 2:
            connectionSocket.close()
            continue

        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        connectionSocket.send(b"HTTP/1.1 200 OK\r\n\r\n")
        connectionSocket.sendall(outputdata.encode())
        connectionSocket.close()
    except IOError:
    # Envia mensagem de erro 404 se o arquivo não for encontrado
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.send(b"<html><body><h1>404 Not Found</h1></body></html>")


    # Fecha o socket do cliente



serverSocket.close()
sys.exit() # Encerra o programa