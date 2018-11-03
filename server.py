import socket
from crypto.signature import Signature
from utilities import Utilities

HOST = '127.0.0.1'

class Server(object):
    def __init__(self, port, algo='rsa', sign='rsa'):
        self.port = port
        self.priv_key, self.pub_key = Utilities.generate_keys()
        self.client_key = None      # Client's public key
        self.activeConn = None
        self.decrypt = Utilities.dec_algos[algo]
        self.encrypt = Utilities.enc_algos[algo]
        self.sign = Utilities.sign_algos[sign]

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.bind((HOST, port))
        self.conn.listen(1)

    def run(self):
        self.activeConn, _ = self.conn.accept()

        # First, key exchange
        self.key_exchange()

        # Recieve and decrypt msg
        signed_cipher = self.activeConn.recv(4096)

        # Verify signature
        if Signature().verify(signed_cipher):
            # Decrypt
            cipher = signed_cipher.split(',')[1]
            plaintext = self.decrypt(cipher, self.client_key)
            print('Recieved: {}'.format(plaintext))
        else:
            raise Exception("Signature couldn't be verified.")

        ## SEND RESPONSE ##
        # Encrypt message with chosen algorithm
        response = "Roger that."
        cipher_response = self.encrypt(response, self.priv_key)

        # Sign response
        signed_cipher = self.sign(cipher_response)

        # Send response
        self.activeConn.send(signed_cipher)

    # Exchange public keys (Diffie Hellman)
    # Use self.activeConn to send and recieve keys
    # Store client key in self.client_key
    def key_exchange(self):
        pass

if __name__ == "__main__":
    server = Server(8080)
    server.run()