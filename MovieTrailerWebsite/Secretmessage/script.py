import os
import time

currentDirectory = os.getcwd()
finalDirectory = currentDirectory + '/prank'
files = os.listdir(finalDirectory)

os.chdir(finalDirectory)

for file in files:

	newname = ''.join(i for i in file if i.isalpha())
	print (file + "--->" + newname)
	os.rename(file, newname)

os.chdir(currentDirectory)