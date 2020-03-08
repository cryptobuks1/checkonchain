#Calculate the dust limit and estimate future value
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.general.standard_charts import *
from checkonchain.general.regression_analysis import *

#Set Constants
blk_max = 210000*6  #max block height to calculate up to
dustlim_min = 172       #bytes
dustlim_avg = 222   #bytes (based on actual performance)
max_fee = 0.01      #Assume 1% of transaction cost is max viable fee
sats = 1e8          #sats per BTC

#Pull Coinmetrics data
BTC_coin = btc_add_metrics().btc_coin()
blk_cur = BTC_coin['blk'].max() #Current block
BTC_coin = BTC_coin.loc[:,[
    'date','blk',
    'CapMrktCurUSD',
    'PriceUSD','PriceRealised','SplyCur',
    'BlkCnt','BlkSizeByte','BlkSizeMeanByte',
    'FeeMeanNtv','FeeMeanUSD',
    'FeeMedNtv','FeeMedUSD',
    'FeeTotNtv','FeeTotUSD',
    'TxCnt','TxTfrCnt'
    ]]
#Add in segwit_adoption from blockchair csv
BTC_segwit = pd.read_csv(r'D:\code_development\checkonchain\checkonchain\btconchain\data\blockchair\segwit_adption.csv')
BTC_segwit.columns = ['date','segwit']
BTC_segwit['date'] = pd.to_datetime(BTC_segwit['date'],utc=True)
BTC_coin = pd.merge(BTC_coin,BTC_segwit,on='date',how='left')
#BTC_coin['segwit'].fillna(0,inplace=True)

#USD cost of a dust transaction
BTC_coin['DustPrice_min']=dustlim_min/sats * BTC_coin['PriceUSD']
BTC_coin['DustPrice_avg']=dustlim_avg/sats * BTC_coin['PriceUSD']
#Minimum viable USD transaction assuming max_fee rate
BTC_coin['MinViableTxUSD'] = BTC_coin['DustPrice_min'] / max_fee
BTC_coin['MinViableTxBTC'] = BTC_coin['MinViableTxUSD'] / BTC_coin['PriceUSD']
#Calculate the average bytes per Tx (TxCnt) and TxTfr (TxTfr)
#Note assume TxTfr is most representative as all fee paying Tx are useful
BTC_coin['TxCntSizeByte']=BTC_coin['BlkSizeByte']/BTC_coin['TxCnt']
BTC_coin['TxTfrSizeByte']=BTC_coin['BlkSizeByte']/BTC_coin['TxTfrCnt']
BTC_coin['DustSizeByte'] = dustlim_min #dust limit in bytes
#Calculate mean and median Fees paid priced in Sats/byte
#Mean Fee(BTC) * Sats = Mean Fee(sats) / Mean Bytes per Tx = Mean sats/byte
BTC_coin['FeeSatsByteMean']= BTC_coin['FeeMeanNtv'] * sats / BTC_coin['TxTfrSizeByte']
BTC_coin['FeeSatsByteMean'].fillna(0)
BTC_coin['FeeSatsByteMed']= BTC_coin['FeeMedNtv'] * sats / BTC_coin['TxTfrSizeByte']
BTC_coin['FeeSatsByteMed'].fillna(0)
#Calculate Max Transactions per block assuming 2MB blocks
BTC_coin['TPBlk_TxTfr_1MB'] =  1000000 / BTC_coin['TxTfrSizeByte']
BTC_coin['TPBlk_TxTfr_2MB'] =  2000000 / BTC_coin['TxTfrSizeByte']
#Calculate Actual transactions per block
BTC_coin['TPBlk_actual']    = BTC_coin['TxTfrCnt']/BTC_coin['BlkCnt']
#Calculate BLock Utilisation Rate (Avg block size / 1MB)
BTC_coin['BlkByteUtil_1MB'] = BTC_coin['BlkSizeMeanByte'] / 1e6
BTC_coin['BlkByteUtil_2MB'] = BTC_coin['BlkSizeMeanByte'] / 2e6


