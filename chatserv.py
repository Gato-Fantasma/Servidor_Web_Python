from socket import *
import sys  # Necessário para encerrar o programa

# Cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepara o socket do servidor
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print(f'Servidor ativo em http://127.0.0.1:{serverPort}')

while True:
    # Estabelece a conexão
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        # Recebe a mensagem do cliente (requisição HTTP)
        message = connectionSocket.recv(1024).decode()
        print("Mensagem recebida:", repr(message))

        # Evita erro caso a requisição venha vazia
        if not message:
            connectionSocket.close()
            continue

        filename = message.split()[1]
        if filename == '/':
            filename = '/index.html'  # Página padrão

        # Abre o arquivo solicitado
        f = open(filename[1:], 'r', encoding='utf-8')
        outputdata = f.read()

        # Envia cabeçalho HTTP 200 OK
        connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')

        # Envia o conteúdo do arquivo
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        # Caso o arquivo não exista, envia erro 404
        connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        connectionSocket.send(b'<html><body><h1>404 Not Found</h1></body></html>\r\n')
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Encerra o programa
