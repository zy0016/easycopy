#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime
import shutil
import threading

s3mainfolder="s3://aws-hcl-scn-opendom/"
folderlist = ["od-automation-staging","od-populator-staging","od-publisher-staging","od-prebuild-staging"]
# folderlist = ["od-automation","od-populator","od-publisher"]
# folderlist = ["od-automation-staging","od-populator-staging","od-publisher-staging","od-prebuild-staging","od-automation","od-populator","od-publisher"]

def savesubfoldertofile(mainfolder,subfolder):
	command = "aws s3 ls " + mainfolder + subfolder + "/>" + subfolder + ".txt"
	print("\nsavesubfoldertofile command=" + command)
	os.system(command)

def readfileandhandle(mainfolder,subfolder):
	comlist = []
	folderlistfilename = subfolder + ".txt"
	with open(folderlistfilename) as f:
		for line in f:
			strall = line.strip()
			if strall.find("PRE") != -1:
				comlist.append("aws s3 rm " + mainfolder + subfolder + "/" + strall.split(' ')[1])
	return comlist

def removefolder(comlist,subfolder):
	i = 0
	timercount = 1
	lslen = len(comlist)
	remaincount = 3
	print("\nIt will remove " + str(lslen - remaincount) + " folders for" + subfolder)
	for x in comlist[:-remaincount]:
		com1 = x + " --recursive"
		print("\n"+ str(i) + " " + com1)
		os.system(com1)
		time.sleep(timercount)
		print("\n"+ str(i) + " " + x)
		os.system(x)
		i+=1
		if i < lslen - remaincount:
			time.sleep(timercount)

def action(folder):
	print("\nHandle the " + folder + "\n")
	savesubfoldertofile(s3mainfolder,folder)
	commandlist = readfileandhandle(s3mainfolder,folder)
	removefolder(commandlist,folder)
	
for i in folderlist:
	t =threading.Thread(target=action,args=(i,))
	t.start()
	
	
# class MyThread(threading.Thread):
    # def __init__(self,arg):
        # super(MyThread, self).__init__()
        # self.arg=arg
    # def run(self):
        # time.sleep(1)
        # print ("\nthe arg is:%s\r\n" % self.arg)

# for i in folderlist:
    # t =MyThread(i)
    # t.start()
	
print("\nmain thread end.\n")
