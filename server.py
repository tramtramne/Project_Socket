from email import message
import socket
from sqlite3 import connect
import threading
import json
import os



HEADER = 64
PORT = 5050

SERVER = socket.gethostbyname('localhost')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


class Note:
  def __init__(self,ID, typeFile,content):
    self.ID = ID
    self.Type = typeFile
    self.Content = content

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen(2)
print('[LISTENING] Server is listening on ',SERVER)


def readFileJSONtoCheckNote(filename,ID):
  with open(filename, "r") as check:
      note = json.load(check)
      for i in note:
          if i['ID'] in ID :
              return False
          else:
            return True
      return False


def writeNoteToFile(conn,filename,newnote):
  try:
    f = open(filename, 'rb')
  except OSError:
    f = open(filename, 'wb')
    f.dumps(newnote)
    f.close()
    return
    
  note = json.loads(f)
  list = []
  if note == 'dict':
    list.append(note)
    list.append(newnote)
    f.close()
    f = open(filename, 'w')
    json.dump(list,f)
    f.close()
  else:
    note.append(newnote)
    f.close()
    f = open(filename, 'w')
    json.dump(note,f)
    f.close()
  print('Finish sending')  
  

def saveFileNote(nameFileNote,conn):
  with open(nameFileNote, 'wb') as f: 
    print('Start saving')
    while True: #count < times:
      print('saving...')
      data = conn.recv(1024*10)
      if not data:
        break
      else:
        f.write(data)
 
  f.close()
  print('Finish saving')
  
  
  
def recieveNote(conn):
  request = 'Which types of formats do you want to note ?\n\t1. Text\n\t2. Images\n\t3. File'
  conn.send(request.encode(FORMAT));
  reply = conn.recv(1024*10).decode(FORMAT)
  print("Client:", reply)
  while reply!= '1' and reply != '2' and reply != '3':
    request = 'You must enter 1 or 2 or 3'
    conn.send(request.encode(FORMAT));
    reply = conn.recv(1024*10).decode(FORMAT)
    print("Client:", reply)
  typeFile = ''
  if (reply == 1):
    typeFile = 'Text'
  if (reply == 2):
    typeFile = 'Images'
  if (reply == 3):
    typeFile = 'File'
  
  request = 'Input the name of file'
  conn.send(request.encode(FORMAT));
  name = conn.recv(1024*10).decode(FORMAT)
  print("Client:", name)
  ID = str(hash(name))
  print(ID)
  #print(type(id))
  dot = name.find('.')
  print(dot)
  dotFile = name[dot:]
  print(dotFile)
  #print(type(dotFile))
  NameFileSave = ID + dotFile
  print(NameFileSave)
  saveFileNote(NameFileSave,conn)
  
  content = os.path.abspath(NameFileSave)
  print('Content',content)
  newnote = Note(ID,typeFile,content)
  print('Get note')
  newnote = newnote.__dict__
  print('Got note')
  filename = 'InforNote.json'

  writeNoteToFile(conn,filename,newnote)
  
  
  
def handle_client(conn, addr):
  print("[NEW CONNECTION]"," connected", addr) 
  chat(conn)
  conn.close()


def chat(conn):
  message = None
  while (message != "x"):
    message = conn.recv(1024*10).decode(FORMAT)
    print ("Client:", message)
    if message == 'y':
      recieveNote(conn)
    
   
    
nClient = 0
while (nClient < 2):
  try: 
    def start():
      conn, addr = server.accept()
      
      thread = threading.Thread(target=handle_client, args=(conn, addr))
      thread.daemon = True
      thread.start()
      print("[ACTIVE CONNECTIONS]" ,threading.activeCount() - 1)
        


    print("[STARTING] server is starting...\n 1.Node")
    start()

  except:
    print("Error")
  nClient += 1

print ("End")
input()
server.close()
