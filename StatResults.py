from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
secUtils = CSecurityMarketDataUtils('Z:/StockData')
indexdf = secUtils.IndexTickDataFrame('000300.SH', '20200423')

def get_all_trades():
    for fut in ['IH', 'IF']:
        for year in range(2018,2021):
            for mon in range(1,13):
                if mon <10 :
                    futname = fut+str(year)[-2:]+'0'+str(mon)

                elif mon >=10 :
                    futname = fut + str(year)[-2:] + str(mon)

                longpath = './result/'+fut+'/longFuture/'
                shortpath = './result/'+fut+'/shortFuture/'

                longdata = pd.read_csv(longpath+futname+'.csv', index_col = 0)
                longdata['TradeMethod'] = 'Long'
                # longdata['FutureName'] = futname
                # longdata.to_csv(longpath+futname+'.csv')
                shortdata = pd.read_csv(shortpath+futname+'.csv', index_col = 0)
                shortdata['TradeMethod'] = 'Short'
                # shortdata['FutureName'] = futname
                # shortdata.to_csv(shortpath+futname+'.csv')
                if futname =='IH1801':
                    data = pd.concat([longdata,shortdata], ignore_index=True)
                else:
                    data = pd.concat([data, longdata, shortdata],ignore_index= True)
    # data.drop_duplicates()
    data.to_csv('./alltrades.csv')
    return

def get_holding_period():
    data = pd.read_csv('alltrades.csv', index_col=0)
    data['HoldingPeriod'] = '0'
    for i in range(len(data.index)):
        data['HoldingPeriod'].iloc[i] = (datetime.datetime.strptime(str(data['endDate'].iloc[i]),
                                                                    '%Y%m%d') - datetime.datetime.strptime(str(
            data['startDate'].iloc[i]), '%Y%m%d')).days

    data['HoldingPeriod'] +=1

    data.to_csv('./alltrades.csv')
    return data

def get_return_rate():
    data = pd.read_csv('alltrades.csv', index_col=0)

    datalong = data
    datashort = data
    datalong['returnRate'] = (datalong['sellETF'] + datalong['buyFuture'] - datalong['buyETF'] - datalong[
        'sellFuture'] - \
                              0.00015 * (datalong['sellETF'] + datalong['buyETF']) - 0.000023 * (
                                          datalong['sellFuture'] +
                                          datalong['buyFuture'])) / datalong['buyFuture']
    data[data['TradeMethod'] == 'Long'] = datalong[datalong['TradeMethod'] == 'Long']

    datashort['returnRate'] = (datashort['buyETF'] + datashort['sellFuture'] - datashort['sellETF'] - datashort[
        'buyFuture'] - \
                               0.00015 * (datashort['sellETF'] + datashort['buyETF']) - 0.000023 * (
                                           datashort['sellFuture'] +
                                           datashort['buyFuture'])) / datashort['buyETF']
    data[data['TradeMethod'] == 'Short'] = datalong[datalong['TradeMethod'] == 'Short']

    return

def get_apr():
    get_holding_period()
    data = pd.read_csv('./alltrades.csv', index_col=0)

    data['APR'] = 0
    data['APR'] = data['returnRate'] * 243 / data['HoldingPeriod']

    data.to_csv('./alltrades.csv')
    return


if __name__ =='__main__':
    get_apr()


