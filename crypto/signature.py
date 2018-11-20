import crypto_utils as utils
import random

class Signature(object):
    def __init__(self):
        pass

    def rsa(self, message):
        return ""

    def el_gamal(self, message, key={}):
        p = key['p']
        alpha = key['alpha']
        a = key['a']
        msg = message.encode('hex')
        msg = int(msg, 16)
        if msg > p:
            raise Exception("WeakKeyError: message is larger than prime (p) potential loss of data")

        # choose k gcd(k,p-1)=1
        k = random.randint(3, p-1)
        g, _, _ = utils.egcd(k, p-1)
        while g != 1:
            k = random.randint(3, p-1)
            g, _, _ = utils.egcd(k, p-1)
        # r = alpha**k mod p
        r = pow(alpha, k, p)

        # s = k**-1 *(m-a*r) mod p-1
        k_inv = utils.modinv(k, p-1)
        s = (k_inv * (msg - a * r)) % (p-1)

        hex_r = hex(int(r))[2:]
        hex_s = hex(int(s))[2:]
        if hex_r[-1] == "L":
            hex_r = hex_r[:-1]
        if hex_s[-1] == "L":
            hex_s = hex_s[:-1]
        return (message, hex_r, hex_s)

    def dsa(self, message):
        pass

    def verify(self, signedmsg, key, option='e'):
        ''' Options:
        e = el_gamal
        r = rsa
        d = dsa
        '''
        msg = signedmsg[0].encode('hex')
        msg = int(msg, 16)

        # el gamal:
        if option == 'e':
            r = int(signedmsg[1], 16)
            s = int(signedmsg[2], 16)

            p = key['p']
            alpha = key['alpha']
            beta = key['beta']

            betator = pow(beta, r, p)
            rtos = pow(r, s, p)

            v1 = (betator * rtos) % p
            v2 = pow(alpha, msg, p)
            return v1 == v2