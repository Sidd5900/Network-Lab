# Single client HTTP server

from socket import *


def startServer():
    # create Socket
    serverPort = 8080
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive on PORT", serverPort)
    while 1:
        connectionSocket, addr = serverSocket.accept()
        print("connection received from client", addr)

        # Get the client request
        # receive in bytes and then convert to utf-8
        request = connectionSocket.recv(1024).decode()
        print(request)
        request = request.upper()
        # send in bytes
        connectionSocket.sendall(request.encode())
        connectionSocket.close()


if __name__ == '__main__':
    startServer()



