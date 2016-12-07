#Code Designed using Ubuntu Operating System using Python 3.4
#Bear with me for Bad Code Practices
#Code designed for hourly breaks...change accordingly

import webbrowser
import time
import vlc
import os

print ("Lets set you up for your breaks :D")
print ("Lets fill up some information before we set you up...")
print ("Am using vlc media player for songs and videos...customize accordingly\n")

breaks = int(input("How many breaks do you want?\n"))
breakTime = int(input("After how many hours do you want break?\n"))

indA = []
durA = []
linkA = []
itr = 0

print("Before we begin lets set a few ground rules for input")
print("1 for youtube video (video link please)")
print("2 for song (song path please)")
print("3 for tv series (video path please)")

print("Okay...lets begin\n")

while(itr < breaks):
	
	index = int(input("What do you wanna do?\n"))
	link = input("Enter the link/path \n")
	duration = int(input("Expected duration of your break in minutes? \n"))
	indA.append(index)
	durA.append(duration)
	linkA.append(link)
	itr = itr + 1

print("Let the party begin..... :D")
print("Party start time: "+time.ctime())

itr = 0

while(itr < breaks):
	
	time.sleep(breakTime)
	if(indA[itr] == 1):
		webbrowser.open(linkA[itr])
	else:
		text = "vlc " + linkA[itr]
		os.system(text)
	time.sleep(durA[itr]*60)
	itr = itr + 1	