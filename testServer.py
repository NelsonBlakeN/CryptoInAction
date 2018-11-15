import socket
from utilities import Utilities


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8080))
server.listen(1)

while True:
    print("Waiting on connection...")
    conn, _ = server.accept()
    print("Connected.")

    # Recieve response
    message = conn.recv(4096)

    print('Recieved: {}'.format(message.decode()))

    # Send data
    conn.send("Roger that.".encode())

    conn.close()
