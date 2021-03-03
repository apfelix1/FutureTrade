from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
secUtils = CSecurityMarketDataUtils('Z:/StockData')
indexdf = secUtils.IndexTickDataFrame('000300.SH', '20200423')
indexdf.to_csv('./index.csv', index = False)
def get_tracking_error():
    secUtils.IndexTickDataFrame('000016.SH', '20200423')
    return
