class Decryption(object):
    def __init__(self):
        pass

    # Decrpyt RSA-encrypted messages
    def rsa(self, cipher, key):
        return ""

    # Decrypt AES-128-encrypted messages
    def aes128(self, cipher, key):
        return ""

    # Decrpyt DES-encrypted messages
    def des(self, cipher, key):
        return ""

    # Decrpyt OTP-encrypted messages
    def one_time_pad(self, cipher, key):
        return ""

    # Decrypt El-Gamal-encrypted messages
    def el_gamal(self, cipher, key={}):
        p = key['p']
        a = key['a']
        r = cipher[0]
        t = cipher[1]
        # m = t*r**-a mod p
        # return m
        return ""