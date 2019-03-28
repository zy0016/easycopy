#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime

s3mainfolder="s3://aws-hcl-scn-opendom/"

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
	filename = argv[4]
	desfolder = argv[5]
	print("run from python subproject:" + subproject + " timestampfile:" + timestampfile + " projecttype:" + projecttype + " filename:" + filename + " desfolder:" + desfolder)
	timestamp = readtimestamp(timestampfile)
	print("timestamp:" + timestamp)
	command = "aws s3 cp " + s3mainfolder + "/" + subproject + "/" + projecttype + timestamp + "/win32/" + filename + " " + desfolder
	print(command)
	os.system(command)

	print("over")

if __name__ == '__main__':
    main(sys.argv)
