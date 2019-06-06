#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime

separator = "\\" if sys.platform == 'win32' else "/"
def main(argv):
	filenamein = argv[1]
	filenameout= argv[2]
	pathname = argv[3]
	path = ""
	htmllist = []
	strfiles = ""
	strresult = ""
	with open(pathname) as f:
		for line in f:
			path = line
			break
	
	with open(filenamein) as f:
		for line in f:
			f1 = path + separator + line
			f2 = f1.replace("\n","").replace("\r","")
			htmllist.append(f2)
	
	for singlfile in htmllist:
		strresult = ""
		bAddTableTitle = False
		with open(singlfile) as f:
			for line in f:
				strall = line.strip()
				if strall.find("FAIL") != -1:
					if strall.find(".html") != -1:
						# for title
						strresult = "<hr><table border=\"1\"><tbody><tr><th scope=\"row\">Test Case</th><td><b>Result</b></td><td><b>Execution Time</b></td><td><b>Start Time</b></td>" + strall + "</td></tr></tbody></table><table border=\"1\"><tbody>\n"
					else:
						if bAddTableTitle == True:
							strresult = strresult + strall + "\r\n"
						else:
							bAddTableTitle = True
							if strall.find("Test Case ID") != -1:
								strresult = strresult + strall + "\r\n"
							else:
								strresult = strresult + "<tr><td>No.</td><td>Test Case ID</td><td>Action Name</td><td>Result</td><td>Detailed Informatin</td><td>Start Time</td></tr>" + strall + "\r\n"

			strresult = strresult + "</tbody></table></body>\r\n"
			strfiles = strfiles + strresult

	resultfile = open(filenameout,'w')
	resultfile.write(strfiles + "\n")
	resultfile.close()

if __name__ == '__main__':
	main(sys.argv)
