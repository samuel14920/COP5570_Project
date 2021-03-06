import socket
import threading
import os
import time
from desCrypt import desCrypt
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.primitives import (
    padding
)


def getIVOfLength(length):
    IV_32 = [174, 138, 140,  75, 123,  99, 175, 145, 197, 135, 142, 155, 139, 132, 122,   8,
             161, 145,  56, 199, 226, 147, 149, 139,  96,  14,  43, 115, 220, 210, 187, 194]
    IV_16 = [50, 194, 253, 226, 253,   5,  43,
             55,   3, 101,  43, 242,  85,  88,  86,  59]
    IV_8 = [50, 194, 253, 226, 253, 5, 43, 155]
    if length == 32:
        return bytes(IV_32)
    elif length == 16:
        return bytes(IV_16)
    elif length == 8:
        return bytes(IV_8)
    else:
        return bytes([])


def getNonceOfLength(length):
    Nonce_32 = [17, 129, 156,  42,  91,  54, 247,  11, 196, 105, 167,  21, 136, 190, 207,  27,
                46, 245, 132,  20, 246,  48,  50, 254,  45, 175, 123, 246,  67, 253, 236, 103]
    Nonce_16 = [108,  43,  46, 150,  28, 161, 231,
                101, 228,   9,  90,  35,  87,  97,  67, 185]
    if length == 32:
        return bytes(Nonce_32)
    elif length == 16:
        return bytes(Nonce_16)
    else:
        return bytes([])


def getKeyOfLength(length):
    key_32 = [247, 243, 40, 10, 220,  77, 213,  52,  44, 151,  50, 121, 236,  88,  68,  68,
              48, 121, 186, 180, 156, 196, 131, 249,  48,  35,  28, 101,  69,  11, 195, 208]
    key_16 = [120, 31, 182, 66, 209, 146, 220,
              175, 238, 56, 52, 145, 154, 31, 146, 171]
    if length == 32:
        return bytes(key_32)
    elif length == 16:
        return bytes(key_16)
    else:
        return bytes([])


def getCipherInfo(cipher):
    # answer array contains {block_size: a, key_size: b}
    # 128 bit keys were valid for all 5 of these keys, so I've chosen to use that number for consistency
    answer = {}
    if cipher == "AES":
        answer['block_size'] = 16
        answer['key_size'] = 16
    if cipher == "TripleDES":
        answer['block_size'] = 8
        answer['key_size'] = 16
    if cipher == "Blowfish":
        answer['block_size'] = 8
        answer['key_size'] = 16
    if cipher == "SM4":
        answer['block_size'] = 16
        answer['key_size'] = 16
    if cipher == "ARC4":
        answer['key_size'] = 16
    return answer


def setEncryptionMode(mode, cipher, block_size=8):
    info = getCipherInfo(cipher)
    if mode == "ECB":
        mode_object = modes.ECB()
    elif mode == "CBC":
        # print(info.get('block_size'))
        mode_object = modes.CBC(getIVOfLength(info.get('block_size')))
        # print(mode_object)
    elif mode == "OFB":
        mode_object = modes.OFB(getIVOfLength(info.get('block_size')))
    elif mode == "CFB":
        mode_object = modes.CFB(getIVOfLength(info.get('block_size')))
    elif mode == "CTR":
        mode_object = modes.CTR(getNonceOfLength(info.get('block_size')))

    return mode_object


def encryptMessage(encryption, mode, message, key=bytes(16)):
    # this will be a kind of switch statement for the different encryptions
    info = getCipherInfo(encryption)
    set_mode = setEncryptionMode(mode, encryption, info.get('block_size'))
    # print(info.get('block_size'))
    # print(message)
    encoded_message = message.encode()
    if encryption == "TripleDES":
        cipher = Cipher(algorithms.TripleDES(
            key), set_mode)
    elif encryption == "Blowfish":
        cipher = Cipher(algorithms.Blowfish(key), set_mode)
    elif encryption == "SM4":
        cipher = Cipher(algorithms.SM4(key), set_mode)
    elif encryption == "ARC4":
        cipher = Cipher(algorithms.ARC4(key), mode=None)
    else:  # encryption == "AES"
        cipher = Cipher(algorithms.AES(key), set_mode)
    encryptor = cipher.encryptor()
    # print(type(encoded_message))
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(encoded_message)
    padded_data += padder.finalize()
    # print(padded_data)
    ct = encryptor.update(padded_data) + encryptor.finalize()

    return ct


def decryptMessage(ciphertext, encryption, mode, key=bytes(16)):
    # same for decryptions
    info = getCipherInfo(encryption)
    set_mode = setEncryptionMode(mode, encryption, info.get('block_size'))
    if encryption == "TripleDES":
        cipher = Cipher(algorithms.TripleDES(
            key), set_mode)
    elif encryption == "Blowfish":
        cipher = Cipher(algorithms.Blowfish(key), set_mode)
    elif encryption == "SM4":
        cipher = Cipher(algorithms.SM4(key), set_mode)
    elif encryption == "ARC4":
        cipher = Cipher(algorithms.ARC4(key),  mode=None)
    else:  # encryption == "AES"
        cipher = Cipher(algorithms.AES(key), set_mode)
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    # print("CIPHERTEXT:\n", ciphertext)
    # print("PADDED DATA:\n", padded_data)
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data)
    # print("DATA:\n", data)
    message = data + unpadder.finalize()
    #print("MESSAGE\n", message)
    return message


# info = getCipherInfo("AES")
# set_mode = setEncryptionMode("CBC", "AES", info.get('block_size'))
# key = getKeyOfLength(16)
# cipher = Cipher(algorithms.AES(key), set_mode)

# message = "hello world"
# encoded_message = message.encode()

# encryptor = cipher.encryptor()
# # print(type(encoded_message))
# padder = padding.PKCS7(128).padder()
# padded_data = padder.update(encoded_message)
# padded_data += padder.finalize()
# # print(padded_data)
# ct = encryptor.update(padded_data) + encryptor.finalize()


# decryptor = cipher.decryptor()
# padded_data = decryptor.update(ct) + decryptor.finalize()
# unpadder = padding.PKCS7(128).unpadder()
# data = unpadder.update(padded_data)
# message = data + unpadder.finalize()
# print(message)
