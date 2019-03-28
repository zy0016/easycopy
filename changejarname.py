#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime

s3mainfolder="s3://aws-hcl-scn-opendom/"
separator = "\\" if sys.platform == 'win32' else "/"
def readfilefile(filename):
	filedatalist = []
	folder = ""
	with open(filename) as f:
		for line in f:
			strall = line.strip()
			if strall.find("Directory") != -1:
				folder = strall.split(' ')[2]
				filedatalist.append(folder)
			if strall.find(".jar") != -1 and strall.find("-") != -1:
				filedatalist.append(folder + "\\" + strall.split(" ")[-1])
				filedatalist.append(strall.split(" ")[-1])
	return filedatalist

def readtimestamp(stampfile):
	strall = ""
	with open(stampfile) as f:
		for line in f:
			strall = line.strip()
	return strall
	
def main(argv):
	timestampfile = argv[1]
	filedata = argv[2]
	print("run from python timestampfile" + timestampfile + " filedata:" + filedata)
	filedatalist = readfilefile(filedata)
	timestamp = readtimestamp(timestampfile)
	print("timestamp:" + timestamp)
	# filedatalist[0]: current folder
	# filedatalist[1]: full file path.
	# filedatalist[2]: only file's name.
	if len(filedatalist) != 0:
		projectname = filedatalist[2].split("-")[0]
		newfilename = filedatalist[0] + separator + projectname + "-" + timestamp + ".jar"
		print("newfilename:" + newfilename)
		os.rename(filedatalist[1],newfilename)
		
		f = open("c:\\temp\\filename.properties", 'w')
		f.write(projectname + "-" + timestamp + ".jar")
		f.close()

	print("over")

if __name__ == '__main__':
    main(sys.argv)
