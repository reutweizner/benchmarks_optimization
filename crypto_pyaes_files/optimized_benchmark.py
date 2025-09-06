#!/usr/bin/env python
from Crypto.Cipher import AES
import multiprocessing
import os

CLEARTEXT = b"This is a test. What could possibly go wrong? " * 500
KEY = b'\xa1\xf6%\x8c\x87}_\xcd\x89dHE8\xbf\xc9,'
NUM_PHYSICAL_CORES = 28

def worker(data, result_queue):
    iv = b'\x00' * 8 # Corrected to 8 bytes to avoid "Nonce is too long" error
    cipher = AES.new(KEY, AES.MODE_CTR, nonce=iv)
    ciphertext = cipher.encrypt(data)
    
    decipher = AES.new(KEY, AES.MODE_CTR, nonce=iv)
    plaintext = decipher.decrypt(ciphertext)
    
    result_queue.put(plaintext)

def bench_pycryptodome_tuned():
    chunk_size = len(CLEARTEXT) // NUM_PHYSICAL_CORES
    chunks = [CLEARTEXT[i:i + chunk_size] for i in range(0, len(CLEARTEXT), chunk_size)]
    
    processes = []
    result_queue = multiprocessing.Queue()
    
    for chunk in chunks:
        p = multiprocessing.Process(target=worker, args=(chunk, result_queue,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    return "done"
