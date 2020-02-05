#Plot Market Cap vs Block Subsidy
from checkonchain.general.standard_charts import *
from checkonchain.general.coinmetrics_api import *

BTC = Coinmetrics_api('btc',"2009-01-03",today).convert_to_pd().set_index('date',drop=False)
LTC = Coinmetrics_api('ltc',"2011-10-07",today).convert_to_pd().set_index('date',drop=False)
DAS = Coinmetrics_api('dash',"2014-01-19",today).convert_to_pd().set_index('date',drop=False)
DCR = Coinmetrics_api('dcr',"2016-02-08",today).convert_to_pd().set_index('date',drop=False)
XMR = Coinmetrics_api('xmr',"2014-04-18",today).convert_to_pd().set_index('date',drop=False)
ZEC = Coinmetrics_api('zec',"2016-10-28",today).convert_to_pd().set_index('date',drop=False)
ETH = Coinmetrics_api('eth',"2015-07-30",today).convert_to_pd().set_index('date',drop=False)


loop_data = [[0,1,],[]]
x_data = [
    #BTC['date'],BTC['date'],
    #LTC['date'],LTC['date'],
    #DAS['date'],DAS['date'],
    #DCR['date'],DCR['date'],
    #XMR['date'],XMR['date'],
    ZEC['date'],ZEC['date'],
    #ETH['date'],ETH['date'],
    ]
y_data = [
    #BTC['CapMrktCurUSD'],BTC['DailyIssuedUSD'].cumsum(),
    #LTC['CapMrktCurUSD'],LTC['DailyIssuedUSD'].cumsum(),
    #DAS['CapMrktCurUSD'],DAS['DailyIssuedUSD'].cumsum(),
    #DCR['CapMrktCurUSD'],DCR['DailyIssuedUSD'].cumsum(),
    #XMR['CapMrktCurUSD'],XMR['DailyIssuedUSD'].cumsum(),
    ZEC['SplyCur'],ZEC['BlkCnt'].cumsum()*12.5,
    #ETH['CapMrktCurUSD'],ETH['DailyIssuedUSD'].cumsum(),
    ]
name_data = [
    #'BTC','BTC',
    #'LTC','LTC',
    #'DAS','DAS',
    #'DCR','DCR',
    #'XMR','XMR',
    'ZEC','ZEC',
    #'ETH','ETH',
    ]
color_data = [
    #'rgb(255, 102, 0)' ,'rgb(255, 102, 0)' ,
    #'rgb(214, 214, 194)','rgb(214, 214, 194)',
    #'rgb(51, 204, 255)','rgb(51, 204, 255)',
    #'rgb(46, 214, 161)','rgb(46, 214, 161)',
    #'rgb(255, 153, 0)','rgb(255, 153, 0)',
    'rgb(255, 255, 0)','rgb(255, 255, 0)',
    #'rgb(153, 51, 255)','rgb(153, 51, 255)',
    ]
dash_data = [
    #'solid','dash',
    #'solid','dash',
    #'solid','dash',
    #'solid','dash',
    #'solid','dash',
    'solid','dash',
    #'solid','dash',
    ]
width_data = [
    1,1,#1,1,1,1,1,1,1,1,1,1,1,1,
    ]
opacity_data = [
    1,1,#1,1,1,1,1,1,1,1,1,1,1,1,
    ]
legend_data = [
    #True,True,
    #True,True,
    #True,True,
    #True,True,
    #True,True,
    True,True,
    #True,True,
    ]
title_data = [
    'ZEC SUpply',
    'Date',
    'Supply',
    'Price USD']
range_data = [[0,4500],[2,6.3],[-2,4.3]]
autorange_data = [True,True,True]
type_data = ['date','linear','linear']#
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()