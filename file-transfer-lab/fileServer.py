#! /usr/bin/env python3

#Server

import socket, sys, re
#from sockHelpers import sendAll

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.bind(('',50001))
ls.listen(1)

convSock, clientAddr = ls.accept()

content = convSock.recv(100)

print(content)
