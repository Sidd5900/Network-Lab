import threading
import socket
import csv
host = '0.0.0.0'
port = 8050


# function which takes client socket and disease name as parameter and sends the corresponding medicine to the client
def sendPrescription(client, message):
    # open csv file and read the records one by one
    file = open("prescription.csv")
    csvreader = csv.reader(file)
    # skip the first row of the csv file
    next(csvreader)
    flag = 0
    for row in csvreader:
        # when disease name in the message matches with some entry in the csv file, send corresponding medicine name
        if row[0].lower() == message.lower():
            client.send(("Medicine: " + row[1]).encode())
            flag = 1
    # if disease name not in the csv list
    if flag == 0:
        client.send("Data not found in the server".encode())
    file.close()


# function to handle requests of a client
def handleClient(client, addr):
    while True:
        try:
            # receive message from client and send them the prescription
            message = client.recv(1024).decode()
            sendPrescription(client, message)
        except:
            # when user closes the chat
            print(f'Client {addr} left the chat')
            client.close()
            break


# Initialize the server
def startServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen()
    print('Server is running and listening on PORT:', port)
    while True:
        # accept connection requests from the clients
        connectionSocket, addr = serverSocket.accept()
        print("Connection received from client", addr)

        # create thread to handle the messages from the client
        thread = threading.Thread(target=handleClient, args=(connectionSocket, addr))
        thread.start()


if __name__ == "__main__":
    startServer()
