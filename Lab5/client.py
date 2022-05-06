import threading
import socket

username = input('Enter your username: ')
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# receive messages from the server
def clientReceive():
    # receive the first message from the server asking for username
    try:
        message = clientSocket.recv(1024)
        serverMessage = 'Enter your username: '.encode('utf-8')

        # send the username to the server
        if message == serverMessage:
            clientSocket.send(username.encode('utf-8'))
    except:
        print('Error!')
        clientSocket.close()
        return

    # receive other messages from the server and print it
    while True:
        try:
            message = clientSocket.recv(1024)
            print(message.decode('utf-8'))
        except:
            print('Error!')
            clientSocket.close()
            break


# Send the messages of the client to the server so that server could broadcast it to all other clients
def clientSend():
    while True:
        message = f'{username}: {input("")}'
        clientSocket.send(message.encode('utf-8'))


# Start connection to the server to send and receive messages
def startClient():
    # Connect to the server
    clientSocket.connect(('192.168.56.1', 8000))

    # Create threads for receiving and sending messages
    receiverThread = threading.Thread(target=clientReceive)
    receiverThread.start()
    senderThread = threading.Thread(target=clientSend)
    senderThread.start()


if __name__ == "__main__":
    startClient()
