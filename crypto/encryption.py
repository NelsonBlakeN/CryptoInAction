import random

class Encryption(object):
    def __init__(self):
        pass

    # RSA Encryption
    # message: the string message to encrypt
    # key: the key used to encrypt (could be multiple values)
    def rsa(self, message, key={}):
        return ""

    # AES-128 Encryption
    # message: the string message to encrypt
    # key: the key used to encrypt (could be multiple values)
    def aes128(self, message, key={}):
        return ""

    # One Time Pad Encryption
    # message: the string message to encrypt
    # key: the key used to encrypt (could be multiple values)
    def one_time_pad(self, message, key={}):
        return ""

    # El Gamal Encryption
    # message: the string message to encrypt
    # key: the key used to encrypt (could be multiple values)
    # encode string: int(str.encode('hex'),16)
    # decode hex: hex[2:].decode('hex')
    def el_gamal(self, message, key={}):
        p = key['p']
        alpha = key['alpha']
        beta = key['beta']
        # choose random k
        k = 7 #random.randint(3,p)
        # r=alpha**k mod p
        r = alpha**k % p
        # t = beta**k * message mod p
        t = beta**k * int(message.encode('hex'), 16) % p
        return (r,t)