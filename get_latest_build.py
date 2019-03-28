#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime

s3mainfolder="s3://aws-hcl-scn-opendom/"
folderlistfile = "folderlist.txt"
filelistfile = "filelist.txt"
def getlastbuilditem(resultfile):
	comlist = []
	with open(resultfile) as f:
		for line in f:
			strall = line.strip()
			if strall.find("PRE") != -1:
				comlist.append(strall.split(' ')[1])
	return comlist[-1]
	
def downloadfiles(filelist,subproject,foldername,desfolder):
	with open(filelist) as f:
		for line in f:
			strall = line.strip()
			filename = strall.split(" ")[-1]
			command = "aws s3 cp " + s3mainfolder + subproject + "/" + foldername + "win32/" + filename + " " + desfolder
			print(command)
			os.system(command)
			
def main(argv):
	subproject = argv[1]
	desfolder = argv[2]
	command1 = "aws s3 ls " + s3mainfolder + subproject + "/>" + folderlistfile
	print(command1)
	os.system(command1)
	
	lastbuilditem = getlastbuilditem(folderlistfile)
	command2 = "aws s3 ls " + s3mainfolder + subproject + "/" + lastbuilditem + "win32/>" + filelistfile
	print(command2)
	os.system(command2)
	
	downloadfiles(filelistfile,subproject,lastbuilditem,desfolder)

	os.remove(folderlistfile)
	os.remove(filelistfile)
	print("over")

if __name__ == '__main__':
    main(sys.argv)
