import random
import math

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
    # encode string: int(string.encode('hex'),16)
    # decode int: str(hex(integer)[2:]).decode('hex')
    def el_gamal(self, message, key={}):
        p = key['p']
        alpha = key['alpha']
        beta = key['beta']
        msg = int(message.encode('hex'), 16)
        if msg > p:
            raise Exception("WeakKeyError: message is larger than prime (p) potential loss of data")

        k = random.randint(3,p)
        r = pow(alpha, k, p)
        t = pow(pow(beta, k, p)*msg,1,p)

        str_r = str(hex(int(r)))[2:]
        str_t = str(hex(int(t)))[2:]
        if(len(str_r)%2==1):
            str_r = '0'+str_r
        if(len(str_t)%2==1):
            str_t = '0'+str_t

        return (str_r.decode('hex'), str_t.decode('hex'))