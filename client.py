import socket
import threading
import os
import time
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

serverHost = '127.0.0.1'
serverPort = 5555
bytesReceive = 2048
# KEYS
# key_32 = [247, 243, 40, 10, 220,  77, 213,  52,  44, 151,  50, 121, 236,  88,  68,  68,
#           48, 121, 186, 180, 156, 196, 131, 249,  48,  35,  28, 101,  69,  11, 195, 208]
# key_16 = [120, 31, 182, 66, 209, 146, 220,
#           175, 238, 56, 52, 145, 154, 31, 146, 171]
# Initialization Vectors
# IV_16 = [50, 194, 253, 226, 253,   5,  43,
#          155,   3, 101,  43, 242,  85,  88,  86,  59]
# IV_8 = [50, 194, 253, 226, 253, 5, 43, 155]

# Nonces
# Nonce_32 = [17, 129, 156,  42,  91,  54, 247,  11, 196, 105, 167,  21, 136, 190, 207,  27,
#             46, 245, 132,  20, 246,  48,  50, 254,  45, 175, 123, 246,  67, 253, 236, 103]

# START OF ACTUAL PROGRAM

# Connecting To Server with IPv4 TCP - STREAM
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serverHost, serverPort))


def getIVOfLength(length):
    IV_32 = [174, 138, 140,  75, 123,  99, 175, 145, 197, 135, 142, 155, 139, 132, 122,   8,
             161, 145,  56, 199, 226, 147, 149, 139,  96,  14,  43, 115, 220, 210, 187, 194]
    IV_16 = [50, 194, 253, 226, 253,   5,  43,
             55,   3, 101,  43, 242,  85,  88,  86,  59]
    IV_8 = [50, 194, 253, 226, 253, 5, 43, 155]
    if length == 32:
        return IV_32
    elif length == 16:
        return IV_16
    elif length == 8:
        return IV_8
    else:
        return []


def getNonceOfLength(length):
    Nonce_32 = [17, 129, 156,  42,  91,  54, 247,  11, 196, 105, 167,  21, 136, 190, 207,  27,
                46, 245, 132,  20, 246,  48,  50, 254,  45, 175, 123, 246,  67, 253, 236, 103]
    Nonce_16 = [108,  43,  46, 150,  28, 161, 231,
                101, 228,   9,  90,  35,  87,  97,  67, 185]
    if length == 32:
        return Nonce_32
    elif length == 16:
        return Nonce_16
    else:
        return []


def getKeyOfLength(length):
    key_32 = [247, 243, 40, 10, 220,  77, 213,  52,  44, 151,  50, 121, 236,  88,  68,  68,
              48, 121, 186, 180, 156, 196, 131, 249,  48,  35,  28, 101,  69,  11, 195, 208]
    key_16 = [120, 31, 182, 66, 209, 146, 220,
              175, 238, 56, 52, 145, 154, 31, 146, 171]
    if length == 32:
        return key_32
    elif length == 16:
        return key_16
    else:
        return []


def getCipherInfo(cipher):
    # answer array contains {block_size: a, key_size: b}
    # 128 bit keys were valid for all 5 of these keys, so I've chosen to use that number for consistency
    answer = {}
    if cipher == "AES":
        answer['block_size'] = 128
        answer['key_size'] = 128
    if cipher == "TripleDES":
        answer['block_size'] = 64
        answer['key_size'] = 128
    if cipher == "Blowfish":
        answer['block_size'] = 64
        answer['key_size'] = 128
    if cipher == "SM4":
        answer['block_size'] = 128
        answer['key_size'] = 128
    if cipher == "ARC4":
        answer['key_size'] = 128
    return answer


def setEncryptionMode(mode, cipher, block_size=8):
    info = getCipherInfo(cipher)
    if mode == "ECB":
        mode_object = modes.ECB()
    elif mode == "CBC":
        mode_object = modes.CBC(getIVOfLength(info.get('block_size')))
    elif mode == "OFB":
        mode_object = modes.OFB(getIVOfLength(info.get('block_size')))
    elif mode == "CFB":
        mode_object = modes.CFB(getIVOfLength(info.get('block_size')))
    elif mode == "CTR":
        mode_object = modes.CTR(getNonceOfLength(info.get('block_size')))

    return mode_object


def encryptMessage(encryption, mode, message, key=bytes(32), iv=bytes(16), Nonce=bytes(32)):
    # this will be a kind of switch statement for the different encryptions
    info = getCipherInfo(cipher)
    set_mode = setEncryptionMode(mode, encryption, info.get('block_size'))
    encoded_message = message.encode()
    ct = encoded_message
    if encryption == "AES":
        cipher = Cipher(algorithms.AES(bytes(getKeyOfLength(16))), set_mode)
        encryptor = cipher.encryptor()
        ct = encryptor.update(encoded_message) + encryptor.finalize()
    elif encryption == "TripleDES":
        cipher = Cipher(algorithms.TripleDES(
            bytes(getKeyOfLength(16))), set_mode)
        encryptor = cipher.encryptor()
        ct = encryptor.update(encoded_message) + encryptor.finalize()
    elif encryption == "Blowfish":
        cipher = Cipher(algorithms.Blowfish(
            bytes(getKeyOfLength(16))), set_mode)
        encryptor = cipher.encryptor()
        ct = encryptor.update(encoded_message) + encryptor.finalize()
    elif encryption == "SM4":
        cipher = Cipher(algorithms.SM4(
            bytes(getKeyOfLength(16))), set_mode)
        encryptor = cipher.encryptor()
        ct = encryptor.update(encoded_message) + encryptor.finalize()
    elif encryption == "ARC4":
        cipher = Cipher(algorithms.ARC4(
            bytes(getKeyOfLength(16))), set_mode)
        encryptor = cipher.encryptor()
        ct = encryptor.update(encoded_message) + encryptor.finalize()
    return ct


def decrypt(encryption, message):
    # same for decryptions
    return message

# def speak(message):
#    if ':' in message:
#        cmd = 'say ' + message.split(':')[0] + 'say' +  ' '.join(message.split(':')[1:])
#    else:
#        cmd = 'say ' + message
#    os.system(cmd)”“”


def write():
    while True:
        message = input('-->')
        message = username + ': ' + message
        # message = encrypt(message)
        key = os.urandom(32)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(b"a secret message") + encryptor.finalize()
        client.send(ct)


def receive():
    while True:
        try:
            message = client.recv(bytesReceive).decode()
            # message = decrypt(message)
            if message != 'USR':
                print(message)
                # speak(message)
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
