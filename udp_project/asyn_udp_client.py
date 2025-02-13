import socket
import threading

def recv(s):
    while True:
        try:
            msg, addr = s.recvfrom(1024)
            print(f"Receives \"{msg.decode('ascii')}\" from {addr[0]}")  # Decoding the byte message to string
        except OSError:
            break

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
except:
    print("Cannot create socket")
    exit()

ip_address = socket.gethostbyname(socket.gethostname())
s.bind((ip_address, 44444))

t = threading.Thread(target=recv, args=[s])
t.start()

while True:
    try:
        msg = input("Message to server: ")
        s.sendto(bytearray(msg, encoding="ascii"), ('<broadcast>', 44444))
        if "BYE" in msg:
            break
    except KeyboardInterrupt:
        break

s.close()
