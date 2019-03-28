#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime
import shutil
import threading

s3mainfolder="s3://aws-hcl-scn-opendom/"
projectlist = ["od-automation-staging","od-populator-staging","od-publisher-staging","od-prebuild-staging","od-automation","od-populator","od-publisher"]

def savesubfoldertofile(mainfolder,subfolder):
	command = "aws s3 ls " + mainfolder + subfolder + "/>" + subfolder + ".txt"
	print("\nsavesubfoldertofile command=" + command)
	os.system(command)

def readfileandhandle(mainfolder,subfolder,removefolderlist):
	timercount = 1
	folderlistfilename = subfolder + ".txt"
	with open(folderlistfilename) as f:
		for line in f:
			strall = line.strip()
			if strall.find("PRE") != -1:
				folder = strall.split(' ')[1][1:-1]
				if folder in removefolderlist:
					com1 = "aws s3 rm " + mainfolder + subfolder + "/" + strall.split(' ')[1] + " --recursive"
					print("\n" + com1 + "\n")
					os.system(com1)
					time.sleep(timercount)
					com2 = "aws s3 rm " + mainfolder + subfolder + "/" + strall.split(' ')[1]
					print("\n" + com2 + "\n")
					os.system(com2)

def action(folder,removefolderlist):
	print("\nHandle the " + folder + "\n")
	savesubfoldertofile(s3mainfolder,folder)
	commandlist = readfileandhandle(s3mainfolder,folder,removefolderlist)
	print("\naction " + folder + " end\n")

# class MyThread(threading.Thread):
	# def __init__(self,arg):
		# super(MyThread, self).__init__()
		# self.arg=arg
	# def run(self):
		# time.sleep(1)
		# print ("\nthe arg is:%s\r\n" % self.arg)

def main():
	removefolderlist = ["201903140200"]
	if len(removefolderlist):
		for i in projectlist:
			t =threading.Thread(target=action,args=(i,removefolderlist,))
			t.start()
		print("\nmain thread end.\n")
	else:
		print("removefolderlist is null")

if __name__ == '__main__':
	main()

