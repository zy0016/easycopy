﻿import os
from datetime import datetime, date, timedelta
import sys
import time;
from FTPSync import FTPSync
from product_file_sync import SSHSession
from func import savelog

# if __name__ == '__main__':
#     # 文件服务器配置信息
#     fileSrcHost = "172.16.117.26"
#     fileSrcPort = 22
#     fileSrcUsername = "ita"
#     fileSrcPassword = "zgita@2016"
#     fileSrcRemotepath = "/home/fileserver/fundcrm/accessory/Tblobstorage"

#     fileLocalPath = "C:/estimate/fundcrmfile"

#     fileDestHost = "172.16.117.38"
#     fileDestPort = 21
#     fileDestUsername = "zggz"
#     fileDestPassword = "0V84zH1d"
#     fileDestRemotePath = "./"

#     # 产品数据库配置信息
#     dbip = '172.16.117.25'
#     dbport = 1521
#     dbSID = 'ZGDBRAC'
#     dbusername = 'fundcrm'
#     dbpassword = 'bjsZBD_2018'

#     # ta数据库配置信息
#     tadbip = '172.16.117.25'
#     tadbport = 1521
#     tadbSID = 'ZGDBRAC'
#     tadbusername = 'ta4'
#     tadbpassword = 'bjsZBD_2018'

#     # 是否下载附件
#     downLoadFile = True
#     # 开始日期
#     startDate = datetime.now().strftime('%Y%m%d')
#     # 结束日期
#     endDate = startDate
#     templetids = ['8', '6']

#     if len(sys.argv) > 2:
#         startDate = sys.argv[1]
#         endDate = sys.argv[2]
#         if len(sys.argv) > 3:
#             if str(sys.argv[3]).lower() == 'true':
#                 downLoadFile = True
#             else:
#                 downLoadFile = False

#     ftpLocalDir = fileLocalPath + os.path.sep + endDate

#     try:
#         xfer = SSHSession(fileSrcHost, fileSrcPort, fileSrcUsername, fileSrcPassword, dbip, dbport, dbSID, dbusername,dbpassword)
#         # 先清空目录
#         xfer.del_file(ftpLocalDir)

#         for templetid in templetids:
#             fundcodes = xfer.getFundcodes(templetid, startDate, endDate, fileLocalPath)
#             if downLoadFile:
#                 for fundinfo in fundcodes:
#                     fundcode = fundinfo.split(',')
#                     xfer.read_tblobstorage_table(fileSrcRemotepath, fileLocalPath, fundcode[0], endDate, fundcode[1])
#             fundtypeName = xfer.getTempleName(templetid)
#             print('【共处理' +fundtypeName+ str(len(fundcodes)) + '个产品】')

#         for templetid in templetids:
#             fundcodes = xfer.getDurationFundinfo_Cash(templetid, startDate, endDate, fileLocalPath)
#             if downLoadFile:
#                 for fundinfo in fundcodes:
#                     fundcode = fundinfo.split(',')
#                     xfer.read_tblobstorage_table_Cash(fileSrcRemotepath, fileLocalPath, fundcode[0], endDate, fundcode[1])
#             fundtypeName = xfer.getTempleName(templetid)
#             print('【共处理兑付' + fundtypeName + str(len(fundcodes)) + '个产品】')

#         # 获取存续期产品信息
#         xfer.getDurationFundinfo(startDate, endDate, fileLocalPath)
#         # 链接TA
#         ita = SSHSession(fileSrcHost, fileSrcPort, fileSrcUsername, fileSrcPassword, tadbip, tadbport, tadbSID,tadbusername, tadbpassword)
#         ita.getFundInfoByTA(fileLocalPath, startDate, endDate)

#         # 上传到目的FTP
#         print('上传附件到ftp开始')
#         ftp = FTPSync(fileDestHost, fileDestPort)
#         ftp.login(fileDestUsername, fileDestPassword)

#         ftp.put_dir(ftpLocalDir, fileDestRemotePath)
#         print('上传附件到ftp结束')
#         ftp.close()

