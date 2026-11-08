import socket
import threading
from main import Game
from cli import CLI
from typing import Any

bind_ip = "0.0.0.0"
bind_port = 4242

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
# we tell the server to start listening with
# a maximum backlog of connections set to 5
server.listen(5)

print(f"[+] Listening on port {bind_ip} : {bind_port}")
rooms: dict[str, Any] = {}

def game_manager(game: Game):
    for player in game.players:
        player.bet()

def handle_client(client_socket):
    name, room = '', ''
    role = client_socket.recv(1024).decode("utf-8")
    interface = CLI(client_socket)
    try:
        if role == 'host':
            print("[+] Host connected\n> ", end='')
            game = interface.create_room(rooms)
            rooms.update(game)
            room = next(iter(game.keys()))
        else:
            print("[+] Joiner connected\n> ", end='')
            room = interface.join_room(rooms)
        name = interface.ask_name(rooms[room], role)
        rooms[room].add_player(name, client, room)
        if role == 'host':
            interface.start(rooms[room])
            rooms[room].start = 1
            threading.Thread(target=game_manager, args=(rooms.pop(room,)))
        else:
            while not rooms[room].start:
                continue
    except BrokenPipeError:
        if room == '':
            print("Room wasnt created\n> ", end='')
        elif name == '':
            if role == 'host':
                print(f"Room {room} will be closed.\n> ", end='')
                rooms.pop(room)
            else:
                print("Unknown player left the server.\n> ", end='')
        else:
            print("Need to delete whole game and send msg to everybody.\n> ", end='')
            # rooms[room].remove_player(name)
    client_socket.close()

def handle_server():
    options = {"help": "Display all commands", "rooms": "Display all existing rooms and the players in it"}
    while True:
        i = input("What is your request?\n> ")
        if i == "rooms":
            if not rooms:
                print("No rooms created right now")
                continue
            for r, g in rooms.items():
                print(f"Room {r} players:")
                print("- "+"\n- ".join([p.name for p in g.players]))
        elif i == "help":
            print("\n".join([f"{k}: {v}" for k, v in options.items()]))
threading.Thread(target=handle_server).start()
while True:
    # When a client connects we receive the
    # client socket into the client variable, and
    # the remote connection details into the addr variable
    client, addr = server.accept()
    print(f"\n[+] Accepted connection from: {addr[0]}:{addr[1]}")
    #spin up our client thread to handle the incoming data
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
