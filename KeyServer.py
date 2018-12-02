#!/usr/bin/env python3

import socket

from utilities import Utilities

class KeyServer(object):
    def __init__(self, port):
        self.keys = {}
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.activeConn = None

        self.conn.bind((Utilities.HOST, port))
        self.conn.listen(1)

    def run(self):
        while True:
            self.activeConn, _  = self.conn.accept()

            name_and_key = self.activeConn.recv(4096).decode()

            if ',' in name_and_key:
                # Set key
                name, key = tuple(name_and_key.split(","))

                self.keys[name] = key
            else:
                # Get key
                name = name_and_key
                key = self.keys[name]
                self.activeConn.send(key.encode())

            # Close connection
            self.activeConn.close()

if __name__ == "__main__":
    ks = KeyServer(6300)
    ks.run()
