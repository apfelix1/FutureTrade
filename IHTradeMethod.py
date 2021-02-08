from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
from datetime import datetime

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
secUtils = CSecurityMarketDataUtils('Z:/StockData')


class FutureTrade:
    def __init__(self, date):
        self.date = date

    def get_first_taq(self):
        if float(self.date[6:]) < 15:
            fCurrent = fUtils.FuturesTickDataFrame('IH' + + self.date[2:6], self.date)
            return fCurrent
        if 15 <= float(self.date[6:]) <= 21 and datetime.strptime(self.date, '%Y%m%d') < 5:
            fCurrent = fUtils.FuturesTickDataFrame('IH' + + self.date[2:6], self.date)
            return fCurrent
        fCurrent = fUtils.FuturesTickDataFrame('IH' + + self.date[2:4] + str(int(float(self.date[4:6]) + 1)), self.date)
        return fCurrent

    def get_sec_future_taq(self):
        month = int(float(self.date[4:6]) + 1)
        if month < 10:
            fCurrent = fUtils.FuturesTickDataFrame('IH' + + self.date[2:4] + '0' + str(month),
                                                   self.date)
            return fCurrent
        elif 10 <= month <= 12:
            fCurrent = fUtils.FuturesTickDataFrame('IH' + + self.date[2:4] + str(int(float(self.date[4:6]) + 1)),
                                                   self.date)
            return fCurrent
        else:
            fCurrent = fUtils.FuturesTickDataFrame('IH' + + str(int(int(self.date[2:4]) + 1)) + '01',
                                                   self.date)
            return fCurrent

    def get_third_future_taq(self):
        month = int((((float(self.date[4:6]) + 1) // 3) + 1) * 3)

        if month <= 9:
            fCurrent = fUtils.FuturesTickDataFrame('IH' + self.date[2:4] + '0' + str(month), self.date)
            return fCurrent
        elif month == 12:
            fCurrent = fUtils.FuturesTickDataFrame('IH' + self.date[2:4] + '12', self.date)
            return fCurrent
        elif month > 12:
            fCurrent = fUtils.FuturesTickDataFrame('IH' + str(int(int(self.date[2:4]) + 1)) + str(month - 12),
                                                   self.date)
            return fCurrent

    def get_forth_future_taq(self):
        month = int((((float(self.date[4:6]) + 1) // 3) + 2) * 3)

        if month <= 9:
            fCurrent = fUtils.FuturesTickDataFrame('IH' + self.date[2:4] + '0' + str(month), self.date)
            return fCurrent
        elif month == 12:
            fCurrent = fUtils.FuturesTickDataFrame('IH' + self.date[2:4] + '12', self.date)
            return fCurrent
        elif month > 12:
            fCurrent = fUtils.FuturesTickDataFrame('IH' + str(int(int(self.date[2:4]) + 1)) + str(month - 12),
                                                   self.date)
            return fCurrent

    def get_etf_taq(self):
        fundTAQ = secUtils.FundTAQDataFrame('510050.SH', self.date)
        fundTAQ = fundTAQ[fundTAQ['TradingTime'] <= '14:57:00.000']
        fundTAQ = fundTAQ[fundTAQ['TradingTime'] >= '09:30:00.000']
        return fundTAQ




a = FutureTrade('20200102')
ft = a.get_third_future_taq()
