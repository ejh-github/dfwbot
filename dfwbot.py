import os, random, requests
from irc_class import *
from bs4 import BeautifulSoup

# Get quotes by author from brainy quotes, was broken in it's current state, but thanks Alaina. https://github.com/alainakafkes/brainscrape/blob/master/brainscrape.py
def getQuotesByAuthor(author, numpages):
	quotes = []
	pageNameArray = [author]
	for i in range(2,numpages+1):
		pageNameArray.append(author + "_" + str(i))

	# For every page pertaining to a topic, scrape it's contents.
	for page in pageNameArray:
		base_url = "http://www.brainyquote.com/quotes/authors/"
		url = base_url + author[0] + "/" + author + ".html"
		response_data = requests.get(url).text[:]
		soup = BeautifulSoup(response_data, 'html.parser')

		# Populate the quotes list
		for item in soup.find_all('a',{'title':'view quote'}):
			quotes.append(item.get_text().rstrip())

	return quotes

# Configure IRC
def irc_config(quotes):
	server = "irc.freenode.net"
	port = 6667
	channel = ""
	nick = "dfwbot"
	password = ""
	irc = IRC()
	irc.connect(server, port, channel, nick, password)
	triggers = [" god ", " christ ", " drugs ", " cia ", " trip ", " math ", "https"]

	# Look for triggers in the chat.
	while True:
		text = irc.get_response()
		print(text)
		if "PRIVMSG" in text and channel in text:
			for i in triggers:
				if i in text:
					irc.send(channel, random.choice(quotes))
					break

def main():
	quotes = getQuotesByAuthor("david_foster_wallace", 1)
	irc_config(quotes)

main()
