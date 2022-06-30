from ctypes import sizeof
import socket
import threading
import json
import pickle
from os import path
IP = "127.0.0.1"
Port = 54321
users = []
filename = 'info.json'
listObj = []

class Store_User:
    def __init__(self, username, password):
        self.Name = username
        self.Pass = password

def receive(client, Mess):
    client.send(bytes(Mess, "utf8"))
    data = ""

    portion = client.recv(1024)
    if portion:
        data += portion.decode("utf8")
    print(type(data.strip()))
    return data.strip()

def response(client):
    data = client.recv(1024)
    data = data.decode("utf8")
    print(data)
    msg = input()
    client.send(bytes(msg, "utf8"))
    return True
    

def validation(username, password):
    print("Log in")
    with open("info.json", "r") as login:
        user_lines = json.load(login)
        for i in user_lines:
            if i['Name'] in username and i['Pass'] in password:
                return True
            else:
                return False

def write_json(new_data, filename='info.json'):
    with open(filename, "r") as file:
        data = json.load(file)
        print(type(data))
        data.append(new_data)
        file.close()
    with open(filename, "w") as file:
        json.dump(data,file)
        

    return True

def New_User(username, password):
    new = Store_User(username, password)
    new = new.__dict__
    print(type(new))
    print(new)
    write_json(new)
    return True

def client_signin(client):
    username = receive(client, "Username: ")
    password = receive(client, "Password: ")
    Check = New_User(username, password)
    while Check == True:
        client.send(bytes("Sign in successfully!", "utf8"))
        client_login(client).start()
        Check = False

def client_login(client):

    username = receive(client, "Username: ")
    password = receive(client, "Password: ")

    Check = validation(username, password)
    while Check == True:
        client.send(bytes("login successfully!", "utf8"))
        Check = False
    while Check == False:
        message = client.recv(1024)
        message = message.decode("utf8")
        print(message)
        Check = False
        if message:
            Client_information(message, client)
        else:
            Check = True
            break

        if not message:
            Check = True
            break

def selection_menu(client):
    res_client = client.recv(1024)
    res_client = res_client.decode("utf8")
    return res_client


def Client_start():
    print('helo')

    # stream: TCP: truyền liên tục
    Main_Stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Main_Stream.bind((IP, Port))  # liên kết main_stream với server
    # lăng nghe trên port với số lương tối đa 2 kết nối chờ
    Main_Stream.listen(2)
    print("hello")
    # client dùng để giao tiếp với client được kết nối
    # addre_client: địa chỉ client được kết nối
    while True:
        client, Addr_client = Main_Stream.accept()
        print("thanh cong")  # chấp nhận kết nối
        users.append(client)

        choice_user = selection_menu(client)
        #choice_user = choice_user.decode("utf8")
        if choice_user == "1":
            client_signin(client).start()
        elif choice_user == "2":
            client_login(client).start()


def Client_information(mess, conncect):
    for user in users:
        if users != conncect:
            try:
                user.sendall(bytes(mess, "utf8"))
            except:
                user.close()

threading.Thread(target=Client_start).start()
