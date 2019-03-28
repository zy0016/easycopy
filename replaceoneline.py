#!/usr/bin/python

import os
import sys
import time;

# def main():
currentpath = os.getcwd()
print("currentpath:"+currentpath)
result = ''
with open("pom.xml") as f:
	for line in f:
		strall = line
		if strall.find("<Include-Resource>ndominojavacapi.dll") != -1:
			strall = strall.replace("ndominojavacapi.dll",currentpath + "\\ndominojavacapi.dll")
		
		result = result + strall + "\r"
		
f = open("pom.xml", 'w')
f.write(result)
f.close()

# if __name__ == '__main__':
    # main()
