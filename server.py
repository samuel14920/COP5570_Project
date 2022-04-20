import socket
import threading
from Encryption_Algos import *
# KEYS
# key_32 = [247, 243, 40, 10, 220,  77, 213,  52,  44, 151,  50, 121, 236,  88,  68,  68,
#           48, 121, 186, 180, 156, 196, 131, 249,  48,  35,  28, 101,  69,  11, 195, 208]
# key_16 = [120, 31, 182, 66, 209, 146, 220,
#           175, 238, 56, 52, 145, 154, 31, 146, 171]
#
# Initialization Vectors
# IV_32 = [174, 138, 140,  75, 123,  99, 175, 145, 197, 135, 142, 155, 139, 132, 122,   8,
#             161, 145,  56, 199, 226, 147, 149, 139,  96,  14,  43, 115, 220, 210, 187, 194]
# IV_16 = [50, 194, 253, 226, 253,   5,  43,
#          155,   3, 101,  43, 242,  85,  88,  86,  59]
# IV_8 = [50, 194, 253, 226, 253, 5, 43, 155]

# Nonces
# Nonce_32 = [17, 129, 156,  42,  91,  54, 247,  11, 196, 105, 167,  21, 136, 190, 207,  27,
#             46, 245, 132,  20, 246,  48,  50, 254,  45, 175, 123, 246,  67, 253, 236, 103]
# Nonce_16 = [108,  43,  46, 150,  28, 161, 231,
#                101, 228,   9,  90,  35,  87,  97,  67, 185]


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
    # this will be a kind of switch statement for the different encryptions
    return message


def decrypt(encryption, message):
    # same for decryptions
    return message


def accept_users():
    try:
        while True:
            print("Server Listening...")
            conn, address = server.accept()

            conn.send('USR'.encode())
            connections.append(conn)

            username = conn.recv(bytesReceive).decode()
            usernames.append(username)

            print("Connected from address " + str(address) +
                  " with username " + username + ".")

            broadcast((username + " joined the chat.").encode())
            conn.send('Welcome to the chat room!'.encode())

            thread = threading.Thread(target=handle_user, args=(conn,))
            thread.start()
    except KeyboardInterrupt:
        print('interrupted!')
        server.close()
        exit(0)


def broadcast(msg):
    for client in connections:
        try:
            # encrypt here later
            client.send(msg)
        except:
            if client in connections:
                connections.remove(client)


def handle_user(client):
    # client.send("Welcome to the chat!".encode())
    while True:
        message = client.recv(bytesReceive)
        #message = message.decode()
        #decryptMessage(ciphertext, encryption, mode, key=bytes(16))
        message = decryptMessage(message, "AES", "CBC", getKeyOfLength(16))
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
