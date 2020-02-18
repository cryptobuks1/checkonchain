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
DASH = Coinmetrics_api('dash',"2014-01-19",today).convert_to_pd().set_index('date',drop=False)
DCR = Coinmetrics_api('dcr',"2016-02-08",today).convert_to_pd().set_index('date',drop=False)
XMR = Coinmetrics_api('xmr',"2014-04-18",today).convert_to_pd().set_index('date',drop=False)
ZEC = Coinmetrics_api('zec',"2016-10-28",today).convert_to_pd().set_index('date',drop=False)
ETH = Coinmetrics_api('eth',"2015-07-30",today).convert_to_pd().set_index('date',drop=False)
XRP = Coinmetrics_api('xrp',"2013-01-01",today).convert_to_pd().set_index('date',drop=False)

print('Coinmetrics')
print(DCR.columns)

metric="CapMrktCurUSD"

DCR['dcr_btc']  = DCR[metric]/ BTC[metric]
DCR['dcr_ltc']  = DCR[metric]/ LTC[metric]
DCR['dcr_bch']  = DCR[metric]/ BCH[metric]
DCR['dcr_dash'] = DCR[metric]/DASH[metric]
DCR['dcr_xmr']  = DCR[metric]/ XMR[metric]
DCR['dcr_zec']  = DCR[metric]/ ZEC[metric]
DCR['dcr_eth']  = DCR[metric]/ ETH[metric]
DCR['dcr_xrp']  = DCR[metric]/ XRP[metric]
#DCR.tail(5)


x_data = [
    DCR['date'],DCR['date'],
    DCR['date'],DCR['date'],
    DCR['date'],DCR['date'],
    DCR['date'],DCR['date']
    ]
y_data = [
    DCR['dcr_btc'],DCR['dcr_ltc'],
    DCR['dcr_bch'],DCR['dcr_dash'],
    DCR['dcr_xmr'],DCR['dcr_zec'],
    DCR['dcr_eth'],DCR['dcr_xrp']
    ]
name_data = [
    'BTC','LTC',
    'BCH','DASH',
    'XMR','ZEC',
    'ETH','XRP'
]
width_data = [
    2,2,
    2,2,
    2,2,
    2,2
]
opacity_data = [
    1,1,
    1,1,
    1,1,
    1,1
]
color_data = [
    'rgb(255, 153, 0)','rgb(214, 214, 194)',
    'rgb(0, 153, 51)','rgb(51, 204, 255)',
    'rgb(255, 102, 0)','rgb(255, 255, 0)',
    'rgb(153, 51, 255)','rgb(51, 102, 255)'
]
dash_data = [
    'solid','solid',
    'solid','solid',
    'solid','solid',
    'solid','solid'
]



fig = make_subplots(specs=[[{"secondary_y": False}]])
for i in range(0,8):
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
fig.update_layout(title_text="Compare Value Metrics")
fig.update_xaxes(
    title_text="<b>Date</b>",
    range=['2016-01-01','2020-03-01']
    )
fig.update_yaxes(
    title_text="<b>DCR / Coin Market Cap</b>",
    type="log",
    secondary_y=False)
fig.update_layout(template="plotly_dark")
fig.show()
