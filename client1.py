from base64 import decode
from concurrent.futures import thread
from email import message
import socket;
import threading
import pickle

IP = "127.0.0.1"
Port = 54321
Menu = ["1.Sign-in", "2.Log-in"]
Funct = ["1.Note", "2.Looking my note", "3.Dowload Note"]

def response(s):
    data = s.recv(1024)
    data = data.decode("utf8")
    print(data)
    msg = input()
    s.send(bytes(msg, "utf8"))
    return True
    
def Choice(s):
    for x in range(len(Menu)):
        print (Menu[x]),
    msg = input()
    s.send(bytes(msg, "utf8"))
    return True
def Connect():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((IP, Port))
    print("-----Welcome to taking note everthing-----")
    choice = Choice(s)
    if choice:
       res = response(s)
       while res:
        res = response(s)

        
        #print('Server: ', data.decode("utf8"))
        #msg = input('Client: ')
    
# Send message
    
  # Take the size of message from client
       # Input a message

# Send size of message
#s.send(bytes(str(len(msg)), "utf8"))
# Send message
#s.send(bytes(msg, "utf8"))

# Receive message
threading.Thread(target = Connect).start()

