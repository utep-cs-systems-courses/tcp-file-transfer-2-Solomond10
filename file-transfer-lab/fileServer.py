#! /usr/bin/env python3

#Server

import socket, sys, re, os

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.bind(('',50001))
ls.listen(1)

convSock, clientAddr = ls.accept()

fileInfo = convSock.recv(1024).decode()
fileName, fileSize = fileInfo.split(":")

#Differentiates file name so we can see what's inside of the file that was recieved
fileName = fileName.replace(".txt", "-received.txt")

#checks to see if file already exist
path = os.getcwd()+"/"+fileName

if os.path.exists(path) is True:
    print("The file is already on the server")
    sys.exit(1)

fileSize = int(fileSize)

count = 0

with open (fileName, "wb") as a:
        while count < fileSize:
            data = convSock.recv(1024)

            if data == "":
                break
            
            a.write(data)
            count += 1

