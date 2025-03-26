import os
from datetime import datetime, date, timedelta
import sys
#from FTPSync import FTPSync
from SFTPSync import SFTPSync
from product_file_sync import SSHSession
from func import savelog, deletefiles, \
    fileSrcHost, fileSrcPort, fileSrcUsername, fileSrcPassword,\
    fileDestHost, fileDestPort, fileDestUsername, fileDestPassword,\
    dbip, dbport, dbSID, dbusername, dbpassword, \
    fileLocalPath, pagecount, remote_path, filename_suffix

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

def assert_action(argv, start_date,end_date,rootpath):
    fileDestRemotePath = rootpath + remote_path + str((date.today()).strftime('%Y%m%d')) + "/"
    filename1 = str(start_date) + "-" + str(end_date) + filename_suffix
    localfilename1 = fileLocalPath + "\\" + filename1
    remotefilename1 = fileDestRemotePath + filename1

    savelog("assert_action start date from " + str(start_date) + " to " + str(end_date) + ",remote path:" + fileDestRemotePath)

    xfer = None
    filelist = []
    try:
        xfer = SSHSession(fileSrcHost, fileSrcPort, fileSrcUsername, fileSrcPassword, dbip, dbport, dbSID, dbusername,dbpassword)
        # 先清空目录
        if xfer is None:
            print("xfer is none!")
        else:
            xfer.read_table1_information(localfilename1,filename1,start_date,end_date,pagecount)
            sftp_fundcode = SFTPSync(fileDestHost, fileDestPort)
            if sftp_fundcode is not None:
                sftp_fundcode.login(fileDestUsername,fileDestPassword)
                savelog('上传附件到sftp开始')
                filelist = [localfilename1 + "," + remotefilename1]
                sftp_fundcode.upload_files(filelist,fileDestRemotePath)
                local_path = 'E:\\code\\python\\定时脚本'
                ftp_path = "/home/fileserver/fundcrm/accessory/Tblobstorage"
                sftp_fundcode.put_dir(local_path,ftp_path)
                savelog('上传附件到sftp结束')
                sftp_fundcode.close_conn()

            # ftp_fundcode = FTPSync(fileDestHost, fileDestPort)
            # if ftp_fundcode is not None:
            #     ftp_fundcode.login(fileDestUsername, fileDestPassword)
            #     savelog('上传附件到ftp开始')
            #     filelist = [localfilename1 + "," + remotefilename1]
            #     ftp_fundcode.upload_files(filelist,fileDestRemotePath)
            #     savelog('上传附件到ftp结束')
            #     ftp_fundcode.close()

    except Exception as e:
        savelog("异常退出:" + str(e))
    finally:
        if xfer is not None:
            xfer.disconnect()

        #deletefiles(filelist)
        savelog("assert_action end!")

# 1.申请按照附件《资产支持计划周报表格取数逻辑》于每周四提取一周资产支持计划相关数据； 
# 需求实现方式如下：
# 需求1：业务数据提取专用ftp增加djjs用户，下设目录/djjs/Abs/yyyymmdd，每周四系统自动生成abs产品的周报报表一、报表二相关数据，表一和表二模板及要素取数规则见附件；
if __name__ == '__main__':
    datestart = 0
    dateend = 0
    rootpath = ""
    daysweek = -6
    if len(sys.argv) == 1:
        #直接运行，命令例如 python main.py
        datestart = (date.today() + timedelta(days=daysweek)).strftime('%Y%m%d')
        dateend = (date.today()).strftime('%Y%m%d')
    elif len(sys.argv) == 2:
        #命令例如 python main.py /tmp
        #rootpath sys.argv[1] 可以指定ftp服务器的某一个目录，程序会在该目录下创建/djjs/Abs/yyyymmdd目录
        datestart = (date.today() + timedelta(days=daysweek)).strftime('%Y%m%d')
        dateend = (date.today()).strftime('%Y%m%d')
        rootpath = sys.argv[1]
    elif len(sys.argv) == 3:
        #主要用于调试，命令例如 python main.py 20220712 20240719
        #sys.argv[1]为开始日期
        #sys.argv[2]为结束日期
        datestart = sys.argv[1]
        dateend = sys.argv[2]
    elif len(sys.argv) == 4:
        #主要用于调试，命令例如 python main.py 20220712 20240719 /tmp
        #sys.argv[1]为开始日期
        #sys.argv[2]为结束日期
        #rootpath sys.argv[3] 可以指定ftp服务器的某一个目录，程序会在该目录下创建/djjs/Abs/yyyymmdd目录
        datestart = sys.argv[1]
        dateend = sys.argv[2]
        rootpath = sys.argv[3]
    else:
        savelog("参数错误!")
        sys.exit(1)

    assert_action(sys.argv, str(datestart), str(dateend),rootpath)