#Calculate Supply Function
BTC_sply = btc_add_metrics().btc_sply_curtailed(blk_max)
#Calculate dust price projected forwards
BTC_sply['DustPrice_min'] = dustlim_min/sats * BTC_sply['PricePlanBmodel']
BTC_sply['DustPrice_avg'] = dustlim_avg/sats * BTC_sply['PricePlanBmodel']
#Calculate USD Price per Transaction (assume sats per byte)
BTC_sply['S2F_1sats_byte'] = BTC_sply['PricePlanBmodel'] * dustlim_min / sats
BTC_sply['S2F_2sats_byte'] = BTC_sply['S2F_1sats_byte'] * 2
BTC_sply['S2F_10sats_byte'] = BTC_sply['S2F_1sats_byte'] * 10
BTC_sply['S2F_30sats_byte'] = BTC_sply['S2F_1sats_byte'] * 30
BTC_sply['S2F_100sats_byte'] = BTC_sply['S2F_1sats_byte'] * 100
BTC_sply['S2F_200sats_byte'] = BTC_sply['S2F_1sats_byte'] * 200


"""
#############################################################################
#############################################################################
#############################################################################
                    BITCOIN BLOCKSPACE CHARTS
#############################################################################
#############################################################################
#############################################################################
"""

"""
#############################################################################
                BYTES PER TX + FEE RATE (SATS/BYTE)
#############################################################################
"""

loop_data=[[0,1,2],[3,4,5,6]]
x_data = [
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin[BTC_coin['FeeSatsByteMean']>0.01]['blk'],
    BTC_coin[BTC_coin['FeeSatsByteMean']>0.01]['blk'],
    BTC_coin[BTC_coin['FeeSatsByteMed']>0.01]['blk'],
    BTC_coin[BTC_coin['FeeSatsByteMed']>0.01]['blk'],
    ]
y_data = [
    #Primary Transaction Size
    BTC_coin['TxTfrSizeByte'],
    BTC_coin['TxTfrSizeByte'].rolling(90).mean(),
    BTC_coin['DustSizeByte'],
    #Secondary Sats/byte
    BTC_coin[BTC_coin['FeeSatsByteMean']>0.01]['FeeSatsByteMean'], #Cull all values < 1
    BTC_coin[BTC_coin['FeeSatsByteMean']>0.01]['FeeSatsByteMean'].rolling(90).mean(), 
    BTC_coin[BTC_coin['FeeSatsByteMed']>0.01]['FeeSatsByteMed'], #Cull all values < 1
    BTC_coin[BTC_coin['FeeSatsByteMed']>0.01]['FeeSatsByteMed'].rolling(90).mean(),
]
name_data = [
    'Bytes per TxTfr',
    'Bytes per TxTfr (90 DMA)',
    'Assumed Dust Limit (176bytes)',
    'Mean Sats/byte',
    'Mean Sats/byte',
    'Median Sats/byte',
    'Median Sats/byte',
]
width_data      = [
    1,3,3,
    1,3,1,3
    ]
opacity_data    = [
    0.5,1,1,
    0.5,1,0.5,1
    ]
dash_data = [
    'solid','dash','dash',
    'solid','dash','solid','dash',
]
color_data = [
    'rgb(254,215,140)',     #Matte Yellow
    'rgb(254,215,140)',     #Matte Yellow
    'rgb(255, 80, 80)',     #Red
    'rgb(102, 204, 255)',   #L.Blue
    'rgb(102, 204, 255)',   #L.Blue
    'rgb(102, 255, 153)', #Turquoise Green
    'rgb(102, 255, 153)', #Turquoise Green
]
legend_data = [
    #False,True,
    False,True,True,
    False,True,False,True
    ]
