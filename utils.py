from time import sleep

while True:
...     print("\033[2J\033[H", end='')
...     print("Waiting")
...     sleep(1)
...     print("\033[2J\033[H", end='')
...     print("Waiting .")
...     sleep(1)
...     print("\033[2J\033[H", end='')
...     print("Waiting ..")
...     sleep(1)    
...     print("\033[2J\033[H", end='')
...     print("Waiting ...")
...     sleep(1)
