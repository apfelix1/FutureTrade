from higgsboom.MarketData.CFuturesMarketDataUtils import *

fUtils = CFuturesMarketDataUtils('Z:/FuturesData', 'cffex-l2')

fList = fUtils.FuturesTickDataFrame('IF2006', '20200103')
print(fList)


