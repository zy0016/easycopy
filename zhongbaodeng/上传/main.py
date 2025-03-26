import os
from datetime import datetime
import sys

from FTPSync import FTPSync
from product_file_sync import SSHSession

if __name__ == '__main__':

    # 文件服务器配置信息
    fileSrcHost = "172.16.117.26"
    fileSrcPort = 22
    fileSrcUsername = "ita"
    fileSrcPassword = "zgita@2016"
    fileSrcRemotepath = "/home/fileserver/fundcrm/accessory/Tblobstorage"

    fileLocalPath = "C:/estimate/fundcrmfile"

    fileDestHost = "172.16.117.38"
    fileDestPort = 21
    fileDestUsername = "zggz"
    fileDestPassword = "0V84zH1d"
    fileDestRemotePath = "./"

    # 产品数据库配置信息
    dbip = '172.16.117.25'
    dbport = 1521
    dbSID = 'ZGDBRAC'
    dbusername = 'fundcrm'
    dbpassword = 'bjsZBD_2018'

    # ta数据库配置信息
    tadbip = '172.16.117.25'
    tadbport = 1521
    tadbSID = 'ZGDBRAC'
    tadbusername = 'ta4'
    tadbpassword = 'bjsZBD_2018'

    # 是否下载附件
    downLoadFile = True
    # 开始日期
    startDate = datetime.now().strftime('%Y%m%d')
    # 结束日期
    endDate = startDate
    templetids = ['8', '6']

    if len(sys.argv) > 2:
        startDate = sys.argv[1]
        endDate = sys.argv[2]
        if len(sys.argv) > 3:
            if str(sys.argv[3]).lower() == 'true':
                downLoadFile = True
            else:
                downLoadFile = False

    ftpLocalDir = fileLocalPath + os.path.sep + endDate

    try:
        xfer = SSHSession(fileSrcHost, fileSrcPort, fileSrcUsername, fileSrcPassword, dbip, dbport, dbSID, dbusername,dbpassword)
        # 先清空目录
        xfer.del_file(ftpLocalDir)

        for templetid in templetids:
            fundcodes = xfer.getFundcodes(templetid, startDate, endDate, fileLocalPath)
            if downLoadFile:
                for fundinfo in fundcodes:
                    fundcode = fundinfo.split(',')
                    xfer.read_tblobstorage_table(fileSrcRemotepath, fileLocalPath, fundcode[0], endDate, fundcode[1])
            fundtypeName = xfer.getTempleName(templetid)
            print('【共处理' +fundtypeName+ str(len(fundcodes)) + '个产品】')

        for templetid in templetids:
            fundcodes = xfer.getDurationFundinfo_Cash(templetid, startDate, endDate, fileLocalPath)
            if downLoadFile:
                for fundinfo in fundcodes:
                    fundcode = fundinfo.split(',')
                    xfer.read_tblobstorage_table_Cash(fileSrcRemotepath, fileLocalPath, fundcode[0], endDate, fundcode[1])
            fundtypeName = xfer.getTempleName(templetid)
            print('【共处理兑付' + fundtypeName + str(len(fundcodes)) + '个产品】')

        # 获取存续期产品信息
        xfer.getDurationFundinfo(startDate, endDate, fileLocalPath)
        # 链接TA
        ita = SSHSession(fileSrcHost, fileSrcPort, fileSrcUsername, fileSrcPassword, tadbip, tadbport, tadbSID,tadbusername, tadbpassword)
        ita.getFundInfoByTA(fileLocalPath, startDate, endDate)

        # 上传到目的FTP
        print('上传附件到ftp开始')
        ftp = FTPSync(fileDestHost, fileDestPort)
        ftp.login(fileDestUsername, fileDestPassword)

        ftp.put_dir(ftpLocalDir, fileDestRemotePath)
        print('上传附件到ftp结束')
        ftp.close()

        # 删除文件夹
        print('清空本地数据 path=' + ftpLocalDir + '\t开始')
        xfer.del_file(ftpLocalDir)
        print('清空本地数据 path=' + ftpLocalDir + '\t结束')

        xfer.disconnect()
        ita.disconnect()
        print('本次获取估值数据结束')
    except Exception as e:
        print("异常退出:" + str(e))
        xfer.disconnect()
        ita.disconnect()
        sys.exit(-2)