#Onchain DCR Volumes
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import *

DCR_tics = dcr_add_metrics().dcr_ticket_models()

loop_data = [[0],[1]]
x_data = [
    DCR_tics['date'],
    DCR_tics['date'],
    DCR_tics['date'],
    ]
y_data = [
    DCR_tics['SplyCur']/DCR_tics['dcr_tic_sply_avg'],
    DCR_tics['SplyCur']/DCR_tics['tic_pool_avg'],
    DCR_tics['CapMVRVCur'],
]
name_data = [
    'DCR Supply / DCR TIcket Pool',
    'DCR Supply / DCR Ticket Count',
    'MVRV',
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
autorange_data = [True,False,False]
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
