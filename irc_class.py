import socket, sys, time

class IRC:
	irc = socket.socket()

	# Define the socket
	def __init__(self):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Transfer the data.
	def send(self, channel, msg):
		self.irc.send(bytes("PRIVMSG " + channel + " :" + msg + "\n", "UTF-8"))
	
	# Connect to the server, perform user authentication, and join the channel.
	def connect(self, server, port, channel, nick, password):
		self.irc.connect((server, port))
		self.irc.send(bytes("USER " + nick + " " + nick + " " + nick + " :python\n", "UTF-8"))
		self.irc.send(bytes("NICK " + nick + "\n", "UTF-8"))
		self.irc.send(bytes("NICKSERV IDENTIFY " + password + "\n", "UTF-8"))
		time.sleep(5)
		self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))
	
	# Get the response.
	def get_response(self):
		time.sleep(1)
		resp = self.irc.recv(2040).decode("UTF-8")
		return resp