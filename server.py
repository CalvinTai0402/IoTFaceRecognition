import os
from socket import *
host = "10.0.0.122" # set to private IP, i.e., the IP running this code
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print("[RECEIVE MODE]")
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    print ("Received: " + data.decode("utf-8"))
    if data == "STOP":
        break
UDPSock.close()
os._exit(0)

# Save as client.py  
# Message Sender 
# import os 
# from socket import * 
# host = "10.0.0.122" #set to private ip of target machine, i.e., server
# port = 13000 
# addr = (host, port) 
# UDPSock = socket(AF_INET, SOCK_DGRAM) 
# while True: 
#     data = raw_input("Enter message to send or type 'exit': ") 
#     UDPSock.sendto(data, addr) 
#     if data == "exit": 
#         break 
# UDPSock.close() 
# os._exit(0) 