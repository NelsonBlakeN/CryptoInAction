#!/usr/bin/python3
import socket
from crypto.signature import Signature
from utilities import Utilities

HOST = '127.0.0.1'
PORT = 8080

class Client(object):

    # Create socket, keys, define algorithms
    def __init__(self, algo='rsa', sign='rsa'):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.priv_key, self.pub_key = Utilities.generate_keys()
        self.server_key = None      # Server's public key
        self.encrypt = Utilities.enc_algos[algo]
        self.decrypt = Utilities.dec_algos[algo]
        self.sign = Utilities.sign_algos[sign]

    # Generate public and private keys
    # In the case of symmetric encryption, something else should happen.
    def generate_keys(self):
        return None, None

    # Connect to server
    def run(self):
        self.client.connect((HOST, PORT))
        self.key_exchange()
        message = input('Write your message: ')

        # Encrpyt message with chosen algorithm
        cipher = self.encrypt(message, self.priv_key)

        # Sign message
        signed_cipher = self.sign(cipher)

        # Send data
        self.client.send(signed_cipher.encode())

        # Recieve response
        signed_response = self.client.recv(4096)

        # Verify signature
        if Signature().verify(signed_response):
            # Decrypt
            cipher_response = signed_response.split(',')[1]
            plaintext = self.decrypt(cipher_response, self.server_key)
            print('Recieved: {}'.format(plaintext))
        else:
            raise Exception("Signature couldn't be verified.")

    # Exchange public keys (Diffie Hellman)
    # Use self.client to send and recieve keys
    # Store server key in self.server_key
    def key_exchange(self):
        pass