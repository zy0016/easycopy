from datetime import datetime, date, timedelta
import time;
import calendar

def savelog(strsen):
    print(strsen)
    try:
        resultfile = open("c:\\temp\\debug.log",'a+')
        resultfile.write("[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "]" + strsen + "\n")
        resultfile.close()
    except Exception as e:
        pass

def valid_month_quarter(quarter,month):
    #判断月份和季度是否匹配
    if (int(month) >= 1 and int(month) <= 3 and int(quarter) == 1) or \
        (int(month) >= 4 and int(month) <= 6 and int(quarter) == 2) or \
        (int(month) >= 7 and int(month) <= 9 and int(quarter) == 3) or \
        (int(month) >= 10 and int(month) <= 12 and int(quarter) == 4):
        return True
    else:
        return False

def get_month_date_from_quarter(year,quarter):
    #根据季度获得当前开始结束日期
    start = ""
    end = ""
    if int(quarter) == 1:
        start = "0101"
        end = "0331"
    elif int(quarter) == 2:
        start = "0401"
        end = "0630"
    elif int(quarter) == 3:
        start = "0701"
        end = "0930"
    else:
        start = "1001"
        end = "1231"
    
    return [str(year) + start,str(year) + end]

def get_pre_month_date_from_quarter(year,quarter):
    #根据当前季度获得前一季度的开始结束日期
    if int(quarter) == 1:
        return get_month_date_from_quarter(int(year) - 1,4)
    else:
        return get_month_date_from_quarter(year,int(quarter) - 1)

def get_quarter_date_from_month(year,month):
    #根据月份获得当前季度的开始结束日期
    start = ""
    end = ""
    if int(month) >= 1 and int(month) <= 3:
        start = "0101"
        end = "0331"
    elif int(month) >= 4 and int(month) <= 6:
        start = "0401"
        end = "0630"
    elif int(month) >= 7 and int(month) <= 9:
        start = "0701"
        end = "0930"
    else:
        start = "1001"
        end = "1231"
    
    return [str(year) + start,str(year) + end]

def get_pre_quarter_date_from_month(year,month):
    #根据当前月份获得前一个季度的开始结束日期
    if int(month) <= 3:
        #当前是月份小于等于3，属于第一季度，返回上一年10月份所在季度(第四季度)的开始结束日期
        return get_quarter_date_from_month(int(year) - 1,10)
    elif int(month) <= 6:
        #当前是月份大于3小于等于6，属于第二季度，返回当年1月份所在季度(第一季度)的开始结束日期
        return get_quarter_date_from_month(year,1)
    elif int(month) <= 9:
        #当前是月份大于6小于等于9，属于第三季度，返回当年4月份所在季度(第二季度)的开始结束日期
        return get_quarter_date_from_month(year,4)
    else:
        #当前是月份大于9小于等于12，属于第四季度，返回当年7月份所在季度(第三季度)的开始结束日期
        return get_quarter_date_from_month(year,7)
    
def get_month_date_from_month(year,month):
    #根据月份获得当前月份的开始结束日期
    date_start = str(year) + str(month) + "01"
    date_end = ""
    if int(month) == 1 or int(month) == 3 or int(month) == 5 or int(month) == 7 or int(month) == 8 or int(month) == 10 or int(month) == 12:
        date_end = str(year) + str(month) + "31"
    elif int(month) == 4 or int(month) == 6 or int(month) == 9 or int(month) == 11:
        date_end = str(year) + str(month) + "30"
    else:
        if calendar.isleap(int(year)) == True:
            date_end = str(year) + str(month) + "29"
        else:
            date_end = str(year) + str(month) + "28"

    return [date_start,date_end]

def get_pre_month_date_from_month(year,month):
    #根据当前月份获得前一个月的开始结束日期
    if int(month) == 1:
        return get_month_date_from_month(int(year) - 1,12)
    else:
        return get_month_date_from_month(year,int(month) - 1)