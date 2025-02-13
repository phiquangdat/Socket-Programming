import socket
import threading
import time

def checksum(packet):
    plen = len(packet)
    if plen%2 == 1:
        plen += 1
        packet.append(0)   # pad a 0 if length is odd

    sum = 0 
    for i in range(0, plen//2):
        sum += packet[2*i]*256 + packet[2*i+1]

    sum = (sum >> 16) + (sum & 0xffff)
    return 0xffff - sum

def send(s):
    seq = 0
    while True:     # sending ICMP type 8 periodically
        time.sleep(1)
        packet = bytearray(b'\x08\x00\x00\x00\x17\x82\x00\x00e2401782')
        seq += 1
        packet[7] = seq
        csum = checksum(packet)
        packet[2] = csum // 256
        packet[3] = csum % 256
        print("Send %s" % packet)
        s.sendto(packet, (target_ip, 0))
        

def recv(s):
    while True:
        d = s.recvfrom(65534)
        if d[1][0] != target_ip:
            continue
        packet = d[0][20:]
        print("Recv %s"%(packet))

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
s.bind(("",0))      # neede for Winsock
target_ip = input("Address to ping: ")
t1 = threading.Thread(target = recv, args=[s]).start()
t2 = threading.Thread(target = send, args=[s]).start()
