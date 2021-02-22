from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
from datetime import datetime

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
secUtils = CSecurityMarketDataUtils('Z:/StockData')

def get_df(future, date):
    rtarr = pd.read_csv('./result/'+future[:,2]+'/'+future+date+'.csv', header=None)
    return rtarr

def get_trade_log(future, date):
    return

def get_trade_date(name):
    year = name[2:4]
    month = name[4:]

    # get the month and year of start date
    if int(month) == 3 or int(month) == 6 or int(month) == 9 or int(month) == 12:
        startmonth = int(month) - 7
        if startmonth > 0:
            startmonth = str(startmonth)
            startyear = year
        else:
            startmonth = str(12 + startmonth)
            startyear = str(int(year) - 1)
    else:
        startmonth = int(month) - 2
        if startmonth > 0:
            startmonth = str(startmonth)
            startyear = year
        else:
            startmonth = str(12 + startmonth)
            startyear = str(int(year) - 1)

    # get the start date
    for i in range(0, 7):
        startday = str(15 + i)
        if datetime.datetime.strptime('20' + startyear + startmonth + startday, '%Y%m%d').weekday() == 4:
            startday = str(int(startday))
            startdate = (datetime.datetime.strptime('20' + startyear + startmonth + startday,
                                                    '%Y%m%d') + datetime.timedelta(days=3)).date()
            break

    # get the end date
    for i in range(0, 7):
        endday = str(15 + i)
        if datetime.datetime.strptime('20' + year + month + endday, '%Y%m%d').weekday() == 4:
            enddate = (datetime.datetime.strptime('20' + year + month + endday, '%Y%m%d').date())
            break

    startdate = str(startdate).replace('-', '')
    enddate = str(enddate).replace('-', '')

    tdPeriodList = TradingDays(startdate, enddate)

    return tdPeriodList