import crypto_utils as utils

class Decryption(object):
    def __init__(self):
        pass

    # Decrpyt RSA-encrypted messages
    # cipher: the string message to decrypt
    # key: the key used to decrypt (could be multiple values)
    def rsa(self, cipher, key={}):
        d = key['d']
        p = key['p']
        q = key['q']
        n = p * q
 
        msg = int(cipher, 16)
        msg = pow(msg, d, n)
        msg = hex(int(msg))[2:]
        if msg[-1] == "L":
            msg = msg[:-1]
        return msg.decode('hex')

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
    def el_gamal(self, cipher, key={}):
        p = key['p']
        a = key['a']
        r = int(cipher[0], 16)
        t = int(cipher[1], 16)

        r_pow = pow(r, a, p)
        r_inv = utils.modinv(r_pow, p)
        m = pow(t*r_inv, 1, p)

        m = hex(int(m))[2:]
        
        return m.decode('hex')