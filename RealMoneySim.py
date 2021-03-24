from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
secUtils = CSecurityMarketDataUtils('Z:/StockData')
pd.set_option("display.max_columns", None)


def get_sim_log(startDate, endDate, initamt):
    balance = pd.DataFrame(columns = ['date', 'timetick', 'tradeMove', 'BalanceChange', 'currentBalance'])
    curamt = initamt
    tdlog = get_strategy()
    tdlog = tdlog[tdlog['startDate'].astype(str)>startDate]
    tdlog = tdlog[tdlog['endDate'].astype(str)<endDate]
    tdperiod = TradingDays(startDate=startDate, endDate=endDate)
    tdperiod = [date.replace('-','') for date in tdperiod]

    for date in tdperiod:
        daylog = tdlog[(tdlog.startDate.astype(str) == date) | (tdlog.endDate.astype(str) == date)]
        if len(daylog.index) == 0:
            continue
        print(date)
        buylog = daylog[daylog['startDate'].astype(str)==date]
        buylog = buylog.sort_values('startTick')
        buylog.reset_index(drop = True, inplace= True)

        selllog = daylog[daylog['endDate'].astype(str) == date]
        selllog = selllog.sort_values('endTick')
        selllog.reset_index(drop = True, inplace = True)

        i1 = i2 = 0
        while i1 + i2 < len(buylog.index) + len(selllog.index):
            while i1 < len(buylog.index) and i2 < len(selllog.index):
                if buylog['startTick'].iloc[i1] < selllog['endTick'].iloc[i2]:

                    if buylog['TradeMethod'].iloc[i1] == 'Long':
                        if curamt < buylog['buyFuture'].iloc[i1]:
                            tdlog = tdlog.drop(tdlog[(tdlog['startDate'] == buylog['startDate'].iloc[i1]) &
                                                     (tdlog['startTick'] == buylog['startTick'].iloc[i1]) &
                                                     (tdlog['FutureName'] == buylog['FutureName'].iloc[i1])].index,
                                               axis=0)
                            i1 += 1
                            continue
                        amtchange = -buylog['buyFuture'].iloc[i1]
                        curamt += amtchange
                    else:
                        if curamt < buylog['buyETF'].iloc[i1]:
                            tdlog = tdlog.drop(tdlog[(tdlog['startDate'] == buylog['startDate'].iloc[i1]) &
                                                     (tdlog['startTick'] == buylog['startTick'].iloc[i1]) &
                                                     (tdlog['FutureName'] == buylog['FutureName'].iloc[i1])].index,
                                               axis=0)
                            i1 += 1
                            continue
                        amtchange = -buylog['buyETF'].iloc[i1]
                        curamt += amtchange

                    balance = balance.append({'date': date, 'timetick': buylog['startTick'].iloc[i1],
                                              'tradeMove': 'Buy '+buylog['FutureName'].iloc[i1], 'BalanceChange':
                                                  amtchange, 'currentBalance': curamt}, ignore_index=True)
                    i1 += 1
                elif buylog['startTick'].iloc[i1] > selllog['endTick'].iloc[i2]:
                    if selllog['TradeMethod'].iloc[i2] == 'Long':
                        amtchange = (selllog['buyETF'].iloc[i2] - selllog['sellETF'].iloc[i2] +
                                     selllog['sellFuture'].iloc[i2])
                        curamt += amtchange
                        balance = balance.append({'date': date, 'timetick': selllog['endTick'].iloc[i2],
                                                  'tradeMove': 'Sell '+ selllog['FutureName'].iloc[i2], 'BalanceChange'
                                                  : amtchange, 'currentBalance': curamt}, ignore_index=True)
                    else:
                        amtchange = (selllog['buyFuture'].iloc[i2] - selllog['sellFuture'].iloc[i2] +
                                     selllog['sellETF'].iloc[i2])
                        curamt += amtchange
                        balance = balance.append({'date': date, 'timetick': selllog['endTick'].iloc[i2],
                                                  'tradeMove': 'Sell ' + selllog['FutureName'].iloc[i2], 'BalanceChange'
                                                  : amtchange, 'currentBalance': curamt}, ignore_index=True)
                    i2 += 1
                else:
                    if selllog['TradeMethod'].iloc[i2] == 'Long':
                        amtchange = (selllog['buyETF'].iloc[i2] - selllog['sellETF'].iloc[i2] +
                                     selllog['sellFuture'].iloc[i2])
                        curamt += amtchange
                        balance = balance.append({'date': date, 'timetick': selllog['endTick'].iloc[i2],
                                                  'tradeMove': 'Sell ' + selllog['FutureName'].iloc[i2], 'BalanceChange'
                                                  : amtchange, 'currentBalance': curamt}, ignore_index=True)

                    else:
                        amtchange = (selllog['buyFuture'].iloc[i2] - selllog['sellFuture'].iloc[i2] +
                                     selllog['sellETF'].iloc[i2])
                        curamt += amtchange
                        balance = balance.append({'date': date, 'timetick': selllog['endTick'].iloc[i2],
                                                  'tradeMove': 'Sell ' + selllog['FutureName'].iloc[i2], 'BalanceChange'
                                                  : amtchange, 'currentBalance': curamt}, ignore_index=True)
                    i2 += 1


                    if buylog['TradeMethod'].iloc[i1] == 'Long':
                        if curamt < buylog['buyFuture'].iloc[i1]:
                            tdlog = tdlog.drop(tdlog[(tdlog['startDate'] == buylog['startDate'].iloc[i1]) &
                                                     (tdlog['startTick'] == buylog['startTick'].iloc[i1]) &
                                                     (tdlog['FutureName'] == buylog['FutureName'].iloc[i1])].index,
                                               axis=0)
                            i1 += 1
                            continue
                        amtchange = -buylog['buyFuture'].iloc[i1]
                        curamt += amtchange
                    else:
                        if curamt < buylog['buyETF'].iloc[i1]:
                            tdlog = tdlog.drop(tdlog[(tdlog['startDate'] == buylog['startDate'].iloc[i1]) &
                                                     (tdlog['startTick'] == buylog['startTick'].iloc[i1]) &
                                                     (tdlog['FutureName'] == buylog['FutureName'].iloc[i1])].index,
                                               axis=0)
                            i1 += 1
                            continue
                        amtchange = -buylog['buyETF'].iloc[i1]
                        curamt += amtchange

                    balance = balance.append({'date': date, 'timetick': buylog['startTick'].iloc[i1],
                                              'tradeMove': 'Buy ' + buylog['FutureName'].iloc[i1], 'BalanceChange':
                                                  amtchange, 'currentBalance': curamt}, ignore_index=True)

                    i1 += 1

            while i1 < len(buylog.index) and i2 == len(selllog.index):

                if buylog['TradeMethod'].iloc[i1] == 'Long':
                    if curamt < buylog['buyFuture'].iloc[i1]:
                        tdlog = tdlog.drop(tdlog[(tdlog['startDate'] == buylog['startDate'].iloc[i1]) &
                                                 (tdlog['startTick'] == buylog['startTick'].iloc[i1]) &
                                                 (tdlog['FutureName'] == buylog['FutureName'].iloc[i1])].index,
                                           axis=0)
                        i1 += 1
                        continue
                    amtchange = -buylog['buyFuture'].iloc[i1]
                    curamt += amtchange
                else:
                    if curamt < buylog['buyETF'].iloc[i1]:
                        tdlog = tdlog.drop(tdlog[(tdlog['startDate'] == buylog['startDate'].iloc[i1]) &
                                                 (tdlog['startTick'] == buylog['startTick'].iloc[i1]) &
                                                 (tdlog['FutureName'] == buylog['FutureName'].iloc[i1])].index,
                                           axis=0)
                        i1 += 1
                        continue
                    amtchange = -buylog['buyETF'].iloc[i1]
                    curamt += amtchange

                balance = balance.append({'date': date, 'timetick': buylog['startTick'].iloc[i1],
                                          'tradeMove': 'Buy ' + buylog['FutureName'].iloc[i1], 'BalanceChange':
                                              amtchange, 'currentBalance': curamt}, ignore_index=True)
                i1 += 1

            while i2 <len(selllog.index) and i1 == len(buylog.index):
                if selllog['TradeMethod'].iloc[i2] == 'Long':
                    amtchange = (selllog['buyETF'].iloc[i2] - selllog['sellETF'].iloc[i2] +
                                 selllog['sellFuture'].iloc[i2])
                    curamt += amtchange
                    balance = balance.append({'date': date, 'timetick': selllog['endTick'].iloc[i2],
                                              'tradeMove': 'Sell ' + selllog['FutureName'].iloc[i2], 'BalanceChange'
                                              : amtchange, 'currentBalance': curamt}, ignore_index=True)

                else:
                    amtchange = (selllog['buyFuture'].iloc[i2] - selllog['sellFuture'].iloc[i2] +
                                 selllog['sellETF'].iloc[i2])
                    curamt += amtchange
                    balance = balance.append({'date': date, 'timetick': selllog['endTick'].iloc[i2],
                                              'tradeMove': 'Sell ' + selllog['FutureName'].iloc[i2], 'BalanceChange'
                                              : amtchange, 'currentBalance': curamt}, ignore_index=True)
                i2 += 1
    balance.to_csv('./testbls20.csv')
    return

def get_strategy():
    tradelog = pd.read_csv('./tradelog/tradelog5modified.csv', index_col=0)
    return tradelog

def get_future_list(date):
    flist = fUtils.FuturesDailySummaryFrame('IF', date)['InstrumentId'].to_list() + \
            fUtils.FuturesDailySummaryFrame('IH', date)['InstrumentId'].to_list()

    return flist

def get_daily_trades(flist, balancedf):
    for future in flist:

        pass
    return


get_sim_log('20170101','20201231',10000000)
