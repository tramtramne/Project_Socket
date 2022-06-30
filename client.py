from email import message
from lib2to3.pytree import Node
import socket
import threading
import json
import os
from requests import request


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def readFileNote(filename):
  with open(filename, 'rb') as f:
    data = f.read(1024*10)

    while data:
      print('saving...')
      client.send(data)
      data = f.read(1024*10)

    client.send("")
    print('Done sending')
    
  f.close()



def sendNote():
  request = client.recv(1024*10).decode(FORMAT)
  print ("Server:", request)
  reply = input("Client: ")
  client.sendall(reply.encode(FORMAT))
  while reply!= '1' and reply != '2' and reply != '3':
    request = client.recv(1024*10).decode(FORMAT)
    print ("Server:", request)
    reply = input("Client: ")
    client.send(reply.encode(FORMAT))

  request = client.recv(1024*10*10).decode(FORMAT)
  print ("Server:", request)
  name = input("Client: ")
  client.send(name.encode(FORMAT))
  readFileNote(name)


def send():
  message = None
  while (message != "x"):
    message = input("Client: ")
    client.send(message.encode(FORMAT))
    #message = client.recv(1024*10).decode(FORMAT)
    #print ("Server:", message)
    if message == 'y':
      sendNote()


try:
  client.connect(ADDR)
  print ("CLIENT SIDE")
  print ("Client address: ",ADDR)
  send()

except:
  print("Error")
  # message = msg.encode(FORMAT)
  # msg_length = len(message)
  # send_length = str(msg_length).encode(FORMAT)
  # send_length += b' ' * (HEADER - len(send_length))
  # client.send(send_length)
  # client.send(message)


