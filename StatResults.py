from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime
import seaborn as sns

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
secUtils = CSecurityMarketDataUtils('Z:/StockData')
indexdf = secUtils.IndexTickDataFrame('000300.SH', '20200423')

docpath = './tradelog/tradelog5.csv'

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

    for tdday in tdPeriodList:
        tradingfuture = fUtils.FuturesList(name[0:2], tdday)
        try:
            b = tradingfuture.index(name)
        except ValueError:            tdPeriodList.remove(tdday)
        else:
            continue

    return tdPeriodList

def get_all_trades():
    for fut in ['IH', 'IF']:
        for year in range(2018,2021):
            for mon in range(1,13):
                if mon <10 :
                    futname = fut+str(year)[-2:]+'0'+str(mon)

                elif mon >=10 :
                    futname = fut + str(year)[-2:] + str(mon)

                longpath = './result/'+fut+'/longFuture10/'
                shortpath = './result/'+fut+'/shortFuture10/'

                longdata = pd.read_csv(longpath+futname+'.csv')
                longdata['TradeMethod'] = 'Long'
                longdata['FutureName'] = futname
                # longdata.to_csv(longpath+futname+'.csv')
                shortdata = pd.read_csv(shortpath+futname+'.csv')
                shortdata['TradeMethod'] = 'Short'
                shortdata['FutureName'] = futname
                # shortdata.to_csv(shortpath+futname+'.csv')
                if futname =='IH1801':
                    data = pd.concat([longdata,shortdata], ignore_index=True)
                else:
                    data = pd.concat([data, longdata, shortdata],ignore_index= True)
    # data.drop_duplicates()
    data.to_csv(docpath)
    return

def get_holding_period():
    data = pd.read_csv(docpath, index_col=0)
    data['HoldingPeriod'] = '0'
    for i in range(len(data.index)):
        data['HoldingPeriod'].iloc[i] = (datetime.datetime.strptime(str(data['endDate'].iloc[i]),
                                                                    '%Y%m%d') - datetime.datetime.strptime(str(
            data['startDate'].iloc[i]), '%Y%m%d')).days

    data['HoldingPeriod'] +=1

    data.to_csv(docpath)
    return data

def get_return_rate():
    data = pd.read_csv(docpath, index_col=0)

    datalong = data[data['TradeMethod'] == 'Long']
    datashort = data[data['TradeMethod'] == 'Short']
    datalong['returnRate'] = (datalong['buyETF'] + datalong['sellFuture'] - datalong['buyFuture'] - datalong[
        'sellETF'] - \
                              0.00015 * (datalong['sellETF'] + datalong['buyETF']) - 0.000023 * (
                                          datalong['sellFuture'] +
                                          datalong['buyFuture'])) / datalong['buyFuture']
    data[data['TradeMethod'] == 'Long'] = datalong

    datashort['returnRate'] = (datashort['buyFuture'] + datashort['sellETF'] - datashort['sellFuture'] - datashort[
        'buyETF'] - \
                               0.00015 * (datashort['sellETF'] + datashort['buyETF']) - 0.000023 * (
                                           datashort['sellFuture'] +
                                           datashort['buyFuture'])) / datashort['buyETF']
    data[data['TradeMethod'] == 'Short'] = datashort
    data.to_csv(docpath)

    return

def get_apr():
    data = pd.read_csv(docpath, index_col=0)

    data['APR'] = 0
    data['APR'] = data['returnRate'] * 243 / data['HoldingPeriod']

    data.to_csv(docpath)
    return

def get_error_changed():
    data = pd.read_csv(docpath, index_col=0)
    data['ErrorChanged'] = data['endError']-data['startError']
    data.to_csv(docpath)

    return
def get_te_result():
    list1 = ['IH', 'IF']
    list2 = ['18','19','20']
    list3 = range(1, 13)
    teslist = []
    teblist= []

    for i1 in list1:
        for i2 in list2:
            for i3 in list3:
                if i3 < 10:
                    name = str(i1) +str(i2)+ '0' + str(i3)
                else:
                    name = str(i1) + str(i2)+str(i3)
                tdlist = get_trade_date(name)
                for date in tdlist:
                    date = date.replace('-','')
                    data = pd.read_csv('./result/' + i1[0:2] + '/' + name + '/' + date + '.csv', index_col = None)
                    datas = data[data['sellETF']!= 0]
                    datab = data[data['buyETF']!=0]
                    data_tes = (datas['IndexPrice'] - datas['sellETF']).mean()
                    data_teb =(datab['IndexPrice'] - datab['buyETF']).mean()
                    teslist.append(data_tes)
                    teblist.append(data_teb)
    print('tes mean is '+str(sum(teslist)/len(teslist)))
    print('teb mean is ' + str(sum(teblist)/len(teblist)))


if __name__ =='__main__':

    get_all_trades()
    get_holding_period()
    get_return_rate()
    get_apr()
    get_error_changed()

    # get_te_result()





