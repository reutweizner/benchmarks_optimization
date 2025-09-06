#!/usr/bin/env python
import pyperf
import pyaes
import os

CLEARTEXT = b"This is a test. What could possibly go wrong? " * 500
KEY = b'\xa1\xf6%\x8c\x87}_\xcd\x89dHE8\xbf\xc9,'

def bench_pyaes():
    aes = pyaes.AESModeOfOperationCTR(KEY)
    ciphertext = aes.encrypt(CLEARTEXT)
    decrypted = aes.decrypt(ciphertext)
    return decrypted
