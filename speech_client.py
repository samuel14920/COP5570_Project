import time
import os
import threading
import socket
import speech_recognition as s_r
r = s_r.Recognizer()
my_mic = s_r.Microphone(device_index=0)


# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


def speak(message):
    if ':' in message:
        cmd = 'say ' + message.split(':')[0] + \
            'say' + ' '.join(message.split(':')[1:])
    else:
        cmd = 'say ' + message
    os.system(cmd)


def write():
    while True:
        time.sleep(1)
        flag = input("choose 'typing' or 'speaking'\n")
        if (flag == "typing"):
            message = input('typing input\n')
        elif flag == "speaking":
            print("speak\n")
            with my_mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            message = r.recognize_google(audio)
        message = username + ': ' + message
        client.send(message.encode())


def receive():
    while True:
        try:
            message = client.recv(2048).decode()
            #message = decrypt(message)
            if message != 'USR':
                print(message)
                speak(message)
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
