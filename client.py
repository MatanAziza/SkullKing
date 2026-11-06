import socket
from sys import argv, exit

target_host = "0.0.0.0"
target_port = 8080
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
response = client.recv(4096)
print(response.decode())
while True:
    client.sendall((input()+'\n').encode())
    response = client.recv(4096).decode()
    if response[:2] != "OK":
        print(response)
        continue
    print(response)
    break
print(client.recv(4096).decode())
while True:
    client.sendall((input()+'\n').encode())
    response = client.recv(4096).decode()
    if response[:2] != "OK":
        print(response)
        continue
    print(response)
    break
