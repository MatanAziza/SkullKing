import socket
import threading
from utils import wait
from sys import argv, exit

def clean_comm(message: str) -> str:
    return message[message.index(' ')+1:]

def treat_ip():
    while True:
        ip = input("What IP address do you want to connect to? (default to 0.0.0.0)\n")
        if not ip:
            return "0.0.0.0"
        parts = ip.split(".")
        if len(parts) != 4:
            print("Wrong format.")
            continue
        for part in parts:
            try:
                nb = int(part)
                if nb < 0 or nb > 255:
                    raise Exception
            except ValueError:
                print(f"{part} is not a valid IP format.")
                continue
            except Exception:
                print("IP part cant be outside of 0-255 scope.")
                continue
        return ip


target_port = 4242
role: str = "join"
if len(argv) > 2:
    print("Wrong number of args: need 'host' or 'join' ('join' by default)")
    exit()
else:
    if len(argv) == 2:
        if argv[1] not in ["join", "host"]:
            print("Wrong arg: need 'host' or 'join' ('join' by default)")
            exit()
        role = argv[-1]
target_host = treat_ip()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send(role.encode())

# QUESTION: Expects answer -> client sendall
# CHECK: Expect answer -> client sendall
# KO : RE-asks QUESTION -> QUESTION
# OK: Send info -> client receive

while True:
    requests = client.recv(4096).decode().split("\t")
    requests = [r for r in requests if r]
    for request in requests:
        r = clean_comm(request) if not request.startswith(("HOST", "JOIN", "START")) else request
        print(r if not r.startswith(("JOIN", "START")) else "\033[2J\033[HWaiting for the game to start ...")
        if request.startswith("STOP"):
            exit()
        if request.startswith(("QUESTION", "CHECK")):
            client.sendall((input()+'\n').encode())
        elif request.startswith("JOIN"):
            anim = threading.Thread(target=wait, daemon=True)
            # anim.start()
        elif request.startswith("START"):
            break
