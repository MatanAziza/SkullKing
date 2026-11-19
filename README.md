# SkullKing

SkullKing is a terminal-based, multiplayer recreation of **Skull King**, the card game created by Brent & Jeffrey Beck.

This project implements the game with some custom rules introduced by friends I play with. Classic game settings are coming soon.

The [rulebook](en-rules.pdf) explains everything you need to know to play. The game also prevents you from performing certain invalid actions.

## Features

- Terminal-based multiplayer gameplay
- Client/server architecture using TCP
- Local network play
- Custom house rules
- In-game instructions and validation

## Requirements

- A terminal
- The [`server.zip`](https://github.com/MatanAziza/SkullKing/releases/download/0.9/server.zip) release (for the host only)
- The [`client.zip`](https://github.com/MatanAziza/SkullKing/releases/download/0.9/client.zip) release (for every player)
- A local network connection, or a virtual LAN such as [Hamachi](https://www.vpn.net/) for remote play

## How to Play

On the **Releases** page, you will find two downloadable archives:

| File | Who needs it | Purpose |
| --- | --- | --- |
| `server.zip` | One player | Hosts the game |
| `client.zip` | Every player | Connects to and plays the game |

Only one player needs to run the server. All other players connect to it using the client.

### Start the Server

1. Download and extract `server.zip`.
2. Open a terminal in the extracted folder.
3. Run the server:

```bash
./server
```

Linux is supported. Windows support still needs to be checked.

Once the server is running, note your IP address. You will need to share it with the other players.

On Linux, you can find your local IP address with:

```bash
ip addr
```

If you are using Hamachi or another virtual private network tool, use the IP address it provides.

> **Important:** The server is TCP-based. Players must be able to reach the host over the local network or through a virtual LAN.

### Start the Client

1. Download and extract `client.zip`.
2. Open a terminal in the extracted folder.
3. Choose one of the following options:

#### Host a Game

To create and host a game, run:

```bash
./client host
```

You will be asked to choose a room name. Share that room name with your friends so they can join.

#### Join a Game

To join an existing game, run:

```bash
./client
```

### Connect to a Game

Before joining, the client asks for the IP address of the server.

- If you are hosting the server, press `Enter` to use the default address.
- If someone else is hosting the server, ask them for their IP address and enter it.

After entering the IP address, you will be asked to provide:

1. The room name
2. Your username

Then follow the instructions shown in the client.

## Playing Remotely

If you and your friends are not on the same local network, use a virtual LAN solution such as Hamachi.

1. The host creates or joins a virtual LAN.
2. The other players join the same virtual LAN.
3. The host shares the IP address provided by the virtual LAN tool.
4. Players launch the client and enter that IP address.

## Troubleshooting

- **Cannot connect:** Make sure the server is running and that you entered the correct IP address.
- **Not on the same network:** Use Hamachi or another virtual LAN tool.
- **Server does not start:** Make sure you extracted `server.zip` and are running the command from the correct folder.
- **Windows support:** The server is currently confirmed to work on Linux; Windows support still needs to be checked.

Enjoy!
