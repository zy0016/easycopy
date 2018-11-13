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
import smtplib
from lxml import etree
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

titles = set()
def foo(hwnd,nouse):
	if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
		titles.add(GetWindowText(hwnd))
		
def fib(n):
	a = 0
	b = 1
	for _ in range(n):
		a,b = b,a+b
		yield a
		
def test1():
	for n in fib(500):
		print(n)
		
def read_file(fpath):
	print("read_file function:",fpath)
	BLOCK_SIZE = 1024
	with open(fpath) as f:
		for line in f:
			#print(line)
			block = f.read(BLOCK_SIZE)
			print(block)
			#if block:
			#	yield block 
			#else:
			#	return
	# with open(fpath, 'rb') as f:
		# print(fpath)
		# while True:
			# block = f.read(BLOCK_SIZE)
			# print("read")
			# if block:
				# print(block)
				# yield block 
			# else: 
				# return
exitFlag = 0
 
class myThread (threading.Thread):	 #????threading.Thread
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self):					 #?????????run???? ???????????run?? 
		print("Run Starting " + self.name)
		print_time(self.name, self.counter, 5)
		print("Run Exiting " + self.name)
 
def print_time(threadName, delay, counter):
	while counter:
		if exitFlag:
			(threading.Thread).exit()
		time.sleep(delay)
		print("\nprint_time %s: %s" % (threadName, time.ctime(time.time())))
		counter -= 1
		
def threadfunc1():
	thread1 = myThread(1, "Thread-1", 1)
	thread2 = myThread(2, "Thread-2", 2)
	thread1.start()
	thread2.start()
	print("Exiting Main Thread")
	
def sendemail():
	attachment_filename = 'debug.py'
	sender = 'zyabc12345@163.com'
	passWord = 'Z#y04690433{22>?'
	mail_host = 'smtp.163.com'
	receivers = ['zy0016@yeah.net']

	msg = MIMEMultipart()
	msg['Subject'] = "Title for python 2"
	msg['From'] = sender
	msg_content = "mail content"
	msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))
	with open(attachment_filename, 'rb') as f:
		mime = MIMEBase('txt', 'txt', filename=attachment_filename)
		mime.add_header('Content-Disposition', 'attachment', filename=attachment_filename)
		mime.add_header('Content-ID', '<0>')
		mime.add_header('X-Attachment-Id', '0')
		mime.set_payload(f.read())
		encoders.encode_base64(mime)
		msg.attach(mime)

	try:
		s = smtplib.SMTP_SSL(mail_host, 465)
		s.set_debuglevel(1)
		s.login(sender,passWord)
		for item in receivers:
			msg['To'] = to = item
			s.sendmail(sender,to,msg.as_string())
			print('Success!')
		s.quit()
		print ("All emails have been sent over!")
	except smtplib.SMTPException as e:
		print ("Falied,%s",e)
	
	
def main():
	print("start")
	sendemail()
	# threadfunc1()
	# sourcepath = input("Enter your test case file path: ")
	# read_file(sourcepath)
	# print("start at:", ctime())
	# test1()
	# print("case end:", ctime())
	# titles.clear()
	# EnumWindows(foo,0)
	# lt = [t for t in titles if t]
	# lt.sort()
	# for i in lt:
		# print(i," len=",len(i))

if __name__ == '__main__':
	main()