title_data = [
    'Bitcoin Transaction Size and Fee Rate',
    '<b>Block Height</b>',
    '<b>Transaction Size (bytes)</b>',
    '<b>Fee Rate (sats/byte)</b>']
range_data = [[0,735000],[0,1000],[-1,4]]
autorange_data = [False,False,False]
type_data = ['linear','linear','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.update_xaxes(dtick=52500)
fig.update_yaxes(secondary_y=False,color='rgb(254,215,140)',showgrid=True)  #Primary Yellow
fig.update_yaxes(secondary_y=True,color='rgb(102, 204, 255)') #Secondary L.Blue
fig.show()



"""
#############################################################################
                    TRANSACTIONS PER BLOCK (ACTUAL + THEORETICAL)
#############################################################################
"""
loop_data=[[0,1,2,3,4,5],[]]
x_data = [
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    ]
y_data = [
    #Maximum Tx/Blk
    BTC_coin['TPBlk_TxTfr_1MB'],
    BTC_coin['TPBlk_TxTfr_1MB'].rolling(90).mean(),
    BTC_coin['TPBlk_TxTfr_2MB'],
    BTC_coin['TPBlk_TxTfr_2MB'].rolling(90).mean(),
    #Segwit Adoption
    BTC_coin['TPBlk_actual'],
    BTC_coin['TPBlk_actual'].rolling(90).mean(),
]
name_data = [
    'Max Tx per 1MB Block',
    'Max Tx per 1MB Block',
    'Max Tx per 2MB Block',
    'Max Tx per 2MB Block',
    'Actual Tx per Block',
    'Actual Tx per Block',
]
width_data      = [
    1,3,
    1,3,
    1,3
    ]
opacity_data    = [
    0.5,1,
    0.5,1,
    0.5,1
    ]
dash_data = [
    'dot','dash',
    'dot','dash',
    'dot','dash',
]
color_data = [
    'rgb(254,215,140)',     #Matte Yellow
    'rgb(254,215,140)',     #Matte Yellow
    'rgb(255, 102, 0)' ,    #Burnt Orange
    'rgb(255, 102, 0)' ,    #Burnt Orange
    'rgb(102, 255, 153)',   #Turquoise Green
    'rgb(102, 255, 153)',   #Turquoise Green
]
legend_data = [
    False,True,
    False,True,
    False,True
    ]
title_data = [
    'Bitcoin Transaction Throughput',
    '<b>Block Height</b>',
    '<b>Transactions per Block</b>',
    '<b></b>']
type_data = ['linear','linear','linear']
range_data = [[0,735000],[0,15000],[0,1.5]]
autorange_data = [False,False,False]
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.update_xaxes(dtick=52500)
fig.update_yaxes(secondary_y=False,dtick=1000)
#fig.update_yaxes(secondary_y=True,tickformat='.0%',dtick=0.1)
fig.show()


"""
#############################################################################
                    BLOCKSPACE UTILISATION + SEGWIT ADOPTION
#############################################################################
"""
loop_data=[[0,1,2,3,4,5,6],[]]
x_data = [
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    [0,1e6],
    BTC_coin['blk'],
    BTC_coin['blk'],
    ]
y_data = [
    #Blockspace Utilisation
    BTC_coin['BlkByteUtil_1MB'],
    BTC_coin['BlkByteUtil_1MB'].rolling(90).mean(),
    BTC_coin['BlkByteUtil_2MB'],
    BTC_coin['BlkByteUtil_2MB'].rolling(90).mean(),
    #Segwit Adoption
    [1,1],
    BTC_coin['segwit'],
    BTC_coin['segwit'].rolling(7).mean(),
]
name_data = [
    'Blockspace Utilisation (1MB)',
    'Blockspace Utilisation (1MB)',
    'Blockspace Utilisation (2MB)',
    'Blockspace Utilisation (2MB)',
    '100%',
    'Segwit Adoption',
    'Segwit Adoption',
]
width_data      = [
    1,3,1,3,
    2,1,2
    ]
opacity_data    = [
    0.5,1,0.5,1,
    0.5,0.5,1
    ]
dash_data = [
    'dot','dash','dot','dash',
    'dash','dot','dash',
]
color_data = [
    'rgb(254,215,140)',     #Matte Yellow
    'rgb(254,215,140)',     #Matte Yellow
    'rgb(255, 102, 0)' ,    #Burnt Orange
    'rgb(255, 102, 0)' ,    #Burnt Orange
    'rgb(255, 80, 80)',     #Red
    'rgb(102, 255, 153)',    #Turquoise Green
    'rgb(102, 255, 153)',   #Turquoise Green
]
legend_data = [
    False,True,False,True,
    False,False,True
    ]
title_data = [
    'Bitcoin Blockspace Utilisation',
    '<b>Block Height</b>',
    '<b>Blockspace Utilisation</b>',
    '<b>Segwit Adoption</b>']
type_data = ['linear','linear','linear']
range_data = [[0,735000],[0,1.5],[0,1.5]]
autorange_data = [False,False,False]
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.update_xaxes(dtick=52500)
fig.update_yaxes(secondary_y=False,tickformat='.0%',dtick=0.1)
#fig.update_yaxes(secondary_y=True,tickformat='.0%',dtick=0.1)
fig.show()



"""
#############################################################################
#############################################################################
#############################################################################
                    BITCOIN TOTAL FEE MARKET CHARTS
#############################################################################
#############################################################################
#############################################################################
"""


"""
#############################################################################
                FEE RATE (SATS/BYTE)
#############################################################################
"""

loop_data=[[0],[1,2,3,4]]
x_data = [
    BTC_coin['blk'],
    BTC_coin[BTC_coin['FeeSatsByteMean']>0]['blk'],
    BTC_coin[BTC_coin['FeeSatsByteMean']>0]['blk'],
    BTC_coin[BTC_coin['FeeSatsByteMed']>0]['blk'],
    BTC_coin[BTC_coin['FeeSatsByteMed']>0]['blk'],
    ]
y_data = [
    #Primary Transaction Size
    BTC_coin['PriceUSD'],
    #Secondary Sats/byte
    BTC_coin[BTC_coin['FeeSatsByteMean']>0]['FeeSatsByteMean'], #Cull all values < 1
    BTC_coin[BTC_coin['FeeSatsByteMean']>0]['FeeSatsByteMean'].rolling(28).mean(), 
    BTC_coin[BTC_coin['FeeSatsByteMed']>0]['FeeSatsByteMed'], #Cull all values < 1
    BTC_coin[BTC_coin['FeeSatsByteMed']>0]['FeeSatsByteMed'].rolling(28).mean(),
]
name_data = [
    'BTC Price',
    'Mean Sats/byte',
    'Mean Sats/byte',
    'Median Sats/byte',
    'Median Sats/byte',
]
width_data      = [
    1,
    1,3,1,3
    ]
opacity_data    = [
    1,
    0.5,1,0.5,1
    ]
dash_data = [
    'solid',
    'solid','dash','solid','dash',
]
color_data = [
    'rgb(255,255,255)',     #White
    'rgb(255, 102, 0)' ,    #Burnt Orange
    'rgb(255, 102, 0)' ,    #Burnt Orange
    'rgb(254,215,140)',     #Matte Yellow
    'rgb(254,215,140)',     #Matte Yellow
]
legend_data = [
    #False,True,
    True,
    False,True,False,True
]
title_data = [
    'Bitcoin Transaction Size and Fee Rate',
    '<b>Block Height</b>',
    '<b>BTC Price</b>',
    '<b>Average Fee Rate (sats/byte)</b>',
]
range_data = [[0,735000],[-1,5],[-1,4]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.update_xaxes(dtick=52500)
fig.update_yaxes(secondary_y=False,showgrid=False)  #Primary Yellow
fig.update_yaxes(secondary_y=True,color='rgb(254,215,140)',showgrid=True) #Secondary L.Blue
fig.show()






"""
#############################################################################
#############################################################################
#############################################################################
                    BITCOIN FORWARD PROJECTIONS
#############################################################################
#############################################################################
#############################################################################
"""

"""
#############################################################################
                    BTC FEE PRICES USD
#############################################################################
Shows the growth of retail user fees assuming Plan B S2F model
"""

loop_data=[[0,1,2,3,4,5,6,7,8],[9]]
x_data = [
    BTC_sply['blk'],BTC_sply['blk'],BTC_sply['blk'],
    BTC_sply['blk'],BTC_sply['blk'],BTC_sply['blk'],
    BTC_coin['blk'],BTC_coin['blk'],BTC_coin['blk'],
    BTC_coin['blk']
    ]
y_data = [
    BTC_sply['S2F_1sats_byte'],
    BTC_sply['S2F_2sats_byte'],
    BTC_sply['S2F_10sats_byte'],
    BTC_sply['S2F_30sats_byte'],
    BTC_sply['S2F_100sats_byte'],
    BTC_sply['S2F_200sats_byte'],
    BTC_coin['DustPrice_min'],
    BTC_coin['FeeMeanUSD'],
    BTC_coin['FeeMedUSD'],
    BTC_coin['PriceUSD']
]
name_data = [
    'S2F 1sats/byte',
    'S2F 2sats/byte',
    'S2F 10sats/byte',
    'S2F 30sats/byte',
    'S2F 100sats/byte',
    'S2F 200sats/byte',
    'Actual Dust Value',
    'Actual Mean Fee',
    'Actual Median Fee',
    'BTC/USD Price'
]
width_data = [
    1,1,1,
    1,1,1,
    1,1,1,
    2
]
opacity_data = [1,1,1,1,1,1,1,1,1,1]
dash_data = [
    'dash','dash','dash',
    'dash','dash','dash',
    'solid','solid','solid',
    'solid'
]
color_data = [
    'rgb(153, 255, 102)', #Gradient Green
    'rgb(255, 255, 102)', #Gradient Lime
    'rgb(255, 204, 102)', #Gradient Yellow
    'rgb(255, 153, 102)', #Gradient Orange
    'rgb(255, 102, 102)', #Gradient L.Red
    'rgb(255, 80, 80)',   #Gradient Red
    'rgb(255, 255, 255)', #White
    'rgb(102, 255, 153)', #Turquoise Green
    'rgb(102, 204, 255)', #L.Blue
    'rgb(255, 102, 0)'    #Burnt Orange
]
legend_data = [True,True,True,True,True,True,True,True,True,True]
title_data = [
    'Bitcoin Dust Pricing Bands (Assuming 172 byte Size)',
    '<b>Block Height</b>',
    '<b>Fee Value (USD)</b>',
    '<b>BTC/USD Price</b>']
type_data = ['linear','log','log']
range_data = [[70000,blk_max],[-6,4],[-2,8]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.update_yaxes(tickformat = '$0:.2f',secondary_y=False,)
fig.update_yaxes(tickformat = '$0:.2f',secondary_y=True,color='rgb(255, 102, 0)')
fig.show()





"""
#############################################################################
                    Minimum Viable Tx SIze
#############################################################################
Shows the minimum viable transaction value assuming 1% Fee
"""

for i in [0.001,0.0025,0.005,0.0075,0.010]:
    name = 'MinViableTxUSD_' + str(i*100)
    print(name)
    BTC_sply[name] = BTC_sply['DustPrice_min'] / i

loop_data=[[0,1,2,3,4],[]]
x_data = [
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    ]
y_data = [
    BTC_coin['MinViableTxUSD_0.1'],
    BTC_coin['MinViableTxUSD_0.25'],
    BTC_coin['MinViableTxUSD_0.5'],
    BTC_coin['MinViableTxUSD_0.75'],
    BTC_coin['MinViableTxUSD_1.0'],
]
name_data = [
    '0.10%',
    '0.25%',
    '0.50%',
    '0.75%',
    '1.00%'
]
width_data   = [
    2,2,2,2,2,
    ]
opacity_data = [
    1,1,1,1,1
    ]
dash_data = [
    'dot','dot','dot','dot','dot','dot',
]
color_data = [
    'rgb(153, 255, 102)', #Gradient Green
    'rgb(255, 255, 102)', #Gradient Lime
    'rgb(255, 204, 102)', #Gradient Yellow
    'rgb(255, 153, 102)', #Gradient Orange
    'rgb(255, 102, 102)', #Gradient L.Red
    'rgb(255, 80, 80)',   #Gradient Red
]
legend_data = [
    True,True,True,True,True,True,
    ]
title_data = [
    'Minimum Viable Transaction Value',
    '<b>Block Height</b>',
    '<b>Minimum USD Size</b>',
    '<b>Minimum BTC Size</b>']
type_data = ['linear','log','log']
range_data = [[0,630000],[1,7],[0,3]]
autorange_data = [False,True,True]
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()


















"""
#############################################################################
                    LINEAR REGRESSION - TxTfr vs MC
#############################################################################
"""
#Performan Linear Regression between x-Market Cap and y-TxTfr
# Intention is to estimate growth of transaction base vs Market Value
#Concept of Veblen good, more value = more demand
BTC_regr = BTC_coin[['CapMrktCurUSD','TxTfrCnt','blk']]
#Fill MCap forwards from early pricing data and then eliminate zeros (log-log regression)
BTC_regr['CapMrktCurUSD'] = BTC_coin['CapMrktCurUSD'].fillna(method='ffill')
BTC_regr['CapMrktCurUSD'] = BTC_regr['CapMrktCurUSD'].fillna(value=0)
BTC_regr = BTC_regr[BTC_regr['CapMrktCurUSD']>0]
BTC_regr = BTC_regr[BTC_regr['TxTfrCnt']>0]
#Run Regression Model and extract parameters
model = regression_analysis().ln_regression(BTC_regr,'CapMrktCurUSD','TxTfrCnt','blk')
intercept = float(model['model_params']['intercept'])
coefficient = float(model['model_params']['coefficient'])
#Apply regression model assuming Plan Bs MCap S2f model
BTC_sply_fwd = BTC_sply#[BTC_sply['blk']>blk_cur]
BTC_sply_fwd = BTC_sply_fwd[['blk','Sply_ideal','PricePlanBmodel','CapPlanBmodel']]
BTC_sply_fwd['TxTfrCnt'] = np.exp(intercept + coefficient * np.log(BTC_sply_fwd['CapPlanBmodel']))


loop_data=[[0,1,],[]]
x_data = [
    BTC_coin['CapMrktCurUSD'],
    BTC_sply_fwd['CapPlanBmodel'],
    ]
y_data = [
    BTC_coin['TxTfrCnt'],
    BTC_sply_fwd['TxTfrCnt'],

]
name_data = [
    'Actual M.Cap vs TxTfrCnt',
    'Power Law M.Cap vs TxTfrCnt',
]
width_data      = [
    3,3,
    ]
opacity_data    = [
    1,1
    ]
dash_data = [
    'solid','dash',
]
color_data = [
    'rgb(102, 255, 153)',   #Turquoise Green
    'rgb(255, 255, 255)' ,    #White
]
legend_data = [
    True,True,False,True,True,
    True,True
    ]
title_data = [
    'A Veblen Good? - Market Cap to Transaction Demand (log-log)',
    '<b>ln(Market Cap)</b>',
    '<b>ln(Transaction Count)</b>',
    '<b>Sats per byte</b>']
type_data = ['linear','log','log']
range_data = [[4,12],[1,7],[0,3]]
autorange_data = [False,False,True]
type_data = ['log','log','log']#
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()