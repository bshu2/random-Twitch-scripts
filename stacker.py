# USAGE: stacker.py channel message [stack_height]
# Creates a pyramid of a message with a specified height (default 3)

import sys, socket, time

HOST = "irc.twitch.tv"
PORT = 6667
NICK = #your twitch username
PASS = #your oauth token
CHAN = "#" + sys.argv[1]
MSG = sys.argv[2] + " "
HEIGHT = int(sys.argv[3] if (len(sys.argv) == 4) else 3)
DELAY = 1.1

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

for i in range(1, HEIGHT + 1):
    time.sleep(DELAY)
    s.send("PRIVMSG {} :{}\r\n".format(CHAN, i*MSG).encode("utf-8"))
for i in range(HEIGHT - 1, 0, -1):
    time.sleep(DELAY)
    s.send("PRIVMSG {} :{}\r\n".format(CHAN, i*MSG).encode("utf-8"))