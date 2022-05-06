#Single client HTTP server

from socket import *

def startServer():
	#create Socket
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive on PORT",serverPort)
    while 1:
        connectionSocket, addr = serverSocket.accept()
        print("connection received from client", addr)
       
        # Get the client request
        request = connectionSocket.recv(1024).decode()
        print(request)

        # Parse HTTP headers
        headers = request.split('\n')
        filename = headers[0].split()[1]

        #default file
        if filename == '/':
            filename = '/index.html'

        #Get the content of the file
        try:
            fin = open('.' + filename)
            content = fin.read()
            fin.close()
            response = 'HTTP/1.0 200 OK\n\n' + content
            
        except FileNotFoundError:
            response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

        connectionSocket.sendall(response.encode())

        connectionSocket.close()


if __name__ == '__main__':
    startServer()



