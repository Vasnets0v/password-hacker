import argparse
from itertools import product
import socket


def new_password():
    with open("passwords.txt", "r") as temp_password:
        for line in temp_password:
            word = line.strip()
            if line.isdigit():
                yield line
            else:
                word_combinations = product(*([letter.lower(), letter.upper()] for letter in word))
                for word in word_combinations:
                    yield ''.join(word)


parser = argparse.ArgumentParser()
parser.add_argument("host", help="Enter IP address")
parser.add_argument("port", help="Enter port from 1024 to 65535")

args = parser.parse_args()

ip_address = args.host
port = int(args.port)
address = (ip_address, port)
password = new_password()
response = ""

with socket.socket() as client_socket:
    client_socket.connect(address)
    while response != "Connection success!":
        data = next(password).encode()
        client_socket.send(data)
        response = client_socket.recv(1024).decode()
    print(data.decode())
