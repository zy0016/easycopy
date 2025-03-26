import os
from datetime import datetime
import sys

from abs_product.FTPSync import FTPSync
from abs_product.SFTPSync import SFTPSync
from abs_product.abs_product_file_sync import SSHSession

if __name__ == '__main__':

    # 文件服务器配置信息
    fileSrcHost = "172.16.117.26"
    fileSrcPort = 22
    fileSrcUsername = "ita"
    fileSrcPassword = "zgita@2016"
    fileSrcRemotepath = "/home/fileserver/fundcrm/accessory/Tblobstorage"

    fileLocalPath = "C:/absfile_zhtjbb/absfile"
    fileLocalTemplateFile = "D:/tools/fundfile/template/combreport_temp.docx"
    #组合类事前登记上线时间
    startDateComb = '20200801'

    fileDestHost = "172.16.117.38"
    fileDestPort = 21
    fileDestUsername = "zczx"
    fileDestPassword = "j4Zf864q"
    fileDestRemotePath = "./"

    # 产品数据库配置信息
    dbip = '172.16.117.25'
    dbport = 1521
    dbSID = 'ZGDBRAC'
    dbusername = 'fundcrm'
    dbpassword = 'bjsZBD_2018'

    downLoadFile = True
    startDate = datetime.now().strftime('%Y%m%d')
    endDate = datetime.now().strftime('%Y%m%d')


    # ['8', '6']
    templetids = ['8']

    if len(sys.argv) > 2:
        fileSrcRemotepath = sys.argv[1]  # 生产文件路径
        fileLocalPath = sys.argv[2]      # 本地文件路径
        if len(sys.argv) > 3:
            if str(sys.argv[3]).lower() == 'true':
                downLoadFile = True
            else:
                downLoadFile = False
    if len(sys.argv) > 3:
        startDateComb=sys.argv[4]
    ftpLocalDir = fileLocalPath + os.path.sep + endDate
    fileLocalTemplateFile=fileLocalPath+ os.path.sep +'template/combreport_temp.docx'
    try:
        xfer = SSHSession(fileSrcHost, fileSrcPort, fileSrcUsername, fileSrcPassword, dbip, dbport, dbSID, dbusername,dbpassword)
        # 先清空目录
        #xfer.del_file(ftpLocalDir)
        xfer.mkdir_ifnotexists(ftpLocalDir)
        for templetid in templetids:
            fundcodes = xfer.getFundcodes(templetid, startDate, endDate, fileLocalPath)
            if downLoadFile:
                for fundinfo in fundcodes:
                    fundcode = fundinfo.split(',')
                    xfer.read_tblobstorage_table(fileSrcRemotepath, fileLocalPath, fundcode[0], endDate, fundcode[1])
            fundtypeName = xfer.getTempleName(templetid)
            print('【共处理' +fundtypeName+ str(len(fundcodes)) + '个产品】')

        xfer.getCombProductReport(startDateComb, endDate, fileLocalTemplateFile,fileLocalPath)
        # 上传到目的FTP
        # print('上传附件到ftp开始')
        # ftp = FTPSync(fileDestHost, fileDestPort)
        # ftp.login(fileDestUsername, fileDestPassword)

        # ftp.put_dir(ftpLocalDir, fileDestRemotePath)
        # ftp.put_dir(ftpLocalDir, fileDestRemotePath)
        # print('上传附件到ftp结束')
        # ftp.close()

        # 上传到目的SFTP
        print('上传附件到sftp开始')
        sftp = SFTPSync(fileDestHost, fileDestPort)
        sftp.login(fileDestUsername, fileDestPassword)

        sftp.put_dir(ftpLocalDir, fileDestRemotePath)
        print('上传附件到sftp结束')
        sftp.close()

        # 删除文件夹
        #print('清空本地数据 path=' + ftpLocalDir + '\t开始')
        #xfer.del_file(ftpLocalDir)
        #print('清空本地数据 path=' + ftpLocalDir + '\t结束')

        xfer.disconnect()
        print('本次资产支持计划附件结束')
    except Exception as e:
        print("异常退出:" + str(e))
        xfer.disconnect()

        sys.exit(-2)