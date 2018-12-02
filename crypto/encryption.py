import crypto_utils as cutils

class Encryption(object):
    def __init__(self):
        pass

    # RSA Encryption
    # message: the string message to encrypt
    # key: the key used to encrypt (could be multiple values)
    def rsa(self, message, key={}):
        e = key['e']
        p = key['p']
        q = key['q']
        n = p * q
        msg = message.encode('hex')
        return math.pow(msg, e, n)

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
        msg = message.encode('hex')
        msg = int(msg, 16)
        if msg > p:
            raise Exception("WeakKeyError: message is larger than prime (p) potential loss of data")

        k = random.randint(3,p)
        r = pow(alpha, k, p)
        t = pow(beta, k, p)*msg % p
        hex_r = hex(int(r))[2:]
        hex_t = hex(int(t))[2:]

        return (hex_r, hex_t)