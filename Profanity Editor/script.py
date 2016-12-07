import os
import urllib
import urllib.request as url

def getText():
	quotes = open("CheckText.txt")
	content = quotes.read()
	quotes.close()	
	profanityCheck(content)

def profanityCheck(check_text):
	
	try:
		connection = url.urlopen("http://www.wdylike.appspot.com/?q=" + urllib.parse.quote(check_text))
		output = connection.read() 
		output = output.decode('ascii')
		connection.close()

		if output == 'true':
			print ("Profanity Alert")
		else:
			print ("Clean Code")

	except:
		print ("The Code Could not be scanned")			

getText()			
