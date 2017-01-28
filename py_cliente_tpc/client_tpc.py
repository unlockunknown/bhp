# -*- coding: utf-8 -*-


import socket


target_host = 'www.google.com'
target_port = 80


# Create object SOCKET
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# cliente CONNECT
client.connect((target_host, target_port))


# send some DATA
client.send('GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')


# receive some DATA
response = client.recv(4096)


print '# RESPONSE \n\r'
print response
