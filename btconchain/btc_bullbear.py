#Analyse Bitcoin Market Behaviour through Bull Bear cycles
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.general.standard_charts import *
from checkonchain.general.regression_analysis import *

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
BTC_coin['200DMA'] = BTC_coin['PriceUSD'].rolling(200).mean()
BTC_coin['50DMA'] = BTC_coin['PriceUSD'].rolling(50).mean()
BTC_coin['MrktChar'] = str('-')
BTC_coin['MrktCode'] = 1
BTC_coin['PriceUSD_bull'] = BTC_coin['PriceUSD_bear'] = np.nan


bull = 1
bear = 0
last = 1 #1 for bull, 0 for bear
for index, row in BTC_coin.iterrows():
    if row['50DMA'] > row['200DMA']: #BULL MARKET
        if last == 0: #If switch from bear to bull
            bull = bull + 1
        last = 1 #switch to bull
        BTC_coin.loc[index,'MrktChar'] = 'Bull_' + str(bull)
        BTC_coin.loc[index,'PriceUSD_bull'] = BTC_coin.loc[index,'PriceUSD']
    else: #BEAR MARKET
        if last == 1:#if switch from bull to bear
            bear = bear + 1
        last = 0
        BTC_coin.loc[index,'MrktChar'] = 'Bear_' + str(bear)
        BTC_coin.loc[index,'PriceUSD_bear'] = BTC_coin.loc[index,'PriceUSD']
    BTC_coin.loc[index,'MrktCode'] = last
    
    


sats = 1e8
BTC_coin['TxCntSizeByte']=BTC_coin['BlkSizeByte']/BTC_coin['TxCnt']
BTC_coin['TxTfrSizeByte']=BTC_coin['BlkSizeByte']/BTC_coin['TxTfrCnt']
BTC_coin['FeeSatsByteMean']= BTC_coin['FeeMeanNtv'] * sats / BTC_coin['TxTfrSizeByte']
BTC_coin['FeeSatsByteMean'].fillna(0)
BTC_coin['FeeSatsByteMed']= BTC_coin['FeeMedNtv'] * sats / BTC_coin['TxTfrSizeByte']
BTC_coin['FeeSatsByteMed'].fillna(0)
#Calculate and Print Fees paid through each market cycle
j = 0
for i in [129470,166253,273109,382090,499687,572941,582610,blk_cur]:
    if j == 0:
        txt = 'FeeTotNtv blk 0 to ' + str(i/1000) + 'k = '
        val = math.floor(float(
            BTC_coin[(BTC_coin['blk'] >= 0) 
            & (BTC_coin['blk'] <= i)]['FeeTotUSD'].cumsum().tail(1))) / (i - j)
        sat_byte = math.floor(float(
            BTC_coin[(BTC_coin['blk'] >= 0) 
            & (BTC_coin['blk'] <= i)]['FeeSatsByteMed'].mean()))

    else:
        txt = 'FeeTotNtv blk ' + str(j/1000) +' to ' + str(i/1000) + 'k = '
        val = math.floor(float(
            BTC_coin[(BTC_coin['blk'] >= j) 
            & (BTC_coin['blk'] <= i)]['FeeTotUSD'].cumsum().tail(1))) / (i - j)
        sat_byte = math.floor(float(
            BTC_coin[(BTC_coin['blk'] >= j) 
            & (BTC_coin['blk'] <= i)]['FeeSatsByteMed'].mean()))
    
    val = math.floor(val*10000)/10000
    print(
        txt + str(val) 
        + ' BTC with average fee paid of ' 
        + str(math.floor(sat_byte)) 
        + 'sats/byte')
    j = i





"""
#############################################################################
                Price, 50, 200 (Bull / Bear)
#############################################################################
"""

loop_data=[[0,1,2,3],[]]
x_data = [
    BTC_coin['blk'],BTC_coin['blk'],
    #BTC_coin[BTC_coin['MrktCode']==0]['blk'],
    #BTC_coin[BTC_coin['MrktCode']==1]['blk'],
    BTC_coin['blk'],
    BTC_coin['blk'],
    ]
y_data = [
    #Primary Transaction Size
    BTC_coin['PriceUSD_bear'],
    BTC_coin['PriceUSD_bull'],
    #BTC_coin[BTC_coin['MrktCode']==0]['PriceUSD'],
    #BTC_coin[BTC_coin['MrktCode']==1]['PriceUSD'],
    BTC_coin['200DMA'],
    BTC_coin['50DMA'],
]
name_data = [
    'PriceUSD (Bear)',
    'PriceUSD (Bull)',
    '200DMA',
    '50DMA',

]
width_data      = [
    2,2,2,2
    ]
opacity_data    = [
    1,1,1,1
    ]
dash_data = [
    'solid','solid','dash','dash',
]
color_data = [
    'rgb(255, 80, 80)',     #Red
    'rgb(102, 255, 153)', #Turquoise Green
    'rgb(254,215,140)',     #Matte Yellow
    'rgb(102, 204, 255)', #L.Blue

]
legend_data = [
    #False,True,
    True,True,True,True
    ]
title_data = [
    'Bitcoin Transaction Size and Fee Rate',
    '<b>Block Height</b>',
    '<b>PriceUSD</b>',
    '<b></b>']
range_data = [[0,735000],[-2,5],[-1,4]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.update_xaxes(dtick=52500)
fig.show()