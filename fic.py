import os
import shutil
import time

#st = os.stat(r"/etc/NetworkManager/system-connections/test.txt")

path = '/etc/NetworkManager/system-connections'
#pathForSavedConfigFiles = "/home/kiwi/Desktop/configFiles"
pathForSavedConfigFiles = os.path.join(os.path.expanduser("~"), "Desktop/configFiles")
TIMEINSECONDSBEFORENEXTCHECK = 3

listOfConfigFiles = []
listOfFileMetadata = []

#Step 1: Take note of all config files in the directory
for filename in os.listdir(path):
	listOfConfigFiles.append(filename)


numOfFiles = len(listOfConfigFiles);

#Step 2a Copy all files in the config directory to specified directory for backup
#Step 2b Also take note of the metadata of these files
for index in range(numOfFiles):
	configFile = listOfConfigFiles[index]
	srcdir = path + "/" + configFile
	dstdir = pathForSavedConfigFiles + "/" + configFile
	st = os.stat(srcdir)
	listOfFileMetadata.append(st)
	shutil.copy(srcdir, dstdir)

#Step 3 Create a permanment listener
while (1 == 1):
	time.sleep(TIMEINSECONDSBEFORENEXTCHECK)
	
	for index in range(numOfFiles):
		tempFile = listOfConfigFiles[index]
		filedir = path + "/" + tempFile

		#Try if file exists
		try:
			tempSt = os.stat(filedir)
			
			#If metadata is different, the backup is copied into the directory
			if (tempSt != listOfFileMetadata[index]):
				srcdir = pathForSavedConfigFiles + "/" + tempFile
				dstdir = path + "/" + tempFile
				shutil.copy(srcdir, dstdir)
				newSt = os.stat(dstdir)
				listOfFileMetadata.insert(index, newSt)
				print("Change detected.  " + tempFile + " has been used to update the directory.")
		
		#If file does not exist, the backup is copied into the directory
		except (OSError):
			srcdir = pathForSavedConfigFiles + "/" + tempFile
			dstdir = path + "/" + tempFile
			shutil.copy(srcdir, dstdir)
			newSt = os.stat(dstdir)
			listOfFileMetadata.insert(index, newSt)
			print("Change detected.  " + tempFile + " has been used to update the directory.")
