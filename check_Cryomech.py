#!/usr/bin/env python3

# Python script to check Cryomech 2xxx compressor via Modbus TCP

# Cecil Chern-Chyi Yen @ NINDS/NIH
# CentOS 7 & Python 3.6

# 7/1/'22 Initial version

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

cpa_host = 'xxx.xxx.xxx.xxx' #Cryomech compressor IP
cpa_port = 502 #Default port of Modbus TCP

try:
    s.connect((cpa_host, cpa_port))
    s.sendall(b'\t\x99\x00\x00\x00\x06\x01\x04\x00\x01\x005') #Ref https://github.com/Cryomech/SampleCode
    rawData = s.recv(1024)
    stateNumber = int.from_bytes(bytes([rawData[9], rawData[10]]), byteorder='big')
    if 0 == stateNumber:
        print("Ready to start")
    elif 2 == stateNumber:
        print("Starting")
    elif 3 == stateNumber:
        print("Running")
    elif 5 == stateNumber:
        print("Stopping")
    elif 6 == stateNumber:
        print("Error Lockout")
    elif 7 == stateNumber:
        print("Error")
    elif 8 == stateNumber:
        print("Helium Overtemp Cooldown")
    elif 9 == stateNumber:
        print("Power Related Error")
    elif 15 == stateNumber:
        print("Recovered From Error")
    else:
        print("Unknown State")
except Exception as err: 
    print("Can't connect to %s:%d, because %s" % (cpa_host, cpa_port, err))
finally:
    s.close()