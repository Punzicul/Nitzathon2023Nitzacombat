import socket
import threading
import time
import random

HOST = "192.168.161.251"
PORT = 5555
TYPE = "utf-8"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()

print(f"[SERVER LISTENING ON PORT {PORT}]")

allClients = []
playClients = []

sentChar = False
character = None

def sendToAllOtherClients(message, conn, printing):
    for client in playClients:
        currentConn = client[0]
        if currentConn != conn:
            if printing:
                print(f"Sending message: {message}")
            currentConn.send(message.encode(TYPE))
            break


def handleClient(conn, addr):
    character = None
    while True:
        try:
            message = conn.recv(4128)
            message = message.decode(TYPE)

            if message.split(":")[0] == "char":
                character = message.split(":")[1]

                enoughPlayers = len(playClients) < 1

                if enoughPlayers:
                    conn.send("not ready".encode(TYPE))
                    playClients.append([conn, message.split(":")[1]])
                    
                else:
                    playClients.append([conn, message.split(":")[1]])

                    for clients in playClients:
                        currentConn = clients[0]    
                        currentConn.send("ready".encode(TYPE))

            elif message == "quit":
                allClients.remove(conn)
                for client in playClients:
                    if conn in client:
                        playClients.remove(client)
                        break
                conn.close()
                print(f"removed client - length of clients: {len(playClients)}")
                break

            if message == "getChar":
                for client in playClients:
                    currentConn = client[0]

                    if currentConn != conn:
                        currentConn.send(f"{character}".encode(TYPE))
                        break

            if message.split(":")[0] == "velo":
                sendToAllOtherClients(message, conn, False)

            if message == "jump\n":
                sendToAllOtherClients(message, conn, True)
            
            if message.split(":")[0] == "dmg" or message.split(":")[0] == "knockback" or message.split(":")[0] == "attack":
                sendToAllOtherClients(message, conn, True)

            
        except Exception as e:
            print(f"Error in handling client {addr}: {e}")
            allClients.remove(conn)

            for client in playClients:
                if conn in client:
                    playClients.remove(client)
                    break

            conn.close()
            break

def getClients():
    while True:
        conn, addr = server.accept()
        allClients.append(conn)
        print(allClients)
        print(f"CONNECTED TO SERVER AT ADRESS - {addr}")
        newThread = threading.Thread(target=handleClient, args=(conn, addr))
        newThread.start()

getClients()