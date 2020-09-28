#! /usr/bin/env python3

#Client

import os, socket, re, sys

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('', 50001))

#nameOfFile = "file.txt"
#sizeOfFile = os.path.getsize(nameOfFile)

fileNm = "file.txt"

try:
    nameOfFile = open(fileNm, "r")
    sizeOfFile = os.path.getsize(fileNm)

except FileNotFoundError as e:
    print("The file doesn't exist")

if sizeOfFile == 0:
    print("There's nothing in the file")
    #break

for line in nameOfFile:
    #print(line)
    clientSocket.send((line).encode())
    
