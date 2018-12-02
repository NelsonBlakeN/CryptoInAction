import utilities as utils
from crypto_utils import *

def RSA_brute_force(ciphertext, e, n):
    p = q = 3
    while p < n:
        if n % p == 0:
            q = n / p
            print p
            print q
            print n
            phi = (p - 1) * (q - 1)
            d = modinv(e, phi)
            return utils.dec.rsa(ciphertext, {'d': d, 'p': p, 'q': q})         
        p += 2
    return "" 