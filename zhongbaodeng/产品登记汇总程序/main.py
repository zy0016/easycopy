import os
from datetime import datetime, date
import sys
from FTPSync import FTPSync
from product_file_sync import SSHSession
from func import savelog, get_quarter_date_from_month,get_month_date_from_month,get_month_date_from_quarter,valid_month_quarter,\
                get_pre_month_date_from_quarter,get_pre_quarter_date_from_month,get_pre_month_date_from_month

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
                # count = xfer.read_tblobstorage_debug()
                # print("read_tblobstorage_debug return:"+str(count))
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

if __name__ == '__main__':
    year_date_start = 0
    year_date_end = 0

    quarter_date_start = 0
    quarter_date_end = 0

    month_date_start = 0
    month_date_end = 0
    
    pre_year_date_start = 0
    pre_year_date_end = 0

    pre_quarter_date_start = 0
    pre_quarter_date_end = 0

    pre_month_date_start = 0
    pre_month_date_end = 0

    dest_year = 0
    dest_quarter = 0
    dest_month = 0
    
    if len(sys.argv) == 1:
        # 没有提供月份参数，则默认为当前月份
        dest_year = (date.today()).strftime('%Y')
        dest_month = (date.today()).strftime('%m')
    else:
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == "-m":
                dest_month = sys.argv[i + 1]
            elif sys.argv[i] == "-q":
                dest_quarter = sys.argv[i + 1]
            elif sys.argv[i] == "-y":
                dest_year = sys.argv[i + 1]

        if dest_year == 0:
            dest_year = (date.today()).strftime('%Y')
        
        if dest_month == 0 and dest_quarter == 0:
            dest_month = (date.today()).strftime('%m')
        
        if dest_quarter != 0 and dest_month != 0 and valid_month_quarter(dest_quarter,dest_month) == False:
            savelog("quarter and month are not valid!")
            sys.exit(1)

    year_date_start = str(dest_year) + "0101"
    year_date_end = str(dest_year) + "1231"
    
    pre_year_date_start = str(int(dest_year) - 1) + "0101"
    pre_year_date_end = str(int(dest_year) - 1) + "1231"

    if int(dest_month) > 12:
        savelog("month is not valid!")
        sys.exit(1)

    if int(dest_quarter) > 4:
        savelog("quarter is not valid!")
        sys.exit(1)

    if dest_month != 0:
        ql = get_quarter_date_from_month(dest_year,dest_month)
        quarter_date_start = ql[0]
        quarter_date_end = ql[1]

        ml = get_month_date_from_month(dest_year,dest_month)
        month_date_start = ml[0]
        month_date_end = ml[1]
        #############################################################
        qp = get_pre_quarter_date_from_month(dest_year,dest_month)
        pre_quarter_date_start = qp[0]
        pre_quarter_date_end = qp[1]

        mp = get_pre_month_date_from_month(dest_year,dest_month)
        pre_month_date_start = mp[0]
        pre_month_date_end = mp[1]

    if dest_quarter != 0:
        ql = get_month_date_from_quarter(dest_year,dest_quarter)
        quarter_date_start = ql[0]
        quarter_date_end = ql[1]
        ###########################################################
        qp = get_pre_month_date_from_quarter(dest_year,dest_quarter)
        pre_quarter_date_start = qp[0]
        pre_quarter_date_end = qp[1]

    print("year range is " + str(year_date_start) + " " + str(year_date_end))
    print("quarter range is " + str(quarter_date_start) + " " + str(quarter_date_end))
    print("month range is " + str(month_date_start) + " " + str(month_date_end))
    print("\n\n")
    print("pre year range is " + str(pre_year_date_start) + " " + str(pre_year_date_end))
    print("pre quarter range is " + str(pre_quarter_date_start) + " " + str(pre_quarter_date_end))
    print("pre month range is " + str(pre_month_date_start) + " " + str(pre_month_date_end))
