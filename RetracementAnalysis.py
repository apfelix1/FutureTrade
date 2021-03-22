from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
secUtils = CSecurityMarketDataUtils('Z:/StockData')
fTradingDays = np.row_stack(fUtils.FuturesTradingDays('IF'))
hTradingDays = np.row_stack(fUtils.FuturesTradingDays('IH'))


def get_tradelog():
    tradelog = pd.read_csv('./tradelog/tradelog1.csv', index_col=0)
    return tradelog

def get_future_data(name,date):
    path = './result/'+name[0:2]+'/'+ name +'/'
    futuredata = pd.read_csv(path+str(date)+'.csv')

    return futuredata

def get_tradelist(name,startdate,enddate):
    if name[0:2] == 'IH':
        tradelist = hTradingDays[hTradingDays[:, 0] >= startdate]
        tradelist = tradelist[tradelist[:, 0] <= enddate]
    if name[0:2] == 'IF':
        tradelist = fTradingDays[fTradingDays[:, 0] >= startdate]
        tradelist = tradelist[tradelist[:, 0] <= enddate]

    return tradelist[:, 0]

def create_future_log(name,startdate,enddate,index):

    tradelist = get_tradelist(name,startdate, enddate)
    # 因为在这个策略中，不存在同一天买入卖出的情况，所以不存在startdate enddate在同一天的情况。如果此后调整策略则需要调整此行代码
    futurelog = pd.DataFrame({'Date':tradelist})
    futurelog['index'] = index

    path = './retracement/'+name+'/'

    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

    exists = os.path.exists(path+name+'.csv')
    if exists:
        futurelog1 = pd.read_csv(path+name+'.csv', index_col= 0)
        futurelog = futurelog1.append(futurelog,ignore_index=True)

    futurelog.to_csv(path+name+'.csv')

    return

def log_retracement(name, initamt, initspread, index, longbool):
    path = './retracement/' + name + '/'
    flog = pd.read_csv(path + name + '.csv', index_col= 0)
    if not 'retracement' in flog:
        flog['retracement'] = 'nah'
        flog['spread'] = 0
    flog1 = flog[flog['index'] == index]


    for i in range(len(flog1.index)):
        date = flog1['Date'].iloc[i]
        data = get_future_data(name,date)
        data = data[data['timetick'] < '14:30:00']
        data = data[data['timetick']> '13:30:00']
        data = data[data['sellETF'] != 0]
        data = data[data['sell'+name[0:2]] != 0]
        data = data[data['buyETF'] != 0]
        data = data[data['buy' + name[0:2]] != 0]

        if longbool:
            spread = (data['buyETF'].mean()-data['sell'+name[0:2]].mean())
            retracement = (initspread - spread)/initamt
            flog1['retracement'].iloc[i] = retracement
            flog1['spread'].iloc[i] = spread
            continue
        spread = (data['buy'+name[0:2]].mean() - data['sellETF'].mean())
        retracement = (initspread - spread)/initamt
        flog1['retracement'].iloc[i] = retracement
        flog1['spread'].iloc[i] = spread

        continue
    flog[flog['index'] == index]= flog1
    flog.to_csv(path + name  + '.csv')
    return


def get_retracement_log(tradelog):
    names = tradelog['FutureName'].drop_duplicates()
    names = names.tolist()
    for fname in names:
        sublog = tradelog[tradelog['FutureName'] == fname]
        sublog.reset_index(drop= True, inplace = True)
        print(sublog.iloc[0])
        for index in range(len(sublog)):
            longbool = sublog['TradeMethod'].iloc[index]=='Long'
            startdate = str(sublog['startDate'].iloc[index])
            enddate = str(sublog['endDate'].iloc[index])
            create_future_log(fname, startdate,enddate,index)
            if longbool:
                log_retracement(fname, sublog['buyETF'].iloc[index]
                                , (sublog['buyETF'].iloc[index] - sublog['buyFuture'].iloc[index])
                                , index, longbool)
                continue
            log_retracement(fname, sublog['buyFuture'].iloc[index]
                            , (sublog['buyFuture'].iloc[index] - sublog['buyETF'].iloc[index])
                            , index, longbool)


    return

def retracement_analysis():
    rtmtlog = pd.DataFrame(columns=['name','index','MaxRetracement'])
    for type in ['IH', 'IF']:
        for year in ['18','19','20']:
            for month in range(1,13):
                if month<10:
                    month = '0'+str(month)

                name = type + year+ str(month)
                print('Analyzing '+name)
                path = './retracement/' + name + '/'
                folder = os.path.exists(path)
                if not folder:
                    continue
                flog = pd.read_csv(path + name + '.csv', index_col=0)

                numindex = flog['index'].nunique()

                for i in range(numindex):
                    flog1 = flog[flog['index'] == i]
                    maxrtmt = flog1[flog1['retracement'].astype(np.float) == flog1['retracement'].astype(np.float).min()]
                    maxrtmt = maxrtmt['retracement'].iloc[0]
                    rtmtlog = rtmtlog.append( {'name': name, 'index': i, 'MaxRetracement': maxrtmt},ignore_index=True)

    rtmtlog.to_csv('./retracement/analysis.csv')

    return


if __name__ == '__main__':
   tradelog = get_tradelog()
   get_retracement_log(tradelog)
   retracement_analysis()

