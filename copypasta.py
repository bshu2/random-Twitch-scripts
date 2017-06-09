# USAGE: copypasta.py channel [n]
# Copies a message if the last n user (efault 3) have sent the same message

import sys, socket, time, re

HOST = "irc.twitch.tv"
PORT = 6667
NICK = #your twitch username
PASS = #your oauth token
CHAN = "#" + sys.argv[1]
N = int(sys.argv[2]) if (len(sys.argv) == 3) else 3
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
DELAY = .1

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
prev_username, prev_message, prev_copypasta = "", "", ""
count = 0

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0) 
        message = CHAT_MSG.sub("", response)[:-2].strip()
        #print(username + ": " + message)

        if message == prev_copypasta:
            count = 0
        if username != prev_username and message == prev_message:
            count += 1
            if count >= N:
                s.send("PRIVMSG {} :{}\r\n".format(CHAN, message).encode("utf-8"))
                count = 0
                prev_copypasta = message
        else:
            count = 1

        prev_username = username
        prev_message = message
        time.sleep(DELAY)