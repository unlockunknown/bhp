# -*- coding: utf-8 -*-


import socket


target_host = '127.0.0.1'
target_port = 80


# Create object SOCKET
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# send some DATA
client.sendto('AAABBBCCC', (target_host, target_port))


# receive some DATA
data, addr = client.recvfrom(4096)


print '# DATA \n\r'
print data
