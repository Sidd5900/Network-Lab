import threading
import socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Start connection to the server to send and receive messages
def startClient():
    # Connect to the server
    clientSocket.connect(('192.168.56.1', 8050))
    while True:
        try:
            # take disease name as input from the client and send it to the server
            message = input("Enter the name of disease/ailment: ")
            clientSocket.send(message.encode('utf-8'))

            # print the message received from the server
            message = clientSocket.recv(1024)
            print(message.decode('utf-8'))
        except:
            print('Error!')
            clientSocket.close()
            break

if __name__ == "__main__":
    startClient()
