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
    def el_gamal(self, message, key={}):
        p = key[0]
        alpha = key[1]
        beta = key[2]
        # choose random k
        # r=alpha**k mod p
        # t = beta**k * message mod p
        # return (r,t)
        return ""