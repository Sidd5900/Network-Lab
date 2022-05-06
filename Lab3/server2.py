#Multithreaded HTTP server to handle multiple requests

import socket
import time
import threading
import json

#import configurations
configuration = json.load(open('configuration.json'))

#Handle request of clients
def handle_request(request):
    print("Request under process : ")
    time.sleep(10)
    
    headers = request.split('\n')
    filename = headers[0].split()[1]

    if filename == '/':
        filename = configuration["defaultFile"]

    try:
        fin = open('.'+filename)
        content = fin.read()
        fin.close()

        response = 'HTTP/1.0 200 OK\n\n' + content
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

    return response

#get the client request from the connection socket and pass the request to handle_client
def handle_client(conn,addr):
    if addr[0] not in configuration["blockedIP"] :
        request = conn.recv(1024).decode()
        print(request)

        # Return an HTTP response
        response = handle_request(request)
        conn.sendall(response.encode())
        conn.close()

    # when IP blocked, close the connection
    else:
        print("Connection Refused as the IP is blocked! ",addr[0])
        response = 'HTTP/1.0 403 UNAUTHORISED\n\nYou are blocked!'
        conn.sendall(response.encode())
        conn.close()

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5058

# Create server socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((SERVER_HOST, SERVER_PORT))
serverSocket.listen()
print("The server is ready to receive on port", SERVER_PORT)

while True:
    # Wait for client connections
    connectionSocket, addr = serverSocket.accept()
    print("connection received from client: ", addr)
    #check for active connections
    if(threading.activeCount()-1 < configuration["maxThreads"]):
        thread= threading.Thread(target=handle_client,args=(connectionSocket,addr))
        thread.start()
        print("Client requests active: ",(threading.activeCount()-1))
    else:
        print("Connection Refused as maximum connection limit reached ")
        response = 'HTTP/1.0 503 Overloaded Server \n\n Maximum Connection limit reached!'
        connectionSocket.sendall(response.encode())
        connectionSocket.close()
