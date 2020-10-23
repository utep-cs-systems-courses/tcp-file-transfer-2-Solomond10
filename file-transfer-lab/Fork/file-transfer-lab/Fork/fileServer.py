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
  
    if not os.fork():

        fileInfo = (framedReceive(sock,debug)).decode()
        print("The file's name, size and remote name file was received")
        print("File Info: ",fileInfo)
        fileName, fileSize, remoteFileName = fileInfo.split(":")
        fileSize = int(fileSize)

        #checks to see if file already exist

        path = os.getcwd()+"/"+remoteFileName

        if os.path.exists(path) is True:
            print("The file is already on the server")
            payload = framedReceive(sock,debug)
            framedSend(sock, payload, debug)

        else:

            print("new child process handling connection from", addr)
            with open (remoteFileName, "w") as f:

                print("File data is being recieved...")
                payload = framedReceive(sock, debug)

                #Decodes payload if it is not none and writes to the remote file
                #If payload is nothing is none then it writes nothing to the remote file
                if payload is not None:
                
                    payloadDecoded = payload.decode()
                    f.write(payloadDecoded)
                    framedSend(sock, payload, debug)


                    print("Exiting.....")    
  
    else:
        sock.close()
