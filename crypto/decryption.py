class Decryption(object):
    def __init__(self):
        pass

    # Decrpyt RSA-encrypted messages
    # cipher: the string message to decrypt
    # key: the key used to decrypt (could be multiple values)
    def rsa(self, cipher, key={}):
        return ""

    # Decrypt AES-128-encrypted messages
    # cipher: the string message to decrypt
    # key: the key used to decrypt (could be multiple values)
    def aes128(self, cipher, key={}):
        return ""

    # Decrpyt OTP-encrypted messages
    # cipher: the string message to decrypt
    # key: the key used to decrypt (could be multiple values)
    def one_time_pad(self, cipher, key={}):
        return ""

    # Decrypt El-Gamal-encrypted messages
<<<<<<< HEAD
    # cipher: the string message to decrypt
    # key: the key used to decrypt (could be multiple values)
    def el_gamal(self, cipher, key={}):
=======
    def el_gamal(self, cipher, key={}):
        p = key['p']
        a = key['a']
        r = cipher[0]
        t = cipher[1]
        # m = t*r**-a mod p
        # return m
>>>>>>> elgamal
        return ""