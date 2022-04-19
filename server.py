import socket
import threading


serverHost = '127.0.0.1'
serverPort = 5555
bytesReceive = 2048

# Server binding for serverHost and serverPort with IPv4 TCP - STREAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((serverHost, serverPort))
server.listen()
usernames = []
connections = []

def encrypt(encryption, message):
    #this will be a kind of switch statement for the different encryptions
    return message
def decrypt(encryption, message):
    #same for decryptions
    return message
def accept_users():
    while True:
        print("Server Listening...")
        conn, address = server.accept()

        conn.send('USR'.encode())
        connections.append(conn)

        username = conn.recv(bytesReceive).decode()
        usernames.append(username)

        print("Connected from address " + str(address) + " with username " + username + ".")

        broadcast((username + " joined the chat.").encode())
        conn.send('Welcome to the chat room!'.encode())

        thread = threading.Thread(target=handle_user, args=(conn,))
        thread.start()


def broadcast(msg):
    for client in connections:
        try:
            #encrypt here later
            client.send(msg)
        except:
            if client in connections:
                connections.remove(client)


def handle_user(client):
    client.send("Welcome to the chat!".encode())
    while True:
        message = client.recv(bytesReceive)
        if message:
            # print(decrypt(message))
            broadcast(message)
        else:
            username = usernames[connections.index(client)]
            connections.remove(client)
            client.close()
            broadcast((username + ' has left the chat,').encode())
            usernames.remove(username)
            break

accept_users()
