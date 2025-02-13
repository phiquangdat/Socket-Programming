import socket 
import time
import random
import threading 

clients = []

print("UDP Broadcast Server, waiting for incoming client...")


def recv(s):
    while True:
        try:
            msg, addr = s.recvfrom(1024)
            if addr not in clients:
                clients.append(addr)
                print(f"Client {addr[0]} comes in.")
            if "BYE" in msg.decode("ascii"):
                print(f"Client {addr[0]} left.")
                clients.remove(addr)
            elif msg:
                print(f"Receives \"{msg.decode('ascii')}\" from {addr[0]}")
        except KeyboardInterrupt:
            break

def send(s):
    while True:
        try:
             for x in clients:
                msg = "Server:" + str(random.random())
                s.sendto(bytearray(msg, encoding="ascii"), x)
             time.sleep(random.randint(3,8))
        except KeyboardInterrupt:
             break


try:    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
except:
    print("Cannot create socket")
    exit()
    
s.bind(('', 44444))
t1 = threading.Thread(target = recv, args=[s]).start()
t2 = threading.Thread(target = send, args=[s]).start()
while True:
    try:
        pass 
    except KeyboardInterrupt:
        break

s.close()
