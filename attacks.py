from __future__ import print_function # coulda used Ruby, js
import utilities as utils
from crypto_utils import *
import time, fractions

def benchmark(attack, algorithm='rsa'):
    if algorithm not in ['rsa', 'el gamal', 'dsa']:
        print("Invalid algorithm passed")
        return None

    message = 'howdy'

    for key_size in range(7, 15):
        print('[' + algorithm + ']' + " (key_size " + str(key_size) + ')', end='')
        print(' ', end='')
        keys = utils.Utilities.generate_keys(algo=algorithm, prime_length=key_size)
        ciphertext = ''
        if algorithm == 'rsa':
            start = stop = time.time()
            ciphertext = utils.enc.rsa(message, keys)
            e = keys['e']
            n = keys['p'] * keys['q']
            output = attack(ciphertext, e, n)
            if output == 'howdy':
                stop = time.time()
                print(str(stop - start) + ' seconds')
            else:
                print("wrong plaintext recovered")

        elif algorithm == 'el gamal':
            ciphertext = utils.enc.el_gamal(message, keys)

        elif algorithm == 'dsa':
            ciphertext = utils.enc.aes128(message, keys)

        else:
            return None

def RSA_brute_force(ciphertext, e, n):
    p = q = 3
    while p < n:
        if n % p == 0:
            q = n / p
            phi = (p - 1) * (q - 1)
            d = modinv(e, phi)
            return utils.dec.rsa(ciphertext, {'d': d, 'p': p, 'q': q})
        p += 2
    return "" 

def RSA_p_minus_1(ciphertext, e, n, bound=100):
    # pick any a > 1
    a = 3
    B = bound
    while True:
        b = pow(a, math.factorial(B), n)
        p = fractions.gcd(b - 1, n)
        if p > 1 and p < n:
            q = n / p
            phi = (p - 1) * (q - 1)
            d = modinv(e, phi)
            return utils.dec.rsa(ciphertext, {'d': d, 'p': p, 'q': q})
        B *= 10

    return ""


# main
benchmark(RSA_brute_force, algorithm='rsa')
