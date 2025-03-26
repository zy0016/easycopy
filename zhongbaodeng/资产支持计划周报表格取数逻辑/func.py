import time;
import os
import os.path

fileLocalPath = "C:\\temp"
tracepath = fileLocalPath + "\\debug.log"
oracle_base_path = 'E:\\app\\hspcadmin\\product'
ORACLE_SID = 'kfzgdb'
remote_path = "/djjs/Abs/"

fileSrcHost = "192.168.10.228"
fileSrcPort = 22
fileSrcUsername = "hundsun"
fileSrcPassword = "hundsun"

# fileDestHost = "192.168.19.110"
# fileDestPort = 21
# fileDestUsername = "admin"
# fileDestPassword = "bjkf@2017"

fileDestHost = "192.168.10.96"
fileDestPort = 22
fileDestUsername = "root"
fileDestPassword = "1234qwer!@#$"

dbip = '192.168.10.228'
dbport = 1521
dbSID = 'kfzgdb'
dbusername = 'interins'
dbpassword = 'hundsun'

# product_file_sync.py how many items it from your sql in one page.
pagecount = 20
filename_suffix = "资产支持计划表1.xlsx"

def savelog(strsen, display = True):
    if display:
        print(strsen)

    try:
        resultfile = open(tracepath,'a+')
        resultfile.write("[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "]" + strsen + "\n")
        resultfile.close()
    except Exception as e:
        pass


def deletefiles(filelist):
    for item in filelist:
        try:
            filepath = item.split(',')
            os.remove(filepath[0])
        except Exception as e:
            pass
