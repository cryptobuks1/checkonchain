#Calculate the dust limit and estimate future value
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.general.standard_charts import *
from checkonchain.general.regression_analysis import *

#Set Constants
blk_max = 210000*6  #max block height to calculate up to
dustlim = 172       #bytes
max_fee = 0.01      #Assume 1% of transaction cost is max viable fee
sats = 1e8          #sats per BTC

#Pull Coinmetrics data
BTC_coin = btc_add_metrics().btc_coin()
blk_cur = BTC_coin['blk'].max() #Current block
BTC_coin = BTC_coin.loc[:,[
    'date','blk',
    'CapMrktCurUSD',
    'PriceUSD','PriceRealised','SplyCur',
    'BlkCnt','BlkSizeByte','BlkSizeMeanByte	',
    'FeeMeanNtv','FeeMeanUSD',
    'FeeMedNtv','FeeMedUSD',
    'FeeTotNtv','FeeTotUSD',
    'TxCnt','TxTfrCnt'
    ]]


#Calculate Actual Fee performance
#USD cost of a dust transaction
BTC_coin['DustPrice']=dustlim/sats * BTC_coin['PriceUSD']
#Minimum viable USD transaction assuming max_fee rate
BTC_coin['MinViableTxUSD'] = BTC_coin['DustPrice'] / max_fee
#Calculate the average bytes per Tx (TxCnt) and TxTfr (TxTfr)
#Note assume TxTfr is most representative as all fee paying Tx are useful
BTC_coin['TxCntSizeByte']=BTC_coin['BlkSizeByte']/BTC_coin['TxCnt']
BTC_coin['TxTfrSizeByte']=BTC_coin['BlkSizeByte']/BTC_coin['TxTfrCnt']
BTC_coin['DustSizeByte'] = dustlim #dust limit in bytes
#Calculate mean and median Fees paid priced in Sats/byte
#Mean Fee(BTC) * Sats = Mean Fee(sats) / Mean Bytes per Tx = Mean sats/byte
BTC_coin['FeeSatsByteMean']=BTC_coin['FeeMeanNtv'] * sats / BTC_coin['TxTfrSizeByte']
BTC_coin['FeeSatsByteMed']=BTC_coin['FeeMedNtv'] * sats / BTC_coin['TxTfrSizeByte']


#Calculate Supply Function
BTC_sply = btc_add_metrics().btc_sply_curtailed(blk_max)
#Calculate USD Price per Transaction (assume sats per byte)
BTC_sply['S2F_1sats_byte'] = BTC_sply['PricePlanBmodel'] * dustlim / sats
BTC_sply['S2F_2sats_byte'] = BTC_sply['S2F_1sats_byte'] * 2
BTC_sply['S2F_10sats_byte'] = BTC_sply['S2F_1sats_byte'] * 10
BTC_sply['S2F_30sats_byte'] = BTC_sply['S2F_1sats_byte'] * 30
BTC_sply['S2F_100sats_byte'] = BTC_sply['S2F_1sats_byte'] * 100
BTC_sply['S2F_200sats_byte'] = BTC_sply['S2F_1sats_byte'] * 200


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
    BTC_coin['DustPrice'],
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
    'Bitcoin Dust Limits (Assuming 172 byte Size)',
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




BTC_sply['CapPlanBmodel'].where(BTC_sply['CapPlanBmodel'] <= maxVal, maxVal)




"""
#############################################################################
                    BYTES PER TX AND SATS/BYTE
#############################################################################
"""
loop_data=[[0,1,2,3,4],[5,6]]
x_data = [
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    ]
y_data = [
    BTC_coin['TxCntSizeByte'],
    BTC_coin['TxCntSizeByte'].rolling(90).mean(),
    BTC_coin['TxTfrSizeByte'],
    BTC_coin['TxTfrSizeByte'].rolling(90).mean(),
    BTC_coin['DustSizeByte'],
    BTC_coin['FeeSatsByteMean'].rolling(14).mean(),
    BTC_coin['FeeSatsByteMed'].rolling(14).mean(),
]
name_data = [
    'Bytes per TxCnt',
    'Bytes per TxCnt (90 DMA)',
    'Bytes per TxTfr',
    'Bytes per TxTfr (90 DMA)',
    'Dust Limit',
    'Mean Sats/byte',
    'Median Sats/byte',
]
width_data      = [
    1,3,1,3,3,
    1,1
    ]
opacity_data    = [
    0.5,1,0.5,1,1,
    0.5,0.5
    ]
dash_data = [
    'solid','dash','solid','dash','dash',
    'solid','solid',
]
color_data = [
    'rgb(102, 255, 153)',   #Turquoise Green
    'rgb(1, 255, 116)',     #Green
    'rgb(102, 204, 255)',   #L.Blue
    'rgb(20, 169, 233)',       #D.Blue
    'rgb(255, 80, 80)',      #White
    'rgb(254, 215, 140)',   #Matte Yellow
    'rgb(255, 102, 0)' ,    #Burnt Orange
]
legend_data = [
    False,True,False,True,True,
    True,True
    ]
title_data = [
    'Bitcoin Transaction Byte Size',
    '<b>Block Height</b>',
    '<b>Transaction Size (bytes)</b>',
    '<b>Sats per byte</b>']
type_data = ['linear','log','log']
range_data = [[0,650000],[-6,4],[0,3]]
autorange_data = [False,True,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
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
    'Theoretical M.Cap vs TxTfrCnt',
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
    'rgb(255, 102, 0)' ,    #Burnt Orange
    'rgb(1, 255, 116)',     #Green
    'rgb(102, 204, 255)',   #L.Blue
    'rgb(20, 169, 233)',     #D.Blue
    'rgb(255, 80, 80)',      #White
    'rgb(254, 215, 140)',
    'rgb(255, 102, 0)' ,
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