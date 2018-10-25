#!/usr/bin/python

# import os
# import sys
import time;
from time import sleep,ctime
import shutil
import threading
import tkinter
import pymouse,pykeyboard,os,sys
from pymouse import *
from pykeyboard import PyKeyboard
from ctypes import *
import ctypes
from win32gui import *
import win32gui 


def doactions(actiontype):
	m = PyMouse() 
	k = PyKeyboard()
	k.press_key(k.space_key)
	k.release_key(k.space_key)
	time.sleep(1)
	procHandle = win32gui.FindWindow(None,"Execution Security Alert")
	if procHandle == 0:
		return False
	
	while True:
		if actiontype.find("MOUSECLICK") >= 0:
			k.press_key(k.down_key)
			k.release_key(k.down_key)
			time.sleep(1)
			k.press_key(k.enter_key)
			k.release_key(k.enter_key)
			time.sleep(1)
			ESA = win32gui.FindWindow(None,"Execution Security Alert")
			if ESA != 0:
				time.sleep(1)
				continue
			else:
				IN = win32gui.FindWindow(None,"IBM Notes")
				# if IN != 0:
					# print("find the IBM Notes dialog!",IN)
					# k.press_key(k.enter_key)
					# k.release_key(k.enter_key)
					# time.sleep(1)
				
				break

	return True
		

def ReadTestCaseFile(testcasefile):
	m = PyMouse()
	k = PyKeyboard()
	
	with open(testcasefile) as f:
		for line in f:
			casename=line.split(",")[0]
			action=line.split(",")[1]
			
			# if action.find("MOUSECLICK") >= 0:
				# print("action is MOUSECLICK")
			# else:
				# print(len(action))
				# print(action)
			
			res = doactions(action)
			print(casename," result:",res)
			
			resultfile = open("lsevaluate_result.txt",'a+')
			resstr = casename + " result:"
			if res == True:
				resstr = resstr + " True\n"
			else:
				resstr = resstr + " False\n"

			resultfile.write(resstr)
			resultfile.close()
			
			time.sleep(1)
			k.press_key(k.right_key)
			k.release_key(k.right_key)
			time.sleep(1)
			
def main():
	print("start at:", ctime())
	sourcepath = input("Enter your test case file path: ")
	m = PyMouse()
	k = PyKeyboard()
	x = 100
	y = 200
	m.move(x,y)
	m.click(x,y,1,1)
	ReadTestCaseFile(sourcepath)
	# h1 = win32gui.FindWindow(None,"IBM Notes")
	# print("IBM Notes handle=",h1)

	# h2 = win32gui.FindWindow(None,"(Untitled) - IBM Notes")
	# print("(Untitled) - IBM Notes handle=",h2)
	
	# m.move(x,y)
	# m.click(x,y,1,1)
	
	# doactions()
	
	# k.press_key(k.right_key)
	# k.release_key(k.right_key)
	# time.sleep(1)
	
	# doactions()
	
	# k.press_key(k.right_key)
	# k.release_key(k.right_key)
	# time.sleep(1)
	
	# doactions()
	
	# k.press_key(k.space_key)
	# k.release_key(k.space_key)
	# time.sleep(1)
	# k.press_key(k.down_key)
	# k.release_key(k.down_key)
	# time.sleep(1)
	# k.press_key(k.enter_key)
	# k.release_key(k.enter_key)
	
	

if __name__ == '__main__':
    main()
