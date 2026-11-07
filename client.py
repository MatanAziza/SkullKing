import socket
import threading
from utils import wait
from sys import argv, exit

target_host = "0.0.0.0"
target_port = 4242
role: str = ""
if len(argv) == 1:
    role = "join"
else:
    if len(argv) != 2:
        print("Wrong number of args: need 'host' or 'join' ('join' by default)")
        exit()
    if argv[-1] not in ["join", "host"]:
        print("Wrong arg: need 'host' or 'join' ('join' by default)")
        exit()
    role = argv[-1]
#creating socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connecting the client
client.connect((target_host, target_port))
#sending data
client.send(role.encode())
#receiving the data
print(client.recv(4096).decode())
while True:
    while True:
        client.sendall((input()+'\n').encode())
        response = client.recv(4096).decode()
        if "QUESTION" in response:
            response = response[:response.index("QUESTION")]+'\n'+response[response.index("QUESTION"):]
        mark = response.split(" ")[0]
        print(response)
        if mark == "OK" or (mark == "WAIT" and role=="host"):
            if "QUESTION" not in response:
                print(client.recv(4096).decode())
            continue
        elif mark == "WAIT":
            anim = threading.Thread(target=wait, daemon=True)
            anim.start()
            response = client.recv(4096).decode()
            mark = response.split(" ")[0]
        if mark == "START":
            break
    if mark == "START":
        break
