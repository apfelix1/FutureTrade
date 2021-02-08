from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')

fCurrent = fUtils.FuturesTickDataFrame('IF2006', '20200103')

class spottrade:
    def get_tradelist(self):
        tdPeriodList = TradingDays(startDate='20200101', endDate='20201231')
        for i in tdPeriodList:
            i = i.replace("-", "")
        return tdPeriodList

    def get_first_taq(self,date):
        fCurrent = fUtils.FuturesTickDataFrame('IF2006', date)
        return fCurrent

    def get_sec_future_taq(self,date):
        fCurrent = fUtils.FuturesTickDataFrame('IF2006', date)
        return fCurrent

    def get_third_future_taq(self,date):
        fCurrent = fUtils.FuturesTickDataFrame('IF2006', date)
        return fCurrent

    def get_forth_future_taq(self,date):
        fCurrent = fUtils.FuturesTickDataFrame('IF2006', date)
        return fCurrent


