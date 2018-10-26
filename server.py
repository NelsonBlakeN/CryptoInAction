import socket

HOST = '127.0.0.1'

class Server(object):
    def __init__(self, port):
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.bind((HOST, port))
        self.conn.listen(1)

    def run(self):
        activeConn, _ = self.conn.accept()
        data = activeConn.recv(1024)
        if not data:
            return ''
        else:
            print("Recieved {}".format(data.decode()))
            activeConn.send("Roger that.".encode())      # ACK

if __name__ == "__main__":
    server = Server(8080)
    server.run()