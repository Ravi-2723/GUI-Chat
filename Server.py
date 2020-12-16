## Importing Modules
import socket
from _thread import *

## Variables Constant
HOST =socket.gethostname() ## gets host name
PORT = 4856
MAX_CONNECTIONS = 2
E = '0'
F = '1'

def send_data(data, client):
    ## getting data length
    data_len = str(len(data))
    ## adding padding bytes
    data_len = (8-len(data_len))*'0' + data_len

    ## Sending data length and data
    client.sendall(data_len.encode())
    client.sendall(data.encode())
    
def recv_data(client):
    ## recving data length
    data_len = client.recv(8).decode()
    ## recving data
    data = client.recv(int(data_len)).decode()

    ## returning data receved
    return data

## All client handling function
## data reciever
def data_recv(client_id, client):
    global msg_avail
    while True:
        ## recving data
        data = recv_data(client) 
        ## adding it to the list       
        msgs[client_id] = data
        ## making msg_avail flag true
        if client_id == 0:
            msg_avail[1] = True
        elif client_id == 1:
            msg_avail[0] = True

## data sender
def data_sender(client_id, client):
    global msg_avail
    while True:
        ## checking msg_avail flag
        if msg_avail[client_id] == True:
            ## sending data
            if client_id == 0:
                send_data(msgs[1], client)
            elif client_id == 1:
                send_data(msgs[0], client)
            ## setting msg_avail flag back to false
            msg_avail[client_id] = False 

## Variables
server = None
connected_clients = 0
msgs = [None, None]
msg_avail = [False, False]

## Socket Declaration
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## Binding host and port/Intialising server
server.bind((HOST, PORT))
print(f"[SERVER STARTED]")
## printing server ip and port
print(f"[HOST : {server.getsockname()[0]}]\n[PORT : {PORT}]")

## listening for connection
server.listen(1)

## loop for recving connections
while True:
    ## accepting connections
    client, addr = server.accept()
    if connected_clients < MAX_CONNECTIONS:
        ## if there is room send them E
        client.sendall(E.encode())
        ## run client handlers
        start_new_thread(data_sender, (connected_clients, client))
        start_new_thread(data_recv, (connected_clients, client))
        print(f"[CONNECTED TO : {addr[0]}]")
        ## and increase connected_clients
        connected_clients += 1

    elif connected_clients >= MAX_CONNECTIONS:
        ## if there is no room send them F
        client.send(F.encode())
        ## then close the client
        client.close()
        