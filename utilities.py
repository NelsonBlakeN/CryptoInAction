from crypto.decryption import Decryption
from crypto.encryption import Encryption
from crypto.signature import Signature

enc = Encryption()
dec = Decryption()
sign = Signature()

class Utilities(object):
    enc_algos = {
        "rsa": enc.rsa,
        "aes": enc.aes128,
        "des": enc.des,
        "otp": enc.one_time_pad,
        "el_gamal": enc.el_gamal
    }
    dec_algos = {
        "rsa": dec.rsa,
        "aes": dec.aes128,
        "des": dec.des,
        "otp": dec.one_time_pad,
        "el_gamal": dec.el_gamal
    }
    sign_algos = {
        "rsa": sign.rsa,
        "el_gamal": sign.el_gamal,
        "dsa": sign.dsa
    }

    def __init__(self):
        pass

    @staticmethod
    def generate_keys():
        return None, None