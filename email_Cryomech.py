#!/usr/bin/env python3

# Python script to check Cryomech 2xxx compressor via Modbus TCP

# Cecil Chern-Chyi Yen @ NINDS/NIH
# CentOS 7 & Python 3.6

# 7/1/'22 Initial version
# 7/2/'22 +Email status

import socket
import smtplib

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

cpa_host = 'xxx.xxx.xxx.xxx' #Cryomech compressor IP
cpa_port = 502 #Default port of Modbus TCP

mail_host1 = "localhost" #local postfix ready
mail_host2 = "xxx" #backup mail server
mail_port = 25

try:
    t = smtplib.SMTP(mail_host1,mail_port)
#    t.set_debuglevel(1)
    from_email = "xxxu@"
    to_email = "xxxn@"
except:
    t = smtplib.SMTP(mail_host2,mail_port)
#    t.set_debuglevel(1)
    from_email = "xxx@"
    to_email = "xxx@"

try:
    s.connect((cpa_host, cpa_port))
    s.sendall(b'\t\x99\x00\x00\x00\x06\x01\x04\x00\x01\x005') #Ref https://github.com/Cryomech/SampleCode
    rawData = s.recv(1024)
    stateNumber = int.from_bytes(bytes([rawData[9], rawData[10]]), byteorder='big')
    if 0 == stateNumber:
        t.sendmail(from_email,to_email,'Subject:[Compressor] Ready to start\n')
    elif 2 == stateNumber:
        t.sendmail(from_email,to_email,'Subject:[Compressor] Starting\n')
    elif 3 == stateNumber:
        pass
#        t.sendmail(from_email,to_email,'Subject:[Compressor] Running\n')
    elif 5 == stateNumber:
        t.sendmail(from_email,to_email,'Subject:[Compressor] Stopping\n')
    elif 6 == stateNumber:
        t.sendmail(from_email,to_email,'Subject:[Compressor] Error lockout\n')
    elif 7 == stateNumber:
        t.sendmail(from_email,to_email,'Subject:[Compressor] Error\n')
    elif 8 == stateNumber:
        t.sendmail(from_email,to_email,'Subject:[Compressor] Helium overtemp cooldown\n')
    elif 9 == stateNumber:
        t.sendmail(from_email,to_email,'Subject:[Compressor] Power related error\n')
    elif 15 == stateNumber:
        t.sendmail(from_email,to_email,'Subject:[Compressor] Recovered from error\n')
    else:
        t.sendmail(from_email,to_email,'Subject:[Compressor] Unknown state\n')
except:
    t.sendmail(from_email,to_email,'Subject:[Compressor] Network error\n')
finally: 
    t.quit()
    s.close()
