#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime
import shutil
import threading
import tkinter

s3mainfolder="s3://aws-hcl-scn-opendom/"
resultfile = "result.txt"
def savesubfoldertofile(mainfolder,subfolder):
	command = "aws s3 ls " + mainfolder + subfolder + "/>" + resultfile
	print("savesubfoldertofile command=" + command)
	os.system(command)

def readfileandhandle(mainfolder,subfolder):
	comlist = []
	with open(resultfile) as f:
		for line in f:
			strall = line.strip()
			if strall.find("PRE") != -1:
				comlist.append("aws s3 rm " + mainfolder + subfolder + "/" + strall.split(' ')[1])
	return comlist

def removefolder(comlist):
	i = 0
	timercount = 1
	lslen = len(comlist)
	remaincount = 2
	print("Remove " + str(lslen - remaincount) + " folders.")
	for x in comlist[:-remaincount]:
		com1 = x + " --recursive"
		print(str(i) + " " + com1)
		os.system(com1)
		time.sleep(timercount)
		print(str(i) + " " + x)
		os.system(x)
		i+=1
		if i < lslen - remaincount:
			time.sleep(timercount)

def main():
	subfolderstr = input("Please input the subfolder name:")
	savesubfoldertofile(s3mainfolder,subfolderstr)
	commandlist = readfileandhandle(s3mainfolder,subfolderstr)
	removefolder(commandlist)
	print("over")

if __name__ == '__main__':
    main()
