# USAGE: stackbreaker.py channel
# Breaks pyramids of size 3 or greater

import sys, socket, time, re

HOST = "irc.twitch.tv"
PORT = 6667
NICK = #your twitch username
PASS = #your oauth token
CHAN = "#" + sys.argv[1]
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
DELAY = .1

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
prev_username, prev_message, stack = "", "", ""
stack_size = 1
descending = False

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0) 
        message = CHAT_MSG.sub("", response)[:-2].strip()
        #print(username + ": " + message)

        if username == prev_username and not descending and message == ((stack + " ")*(stack_size + 1)).strip():
            stack_size += 1
        elif username == prev_username and stack_size >= 3 and message == ((stack + " ")*(stack_size - 1)).strip():
            descending = True
            stack_size -= 1
            if stack_size == 2 and descending:
                s.send("PRIVMSG {} :{}\r\n".format(CHAN, stack).encode("utf-8"))
                descending = False
                stack = ""
                stack_size = 1
        else:
            stack = message
            stack_size = 1
            descending = False

        prev_username = username
        time.sleep(DELAY)