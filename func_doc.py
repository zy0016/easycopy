#!/usr/bin/env python
# Filename: func_doc.py

import urllib
import os
import requests
import json
import time
import random
import smtplib
from lxml import etree
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from PIL import Image
# import numpy as np

def log1(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
	
def log2(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log1
def now1():
    print('in now1');

    
@log2('execute---->')
def now3():
    print('in now3')


def get_one_page(url):
 headers = {
   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
 }
 response = requests.get(url,headers=headers)
 if response.status_code == 200:
   return response.text
 return None

def parse_one_page(html):
 data = json.loads(html)['cmts']
 for item in data:
   yield{
   'comment':item['content'],
   'date':item['time'].split(' ')[0],
   'rate':item['score'],
   'city':item['cityName'],
   'nickname':item['nickName']
   }

def save_to_txt():
 for i in range(1,1001):
   url = 'http://m.maoyan.com/mmdb/comments/movie/248566.json?_v_=yes&offset=' + str(i)
   html = get_one_page(url)
   print('Saving the %d page'% i)
   for item in parse_one_page(html):
     with open('xiazai.txt','a',encoding='utf-8') as f:
       f.write(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ',' +str(item['rate'])+','+item['comment']+'\n')
   time.sleep(5 + float(random.randint(1, 100)) / 20)
   
#########################################
# def openf():
	# a = np.array(Image.open('C:\9.jpg'))
	# b = [255,255,255] - a
	# im = Image.fromarray(b.astype('uint8'))
	# im.save('C:\91.jpg')
	# with open(u'C:\9.jpg', 'rb') as f:
		# print("open 9.jpg");

def sendemail():
	sender = 'zyabc12345@163.com'
	passWord = 'Z#y04690433{22>?'
	mail_host = 'smtp.163.com'
	receivers = ['zy0016@yeah.net']

	msg = MIMEMultipart()
	msg['Subject'] = "Title for python"
	msg['From'] = sender
	msg_content = "mail content"
	msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))
	with open(u'C:\input.txt', 'rb') as f:
		mime = MIMEBase('txt', 'txt', filename='input.txt')
		mime.add_header('Content-Disposition', 'attachment', filename='input.txt')
		mime.add_header('Content-ID', '<0>')
		mime.add_header('X-Attachment-Id', '0')
		mime.set_payload(f.read())
		encoders.encode_base64(mime)
		msg.attach(mime)

	try:
		s = smtplib.SMTP_SSL("smtp.163.com", 465)
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

###############################################################
# keyWord = input(f"{'Please input the keywords that you want to download :'}")
keyWord = "girl"
class Spider():
    def __init__(self):
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
        }
        self.filePath = ('C:\\temp\\1\\')

    def creat_File(self):
        filePath = self.filePath
        if not os.path.exists(filePath):
            os.makedirs(filePath)

    def get_pageNum(self):
        total = ""
        url = ("https://alpha.wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc").format(keyWord)
        html = requests.get(url)
        selector = etree.HTML(html.text)
        pageInfo = selector.xpath('//header[@class="listing-header"]/h1[1]/text()')
        string = str(pageInfo[0])
        numlist = list(filter(str.isdigit,string))
        for item in numlist:
            total += item
        totalPagenum = int(total)
        return totalPagenum

    def main_fuction(self):
        self.creat_File()
        count = self.get_pageNum()
        print("We have found:{} images!".format(count))
        times = int(count/24 + 1)
        j = 1
        for i in range(times):
            pic_Urls = self.getLinks(i+1)
            for item in pic_Urls:
                self.download(item,j)
                j += 1

    def getLinks(self,number):
        url = ("https://alpha.wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc&page={}").format(keyWord,number)
        try:
            html = requests.get(url)
            selector = etree.HTML(html.text)
            pic_Linklist = selector.xpath('//a[@class="jsAnchor thumb-tags-toggle tagged"]/@href')
        except Exception as e:
            print(repr(e))
        return pic_Linklist


    def download(self,url,count):
        string = url.strip('/thumbTags').strip('https://alpha.wallhaven.cc/wallpaper/')
        html = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + string + '.jpg'
        pic_path = (self.filePath + keyWord + str(count) + '.jpg' )
        try:
            pic = requests.get(html,headers = self.headers)
            f = open(pic_path,'wb')
            f.write(pic.content)
            f.close()
            print("Image:{} has been downloaded!".format(count))
            time.sleep(random.uniform(0,2))
        except Exception as e:
            print(repr(e))

# sendemail()
spider = Spider()
spider.main_fuction()
# now1()
# print("----------------")
# now3()
#if __name__ == '__main__':
	# openf()
	# sendemail()
	#save_to_txt()

	
	
