from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
secUtils = CSecurityMarketDataUtils('Z:/StockData')

def get_sim_log(startDate, endDate, initamt, tradelmt = True):
    tdperiod = TradingDays(startDate=startDate, endDate=endDate)
    for date in tdperiod:
        flist = get_future_list()
    return

def get_future_list(date):
    flist = fUtils.FuturesDailySummaryFrame('IF', date)['InstrumentId'].to_list() + \
            fUtils.FuturesDailySummaryFrame('IH', date)['InstrumentId'].to_list()

    return flist

def get_daily_trades(flist):
    for future in flist:

        pass
    return


get_sim_log('20200423','20200424',10000000)
