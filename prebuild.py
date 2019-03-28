#!/usr/bin/python
import os
import sys
import time;
print("run python script")
os.system("aws s3 cp s3://aws-hcl-scn-opendom/Jenkins/uploadfile.py c:\\temp\\")
os.system("aws s3 cp s3://aws-hcl-scn-opendom/Jenkins/timestamp c:\\temp\\")
os.system("aws s3 cp s3://aws-hcl-scn-opendom/Jenkins/auto.properties c:\\temp\\")
currentpath = os.getcwd()
print("currentpath:"+currentpath)
hostname = ""
rootDir = ""
jarprogram = ""
testtype = ""
deploydomino = ""
runautomationprogram = ""
od_publisher = ""
od_populator = ""
od_prebuild = ""
od_automation = ""
with open("c:\\temp\\auto.properties") as f:
	for line in f:
		strall = line
		if strall.find("hostname=") != -1:
			hostname = strall.split("=")[1].replace("\r","").replace("\n","")
		elif strall.find("rootDir=") != -1:
			dir = strall.split("=")[1].replace("\r","").replace("\n","")
			if dir[0] == '/':
				rootDir = "c:\\" + dir[1:]
		elif strall.find("PopulatorJarType=") != -1:
			if strall.split("=")[1].find("populator") != -1:
				jarprogram = "populator-test-1.0.0-SNAPSHOT.jar"
			else:
				jarprogram = "publisher-test-1.0.0-SNAPSHOT.jar"
		elif strall.find("TestType=") != -1:
			testtype = strall.split("=")[1].replace("\r","").replace("\n","")
		elif strall.find("DeployTheDomino=") != -1:
			deploydomino = strall.split("=")[1].replace("\r","").replace("\n","")
		elif strall.find("RunAutomationProgram=") != -1:
			runautomationprogram = strall.split("=")[1].replace("\r","").replace("\n","")
		elif strall.find("trigger_od_publisher=") != -1:
			od_publisher = strall.split("=")[1].replace("\r","").replace("\n","")
		elif strall.find("trigger_od_populator=") != -1:
			od_populator = strall.split("=")[1].replace("\r","").replace("\n","")
		elif strall.find("trigger_od_prebuild=") != -1:
			od_prebuild = strall.split("=")[1].replace("\r","").replace("\n","")
		elif strall.find("trigger_od_automation=") != -1:
			od_automation = strall.split("=")[1].replace("\r","").replace("\n","")

print("read end")
print(hostname)
print(rootDir)
print(jarprogram)
print(testtype)
print(deploydomino)
print(od_publisher)
print(od_populator)
print(od_prebuild)
print(od_automation)
filepro = currentpath + "\\automation\\open-domino-auto\\populator-executor\\src\\main\\resources\\com\\hcl\\opendomino\\spring\\populator-settings.properties"
result = ''
with open(filepro) as f:
	for line in f:
		strall = line
		if strall.find("populatorConfig.rootDir") != -1:
			result = result + "populatorConfig.rootDir=" + rootDir
		elif strall.find("populatorJar") != -1:
			result = result + "populatorJar=" + jarprogram
		elif strall.find("testType") != -1:
			result = result + "testType=\"" + testtype + "\""
		else:
			result = result + strall + "\r"

f = open(filepro, 'w')
f.write(result)
f.close()

