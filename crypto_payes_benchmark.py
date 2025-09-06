#!/usr/bin/env python
"""
Optimized benchmark of AES using PyCryptodome and multiprocessing.
This version is tuned for the specific CPU with 28 physical cores.
"""
import pyperf
from Crypto.Cipher import AES
import multiprocessing
import os

# 23,000 bytes
CLEARTEXT = b"This is a test. What could possibly go wrong? " * 500
# 128-bit key (16 bytes)
KEY = b'\xa1\xf6%\x8c\x87}_\xcd\x89dHE8\xbf\xc9,'

# Number of physical cores based on lscpu output
NUM_PHYSICAL_CORES = 28

def worker(data, result_queue):
    """
    Worker function to encrypt and decrypt a chunk of data.
    """
    iv = b'\x00' * 16
    cipher = AES.new(KEY, AES.MODE_CTR, iv)
    ciphertext = cipher.encrypt(data)

    decipher = AES.new(KEY, AES.MODE_CTR, iv)
    plaintext = decipher.decrypt(ciphertext)

    result_queue.put(plaintext)

def bench_pycryptodome_tuned(loops):
    chunk_size = len(CLEARTEXT) // NUM_PHYSICAL_CORES
    chunks = [CLEARTEXT[i:i + chunk_size] for i in range(0, len(CLEARTEXT), chunk_size)]

    t0 = pyperf.perf_counter()

    for _ in range(loops):
        processes = []
        result_queue = multiprocessing.Queue()

        for chunk in chunks:
            p = multiprocessing.Process(target=worker, args=(chunk, result_queue,))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

    dt = pyperf.perf_counter() - t0
    return dt

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = ("Tuned AES benchmark using PyCryptodome and multiprocessing, "
                                      "optimized for physical cores.")
    runner.bench_time_func('crypto_pycryptodome_tuned', bench_pycryptodome_tuned)
