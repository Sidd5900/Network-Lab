from socket import *

def startClient():
    #print("started client")
    serverPort = 8080
    serverName= '127.0.0.1'
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    #send in bytes
    sentence = input("Enter a sentence")
    print(sentence)
    sentence = sentence.encode()
    clientSocket.sendall(sentence)

    #received in bytes, then encoded to utf-8
    msentence = clientSocket.recv(1024).decode()
    print("From server", msentence)
    clientSocket.close()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startClient()