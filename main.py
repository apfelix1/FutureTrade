from higgsboom.MarketData.CFuturesMarketDataUtils import *
import pandas as pd
import numpy as np
from higgsboom.MarketData.CSecurityMarketDataUtils import *
import datetime
import multiprocessing as mp
import matplotlib.pyplot as plt


secUtils = CSecurityMarketDataUtils('Z:/StockData')

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')
print(fUtils.FuturesTickDataFrame('IH2005','20200323'))
print(secUtils.FundTAQDataFrame('510050.SH', '20200323'))

