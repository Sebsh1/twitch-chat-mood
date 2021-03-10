import socket
import logging
import re
import json
from datetime import datetime

def get_chat_messages(channel_name):
    print("Connecting to chat...")
    
    server = 'irc.chat.twitch.tv'
    port = 6667
    channel = f'#{channel_name}'

    with open('twitch_api_cred.txt') as f: 
                data = f.read() 
                js = json.loads(data) 
    nickname = js["nickname"]
    token = js["token"]

    sock = socket.socket()
    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    sock.recv(2048).decode('utf-8') # Welcome Message
    sock.recv(2048).decode('utf-8') # Joining the channel

    print("Connection established...")

    while True:
        resp = sock.recv(2048).decode('utf-8')
        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        elif len(resp) > 0:
            time = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
            _, _, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp).groups()
            yield(time, message) 
            
    sock.close()

if __name__ == "__main__":
    for time, msg in get_chat_messages("sovietwomble"):
        print(time, msg)
    #get_chat_messages("sovietwomble")