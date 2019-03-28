#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime

def readfilefile(filename):
	filelist = []
	folder = ""
	with open(filename) as f:
		for line in f:
			strall = line.strip()
			if strall.find("Directory") != -1:
				folder = strall.split(' ')[2]
			if strall.find(".jar") != -1:
				filelist.append(folder + "\\" + strall.split(" ")[-1])
	return filelist
	
def main(argv):
	filedata = argv[1]
	groupid = argv[2]
	artifactId = argv[3]
	version = argv[4]
	print("run from python filedata:" + filedata)
	filenamelist = readfilefile(filedata)
	for id in filenamelist:
		command = "mvn install:install-file -Dfile=" + id + " -DgroupId=" + groupid + " -DartifactId=" + artifactId + " -Dversion=" + version + " -Dpackaging=jar"
		print(command)
		os.system(command)

	print("over")

if __name__ == '__main__':
    main(sys.argv)
