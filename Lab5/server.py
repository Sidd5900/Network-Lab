import threading
import socket
host = '0.0.0.0'
port = 8000

# To store the active client sockets
clients = []

# To store corresponding usernames of the clients
usernames = []


# send message to all the clients
def broadcast(message):
    for client in clients:
        client.send(message)


# receive messages from a client and send it to all the clients
def handleClient(client, addr):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            username = usernames[index]
            clients.remove(client)
            client.close()
            broadcast(f'{username} has left the chat room!'.encode('utf-8'))
            usernames.remove(username)
            break


# Initialize the server
def startServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen()
    print('Server is running and listening on PORT:',port)
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Connection received from client", addr)

        # ask for username from the client
        connectionSocket.send('Enter your username: '.encode('utf-8'))

        # store the client's information
        username = connectionSocket.recv(1024).decode()
        usernames.append(username)
        clients.append(connectionSocket)
        print('Username of the client: ', username)
        broadcast(f'{username} joined the chat room'.encode('utf-8'))
        connectionSocket.send('Connected to the chat room...'.encode('utf-8'))

        # create thread to handle the messages from the client
        thread = threading.Thread(target=handleClient, args=(connectionSocket,addr))
        thread.start()


if __name__ == "__main__":
    startServer()
