#PermabullNinos Block Subsidy Charts
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.general.general_helpers import *

DCR_subs = dcr_add_metrics().dcr_ticket_models()


"""
#############################################################################
                    DCR USD BLOCK SUBSIDY MODELS
#############################################################################
"""
loop_data = [[0,1,2,3,4,6],[5]]
x_data = [
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    ]
y_data = [
    DCR_subs['PoW_income_usd'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['PoS_income_usd'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['Fund_income_usd'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['Total_income_usd'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['PriceUSD'],DCR_subs['DiffMean'],
    DCR_subs['PriceUSD'].rolling(200).mean()
    ]
name_data = [
    'POW-USD','POS-USD','Treasury-USD','Total-USD',
    'DCR/USD Price', 'Difficulty Ribbon','200DMA'
    ]
color_data = [
    'rgb(250, 38, 53)' ,'rgb(114, 49, 163)','rgb(255, 192, 0)',
    'rgb(20, 169, 233)','rgb(239, 125, 50)','rgb(156,225,143)',
    'rgb(0,176,80)']
dash_data = ['solid','solid','solid','solid','solid','solid','solid']
width_data = [2,2,2,2,2,1,1]
opacity_data = [1,1,1,1,1,1,1]
legend_data = [True,True,True,True,True,True,True]#
title_data = ['Decred Miner Subsidy Models','Date','DCR/USD Pricing','Difficulty']
range_data = [['01-02-2016','01-02-2020'],[-2,3],[5,11]]
autorange_data = [True,False,False]
type_data = ['date','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )

""" =================================
    ADD DIFFICULTY RIBBON BAR CHARTS
================================="""
for i in [9,14,25,40,60,90,128,200]:
    fig.add_trace(go.Scatter(
        mode='lines',
        x=DCR_subs['date'], 
        y=DCR_subs['DiffMean'].rolling(i).mean(),
        name='Difficulty '+str(i),
        opacity=0.5,
        showlegend=False,
        line=dict(
            width=i/200*2,
            color='rgb(156,225,143)',
            dash='solid'
            )),
        secondary_y=True)
""" =================================
    ADD VOLUME BAR CHARTS
================================="""
x_data = [
    DCR_subs['date'],
    DCR_subs['date']
]
y_data = [
    100000+DCR_subs['dcr_tic_vol'],
    100000+DCR_subs['dcr_tfr_vol']
]
color_data = ['rgb(237,96,136)','rgb(37,187,217)']
loop_data = [0,1]
name_data = ['Ticket Vol (DCR)','Transfer Vol (DCR)']

for i in loop_data:
    fig.add_trace(
        go.Bar(x=x_data[i],y=y_data[i],name=name_data[i],opacity=0.5,marker_color=color_data[i],yaxis="y2"))
fig.update_layout(barmode='stack',bargap=0.01,yaxis2=dict(side="right",position=0.15))

fig.show()


"""
#############################################################################
                    DCR BTC BLOCK SUBSIDY MODELS
#############################################################################
"""
loop_data = [[0,1,2,3,4,6],[5]]
x_data = [
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    ]
y_data = [
    DCR_subs['PoW_income_btc'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['PoS_income_btc'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['Fund_income_btc'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['Total_income_btc'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['PriceBTC'],
    DCR_subs['dcr_tic_sply_avg'],
    DCR_subs['PriceBTC'].rolling(200).mean()
    ]
name_data = [
    'POW (BTC)','POS (BTC)','Treasury (BTC)','Total (BTC)',
    'DCR/BTC Price','Ticket Pool Value (DCR)','200DMA'
    ]
color_data = [
    'rgb(250, 38, 53)' ,'rgb(114, 49, 163)','rgb(255, 192, 0)',
    'rgb(20, 169, 233)','rgb(239, 125, 50)','rgb(156,225,143)',
    'rgb(0,176,80)']
dash_data = ['solid','solid','solid','solid','solid','solid','solid']
width_data = [2,2,2,2,2,2,1]
opacity_data = [1,1,1,1,1,1,1]
legend_data = [True,True,True,True,True,True,True]#
title_data = ['Decred Stakeholder Subsidy Models','Date','Network Valuation (BTC)','Total DCR in Tickets']
range_data = [['01-02-2016','01-02-2020'],[-4,-1],[0,1]]
autorange_data = [True,False,True]
type_data = ['date','log','linear']#
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
""" =================================
    ADD VOLUME BAR CHARTS
================================="""
x_data = [
    DCR_subs['date'],
    DCR_subs['date']
]
y_data = [
    DCR_subs['dcr_tic_vol'],
    DCR_subs['dcr_tfr_vol']
]
color_data = ['rgb(237,96,136)','rgb(37,187,217)']
loop_data = [0,1]
name_data = ['Ticket Vol (DCR)','Transfer Vol (DCR)']
for i in loop_data:
    fig.add_trace(
        go.Bar(x=x_data[i],y=y_data[i],name=name_data[i],marker_color=color_data[i]),secondary_y=True)
fig.update_layout(barmode='stack',bargap=0.01)
fig.show()
