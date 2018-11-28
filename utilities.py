from crypto.decryption import Decryption
from crypto.encryption import Encryption
from crypto.signature import Signature
import crypto_utils as cutils
import random

enc = Encryption()
dec = Decryption()
sign = Signature()

class Utilities(object):
    enc_algos = {
        "rsa": enc.rsa,
        "aes": enc.aes128,
        "otp": enc.one_time_pad,
        "el_gamal": enc.el_gamal
    }
    dec_algos = {
        "rsa": dec.rsa,
        "aes": dec.aes128,
        "otp": dec.one_time_pad,
        "el_gamal": dec.el_gamal
    }
    sign_algos = {
        "rsa": sign.rsa,
        "el_gamal": sign.el_gamal,
        "dsa": sign.dsa
    }

    HOST = '127.0.0.1'
    SERVER_PORT = 8080

    def __init__(self):
        pass

    @staticmethod
    def generate_keys(algo="el_gamal", prime_length = 31):
        if algo == "el_gamal":
            p = cutils.find_large_prime(prime_length)
            alpha = cutils.randroot(2, p-1)
            a = random.randint(3, p-1) # private key
            beta = pow(alpha, a, p)
            return {'p': p, 'alpha': alpha, 'beta': beta, 'a': a}
        elif algo == "dsa":
            q = cutils.find_large_prime(prime_length)
            p = 2*q + 1
            while (p - 1) % q != 0 or not cutils.isPrime(p):
                #print("Testing Prime:", p)
                p = p + q
                while not cutils.isPrime(p):
                    p = p + q
            #print("Found (p, q): {},{}".format(p, q))

            g = cutils.randroot(p)
            alpha = pow(g, (p-1) / q, p)
            while pow(alpha, q, p) != 1:
                g = cutils.randroot(p, 2, q-1)
                alpha = pow(g, (p-1) / q, p)
            
            a = random.randint(3, q-1) # private key
            beta = pow(alpha, a, p)
            return {'p': p, 'q': q, 'alpha': alpha, 'beta': beta, 'a': a}
        else:
            return {}