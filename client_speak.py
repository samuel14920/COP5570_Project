import socket
import threading
#import os


# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def encrypt(encryption, message):
    #this will be a kind of switch statement for the different encryptions
    return message
def decrypt(encryption, message):
    #same for decryptions
    return message

#def speak(message):
#    if ':' in message:
#        cmd = 'say ' + message.split(':')[0] + 'say' +  ' '.join(message.split(':')[1:])
#    else:
#        cmd = 'say ' + message
#    os.system(cmd)”“”

def write():
    while True:
        message = input('')
        message = username + ': ' + message
        #message = encrypt(message)
        client.send(message.encode())

def receive():
    while True:
        try:
            message = client.recv(2048).decode()
            #message = decrypt(message)
            if message != 'USR':
                print(message)
                #speak(message)
            else:
                # encrypt(username.encode('ascii')
                client.send(username.encode())
        except:
            print("Connection Error")
            client.close()
            break




username = input("Select Username: ")

receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

receive_thread.start()
write_thread.start()
