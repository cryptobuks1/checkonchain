#Onchain DCR Volumes
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import *

DCR_subs = dcr_add_metrics().dcr_coin()

loop_data = [[0,1],[2]]
x_data = [
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    ]
y_data = [
    DCR_subs['CapMrktCurUSD'],
    DCR_subs['CapRealUSD'],
    DCR_subs['CapMVRVCur'],
]
name_data = [
    'Market Cap',
    'Realised Cap',
    'MVRV Ratio',
    ]
color_data = [
    'rgb(239, 125, 50)',    #Price Orange
    'rgb(46, 214, 161)',    #Turquoise
    'rgb(255,255,255)'      #White
    ]
dash_data = ['solid','dash','solid',]
width_data = [2,2,2]
opacity_data = [1,1,1]
legend_data = [True,True,True]#
title_data = ['Decred MVRV Ratio','Date','DCR/USD Valuation','MVRV Ratio']
range_data = [['01-02-2016','01-02-2020'],[-2,3],[0,500e6]]
autorange_data = [True,False,True]
type_data = ['date','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,
    x_data,
    y_data,
    name_data,
    color_data,
    dash_data,
    width_data,
    opacity_data,
    legend_data
    )
fig.show()
