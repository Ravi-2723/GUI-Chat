## Importing Modules
import socket
from tkinter import *
from _thread import *
from functools import partial

## okButton Function
def OBPok():
	host_entry.destroy()
	port_entry.destroy()
	ok_button.destroy()

	try:
		## if port is provided
		if port.get() != '':
			## Trying to connect to the server
			client.connect((host.get(), int(port.get())))
		## if port is not provided
		else:
			client.connect((host.get(), 4856))
		## Recv data from server
		mode = client.recv(1).decode()
		if mode == F:
			## if server is full
			server_full()
		elif mode == E:
			## if server is not full
			start_new_thread(msg_recv, ())
			text_area()
	except:
		## if server not found
		unable_to_connect()

def send_data(data):
	## getting data length
	data_len = str(len(data))
	## adding padding bytes
	data_len = (8-len(data_len))*'0' + data_len

	## Sending data length and data
	client.send(data_len.encode())
	client.send(data.encode())
	
def recv_data():
	## recving data length
	data_len = client.recv(8).decode()
	## recving data
	data = client.recv(int(data_len)).decode()

	## returning data receved
	return data

## on button press Send function
def OBPSend():
	global msg
	if msg.get() != '':
		send_data(msg.get())
	msg.set('')

def msg_recv():
	global msgs
	global surface
	while True:
		## recving data
		data = recv_data()
		## adding it to the messgae list
		msgs.append(data)
		## removing any extra messages
		msgs = msgs[-MAX_MESSAGES:]
		## destroying old labels
		msgs_label.clear()

		## then creating new ones
		for i, msg in enumerate(msgs):
			msgs_label.append(Label(surface, text=msg, font='Arial 13 Bold'))
			msgs_label[i].place(x=0, y=30*i, width=300, height=30)

## text_area function
def text_area():
	global msg

	## changing size of the screen
	surface.geometry(f'{WIDTH*2}x{HEIGHT*2}')

	## widgets
	msg_entry = Entry(surface, textvariable=msg, font='Arial 13')
	send_button =  Button(surface, text='Send', command=OBPSend)

	## widgets placement
	msg_entry.place(x=0, y=370, width=230, height=30)
	send_button.place(x=230, y=370, width=70, height=30)

## unable_to_connect fucntion
def unable_to_connect():
	## Label
	server_not_found_label = Label(surface, text="Server is either not active \nor\n Server id is incorrect")

	## Widget Placement
	server_not_found_label.place(x=0, y=50)

## Variable Constants
WIDTH = 150
HEIGHT = 200
E = '0'
F = '1'
MAX_MESSAGES = 12

## Variables
host = None
port = None
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msgs = []
msgs_label = []

## Intilaizing Screen
surface = Tk()
## Setting screen size
surface.geometry(f"{WIDTH}x{HEIGHT}")

## getting host and port to hold entry value
host = StringVar()
port = StringVar()
msg = StringVar()
## Entries
host_entry = Entry(surface, textvariable=host)
port_entry = Entry(surface, textvariable=port)
## Button
ok_button = Button(surface, text="OK", command=OBPok)

## Widget Placement
host_entry.place(x=10, y=20, width=130, height=30)
port_entry.place(x=10, y=70, width=130, height=30)
ok_button.place(x=50, y=120, width=50, height=30)

## MainLoop
surface.mainloop()
