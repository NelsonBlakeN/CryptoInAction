import socket
from utilities import Utilities


Utilities.keyserv['blake'] = 'key'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))

message = input('Write your message: ')

# Send data
client.send(message.encode())

# Recieve response
response = client.recv(4096)

print('Recieved: {}'.format(response))
