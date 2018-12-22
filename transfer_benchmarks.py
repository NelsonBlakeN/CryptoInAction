
import time
import utilities as utils

message = "h"

def rsa(min=3, max=15):
    for key_size in range(min, max+1):
        start = stop = time.time()
        keys = utils.Utilities.generate_keys(algo='rsa', prime_length=key_size)
        ciphertext = utils.enc.rsa(message, keys)
        plaintext = utils.dec.rsa(ciphertext, keys)
        stop = time.time()
        if plaintext == message:
            print str(stop - start)
        else:
            raise Exception("Decryption failed")

def elgamal(min=3, max=15):
    for key_size in range(min, max+1):
        start = stop = time.time()
        keys = utils.Utilities.generate_keys(algo='el_gamal', prime_length=key_size)
        ciphertext = utils.enc.el_gamal(message, keys)
        plaintext = utils.dec.el_gamal(ciphertext, keys)
        stop = time.time()
        if plaintext == message:
            print str(stop - start)
        else:
            raise Exception("Decryption failed")


def des(min=3, max=15):
    for key_size in range(min, max+1):
        start = stop = time.time()
        keys = utils.Utilities.generate_keys(algo='des', prime_length=key_size, key="hello")
        ciphertext = utils.enc.des(message, keys)
        # plaintext = utils.dec.des(ciphertext, keys)
        stop = time.time()
        # if plaintext == message:
        #     print str(stop - start)
        # else:
        #     raise Exception("Decryption failed")
        print str(stop - start)

def otp(min=3, max=15):
    binary_msg = bin(int(message.encode('hex'), 16))[2:]

    for key_size in range(min, max+1):
        start = stop = time.time()
        keys = utils.Utilities.generate_keys(algo='otp', prime_length=key_size, key=binary_msg)
        ciphertext = utils.enc.one_time_pad(binary_msg, keys)
        plaintext = utils.dec.one_time_pad(ciphertext, keys)
        stop = time.time()
        if plaintext == binary_msg:
            print str(stop - start)
        else:
            raise Exception("Decryption failed")

print "Running benchmark..."

# rsa(min=3, max=20)
# elgamal(min=3, max=20)
# des(min=3, max=20)
otp(min=3, max=20)