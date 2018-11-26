#!/usr/bin/python

import time;
from time import sleep,ctime
import shutil
import threading
import tkinter
from tkinter import messagebox
import pymouse,pykeyboard,os,sys
from pymouse import *
from pykeyboard import PyKeyboard
from ctypes import *
import ctypes
from win32gui import *
import win32gui
from win32con import *
import win32con

titles = set()
def foo(hwnd,nouse):
	if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
		titles.add(GetWindowText(hwnd))


def doactions(casename,key1num,actiontime):
	print("Run case:",casename," key1num:",key1num," actiontime:",actiontime)
	othertime = 0
	
	k = PyKeyboard()
	
	time.sleep(1)
	k.press_key(k.alt_l_key)
	time.sleep(1)
	k.release_key(k.alt_l_key)
	
	time.sleep(1)
	menuindex = 4
	for i in range(int(menuindex)):
		k.press_key(k.right_key)
		k.release_key(k.right_key)

	k.press_key(k.enter_key)
	k.release_key(k.enter_key)

	menuindex = 9
	for i in range(int(menuindex)):
		k.press_key(k.down_key)
		k.release_key(k.down_key)

	k.press_key(k.enter_key)
	k.release_key(k.enter_key)

	for i in range(int(key1num)):
		time.sleep(1)
		k.press_key(k.down_key)
		k.release_key(k.down_key)
		time.sleep(1)

	time.sleep(3)
	k.press_key(k.enter_key)
	k.release_key(k.enter_key)
	time.sleep(1)

	titles.clear()
	procHandle = win32gui.FindWindow(None,"Execution Security Alert")
	if procHandle == 0:
		EnumWindows(foo,0)
		lt = [t for t in titles if t]
		lt.sort()
		titles.clear()
		while True:
			time.sleep(1)
			EnumWindows(foo,0)
			lsw = [t for t in titles if t]
			lsw.sort()
			time.sleep(1)
			if "IBM Notes" in lsw or "Agent Log" in lsw:
				k.press_key(k.enter_key)
				k.release_key(k.enter_key)
				titles.clear()
				time.sleep(1)
			else:
				break

		return False

	while True:
		k.press_key(k.down_key)
		k.release_key(k.down_key)
		time.sleep(1)
		k.press_key(k.enter_key)
		k.release_key(k.enter_key)
		time.sleep(actiontime)
		ESA = win32gui.FindWindow(None,"Execution Security Alert")
		if ESA != 0:
			time.sleep(1)
			continue
		else:
			titles.clear()
			EnumWindows(foo,0)
			lsw = [t for t in titles if t]
			lsw.sort()
			# for i in lsw:
				# print(i)

			if "IBM Notes" in lsw or "Agent Log" in lsw:
				print(">>>>>>>>>>>>>>>find IBM Notes dialog")
				k.press_key(k.enter_key)
				k.release_key(k.enter_key)
				time.sleep(1)
			elif "Mail Send" in lsw:
				print(">>>>>>>>>>>>>>>find Mail Send dialog")
				k.press_key(k.escape_key)
				k.release_key(k.escape_key)
				time.sleep(1)
			else:
				print("other status")
				break

	return True


def ReadTestCaseFile(testcasefile):
	outputfilename = "menu_result.txt"
	
	resultfile = open(outputfilename,'a+')
	resultfile.write(testcasefile + "\n")
	resultfile.close()
	with open(testcasefile) as f:
		for line in f:
			if len(line) < 3:
				continue

			timedefault = 5
			actiontime = 1
			res = False
			key1 = ""
			if line[-1] == '\n':
				line = line[:-1]
			if line[-1] == '\r':
				line = line[:-1]

			arr = line.split(",")
			casename = arr[0]
			arrlen = len(arr)
			if arrlen == 3:
				param3 = arr[2]
				if param3.isdigit() == True:
					actiontime = int(param3)
					print("set new timer:",str(actiontime))

			
			key1 = arr[1].split("=")[1]
			res = doactions(casename,key1,actiontime)
			
			print(casename," result:",res," key1:",key1)
			
			resultfile = open(outputfilename,'a+')
			resultfile.write(casename + " result:" + str(res) + "\n")
			resultfile.close()
			
			time.sleep(timedefault)
			
def main():
	print("start at:", ctime())
	sourcepath = input("Enter your test case file path: ")
	m = PyMouse()
	x = 100
	y = 200
	m.move(x,y)
	m.click(x,y,1,1)
	ReadTestCaseFile(sourcepath)
	
	print("case end:", ctime())
	messagebox.showinfo("Test case","The test case is over!")
	
if __name__ == '__main__':
    main()
