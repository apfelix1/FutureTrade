from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
secUtils = CSecurityMarketDataUtils('Z:/StockData')


def get_df(future, date):
    rtarr = pd.read_csv('./result/' + future[0:2] + '/' + future + '/'+date + '.csv')
    return rtarr


def get_short_trade_log(future, buyspread, sellspread):
    name = future
    tradelist = get_trade_date(name)
    tradelog = pd.DataFrame(
        columns=['startDate',  'startTick',  'endDate', 'endTick', 'buyFuture', 'buyETF',
                 'sellFuture', 'sellETF', 'returnRate'])
    canbuy = True
    for i in range(len(tradelist)):
        tradelist[i] = tradelist[i].replace('-','')
    for date in tradelist:
        print(date)
        date = date.replace('-', '')
        rtarr = get_df(future, date)
        if canbuy == False:
            rtarr['sellRate'] = pd.to_numeric(rtarr['sellRate'])
            rtarrs = rtarr[rtarr['sellRate'] < sellspread]
            rtarrs = rtarrs[rtarrs['sellRate'] != 0]
            print(date)
            if date != tradelist[-1]:
                if len(rtarrs.index) == 0:
                    print('cant sell case0')
                    continue
                else:
                    print('trying to sell, case1')
                    i = len(tradelog.index) - 1
                    tradelog.loc[i] = [tradelog['startDate'].iloc[i], tradelog['startTick'].iloc[i], date,
                                       rtarrs['timetick'].iloc[0], tradelog['buyFuture'].iloc[i],
                                       tradelog['buyETF'].iloc[i],
                                       rtarrs['buy' + future[0:2]].iloc[0], rtarrs['sellETF'].iloc[0], 0]
                    canbuy = True
                    continue

            if len(rtarrs.index) == 0:
                rtarrs = rtarr[rtarr['timetick'] > '14:30:00.000']

                print('trying to sell, case2')
                i = len(tradelog.index) - 1
                tradelog.loc[i] = [tradelog['startDate'].iloc[i], tradelog['startTick'].iloc[i], date,
                                   rtarrs['timetick'].iloc[0], tradelog['buyFuture'].iloc[i],
                                   tradelog['buyETF'].iloc[i],
                                   rtarrs['buy' + future[0:2]].iloc[0], rtarrs['sellETF'].iloc[0], 0]
                canbuy = True
                continue
            print('trying to sell, case3')
            i = len(tradelog.index) - 1
            tradelog.loc[i] = [tradelog['startDate'].iloc[i], tradelog['startTick'].iloc[i], date,
                               rtarrs['timetick'].iloc[0], tradelog['buyFuture'].iloc[i], tradelog['buyETF'].iloc[i],
                               rtarrs['buy' + future[0:2]].iloc[0], rtarrs['sellETF'].iloc[0], 0]
            canbuy = True

        else:

            rtarr['sellRate'] = pd.to_numeric(rtarr['sellRate'])
            rtarrb = rtarr[rtarr['sellRate'] > buyspread]
            if date != tradelist[-1]:
                if len(rtarrb.index) == 0:
                    print('cant buy, case 0')
                    continue
                else:
                    print('trying to buy, case 1')
                    canbuy = False
                    tradelog.loc[len(tradelog.index)] = [date, rtarrb['timetick'].iloc[0], 'TBD', 'TBD',
                                                         rtarrb['sell' + future[0:2]].iloc[0],
                                                         rtarrb['buyETF'].iloc[0], 'TBD', 'TBD', 0]
                    continue
            # cant buy cuz its last day
            print('cant buy, case 2')
            continue

    print(tradelog)
    list = ['buyFuture', 'buyETF', 'sellFuture', 'sellETF']
    for i in list:
        tradelog[i] = pd.to_numeric(tradelog[i])
    tradelog['returnRate'] = (tradelog['sellETF'] - tradelog['buyETF'] - tradelog['sellFuture'] + tradelog['buyFuture'])/ (
        tradelog['buyETF'])
    print(tradelog)
    return tradelog

