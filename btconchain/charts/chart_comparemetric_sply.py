#Extract Market Cap and Compare Growth of DCR to top coins
import pandas as pd
import numpy as np
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

from checkonchain.general.coinmetrics_api import *

BTC = Coinmetrics_api('btc',"2009-01-03",today).convert_to_pd().set_index('date',drop=False)
LTC = Coinmetrics_api('ltc',"2011-10-07",today).convert_to_pd().set_index('date',drop=False)
BCH = Coinmetrics_api('bch',"2017-08-01",today).convert_to_pd().set_index('date',drop=False)
DAS = Coinmetrics_api('dash',"2014-01-19",today).convert_to_pd().set_index('date',drop=False)
DCR = Coinmetrics_api('dcr',"2016-02-08",today).convert_to_pd().set_index('date',drop=False)
XMR = Coinmetrics_api('xmr',"2014-04-18",today).convert_to_pd().set_index('date',drop=False)
ZEC = Coinmetrics_api('zec',"2016-10-28",today).convert_to_pd().set_index('date',drop=False)
ETH = Coinmetrics_api('eth',"2015-07-30",today).convert_to_pd().set_index('date',drop=False)
XRP = Coinmetrics_api('xrp',"2013-01-01",today).convert_to_pd().set_index('date',drop=False)

#Calculation
for i in [BTC,LTC,BCH,DAS,DCR,XMR,ZEC,ETH]:
    i['IssuedCapUSD']


metric="TxTfrValUSD"



x_data = [
    BTC['SplyCur']/21e6,
    LTC['SplyCur']/84e6,
    BCH['SplyCur']/21e6,
    DASH['SplyCur']/17.66e6,
    DCR['SplyCur']/21e6
    ]
y_data = [
    BTC[metric].rolling(14).mean(),LTC[metric].rolling(14).mean(),
    BCH[metric].rolling(14).mean(),DASH[metric].rolling(14).mean(),
    DCR[metric].rolling(14).mean()
    ]
name_data = [
    'BTC','LTC',
    'BCH','DASH',
    'DCR'
]
width_data = [
    2,2,
    2,2,
    2,2,
    2
]
opacity_data = [
    1,1,
    1,1,
    1,1,
    1
]
color_data = [
    'rgb(238,125,33)','rgb(255, 255, 0)',
    'rgb(0,176,80)','rgb(174,117,195)',
    'rgb(46, 214, 161)'
]
dash_data = [
    'solid','solid',
    'solid','solid',
    'solid','solid',
    'solid','solid'
]



fig = make_subplots(specs=[[{"secondary_y": False}]])
for i in range(0,5):
    fig.add_trace(go.Scatter(
        x=x_data[i], y=y_data[i],
        mode='lines',
        name=name_data[i],
        opacity=opacity_data[i],
        line=dict(
            width=width_data[i],
            color=color_data[i],
            dash=dash_data[i]
            )),
        secondary_y=False)



"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(title_text="Compare On-chain Volume vs Coin Age")
fig.update_xaxes(
    title_text="<b>Current Coin Supply / 2050 Supply</b>",
    range=[0,1]
    )
fig.update_yaxes(
    title_text="<b>On-chain Volume (USD)</b>",
    type="log",
    secondary_y=False)
fig.update_layout(template="plotly_dark")
fig.show()
