import socket

HOST = '127.0.0.1'
PORT = 8080


# Create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Send data
client.send("Hello World".encode())

# Recieve response
resp = client.recv(4096)

print("Recieved: {}".format(resp.decode()))