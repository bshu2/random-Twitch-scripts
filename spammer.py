# USAGE: spammer.py channel message delay
# Periodically spams a channel with a specific message

import sys, socket, time

HOST = "irc.twitch.tv"
PORT = 6667
NICK = #your twitch username
PASS = #your oauth token
CHAN = "#" + sys.argv[1]
MSG = sys.argv[2]
DELAY = float(sys.argv[3])

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

while 1:
	s.send("PRIVMSG {} :{}\r\n".format(CHAN, MSG).encode("utf-8"))
	time.sleep(DELAY)