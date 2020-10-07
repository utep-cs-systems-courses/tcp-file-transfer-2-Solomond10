#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive
    fileInfo = (framedReceive(sock,debug)).decode()
    print("The file's name, size and remote name file was received")
    print("File Info: ",fileInfo)
    fileName, fileSize, remoteFileName = fileInfo.split(":")
    fileSize = int(fileSize)
    
    
    if not os.fork():
        print("new child process handling connection from", addr)

        while True:
            
            with open (remoteFileName, "wb") as a:
                count = 0
                while count < fileSize:
                    print("File data is being recieved...")
                    payload = framedReceive(sock, debug)
                    payloadByte = bytes(payload)
                    
                    if payload == b'':
                        break
                    
                    a.write(payloadByte)
                    count += 1
            
            if debug: print("rec'd: ", payload)

            if payload is b'':
                print("The file was received successfully")
                print("The child process is exiting...")
            
                sys.exit(0)
