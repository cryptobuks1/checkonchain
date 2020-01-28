from checkonchain.general.coinmetrics_api import *
from checkonchain.general.standard_charts import *
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.dcronchain.dcr_add_metrics import *


BTC = btc_add_metrics().btc_coin()
DCR = dcr_add_metrics().dcr_coin()
ETH = Coinmetrics_api('eth',"2015-07-30",today).convert_to_pd()
ETH['age_days'] = (ETH[['date']] - ETH.loc[0,['date']])/np.timedelta64(1,'D')
ETH['age_sply'] = ETH['SplyCur']/135135633


loop_data = [[0,2,1,3,4,5],[]]
x_data = [
    BTC['age_sply'],
    BTC['age_sply'],
    ETH['age_sply'],
    ETH['age_sply'],
    DCR['age_sply'],
    DCR['age_sply'],
    ]
y_data = [
    BTC['CapMrktCurUSD'],
    BTC['DailyIssuedUSD'].cumsum(),
    ETH['CapMrktCurUSD'],
    ETH['DailyIssuedUSD'].cumsum(),
    DCR['CapMrktCurUSD'],
    DCR['DailyIssuedUSD'].cumsum()*0.9,
    ]
name_data = [
    'BTC Market Cap',
    'BTC Cumulative PoW Issued',
    'ETH Market Cap',
    'ETH Cumulative PoW Issued',
    'DCR Market Cap',
    'DCR Cumulative PoW Issued',
    ]
color_data = [
    'rgb(239, 125, 50)',    #Price Orange
    'rgb(250, 38, 53)' ,    #PoW Red
    'rgb(153, 51, 255)',    #Purple
    'rgb(51, 102, 255)',    #Dark Blue
    'rgb(46, 214, 161)' ,   #Turquoise
    'rgb(65, 191, 83)',     #Decred Green
    ]
dash_data = [
    'solid','dot','solid','dot','solid','dot',
    ]
width_data = [
    2,2,2,2,2,2
    ]
opacity_data = [
    1,1,1,1,1,1
    ]
legend_data = [
    True,True,True,True,True,True,
    ]
title_data = [
    'PoW Production Monetary Premium',
    'Protocol Age (days)',
    'Value (USD)',
    '']
range_data = [[0,4380],[6,12],[2,8]]
autorange_data = [False,False,True]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
#fig.update_xaxes(dtick=0.1)
fig.show()