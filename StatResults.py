from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
secUtils = CSecurityMarketDataUtils('Z:/StockData')
indexdf = secUtils.IndexTickDataFrame('000300.SH', '20200423')


def get_tracking_error(futurename, etfname, date):


    return
