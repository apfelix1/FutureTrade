from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime

def get_short_future_return(future):
    monthlist = range(2001, 2013)
    startquant = 0
    endquant = 0
    tdPeriodList = TradingDays('20200101', '20201231')
    num_trades = 0
    holding_bool = 0
    holdday = 0
    for date in tdPeriodList:
        date = date.replace('-', '')
        if holding_bool > 0:
            holdday += 1
            print(date)
            print(holding_bool)
        for month in monthlist:
            name = future + str(month)
            tradelog = pd.read_csv('./result/' + future + '/shortFuture/' + name + '.csv')
            tradelog1 = tradelog[tradelog['startDate'].astype(str) == date]
            tradelog2 = tradelog[tradelog['endDate'].astype(str) == date]


            if len(tradelog2.index) != 0:
                if holding_bool > 0:
                    # get the return earned from future or etf
                    future_delta = tradelog2['buyFuture'].iloc[0] - tradelog2['sellFuture'].iloc[0]
                    etf_delta = tradelog2['sellETF'].iloc[0]
                    endquant += (future_delta + etf_delta)

                    # counts the days that have position on etf and future
                    num_trades += 1
                    holding_bool -= 1
                    # get the tax cost of trades
                    etftax = (tradelog2['sellETF'].iloc[0] + tradelog2['buyETF'].iloc[0]) * 0.00015
                    futuretax = (tradelog2['sellFuture'].iloc[0] + tradelog2['buyFuture'].iloc[0]) * 0.000023
                    endquant -= (etftax + futuretax)

            # calculate the amount of money needed of a new trade
            if len(tradelog1.index) != 0:
                reqquant = tradelog1['buyETF'].iloc[0]
                if reqquant > endquant:
                    startquant += reqquant - endquant
                    endquant = 0

                if reqquant <= endquant:
                    endquant -= reqquant
                holding_bool += 1
                if holding_bool == 1:
                    holdday += 1

    print('input quant is' + str(startquant))
    print('out quant is ' + str(endquant))
    print('absolute earning is ' + str(endquant - startquant))
    print('number of trades is ' + str(num_trades))
    print('number of days holding future is ' + str(holdday))
    returnlog = (endquant - startquant) / startquant

    return returnlog

def get_long_future_return(future):
    monthlist = range(2001, 2013)
    startquant = 0
    endquant = 0
    tdPeriodList = TradingDays('20200101', '20201231')
    num_trades = 0
    holding_bool = 0
    holdday = 0
    for date in tdPeriodList:
        date = date.replace('-', '')
        if holding_bool > 0:
            holdday += 1
            print(date)
            print(holding_bool)
        for month in monthlist:
            name = future + str(month)
            tradelog = pd.read_csv('./result/' + future + '/' + name + '.csv')
            tradelog1 = tradelog[tradelog['startDate'].astype(str) == date]
            tradelog2 = tradelog[tradelog['endDate'].astype(str) == date]

            if len(tradelog2.index) != 0:
                if holding_bool > 0:
                    # get the return earned from future or etf
                    future_delta = tradelog2['buyFuture'].iloc[0] - tradelog2['sellFuture'].iloc[0]
                    etf_delta = tradelog2['sellETF'].iloc[0]
                    endquant += (future_delta + etf_delta)

                    # counts the days that have position on etf and future
                    num_trades += 1
                    holding_bool -= 1
                    # get the tax cost of trades
                    etftax = (tradelog2['sellETF'].iloc[0] + tradelog2['buyETF'].iloc[0]) * 0.00015
                    futuretax = (tradelog2['sellFuture'].iloc[0] + tradelog2['buyFuture'].iloc[0]) * 0.000023
                    endquant -= (etftax + futuretax)

            # calculate the amount of money needed of a new trade
            if len(tradelog1.index) != 0:
                reqquant = tradelog1['buyETF'].iloc[0]
                if reqquant > endquant:
                    startquant += reqquant - endquant
                    endquant = 0

                if reqquant <= endquant:
                    endquant -= reqquant
                holding_bool += 1
                if holding_bool == 1:
                    holdday += 1

    print('input quant is' + str(startquant))
    print('out quant is ' + str(endquant))
    print('absolute earning is ' + str(endquant - startquant))
    print('number of trades is ' + str(num_trades))
    print('number of days holding future is ' + str(holdday))
    returnlog = (endquant - startquant) / startquant

    return returnlog

def get_quant_simulation(future, quant):
    monthlist = range(2001, 2013)
    startquant = quant
    currquant = quant
    tdPeriodList = TradingDays('20200101', '20201231')
    num_trades = 0
    holding_bool = 0
    holdday = 0
    for date in tdPeriodList:
        date = date.replace('-', '')
        for month in monthlist:
            name = future + str(month)
            tradelog = pd.read_csv('./result/' + future + '/' + name + '.csv')
            tradelog1 = tradelog[tradelog['startDate'].astype(str) == date]
            tradelog2 = tradelog[tradelog['endDate'].astype(str) == date]

            # calculate the amount of money needed of a new trade
            if len(tradelog1.index) != 0:
                reqquant = tradelog1['buyETF'].iloc[0]
                if reqquant <= currquant:
                    currquant -= reqquant
                holding_bool += 1

            if len(tradelog2.index) != 0:
                # get the return earned from future or etf
                future_delta = tradelog2['buyFuture'].iloc[0] - tradelog2['sellFuture'].iloc[0]
                etf_delta = tradelog2['sellETF'].iloc[0]
                currquant += (future_delta + etf_delta)

                # counts the days that have position on etf and future
                num_trades += 1
                holding_bool -= 1
                # get the tax cost of trades
                etftax = (tradelog2['sellETF'].iloc[0] + tradelog2['buyETF'].iloc[0]) * 0.00015
                futuretax = (tradelog2['sellFuture'].iloc[0] + tradelog2['buyFuture'].iloc[0]) * 0.000023
                currquant -= (etftax + futuretax)

        if holding_bool > 0:
            holdday += 1

    endquant = currquant
    print('input quant is' + str(startquant))
    print('output quant is ' + str(endquant))
    print('absolute earning is ' + str(endquant - startquant))
    print('number of trades is ' + str(num_trades))
    print('number of days holding future is ' + str(holdday))
    returnlog = (endquant - startquant) / startquant

    return returnlog

IHSreturn = get_short_future_return('IF')
# IHLreturn = get_long_future_return('IH')
print(IHSreturn)
# print(IHLreturn)

