#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive

fileName = ""

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    
)

progname = "fileClient"

try:

    paramMap = params.parseParams(switchesVarDefaults)
    server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]
    
    if usage:
        params.usage()
    
except:
    pass


try:
        serverHost, serverPort = re.split(":",server)
        serverPort = int(serverPort)
        print("Server: ",server)
        print("Server Host: ",serverHost)
        print("Server Port: ",serverPort)

except:

    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)
    
fileName = input("Enter the file name from the client: ")
remoteFileName = input("Enter the remote name for the server: ")
separator = ":"
        
addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

try:

    sizeOfFile = os.path.getsize(fileName)
    
    if sizeOfFile == 0:
        print("There's nothing in the file")
        sys.exit(0)
    
    info = (f"{fileName}{separator}{sizeOfFile}{separator}{remoteFileName}".encode())
    print(info)
    print("The file's name, size and remote name file was sent")
    framedSend(s,info,debug)

    content = ""
    
    with open (fileName, "r") as a:
        for data in fileName:
            data = a.read()
            
            if not data:
                break
            else:
                content = data.encode()

        print("File data is being sent...")
        framedSend(s,content,debug)

    print("File contents being sent back")
    framedReceive(s,debug)
            
except FileNotFoundError as e:

    print("The file doesn't exist")
    sys.exit(0)