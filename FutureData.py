from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime
import multiprocessing as mp
import os
import matplotlib.pyplot as plt


class FutureTrade:
    fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
    secUtils = CSecurityMarketDataUtils('Z:/StockData')


    def __init__(self, name, etfname):
        self.name = name
        self.etfNumber = etfname


    def get_etf_TAQ_array(self, date):
        fundTAQ = self.secUtils.FundTAQDataFrame(self.etfNumber, date)
        fundArray = np.array(fundTAQ)
        fundArray = fundArray[fundArray[:, fundTAQ.columns.values.tolist().index('TradingTime')] < '14:57:00.000']
        fundArray = fundArray[fundArray[:, fundTAQ.columns.values.tolist().index('TradingTime')] > '09:30:00.000']
        self.etfArray = fundArray

        self.etf_i_b10 = fundTAQ.columns.values.tolist().index('BuyVolume10')
        self.etf_i_b1 = fundTAQ.columns.values.tolist().index('BuyVolume01')
        self.etf_i_bp10 = fundTAQ.columns.values.tolist().index('BuyPrice10')
        self.etf_i_bp1 = fundTAQ.columns.values.tolist().index('BuyPrice01')

        self.etf_i_s10 = fundTAQ.columns.values.tolist().index('SellVolume10')
        self.etf_i_s1 = fundTAQ.columns.values.tolist().index('SellVolume01')
        self.etf_i_sp10 = fundTAQ.columns.values.tolist().index('SellPrice10')
        self.etf_i_sp1 = fundTAQ.columns.values.tolist().index('SellPrice01')

        rtarr = np.zeros((fundArray.shape[0], 9))
        rtarr = np.concatenate(
            (np.row_stack(fundArray[:, fundTAQ.columns.values.tolist().index('TradingTime')]), rtarr), axis=1)

        return rtarr

    def get_discount_etf(self, rtarr):
        fundtaq = self.etfArray
        i_s10 = self.etf_i_s10
        i_s1 = self.etf_i_s1

        i_sp1 = self.etf_i_sp1
        dcetf = np.zeros((fundtaq.shape[0], 1))
        fundtaq = np.concatenate((fundtaq, dcetf), axis=1)
        for index in range(fundtaq.shape[0]):
            ttshare = 300000
            current_share = 0
            ttcost = 0
            i = 0
            # return only the row at trade time

            sum_vol = fundtaq[index, i_s10:i_s1 + 1].sum()
            # check if there is enough shares to trade
            if ttshare > sum_vol:
                # print('cant buy' + self.etfNumber)
                fundtaq[index, -1] = 0
            else:
                while i < 10:
                    if float(fundtaq[index, i_s1 - i]) < ttshare - current_share:
                        current_share += float(fundtaq[index, i_s1 - i])
                        ttcost += float(fundtaq[index, i_s1 - i]) * float(fundtaq[index, i_sp1 - i])
                        i += 1
                    else:
                        ttcost += float(ttshare - current_share) * float(fundtaq[index, i_sp1 - i])
                        current_share += ttshare - current_share
                        i = 10
                fundtaq[index, -1] = ttcost

        rtarr[:, 1] = fundtaq[:, -1]
        return rtarr

    def get_premium_etf(self, rtarr):
        fundtaq = self.etfArray
        i_b10 = self.etf_i_b10
        i_b1 = self.etf_i_b1
        i_bp10 = self.etf_i_bp10
        i_bp1 = self.etf_i_bp1
        dcetf = np.zeros((fundtaq.shape[0], 1))
        fundtaq = np.concatenate((fundtaq, dcetf), axis=1)
        for index in range(fundtaq.shape[0]):
            ttshare = 300000
            current_share = 0
            ttreturn = 0
            i = 0

            sum_vol = fundtaq[index, i_b1:i_b10 + 1].sum()
            # check if there is enough shares to trade
            if ttshare > sum_vol:
                # print('cant sell' + self.etfNumber)
                fundtaq[index, -1] = 0
            else:
                while i < 10:
                    if float(fundtaq[index, i_b1 + i]) < ttshare - current_share:
                        current_share += float(fundtaq[index, i_b1 + i])
                        ttreturn += float(fundtaq[index, i_b1 + i]) * float(fundtaq[index, i_bp1 + i])
                        i += 1
                    else:
                        ttreturn += float(ttshare - current_share) * float(fundtaq[index, i_bp1 + i])
                        current_share += ttshare - current_share
                        i = 10
                fundtaq[index, -1] = ttreturn

        rtarr[:, 2] = fundtaq[:, -1]
        return rtarr

    def get_buy_future(self, rtarr, date):
        name = self.name
        futuredf = self.fUtils.FuturesTickDataFrame(name, date)
        timetick = rtarr[:, 0]
        pricelist = []

        for i in timetick:
            tick = i[:-4]
            tickdf = futuredf[futuredf['UpdateTime'] == tick]
            if len(tickdf.index) == 0:
                minprice = 0
            else:
                minprice = tickdf['AskPrice1'].min()
            mintotalprice = float(minprice) * 300

            pricelist.append(mintotalprice)
        # pricelist = np.row_stack(pricelist)

        rtarr[:, 3] = pricelist
        return rtarr

    def get_sell_future(self, rtarr, date):
        name = self.name
        futuredf = self.fUtils.FuturesTickDataFrame(name, date)
        timetick = rtarr[:, 0]

        pricelist = []

        for i in timetick:
            tick = i[:-4]
            tickdf = futuredf[futuredf['UpdateTime'] == tick]
            if len(tickdf.index) == 0:
                minprice = 0
            else:
                minprice = tickdf['BidPrice1'].min()
            mintotalprice = float(minprice) * 300

            pricelist.append(mintotalprice)
        # pricelist = np.row_stack(pricelist)

        rtarr[:, 4] = pricelist
        return rtarr

    def get_return_rate(self, rtarr):
        # buy future sell etf
        rtarr[:, 5] = rtarr[:, 3].astype(np.float) - rtarr[:, 2].astype(np.float)
        # buy etf sell future
        rtarr[:, 6] = rtarr[:, 1].astype(np.float) - rtarr[:, 4].astype(np.float)

        buyf1 = rtarr[rtarr[:, 2].astype(np.float) != 0]
        buyf1 = buyf1[buyf1[:, 5].astype(np.float) != 0]
        buyf1[:, 7] = buyf1[:, 5].astype(np.float)/ buyf1[:, 2].astype(np.float)
        rtarr[rtarr[:,5].astype(np.float)*rtarr[:, 2].astype(np.float) != 0] = buyf1

        sellf1 = rtarr[rtarr[:, 1].astype(np.float) != 0]
        sellf1 = sellf1[sellf1[:, 6].astype(np.float) != 0]
        sellf1[:, 8] = sellf1[:, 6].astype(np.float)/ sellf1[:,1].astype(np.float)
        rtarr[rtarr[:, 6].astype(np.float)*rtarr[:, 1].astype(np.float) != 0] = sellf1

        rtarr1 = rtarr[rtarr[:, 1].astype(np.float)*rtarr[:, 2].astype(np.float)*rtarr[:, 3].astype(np.float)*rtarr[:, 4].astype(np.float) == 0]
        rtarr1[:, 7] = 0
        rtarr1[:, 8] = 0
        rtarr[rtarr[:, 1].astype(np.float) * rtarr[:, 2].astype(np.float) * rtarr[:, 3].astype(np.float) * rtarr[:,
                                                                                                           4].astype(
            np.float) == 0] = rtarr1

        return rtarr

    def get_tracking_error(self, rtarr, date):
        if self.name[0:2]=='IH':
            indexname = '000016.SH'
        if self.name[0:2] == 'IF':
            indexname = '000300.SH'
        indexdf = self.secUtils.IndexTickDataFrame(indexname, date)
        for i in range(len(rtarr[:,0])):
            timetick = rtarr[i,0]
            index = indexdf[indexdf['TradingTime'] < timetick]['LastPrice'].iloc[-1]
            rtarr[i,9] = float(index)*300
        return rtarr



    def get_rtarr(self, date):
        print('getting rtarr for'+self.name+ 'on' + date)
        rtarr = self.get_etf_TAQ_array(date)
        # print('getting etf array on ' + date)
        rtarr = self.get_discount_etf(rtarr)
        # print('getting etf dcetf  ' + date)
        rtarr = self.get_premium_etf(rtarr)
        # print('getting etf pretf ' + date)
        rtarr = self.get_buy_future(rtarr, date)
        # print('buy future ' + date)
        rtarr = self.get_sell_future(rtarr, date)
        # print('sell future ' + date)
        rtarr = self.get_return_rate(rtarr)
        # print('getting return rate' + date)
        rtarr = self.get_tracking_error(rtarr, date)

        name = self.name
        rtarr_df = pd.DataFrame(rtarr)
        rtarr_df = rtarr_df.rename(
            columns={0: 'timetick', 1: 'buyETF', 2: 'sellETF', 3: 'buy' + name[0:2], 4: 'sell' + name[0:2],
                     5: 'buyDiff', 6: 'sellDiff',
                     7: 'sellRate', 8: 'buyRate', 9:'IndexPrice'})
        path = '.\\result\\' + name[0:2] + '\\' + name
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        rtarr_df.to_csv(path + '\\' + date + '.csv', index=False)
        print('got rtarr on '+ date)

        return





