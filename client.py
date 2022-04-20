import socket
import threading
import os
import time
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
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
outstandingMessages = set()
# START OF ACTUAL PROGRAM

# Connecting To Server with IPv4 TCP - STREAM
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serverHost, serverPort))
startEncryption, endEncryption = 0, 0
# encryptMessage(encryption, mode, message, key=bytes(16), iv=bytes(16), Nonce=bytes(32))
# encryptMessage(encryption, mode, message, key=bytes(16))

client.settimeout(0.5)


def write():
    while True:
        try:
            message = input('-->')

            if message.endswith(".txt"):
                message_file = open(message, encoding="utf8")
                client.send(message.encode("utf-8"))
                l = message_file.read(bytesReceive)
                while (l):
                    client.send(l.encode("utf-8"))
                    l = message_file.read(bytesReceive)
                message_file.close()
            else:
                message = username + ': ' + message
                outstandingMessages.add(message)
            startEncryption = time.perf_counter_ns()
            # for i in range(1000):
            #     encrypted_message = encryptMessage(
            #         "AES", "CBC", message, getKeyOfLength(16))
            encrypted_message = encryptMessage(
                "AES", "CBC", message, getKeyOfLength(16))
            endEncryption = time.perf_counter_ns()
            print(endEncryption - startEncryption)
            client.send(encrypted_message)
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            print("Connection Error")
            client.close()
            break


def receive():
    while True:
        try:
            message = client.recv(bytesReceive).decode()
            # message = decrypt(message)
            if message in outstandingMessages:
                # endEncryption = time.time_ns()
                outstandingMessages.remove(message)
                # print(endEncryption - startEncryption)
            if message != 'USR':
                print(message)
                # speak(message)
            else:
                # encrypt(username.encode('ascii')
                client.send(username.encode())
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            print("Connection Error")
            client.close()
            break


username = input("Select Username: ")

receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

try:
    receive_thread.start()
    write_thread.start()
except KeyboardInterrupt:
    receive_thread.join()
    write_thread.join()
    exit(0)
