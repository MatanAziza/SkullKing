import re
import socket
import threading
from main import Game

bind_ip = "0.0.0.0"
bind_port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
# we tell the server to start listening with
# a maximum backlog of connections set to 5
server.listen(5)

def join_room(client_socket) -> str:
    client_socket.send("What's the room's name:".encode())
    while True:
        request = client_socket.recv(1024).decode("utf-8")
        if request == '\n':
            client_socket.send("KO: Cant join room with empty name!\nWhat's the room's name:".encode())
            continue
        if rooms.get(request[:-1], "error") != "error":
            break
        client_socket.send("KO: Room doesn't exists!\nWhat's the room's name:".encode())
    client_socket.send(f"OK: Room '{str(request[:-1])}' joined".encode())
    return request[:-1]

def create_room(client_socket) -> str:
    client_socket.send("What's your room name:".encode())
    while True:
        request = client_socket.recv(1024).decode("utf-8")
        if request == '\n':
            client_socket.send("KO: Cant create room with empty name!\nWhat's your room name:".encode())
            continue
        if rooms.get(request[:-1], "error") == "error":
            break
        client_socket.send("KO: Room already exists!\nWhat's your room name:".encode())
    client_socket.send(f"OK: Room created {str(request[:-1])}".encode())
    rooms.update({request[:-1]: Game()})
    return request[:-1]

def ask_name(client_socket, room: Game):
    client_socket.send("What's your username:".encode())
    while True:
        request = client_socket.recv(1024).decode("utf-8")
        if request == '\n':
            client_socket.send("KO: Cant create empty username!\nWhat's your username:".encode())
            continue
        players = [player.name for player in room.players]
        if request[:-1] in players:
            client_socket.send("KO: User already exists!\nWhat's your username:".encode())
            continue
        client_socket.send("Are you sure ? yes[y]/Enter | no[n]".encode())
        check = client_socket.recv(1024).decode("utf-8")
        if check in ["no\n", "n\n"]:
            continue
        break
    client_socket.send(f"OK: Joined with username {str(request[:-1])}".encode())
    return request[:-1]

print(f"[+] Listening on port {bind_ip} : {bind_port}")
rooms: dict[str, Game] = {}
#client handling thread
def handle_client(client_socket):
    #printing what the client sends
    request = client_socket.recv(1024).decode("utf-8")
    if request == 'host':
        print("[+] Host connected")
        room = create_room(client_socket)
    else:
        print("[+] Joiner connected")
        room = join_room(client_socket)
    name = ask_name(client_socket, rooms[room])
    rooms[room].add_player(name, room)
    print(name)
    #sending back the packet
    client_socket.close()

while True:
    # When a client connects we receive the
    # client socket into the client variable, and
    # the remote connection details into the addr variable
    client, addr = server.accept()
    print(f"[+] Accepted connection from: {addr[0]}:{addr[1]}")
    #spin up our client thread to handle the incoming data
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