def get_trade_date(name):
    year = name[2:4]
    month = name[4:]
    fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')

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
        except ValueError:
            tdPeriodList.remove(tdday)
        else:
            continue

    return tdPeriodList




if __name__ == '__main__':
    year = 2018
    for fut in ['IH', 'IF']:
        for month in range(1, 13):
            if month < 10:
                name = fut+str(year)[-2:]+ '0' + str(month)
            else:
                name = fut+str(year)[-2:] + str(month)
            if fut == 'IH':
                etfname = '510050.SH'
            if fut == 'IF':
                etfname = '510300.SH'
            tradelist = get_trade_date(name)

            rtarr_list = []
            for i in range(len(tradelist)):
                tradelist[i] = tradelist[i].replace('-', '')

            a = FutureTrade(name, etfname)
            pool = mp.Pool(mp.cpu_count())
            rtarr_list = pool.map(a.get_rtarr, [(td) for td in tradelist])

'''
        buymax = []
        sellmax = []
        for i in range(len(rtarr_list)):
            date = tradelist[i]
            rtarr = rtarr_list[i]
            rtarr_df = pd.DataFrame(rtarr)
            rtarr_df = rtarr_df.rename(
                columns={0: 'timetick', 1: 'buyETF', 2: 'sellETF', 3: 'buy' + name[0:2], 4: 'sell' + name[0:2],
                         5: 'buyDiff', 6: 'sellDiff',
                         7: 'sellRate', 8: 'buyRate'})
            path = '.\\result\\' + name[0:2] + '\\' + name
            folder = os.path.exists(path)
            if not folder:
                os.makedirs(path)
            rtarr_df.to_csv(path + '\\' + date + '.csv', index=False)
            buymax.append(rtarr[:, 7].astype(np.float).max())
            sellmax.append(rtarr[:, 8].astype(np.float).max())
            '''







'''
    for i in range(len(rtarr_list)):
        rtarr_list[i] = a.get_return_rate(rtarr_list[i])

'''

