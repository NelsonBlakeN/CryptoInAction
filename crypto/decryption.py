class Decryption(object):
    def __init__(self):
        pass

    # Decrpyt RSA-encrypted messages
    # cipher: the string message to decrypt
    # key: the key used to decrypt
    # info: a dictionary of any values (n, etc) that is necessary to decrypt
    def rsa(self, cipher, key={}):
        return ""

    # Decrypt AES-128-encrypted messages
    # cipher: the string message to decrypt
    # key: the key used to decrypt (could be multiple values)
    def aes128(self, cipher, key={}):
        return ""

    # Decrpyt DES-encrypted messages
    # cipher: the string message to decrypt
    # key: the key used to decrypt (could be multiple values)
    def des(self, cipher, key={}):
        return ""

    # Decrpyt OTP-encrypted messages
    # cipher: the string message to decrypt
    # key: the key used to decrypt (could be multiple values)
    def one_time_pad(self, cipher, key={}):
        return ""

    # Decrypt El-Gamal-encrypted messages
    # cipher: the string message to decrypt
    # key: the key used to decrypt (could be multiple values)
    def el_gamal(self, cipher, key={}):
        return ""