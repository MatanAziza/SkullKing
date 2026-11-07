import re
import socket
import threading
from main import Game
from cli import CLI

bind_ip = "0.0.0.0"
bind_port = 4242

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
# we tell the server to start listening with
# a maximum backlog of connections set to 5
server.listen(5)

print(f"[+] Listening on port {bind_ip} : {bind_port}")
rooms: dict[str, Game] = {}
#client handling thread
def handle_client(client_socket):
    #printing what the client sends
    request = client_socket.recv(1024).decode("utf-8")
    interface = CLI(client_socket)
    if request == 'host':
        print("[+] Host connected")
        game = interface.create_room(rooms)
        rooms.update(game)
        room = next(iter(game.keys()))
    else:
        print("[+] Joiner connected")
        room = interface.join_room(rooms)
    name = interface.ask_name(rooms[room])
    rooms[room].add_player(name, client, room)
    if request == 'host':
        interface.start(rooms[room])
        rooms[room].start = 1
    else:
        while not rooms[room].start:
            continue
    print(name, room)
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
