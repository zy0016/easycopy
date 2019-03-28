#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime

s3mainfolder="s3://aws-hcl-scn-opendom/"

def readfilefile(filename):
	filelist = []
	folder = ""
	with open(filename) as f:
		for line in f:
			strall = line.strip()
			if strall.find("Directory") != -1:
				folder = strall.split(' ')[2]
			if strall.find(".jar") != -1 or strall.find(".dll") != -1 or strall.find(".properties") != -1:
				filelist.append(folder + "\\" + strall.split(" ")[-1])
	return filelist

def readtimestamp(stampfile):
	strall = ""
	with open(stampfile) as f:
		for line in f:
			strall = line.strip()
	return strall
	
def main(argv):
	subproject = argv[1]
	projecttype = argv[2]
	timestampfile = argv[3]
	filedata = argv[4]
	print("run from python subproject:" + subproject + " timestampfile:" + timestampfile + " projecttype:" + projecttype + " filedata:" + filedata)
	filenamelist = readfilefile(filedata)
	timestamp = readtimestamp(timestampfile)
	print("timestamp:" + timestamp)
	for id in filenamelist:
		if os.path.isfile(id):
			command = "aws s3 cp " + id + " " + s3mainfolder + subproject + "/" + projecttype + timestamp + "/win32/"
			print(command)
			os.system(command)
		else:
			print("can't find the " + id + ",skip the file")

	print("over")

if __name__ == '__main__':
    main(sys.argv)
