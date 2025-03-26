from datetime import datetime, date, timedelta
import time;

def savelog(strsen):
    print(strsen)
    try:
        resultfile = open("c:\\temp\\debug.log",'a+')
        resultfile.write("[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "]" + strsen + "\n")
        resultfile.close()
    except Exception as e:
        pass