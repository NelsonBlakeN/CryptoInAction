import socket
from utilities import enc

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))

message = input('Write your message: ')

ciphertext = str(enc.rsa(message, {'e': 1, 'p': 5, 'q': 7}))

# Send data
client.send(ciphertext.encode())

# Recieve response
response = client.recv(4096)

print('Recieved: {}'.format(response))
