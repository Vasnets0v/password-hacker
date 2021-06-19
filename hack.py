import socket
import argparse
from itertools import combinations_with_replacement

dictionary = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
              "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
              0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

parser = argparse.ArgumentParser()
parser.add_argument("ip")
parser.add_argument("port")
args = parser.parse_args()

with socket.socket() as client_socket:
    hostname = (args.ip, int(args.port))

    client_socket.connect(hostname)

    for i in range(1, 4):
        for password in combinations_with_replacement(dictionary, i):
            a = ""
            for j in password:
                a += str(j)
            text = a
            text = text.encode()
            client_socket.send(text)

            response = client_socket.recv(1024)
            response = response.decode()
            if response == "Connection success!":
                print(a)
                break

