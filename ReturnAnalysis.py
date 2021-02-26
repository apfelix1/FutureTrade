from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime

def get_data(future):
    return

def get_simulated_return(future):
    monthlist = range(2001,2013)
    startquant  = 0
    endquant = 0
    tdPeriodList = TradingDays('20200101', '20201231')
    num_trades = 0
    holding_bool = 0
    holdday = 0
    for date in tdPeriodList:
        date = date.replace('-', '')
        for month in monthlist:
            name = future + str(month)
            tradelog = pd.read_csv('./result/'+future+'/' + name + '.csv')
            tradelog1 = tradelog[tradelog['startDate'].astype(str) == date]
            tradelog2 = tradelog[tradelog['endDate'].astype(str) == date]
            if len(tradelog1.index) != 0:
                reqquant = tradelog1['buyETF'].iloc[0]
                if reqquant > endquant:
                    startquant += reqquant - endquant

                if reqquant <= endquant:
                    endquant -= reqquant
                holding_bool += 1


            if len(tradelog2.index) != 0:
                future_delta = tradelog2['sellFuture'].iloc[0]-tradelog2['buyFuture'].iloc[0]
                etf_delta = tradelog2['sellETF'].iloc[0]
                endquant += future_delta + etf_delta
                num_trades += 1
                holding_bool -=1
        if holding_bool > 0:
            holdday += 1



    print('input quant is'+ str(startquant))
    print('out quant is ' + str(endquant))
    print('absolute earning is ' + str(endquant-startquant))
    print('number of trades is' + str(num_trades))
    print('number of days holding future is '+str(holdday))
    returnlog = (endquant-startquant)/startquant

    return returnlog

def get_yearly_return(future):
    return

IHreturn = get_simulated_return('IH')
print(IHreturn)

