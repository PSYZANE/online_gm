import socket
from _thread import *
import sys

server = socket.gethostbyname(socket.gethostname())
port = 5050

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("[server started] waiting for connection")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(0,0), (100,100)]

def threaded_client(conn,currentPlayer):
    conn.send(str.encode(make_pos(pos[currentPlayer])))
    reply = ""
    while True:
        try :
            data = read_pos(conn.recv(2048).decode())
            pos[currentPlayer] = data

            if not data:
                print("Disconnected")
                break
            else:
                if currentPlayer == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", reply)
                print("Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except :
            break
    
    print("[Lost connection]")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("[Connected to:] ",addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1