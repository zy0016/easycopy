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


def doactions(casename,actiontype):
	print("Run case:",casename)
	m = PyMouse() 
	k = PyKeyboard()
	k.press_key(k.space_key)
	k.release_key(k.space_key)
	time.sleep(1)
	titles.clear()
	procHandle = win32gui.FindWindow(None,"Execution Security Alert")
	if procHandle == 0:
		EnumWindows(foo,0)
		lt = [t for t in titles if t]
		lt.sort()
		if "IBM Notes" in lt:
			k.press_key(k.enter_key)
			k.release_key(k.enter_key)
			time.sleep(1)

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
				titles.clear()
				EnumWindows(foo,0)
				lsw = [t for t in titles if t]
				lsw.sort()
				if "IBM Notes" in lsw:
					print(">>>>>>>>>>>>>>>find IBM Notes dialog")
					k.press_key(k.enter_key)
					k.release_key(k.enter_key)
					time.sleep(1)
				elif "Mail Send" in lsw:
					print(">>>>>>>>>>>>>>>find Mail Send dialog")
					k.press_key(k.escape_key)
					k.release_key(k.escape_key)
					time.sleep(1)

				break

	return True


def ReadTestCaseFile(testcasefile):
	outputfilename = "test_result.txt"
	m = PyMouse()
	k = PyKeyboard()
	
	resultfile = open(outputfilename,'a+')
	resultfile.write(testcasefile + "\n")
	resultfile.close()
	with open(testcasefile) as f:
		for line in f:
			if len(line) < 3:
				continue
			if line[-1] == '\n':
				line = line[:-1]
			if line[-1] == '\r':
				line = line[:-1]
			
			timedefault = 1
			arr = line.split(",")
			casename = arr[0]
			action = arr[1]
			arrlen = len(arr)
			if arrlen == 3:
				param3 = arr[2]
				if param3.isdigit() == True:
					timedefault = int(param3)
					print("set new timer:",str(timedefault))


			res = doactions(casename,action)
			print(casename," result:",res)
			
			resultfile = open(outputfilename,'a+')
			resstr = casename + " result:"
			if res == True:
				resstr = resstr + " True\n"
			else:
				resstr = resstr + " False\n"

			resultfile.write(resstr)
			resultfile.close()
			
			time.sleep(timedefault)
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
	
	print("case end:", ctime())
	messagebox.showinfo("Test case","The test case is over!")
	
if __name__ == '__main__':
    main()
