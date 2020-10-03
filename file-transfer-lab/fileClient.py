#! /usr/bin/env python3

#Client

import os, socket, re, sys

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("127.0.0.1", 50001))

separator = ":"
fileName = input("Enter the name of the file: ")

try:

    sizeOfFile = os.path.getsize(fileName)

    if sizeOfFile == 0:
        print("There's nothing in the file")
    
    clientSocket.send(f"{fileName}{separator}{sizeOfFile}".encode())
    
    with open (fileName, "rb") as a:
        for data in fileName:
            data = a.read(1024)

            if data == "":
                break

            clientSocket.send(data)
            
except FileNotFoundError as e:

    print("The file doesn't exist")

