import socket
import threading
from game import Game
from classes.cli import CLI
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

def game_manager(g: dict[str, Game], name: str):
    game = next(iter(g.values()))
    rounds = 10
    for ante in range(rounds):
        game.deal()
        game.bets()
        for i in range(len(game.players[0].hand)):
            game.next(name, False, i)
            # for player in game.players:
            #     if player.name == name:
            #         t = threading.Thread(target=player.signal, args=(game, f"OK {game.hands_recap()}Cards played:",))
            #         t.start()
            #     else:
            #         player.send(f"OK Waiting for the host to {["start", "continue"][i != 0]} ...")
            # t.join()
            game.plis()
        oz = game.recap()
        game.ante += 1
        if ante == rounds - 1:
            game.end(name, oz)
        else:
            game.next(name, True, 1)
    for player in game.players:
        player.interface.close()


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
        rooms[room].add_player(name, interface, room)
        if role == 'host':
            interface.start(rooms[room])
            rooms[room].start = 1
            threading.Thread(target=game_manager, args=({room: rooms.pop(room)}, name)).start()
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
            for player in rooms[room].players:
                if player.name != name:
                    player.send("STOP An error has occured with the room you were in. Room closed.")
            rooms.pop(room)

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
    client, addr = server.accept()
    print(f"\n[+] Accepted connection from: {addr[0]}:{addr[1]}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
