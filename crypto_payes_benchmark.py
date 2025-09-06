#!/usr/bin/env python
"""
Original benchmark of AES using pyaes.
"""
import pyperf
import pyaes

# 23,000 bytes
CLEARTEXT = b"This is a test. What could possibly go wrong? " * 500
# 128-bit key (16 bytes)
KEY = b'\xa1\xf6%\x8c\x87}_\xcd\x89dHE8\xbf\xc9,'

def bench_pyaes(loops):
    t0 = pyperf.perf_counter()
    for _ in range(loops):
        aes = pyaes.AESModeOfOperationCTR(KEY)
        ciphertext = aes.encrypt(CLEARTEXT)
        decrypted = aes.decrypt(ciphertext)
    dt = pyperf.perf_counter() - t0
    return dt

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = "Original AES benchmark with pyaes library."
    runner.bench_time_func('crypto_pyaes_original', bench_pyaes)
