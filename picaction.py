#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime
import shutil
import threading
import tkinter
from PIL import Image
from PIL import ImageChops 

def scanfile(filepath_sour):
	pic_type_groups = [".bmp",".png",".gif",".jpg",".jpeg"]
	filelist = []
	list = os.listdir(filepath_sour)
	for i in range(0,len(list)):
		path = os.path.join(filepath_sour,list[i]).lower()
		if os.path.isfile(path):
			extendfilename = os.path.splitext(path)[-1]
			if extendfilename in pic_type_groups:
				filelist.append(path)
					
	checkfilelist = []
	samefilelist = []
	for i in filelist:
		for j in filelist:
			if i == j:
				continue
			# print("----->>>>>>>>begin-----")
			# for m in checkfilelist:
				# print(">>>>>>>>>>",m)
			# print("----->>>>>>>>end-------")
			if i in checkfilelist:
				# print(i,"in checkfilelist")
				continue
			else:
				print("checkfilelist append ",i)
				checkfilelist.append(i)
				
			print("==========")
			print("i = ",i)
			print("j = ",j)
			# print("-----begin-----")
			# for m in checkfilelist:
				# print(m)
			# print("-----end-------")
			
			file1 = Image.open(i)
			file2 = Image.open(j)
			try:
				diff = ImageChops.difference(file1, file2)
				if diff.getbbox() is None:
					samefilelist.append(i)
				else:
					diff.save(diff_save_location)
			except ValueError as e:
				# text = ("Pastes another image into this image."
				# "The box argument is either a 2-tuple giving the upper left corner, a 4-tuple defining the left, upper, "
				# "right, and lower pixel coordinate, or None (same as (0, 0)). If a 4-tuple is given, the size of the pasted "
				# "image must match the size of the region.")
				# print("{0}{1}".format(e,text))
				print("exception i:",i)
				samefilelist.append(i)

	print("output samefilelist len=",str(len(samefilelist)))
	for k in samefilelist:
		print(k)
		
	print("output checkfilelist")
	for k in checkfilelist:
		print(k)

def main():
	sourcepath = input("Enter your source path: ")
	
	if os.path.isdir(sourcepath) == True:
		scanfile(sourcepath)
	else:
		print ("invalid path:", sourcepath)

if __name__ == '__main__':
	main()
