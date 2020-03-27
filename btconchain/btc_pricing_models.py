# Plot Coin Pricing Models
#Data Science
import pandas as pd
import numpy as np
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

#Internal Modules
from checkonchain.btconchain.btc_add_metrics import *

# Plotly Libraries (+ force browser charts)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "browser"


BTC = btc_add_metrics().btc_oscillators()

asset = BTC
blk_max = int(asset['blk'][asset.index[-1]])

# Create Input Dataset for TOP PLOT
x_data_1 = [
    asset['blk'],asset['blk'],asset['blk'],
    asset['blk'],asset['blk'],asset['blk'],
    asset['blk'],asset['blk'],asset['blk'],
    asset['blk']
    ]

y_data_1 = [
    asset['PriceUSD'],asset['PriceRealUSD'],asset['PriceAvg'],
    asset['PriceDelta'],asset['PriceTop'],asset['PriceInflow'],
    asset['PriceS2Fmodel'],
    asset['TxTfrValAdjUSD'].rolling(28).mean()
]
#STAKER INFLOW!!!!!
names_1 = [
    'Price USD','Realised Price','Average Price',
    'Delta Price','Top Price','Price Miner Inflow',
    'Actual S2F Model',
    'TxTfrValAdjUSD'
]
line_size_1 = [
    2,2,1,
    1,1,1,
    1,
    1
]
dash_type_1 = [
    'solid','solid','dash',
    'dash','dash','dash',
    'dot',
    'solid'#,'dash'
]
opacity_1 = [
    1,1,0.75,
    0.75,0.75,0.75,
    0.75,
    1
]
color_data_1 = [
    'rgb(255, 255, 255)', 'rgb(102, 255, 153)', 'rgb(102, 204, 255)',
    'rgb(153, 255, 102)', 'rgb(255, 255, 102)', 'rgb(255, 204, 102)',
    'rgb(255, 153, 102)',
    'rgb(102, 255, 153)'
]


"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CREATE PLOT 01 (Bottom)
NVT/RVT OSCILLATORS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
#Create Plot against block height
# Y-axis 1 = NVT | RVT RATIO

# Create Input Dataset for TOP PLOT
x_data_2 = [
    asset['blk'],asset['blk'],asset['blk'],
    asset['blk'],asset['blk'],asset['blk']
    ]

y_data_2 = [
    asset['NVT_28'],asset['NVT_90'],asset['NVTS'],
    asset['RVT_28'],asset['RVT_90'],asset['RVTS']
]
#STAKER INFLOW!!!!!
names_2 = [
    'NVT 28D','NVT 90D','NVTS',
    'RVT 29D','RVT 90D','RVTS'
]
line_size_2 = [
    1,1,1,
    1,1,1
]
dash_type_2 = [
    'dot','dash','solid',
    'dot','dash','solid'
]
opacity_2 = [
    1,1,1,
    1,1,1
]
color_data_2 = [
    'rgb(153, 255, 102)', 'rgb(255, 255, 102)', 'rgb(255, 204, 102)',
    'rgb(255, 153, 102)', 'rgb(255, 102, 102)', 'rgb(255, 80, 80)'
]


fig = make_subplots(
    rows=2,cols=1,
    shared_xaxes=True, 
    vertical_spacing=0.05,
    row_heights=[0.7,0.3],
    specs=[[{"secondary_y": True}],[{}]]
    )
fig.update_layout(template="plotly_dark",title="Bitcoin Pricing Models")

"""Create Primary - Pricing Model Plots"""
for i in range(0,7):
    fig.add_trace(go.Scatter(
        mode='lines',
        x=x_data_1[i], 
        y=y_data_1[i],
        name=names_1[i],
        opacity=opacity_1[i],
        line=dict(
            width=line_size_1[i],
            color=color_data_1[i],
            dash=dash_type_1[i]
            )),
        secondary_y=False,
        row=1,col=1)

"""Create Secondary - Transaction Volume"""
#for i in range(7,8):
#    fig.add_trace(go.Scatter(
#        mode='lines',
#        x=x_data_1[i], 
#        y=y_data_1[i],
#        name=names_1[i],
#        opacity=opacity_1[i],
#        line=dict(
#            width=line_size_1[i],
#            color=color_data_1[i],
#            dash=dash_type_1[i]
#            )),
#        secondary_y=True,
#        row=1,col=1)

"""Create NVT Plots"""
for i in range(0,6):
    fig.add_trace(go.Scatter(
        mode='lines',
        x=x_data_2[i], 
        y=y_data_2[i],
        name=names_2[i],
        opacity=opacity_2[i],
        line=dict(
            width=line_size_2[i],
            color=color_data_2[i],
            dash=dash_type_2[i]
            )),
        secondary_y=False,
        row=2,col=1)

fig.update_xaxes(row=2,col=1)
fig.update_xaxes(
    row=2,col=1,
    title_text="<b>Block Height</b>",
    type="linear",
    range=[0,blk_max]
    )

"""Primary Axes PRICING"""
fig.update_yaxes(
    row=1,col=1,
    title_text="<b>BTC Price (USD)</b>",
    type="log",
    secondary_y=False,
    range=[-2,5]
    )

"""Secondary Axes TRANSACTION VOL"""
fig.update_yaxes(
    row=1,col=1,
    title_text="<b>On-chain Transaction Volume (USD)</b>",
    type="log",
    secondary_y=True,
    range=[5,12]
    )

"""Primary Axes NVT/RVT"""
fig.update_yaxes(
    row=2,col=1,
    title_text="<b>NVT | RVT Ratio</b>",
    type="linear",
    secondary_y=False,
    range=[0,40],
    dtick=10
    )
#fig.update_yaxes(
#    title_text="<b>BTCUSD Price</b>",
#    tickformat = '$0:.2f',
#    type="log",
#    secondary_y=True,
#    range=[-2,8],
#    color='rgb(102, 102, 153)'
#    )
fig.show()