#         # 删除文件夹
#         print('清空本地数据 path=' + ftpLocalDir + '\t开始')
#         xfer.del_file(ftpLocalDir)
#         print('清空本地数据 path=' + ftpLocalDir + '\t结束')

#         xfer.disconnect()
#         ita.disconnect()
#         print('本次获取估值数据结束')
#     except Exception as e:
#         print("异常退出:" + str(e))
#         xfer.disconnect()
#         ita.disconnect()
#         sys.exit(-2)

def daily_action(argv, dest_date,rootpath):
    #product_file_sync.py文件read_tblobstorage_table_attachment函数中每一条sql语句，最多可以获得的文件id个数
    pagecount = 20
    # 文件服务器配置信息
    fileSrcHost = "192.168.10.96"
    fileSrcPort = 22
    fileSrcUsername = "hundsun"
    fileSrcPassword = "hundsun"
    fileSrcRemotepath = ""

    fileLocalPath = "C:\\temp"

    fileDestHost = "192.168.19.110"
    fileDestPort = 21
    fileDestUsername = "admin"
    fileDestPassword = "bjkf@2017"
    
    # 产品数据库配置信息
    dbip = '192.168.10.228'
    dbport = 1521
    dbSID = 'kfzgdb'
    dbusername = 'interins'
    dbpassword = 'hundsun'

    # 开始日期
    startDate = datetime.now().strftime('%Y%m%d')
    # 结束日期
    endDate = startDate
    ftpLocalDir = fileLocalPath + os.path.sep + endDate
    fileDestRemotePath = rootpath + "/gzfile/" + endDate + "/infoannex/"

    savelog("daily_action starts for " + str(dest_date) + ",remote path:" + fileDestRemotePath)

    xfer = None
    try:
        xfer = SSHSession(fileSrcHost, fileSrcPort, fileSrcUsername, fileSrcPassword, dbip, dbport, dbSID, dbusername,dbpassword)
        # 先清空目录
        if xfer is None:
            print("xfer is none!")
        else:
            xfer.del_file(ftpLocalDir)
            attachments = xfer.read_tblobstorage_table_attachment(fileSrcRemotepath,fileLocalPath,endDate,dest_date,pagecount)
            if len(attachments) == 0:
                count = xfer.read_tblobstorage_debug()
                print("read_tblobstorage_debug return:"+str(count))
                savelog("没有附件!")
            else:
                ftp_fundcode = FTPSync(fileDestHost, fileDestPort)
                if ftp_fundcode is not None:
                    ftp_fundcode.login(fileDestUsername, fileDestPassword)
                    savelog('上传附件到ftp开始')
                    for it in iter(attachments):
                        item = str(it)
                        arr = item.split(",")
                        dirpath = str(arr[0])
                        product_code = arr[1]
                        destpath = fileDestRemotePath + product_code
                        ftp_fundcode.upload_dir(dirpath,destpath)

                    savelog('上传附件到ftp结束')
                else:
                    savelog("FTPSync return none!")        

    except Exception as e:
        savelog("异常退出:" + str(e))
    finally:
        if xfer is not None:
            xfer.disconnect()
            try:
                xfer.del_file(ftpLocalDir)
            except Exception as e:
                pass

        savelog("daily_action end!")


## T+1日凌晨将T日新增的信息披露状态为“已发布”、产品种类为“债权投资计划”或“资产支持计划”、披露类型为“临时披露”的所有信息披露附件文件提取，
## 上传至ftp服务器gzfile/yyyymmdd/infoannex/产品代码目录下，一只产品对应一个文件夹。

if __name__ == '__main__':
    dest_date = 0
    rootpath = ""
    if len(sys.argv) == 1:
        dest_date = (date.today()).strftime('%Y%m%d')
        savelog("date is " + str(dest_date))
    elif len(sys.argv) == 2:
        dest_date = sys.argv[1]
        savelog("date is from parameter " + str(dest_date))
    else:
        dest_date = sys.argv[1]
        rootpath = sys.argv[2]
        savelog("date is " + str(dest_date) + " rootpath:" + rootpath)

    daily_action(sys.argv, str(dest_date),rootpath)
