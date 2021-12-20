import socket
import threading
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 3389))
 
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left'.encode('ascii'))
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        try:
            client,address = server.accept()
            print(f"{str(address)} connected.")
            client.send('ready'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            print(f'Nickname of the client is {nickname}')
            broadcast(f'{nickname} joined'.encode('ascii'))
            client.send('Connected to the server!'.encode('ascii'))
            
            thread = threading.Thread(target=handle,args=(client,))
            thread.start()
        except:
            recieve()

print("Server is listening")
recieve()