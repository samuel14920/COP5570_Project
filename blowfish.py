from pydoc import plain
from turtle import right
from blowfish_init_data import *
import base64
import numpy as np


def f_function(n: int):
    intermediate = S[0][n & (2^8 - 1)] + S[1][ (n >> 16) << 16 & 0xff]
    answer = (intermediate ^ S[2][n >> 8 & 0xff]) + S[3][n & 0xff]
    return answer

def Encrypt(l, r):
    for i in range(0, 16):
        l = l ^ P[i]
        r = f_function(l) ^ r
        l, r = r, l
    l, r = r, l
    r = r ^ P[16]
    l = l ^ P[17]


def Decrypt(l, r):
    for i in range(17, 1, -1):
        l = l^ P[i]
        r = f_function(l) ^ r
        l, r = r, l
    l, r = r, l
    r = r ^ P[1]
    l = l ^ P[0]


def Init_Subkeys(key):
    for i in range(0, 18):
        P[i] = P[i] ^ key[i % 14]
    # c = 0
    # for i in range(0, 18):
    #     base = 0
    #     for j in range(0, 4):
    #         base = (base << 8) | int(str(key)[c: c + 8])  # & (2**8 - 1)
    #         c = (c + 1) % len(str(key))
    #     P[i] ^= base

    # 521 iteration subkey calculation
    left, right = 0, 0
    for i in range(0, 18, 2):
        Encrypt(left, right)
        P[i] = left
        P[i + 1] = right

    for i in range(0, 4):
        for j in range(0, 256, 2):
            Encrypt(left, right)
            S[i][j] = left
            S[i][j + 1] = right


key = [0x77AFA1C5, 0x20756060,
       0x85CBFE4E, 0x8AE88DD8, 0x7AAAF9B0, 0x4CF9AA7E,
       0x1948C25C, 0x02FB8A8C, 0x01C36AE4, 0xD6EBE1F9,
       0x90D4F869, 0xA65CDEA0, 0x3F09252D, 0xC208E69F]

    # plaintext_bytes = text2Binary(plaintext); console.log(plaintext_bytes);
    # plaintext_bytes = plaintext_bytes.replace(/\s/g, ''); console.log(plaintext_bytes);
    #
    # //convert to int representation
    # left_string = (plaintext_bytes.substring(0,32)); let left_rep = parseInt(left_string, 2);console.log(left_rep); setLeftInitial(left_rep);
    # right_string = (plaintext_bytes.substring(32,64)); let right_rep = parseInt(right_string, 2);console.log(right_rep); setRightInitial(right_rep);


plaintext = "abcdefgh"
plaintext_bytes = plaintext.encode("ascii")
print(plaintext_bytes)
plaintext_int = (np.uint64(int.from_bytes(plaintext_bytes, "little")))
left_text = (plaintext_int >> 32) << 32 #plaintext_string[0:32]#(int.from_bytes(plaintext_bytes, "big")# >> 32) << 32#& ((2 ^ 32) - 1)
right_text = plaintext_int << 32
print(left_text, right_text)
Init_Subkeys(key)
Encrypt(left_text, right_text)
print(left_text, right_text)
Decrypt(left_text, right_text)
print(left_text, right_text)