def get_long_trade_log(future, buyspread, sellspread):
    name = future
    tradelist = get_trade_date(name)
    tradelog = pd.DataFrame(
        columns=['startDate',  'startTick',  'endDate', 'endTick', 'buyFuture', 'buyETF',
                 'sellFuture', 'sellETF', 'returnRate'])
    canbuy = True
    for i in range(len(tradelist)):
        tradelist[i] = tradelist[i].replace('-','')
    for date in tradelist:
        print(date)
        date = date.replace('-', '')
        rtarr = get_df(future, date)
        if canbuy == False:
            rtarr['buyRate'] = pd.to_numeric(rtarr['buyRate'])
            rtarrs = rtarr[rtarr['buyRate'] < sellspread]
            rtarrs = rtarrs[rtarrs['buyRate'] != 0]
            print(date)
            if date != tradelist[-1]:
                if len(rtarrs.index) == 0:
                    print('cant sell case0')

                else:
                    print('trying to sell, case1')
                    i = len(tradelog.index) - 1
                    tradelog.loc[i] = [tradelog['startDate'].iloc[i], tradelog['startTick'].iloc[i], date,
                                       rtarrs['timetick'].iloc[0], tradelog['buyFuture'].iloc[i],
                                       tradelog['buyETF'].iloc[i],
                                       rtarrs['sell' + future[0:2]].iloc[0], rtarrs['buyETF'].iloc[0], 0]
                    canbuy = True

            if len(rtarrs.index) == 0:
                rtarrs = rtarr[rtarr['timetick'] > '14:30:00.000']

                print('trying to sell, case2')
                i = len(tradelog.index) - 1
                tradelog.loc[i] = [tradelog['startDate'].iloc[i], tradelog['startTick'].iloc[i], date,
                                   rtarrs['timetick'].iloc[0], tradelog['buyFuture'].iloc[i],
                                   tradelog['buyETF'].iloc[i],
                                   rtarrs['sell' + future[0:2]].iloc[0], rtarrs['buyETF'].iloc[0], 0]
                canbuy = True
                continue
            print('trying to sell, case3')
            i = len(tradelog.index) - 1
            tradelog.loc[i] = [tradelog['startDate'].iloc[i], tradelog['startTick'].iloc[i], date,
                               rtarrs['timetick'].iloc[0], tradelog['buyFuture'].iloc[i], tradelog['buyETF'].iloc[i],
                               rtarrs['buy' + future[0:2]].iloc[0], rtarrs['sellETF'].iloc[0], 0]
            canbuy = True
            continue

        if canbuy == True:

            rtarr['buyRate'] = pd.to_numeric(rtarr['buyRate'])
            rtarrb = rtarr[rtarr['buyRate'] > buyspread]
            if date != tradelist[-1]:
                if len(rtarrb.index) == 0:
                    print('cant buy, case 0')
                    continue
                else:
                    print('trying to buy, case 1')
                    canbuy = False
                    tradelog.loc[len(tradelog.index)] = [date, rtarrb['timetick'].iloc[0], 'TBD', 'TBD',
                                                         rtarrb['buy' + future[0:2]].iloc[0],
                                                         rtarrb['sellETF'].iloc[0], 'TBD', 'TBD', 0]
                    continue
            # cant buy cuz its last day
            print('cant buy, case 2')
            continue

    print(tradelog)
    list = ['buyFuture', 'buyETF', 'sellFuture', 'sellETF']
    for i in list:
        tradelog[i] = pd.to_numeric(tradelog[i])
    tradelog['returnRate'] = (-tradelog['sellETF'] + tradelog['buyETF'] + tradelog['sellFuture'] - tradelog['buyFuture'])/ (
        tradelog['sellETF'])
    print(tradelog)
    return tradelog


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


if __name__ == '__main__':
    list1 = ['IH','IF']
    list2 = range(2001, 2013)
    buyspread = 0.015
    sellspread = 0.0015
    for i1 in list1:
        for i2 in list2:
            name = str(i1)+str(i2)

            tradelog = get_long_trade_log(name, buyspread, sellspread)

            path = './result/' + name[0:2] + '/longFuture/'
            folder = os.path.exists(path)
            if not folder:
                os.makedirs(path)
            tradelog.to_csv(path + name + '.csv', index=False)

            print('logged' + name)
