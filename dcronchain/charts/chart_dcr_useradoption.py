#Compare the Usage adoption metrics for Decred and Bitcoin
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.btconchain.btc_add_metrics import *


"""
GOVERNANCE, USER ADOPTION AND RESILIENCE:
Establish user adoption metrics for the Decred chain
Three parties involved

Miners
- PoW Growth over time
    - Plot Difficulty and Hashrate vs Coin-age
    - Plot Difficulty growth from 
"""

#Compile Input Dataframes
BTC_data = btc_add_metrics().btc_subsidy_models()
DCR_data = dcr_add_metrics().dcr_ticket_models()

#Calculate halving lines
BTC_half = btc_add_metrics().btc_sply_halvings_step()
#Cull to first 3 halvings and add nearest date column
BTC_half = pd.merge_asof(
    BTC_half[BTC_half.index<=6],
    BTC_data[['date','SplyCur']],
    left_on='end_sply',
    right_on='SplyCur'
    )
#Update 2020 Halving
BTC_half.loc[5:6,['date']] = pd.to_datetime(np.datetime64('2020-05-13'),utc=True)
#Add column for coin age in days
BTC_half['age_days'] = (
    pd.Series(delta.days for delta in (
        BTC_half['date'] 
        - pd.to_datetime(np.datetime64('2009-01-09'),utc=True)
    )
))



"""
#############################################################################
                    USER METRICS - ACTIVE ADDRESSES
#############################################################################
"""
#Adjust Active address by removing extra use of tickets (50% use 4x, 50% use 2x)
DCR_data['AdrActCntAdj'] = DCR_data['AdrActCnt'] - DCR_data['tic_day'].rolling(7).mean()*3

loop_data = [[0,1,2],[3,4,5]]
x_data = [
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_data['age_days'],DCR_data['age_days'],
    BTC_half['age_days'],    
    ]
y_data = [
    BTC_data['AdrActCnt'],DCR_data['AdrActCntAdj'].rolling(7).mean(),DCR_data['tic_day'].rolling(7).mean()*3,
    BTC_data['PriceUSD'],DCR_data['PriceUSD'],
    BTC_half['y_arb'],
    ]
name_data = [
    'BTC AdrActCnt','DCR AdrActCnt','3x Ticket Buys',
    'BTC Price','DCR Price',
    'Bitcoin Halvings'
    ]
color_data = [
    'rgb(254, 215, 140)','rgb(65, 191, 83)','rgb(112, 203, 255)',
    'rgb(255, 102, 0)' , 'rgb(46, 214, 161)',
    'rgb(255,255,255)'
    ]
dash_data = [
    'solid','solid','solid',
    'solid','solid',
    'dash',
    ]
width_data = [
    0.5,0.75,2,
    2,2,
    1,
    ]
opacity_data = [
    1,1,1,
    1,1,
    0.5
    ]
legend_data = [
    True,True,True,
    True,True,
    True,
    ]
title_data = [
    'Daily USD Value Secured and Settled',
    'Protocol Age (days)',
    'Active Address Count',
    'Price USD']
range_data = [[0,4500],[2,6.3],[-2,4.3]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()

"""
#############################################################################
                USER METRICS - DCRBTC ACTIVE ADDRESS RATIO (AGE_DAYS)
#############################################################################
"""

DCR_data = DCR_data.merge(BTC_data[['age_days','AdrActCnt','TxTfrCnt']],on='age_days',how='left',suffixes=('', '_BTC'))
#DCR_data.rename(columns={'AdrActCnt_y':'AdrActCnt_BTC'}, inplace=True)
DCR_data['DCRBTC_AdrActCnt'] = DCR_data['AdrActCnt'] / DCR_data['AdrActCnt_BTC']
DCR_data['DCRBTC_TxTfrCnt'] = DCR_data['TxTfrCnt'] / DCR_data['TxTfrCnt_BTC']


loop_data = [[1,2,3,0],[]]
x_data = [
    DCR_data['age_days'],
    [0,5000],[0,5000],[0,5000],
    BTC_half['age_days']
]
y_data = [
    DCR_data['DCRBTC_AdrActCnt'].rolling(7).mean(),
    [1,1],[0.5,0.5],[0.25,0.25],
    BTC_half['y_arb']
]
name_data = ['DCR/BTC Act.Adr Ratio','Equal, 100%','Half, 50%','Quarter, 25%','BTC Halvings']
color_data = ['rgb(255,255,255)','rgb(153, 255, 102)','rgb(255, 204, 102)','rgb(255, 80, 80)','rgb(255,255,255)']
width_data = [2,1,1,1,1]
opacity_data = [1,0.75,0.75,0.75,0.5]
dash_data = ['solid','dash','dash','dash','dash']
legend_data = [True,True,True,True,False]
title_data = ['','Protocol Age (days)','DCR/BTC Act.Adr Ratio','']                         
range_data = [[0,4500],[-1,3],[]]
type_data = ['linear','log']
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
#fig.update_xaxes(dtick=0.1)
fig.show()



"""
#############################################################################
                    USER METRICS - TRANSACTION COUNTS
#############################################################################
"""

loop_data = [[0,1,2],[3,4,5,6]]
x_data = [
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_half['age_days'],    
    ]
y_data = [
    BTC_data['TxTfrCnt'].rolling(1).mean(),
    DCR_data['TxTfrCnt'].rolling(3).mean(),
    DCR_data['tic_day'].rolling(3).mean()*3,
    BTC_data['TxTfrCnt'].cumsum(),
    DCR_data['TxTfrCnt'].cumsum(),
    DCR_data['tic_day'].cumsum()*3,
    BTC_half['y_arb'],
    ]
name_data = [
    'BTC TxTfrCnt','DCR TxTfrCnt','DCR Ticket Baseline',
    'BTC Cumulative TxTfr','DCR Cumulative TxTfr','DCR Cumulative Tickets',
    'Bitcoin Halvings'
    ]
color_data = [
    'rgb(254, 215, 140)', 'rgb(65, 191, 83)','rgb(112, 203, 255)',
    'rgb(255, 102, 0)' , 'rgb(65, 191, 83)','rgb(112, 203, 255)',
    'rgb(255,255,255)'
    ]
dash_data = [
    'solid','solid','solid',
    'dot','dot','dot',
    'dash',
    ]
width_data = [
    1,1,1,
    4,4,4,
    1,
    ]
opacity_data = [
    1,1,1,
    1,1,1,
    0.5
    ]
legend_data = [
    True,True,True,
    True,True,True,
    True,
    ]
title_data = [
    'Transaction Counts',
    'Protocol Age (days)',
    'Daily Transaction Counts',
    'Cumulative Transaction Count']
range_data = [[0,4500],[0,6.2],[2,9.2]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()






"""
#############################################################################
            USER METRICS - GLOBAL NATIVE UNITS TRANSFERRED
#############################################################################
"""


DCR_data['dcr_tic_buy'] = DCR_data['tic_day']*DCR_data['tic_price_avg']

loop_data = [[0,1,2],[3,4,5,6]]
x_data = [
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_half['age_days'],    
    ]
y_data = [
    BTC_data['TxTfrValNtv'].rolling(7).mean(),
    DCR_data['TxTfrValNtv'].rolling(7).mean(),
    DCR_data['dcr_tic_buy'].rolling(7).mean(),
    BTC_data['TxTfrValNtv'].cumsum(),
    DCR_data['TxTfrValNtv'].cumsum(),
    DCR_data['dcr_tic_buy'].cumsum(),
    BTC_half['y_arb'],
    ]
name_data = [
    'BTC TxTfrValNtv','DCR TxTfrValNtv','DCR Ticket Buys',
    'BTC Cum. TxTfrValNtv','DCR Cum TxTfrValNtv','Cum. DCR in Tics',
    'Bitcoin Halvings'
    ]
color_data = [
    'rgb(254, 215, 140)', 'rgb(65, 191, 83)','rgb(112, 203, 255)',
    'rgb(255, 102, 0)' , 'rgb(65, 191, 83)','rgb(112, 203, 255)',
    'rgb(255,255,255)'
    ]
dash_data = [
    'solid','solid','solid',
    'dot','dot','dot',
    'dash',
    ]
width_data = [
    1,1,1,
    5,5,5,
    1,
    ]
opacity_data = [
    1,1,1,
    1,1,1,
    0.5
    ]
legend_data = [
    True,True,True,
    True,True,True,
    True,
    ]
title_data = [
    'Native Units Transferred On-chain',
    'Protocol Age (days)',
    'Daily Native Units Transferred',
    'Cumulative Native Units Transferred']
range_data = [[0,4500],[2,8],[2,12]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()




"""
#############################################################################
            USER METRICS - CUMULATIVE VALUE TRANSFERRED
#############################################################################
"""

loop_data = [[0,1,2,3,4,5],[7,8,6]]
x_data = [
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_half['age_days'],
    BTC_data['age_days'],DCR_data['age_days']    
    ]
y_data = [
    BTC_data['TxTfrValNtv'].cumsum(),
    DCR_data['TxTfrValNtv'].cumsum(),
    DCR_data['dcr_tic_buy'].cumsum(),
    BTC_data['TxTfrValUSD'].cumsum(),
    DCR_data['TxTfrValUSD'].cumsum(),
    DCR_data['tic_usd_cost'].cumsum(),
    BTC_half['y_arb'],
    BTC_data['PriceUSD'],DCR_data['PriceUSD']
    ]
name_data = [
    'BTC Settled','DCR Settled','DCR Settled in Tickets',
    'Bitcoin Settled USD','Decred Settled USD','Decred USD in Tickets',
    'Bitcoin Halvings',
    'Bitcoin Price','Decred Price'
    ]
color_data = [
    'rgb(255, 102, 0)' , 'rgb(65, 191, 83)','rgb(112, 203, 255)',
    'rgb(255, 102, 0)' , 'rgb(65, 191, 83)','rgb(112, 203, 255)',
    'rgb(255,255,255)',
    'rgb(255,255,255)','rgb(46, 214, 161)'
    ]
dash_data = [
    'dash','dash','dash',
    'solid','solid','solid',
    'dash',
    'solid','solid'
    ]
width_data = [
    3,3,3,
    3,3,3,
    1,
    1,1
    ]
opacity_data = [
    1,1,1,
    1,1,1,
    0.5,
    1,1
    ]
legend_data = [
    True,True,True,
    True,True,True,
    True,
    True,True,
    ]
title_data = [
    'Cumulative Value Settled On-chain',
    'Protocol Age (days)',
    'Value Settled (USD, BTC, DCR)',
    'Coin Price']
range_data = [[0,4500],[3,13],[-2,6]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()



"""
#############################################################################
            USER METRICS - DAILY VALUE TRANSFERRED
#############################################################################
"""

loop_data = [[0,1,2,3,4,5],[7,8,6]]
x_data = [
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_half['age_days'],
    BTC_data['age_days'],DCR_data['age_days']    
    ]
y_data = [
    BTC_data['TxTfrValNtv'].rolling(7).mean(),
    DCR_data['TxTfrValNtv'].rolling(7).mean(),
    DCR_data['dcr_tic_buy'].rolling(7).mean(),
    BTC_data['TxTfrValUSD'].rolling(7).mean(),
    DCR_data['TxTfrValUSD'].rolling(7).mean(),
    DCR_data['tic_usd_cost'].rolling(7).mean(),
    BTC_half['y_arb'],
    BTC_data['PriceUSD'],DCR_data['PriceUSD']
    ]
name_data = [
    'BTC Settled','DCR Settled','DCR Settled in Tickets',
    'Bitcoin Settled USD','Decred Settled USD','Decred USD in Tickets',
    'Bitcoin Halvings',
    'Bitcoin Price','Decred Price'
    ]
color_data = [
    'rgb(255, 102, 0)' , 'rgb(65, 191, 83)','rgb(112, 203, 255)',
    'rgb(255, 102, 0)' , 'rgb(65, 191, 83)','rgb(112, 203, 255)',
    'rgb(255,255,255)',
    'rgb(255,255,255)','rgb(46, 214, 161)'
    ]
dash_data = [
    'solid','solid','solid',
    'solid','solid','solid',
    'dash',
    'solid','solid'
    ]
width_data = [
    1,1,1,
    1,1,1,
    1,
    1,1
    ]
opacity_data = [
    1,1,1,
    1,1,1,
    0.5,
    1,1
    ]
legend_data = [
    True,True,True,
    True,True,True,
    True,
    True,True,
    ]
title_data = [
    'Daily Value Settled On-chain',
    'Protocol Age (days)',
    'Value Settled (USD, BTC, DCR)',
    'Coin Price']
range_data = [[0,4500],[3,13],[-2,6]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()



"""
#############################################################################
            USER METRICS - LOCAL TRANSACTION FLOWS
#############################################################################
"""

loop_data = [[0,1,2,3,4],[5,6,7]]
x_data = [
    #Transaction Volume
    BTC_data['age_days'],
    BTC_data['age_days'],
    DCR_data['age_days'],
    DCR_data['age_days'],
    DCR_data['age_days'],
    #Address Density
    BTC_data['age_days'],
    DCR_data['age_days'],
    BTC_half['age_days'],
    ]
y_data = [
    BTC_data['TxTfrValMedNtv'].rolling(2).mean(),
    BTC_data['TxTfrValMeanNtv'],
    DCR_data['TxTfrValMedNtv'].rolling(2).mean(),
    DCR_data['TxTfrValMeanNtv'],
    DCR_data['tic_price_avg'],
    #Address Density
    BTC_data['PriceUSD'],
    DCR_data['PriceUSD'],
    BTC_half['y_arb']
    ]
name_data = [
    'BTC Median Tx',
    'BTC Mean Tx',
    'DCR Median Tx',
    'DCR Mean Tx',
    'DCR Ticket Price',
    'BTC Price',
    'DCR Price',
    'Bitcoin Halvings',

    ]
color_data = [
    'rgb(254, 150, 70)',
    'rgb(255, 102, 0)',
    'rgb(112, 203, 255)',
    'rgb(47, 116, 251)',#'rgb(65, 191, 83)',
    'rgb(255,255,255)',
    'rgb(255, 255, 255)',
    'rgb(46, 214, 161)',
    'rgb(255,255,255)'
    ]
dash_data = [
    'solid','solid',
    'solid','solid','solid',
    'dot','dot',
    'dash',
    ]
width_data = [
    1,1,
    2,2,2,
    1,1,
    1,
    ]
opacity_data = [
    1,1,
    1,1,1,
    0.6,0.6,
    0.5
    ]
legend_data = [
    True,True,
    True,True,True,
    True,True,
    True,
    ]
title_data = [
    'Native Units Transferred On-chain',
    'Protocol Age (days)',
    'Daily Native Units Transferred',
    'Coin Price USD']
range_data = [[0,4500],[-5,5],[-2,6]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()



#Address Density
BTC_data['AdrDens'] = BTC_data['TxTfrValAdjNtv']/BTC_data['AdrActCnt']
DCR_data['AdrDens'] = (
    DCR_data['TxTfrValNtv'] 
    - DCR_data['tic_day'].rolling(7).mean()*3
    )/DCR_data['AdrActCnt']


loop_data = [[5,6],[]]
title_data = [
    'Address Density',
    'Protocol Age (days)',
    'Active Coins per Active Address',
    'Active Coins per Active Address']
range_data = [[0,4500],[-1,3],[-1,9]]
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()



"""
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                    MINERS AND POW
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
"""


"""
#############################################################################
                    BITCOIN AND DECRED POW GROWTH
#############################################################################
"""

BTC_hash = btc_add_metrics().btc_hash()
DCR_hash = DCR_data[DCR_data['pow_hashrate_THs_avg']>1]


loop_data = [[0,1,2,3],[4,5]]
x_data = [
    BTC_hash['age_days'],DCR_hash['age_days'],
    BTC_hash['age_days'],DCR_hash['age_days'],
    BTC_hash['age_days'],DCR_hash['age_days'],
    ]
y_data = [
    BTC_hash['DiffMean'],DCR_hash['DiffMean'],
    BTC_hash['pow_hashrate_THs'],DCR_hash['pow_hashrate_THs_avg'],
    BTC_hash['PriceUSD'],DCR_hash['PriceUSD'],
    ]
name_data = [
    'Bitcoin Difficulty Ribbon','Decred Difficulty Ribbon',
    'Bitcoin Hashrate','Decred Hashrate',
    'BTC Price','DCR Price',
    ]
color_data = [
    'rgb(255, 102, 0)' , 'rgb(46, 214, 161)' ,
    'rgb(254, 215, 140)','rgb(65, 191, 83)',
    'rgb(255, 102, 0)' , 'rgb(46, 214, 161)' ,
    #'rgb(255, 80, 80)','rgb(255, 102, 102)',
    #'rgb(255, 153, 102)','rgb(255, 255, 102)',
    #'rgb(156,225,43)', 'rgb(1, 255, 116)',
    #'rgb(255, 255, 255)', 'rgb(46, 214, 161)',
    ]
dash_data = [
    'solid','solid',
    'solid','solid',
    'dot','dot',
    ]
width_data = [
    2,2,1,1,1,1
    ]
opacity_data = [
    1,1,1,1,0.75,0.75
    ]
legend_data = [
    True,True,True,True,True,True,
    ]#
title_data = [
    'Proof of Work Growth',
    'Coin Age (Days since Launch)',
    'Protocol Difficulty  |  Network Hashrate (TH/s)',
    'Coin Price (USD)']
range_data = [[0,4380],[0,14],[-2,5]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_xaxes(dtick=365)

""" =================================
    ADD DIFFICULTY RIBBON BAR CHARTS
================================="""
for i in [9,14,25,40,60,90,128,200]:
    fig.add_trace(go.Scatter(
        mode='lines',
        x=DCR_hash['age_days'], 
        y=DCR_hash['DiffMean'].rolling(i).mean(),
        name='Difficulty '+str(i),
        opacity=0.5,
        showlegend=False,
        line=dict(
            width=i/200*2,
            color='rgb(156,225,143)',
            dash='solid'
            )),
        secondary_y=False)

for i in [9,14,25,40,60,90,128,200]:
    fig.add_trace(go.Scatter(
        mode='lines',
        x=BTC_hash['age_days'], 
        y=BTC_hash['DiffMean'].rolling(i).mean(),
        name='Difficulty '+str(i),
        opacity=0.5,
        showlegend=False,
        line=dict(
            width=i/200*2,
            color='rgb(255, 102, 0)',
            dash='solid'
            )),
        secondary_y=False)


fig.show()





"""
#############################################################################
                    MINER CUMMULATIVE INCOMES
#############################################################################
"""

BTC_hash['PoW_income_usd'] = BTC_hash['DailyIssuedUSD'] + BTC_hash['FeeTotUSD']
BTC_hash['FeeRatio'] = BTC_hash['FeeTotUSD']/BTC_hash['PoW_income_usd']
DCR_hash['FeeRatio'] = DCR_hash['FeeTotUSD']/DCR_hash['PoW_income_usd']


loop_data = [[0,2,6,4,1,3,7,5],[]]
x_data = [
    BTC_hash['age_sply'],DCR_hash['age_sply'],
    BTC_hash['age_sply'],DCR_hash['age_sply'],
    BTC_hash['age_sply'],DCR_hash['age_sply'],
    BTC_hash['age_sply'],DCR_hash['age_sply'],
    #Second Chart
    BTC_hash['age_sply'],DCR_hash['age_sply'],
    ]
y_data = [
    BTC_hash['PoW_income_usd'].cumsum(),
    DCR_hash['PoW_income_usd'].cumsum(),
    BTC_hash['FeeTotUSD'].cumsum(),
    DCR_hash['FeeTotUSD'].cumsum(),
    BTC_hash['PoW_income_usd'],
    DCR_hash['PoW_income_usd'],
    BTC_hash['CapMrktCurUSD'],
    DCR_hash['CapMrktCurUSD'],
    #Second Chart
    BTC_hash['FeeRatio'],   #Fee Ratio
    DCR_hash['FeeRatio'],   #Fee Ratio
    ]
name_data = [
    'Bitcoin Cumulative PoW Reward','Decred Cumulative PoW Reward',
    'Bitcoin Cumulative Tx Fees','Decred Cumulative Tx Fees',
    'Bitcoin Daily PoW Reward','Decred Daily PoW Reward',
    'Bitcoin Market Cap', 'Decred Market Cap',
    'Bitcoin Fee Ratio','Decred Fee Ratio'
    ]
color_data = [
    'rgb(255, 102, 0)' , 'rgb(46, 214, 161)' ,
    'rgb(255, 102, 0)' , 'rgb(46, 214, 161)',
    'rgb(254, 215, 140)','rgb(65, 191, 83)',
    'rgb(255, 102, 0)' , 'rgb(46, 214, 161)',
    #Second Chart
    'rgb(255, 102, 0)' , 'rgb(46, 214, 161)',
    ]
dash_data = [
    'solid','solid',
    'dash','dash',
    'dot','dot',
    'solid','solid',
    'solid','solid'
    ]
width_data = [
    2,2,2,2,1,1,1,1,
    1,1
    ]
opacity_data = [
    1,1,1,1,0.75,0.75,1,1,
    1,1
    ]
legend_data = [
    True,True,
    True,True,
    False,False,
    True,True,
    True,True,
    ]#
title_data = [
    'Proof of Work Miner Rewards',
    'Coin Age (Supply / 21M)',
    'Value (USD)',
    '']
range_data = [[0,1],[2,12],[2,8]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_xaxes(dtick=0.1)
fig.show()

#Fee Ratio Chart

loop_data = [[8,9],[]]
title_data = [
    'Fee Ratio of PoW Block Reward',
    'Coin Age (Supply / 21M)',
    'Fee Ratio','']
range_data = [[0,1],[-5,0],[0,0]]
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_xaxes(dtick=0.1)
fig.update_yaxes(tickformat = ".2%")
fig.show()




















"""
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                    STAKEHOLDERS
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
"""

"""
#############################################################################
                    STAKEHOLDER TOTAL LOCKED IN TICKETS - USD
#############################################################################
"""


loop_data = [[0,1,2,3],[]]
x_data = [
    DCR_hash['date'],
    DCR_hash['date'],
    DCR_hash['date'],
    DCR_hash['date'],
    ]
y_data = [
    DCR_hash['CapMrktCurUSD'],
    DCR_hash['tic_usd_cost'].cumsum(),
    DCR_hash['PoW_income_usd'].cumsum(),
    DCR_hash['CapRealUSD'],
    ]
name_data = [
    'Market Cap',
    'Cumulative Ticket Lockup',
    'Cumulative PoW Block Reward',
    'Realised Cap',
    ]
color_data = [
    'rgb(46, 214, 161)' ,   #Turquoise
    'rgb(65, 191, 83)',     #Decred Green
    'rgb(250, 38, 53)' ,    #PoW Red
    'rgb(239, 125, 50)',    #Price Orange
    ]
dash_data = [
    'solid','solid','solid','dot',
    ]
width_data = [
    2,2,2,2
    ]
opacity_data = [
    1,1,1,1
    ]
legend_data = [
    True,True,True,True,
    ]
title_data = [
    'Stakeholder Commitments',
    'date',
    'Value (USD)',
    '']
range_data = [['2016-01-01','2021-01-01'],[6,10],[2,8]]
autorange_data = [False,False,True]
type_data = ['date','log','log']#
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
#fig.update_xaxes(dtick=0.1)
fig.show()


"""
#############################################################################
                    STAKEHOLDER TOTAL LOCKED IN TICKETS - BTC
#############################################################################
"""
DCR_data = DCR_data.merge(BTC_data[['date','PriceUSD',]],on='date',how='left',suffixes=('', '_BTC'))
DCR_data['CapRealBTC'] = DCR_data['CapRealUSD'].diff(periods=1)/DCR_data['PriceUSD_BTC']
DCR_data['CapRealBTC'] = DCR_data['CapRealBTC'].cumsum()


loop_data = [[0,1,2,3,4],[]]
x_data = [
    DCR_data['date'],
    DCR_data['date'],
    DCR_data['date'],
    DCR_data['date'],
    DCR_data['date'],
    ]
y_data = [
    DCR_data['SplyCur']*DCR_data['PriceBTC'],
    DCR_data['tic_btc_cost'].cumsum(),
    DCR_data['PoS_income_btc'].cumsum(),
    DCR_data['PoW_income_btc'].cumsum(),
    DCR_data['CapRealBTC'],
    ]
name_data = [
    'Market Cap',
    'Cumulative Ticket Lockup',
    'Cumulative PoS Block Reward',
    'Cumulative PoW Block Reward',
    'Realised Cap',
    ]
color_data = [
    'rgb(46, 214, 161)' ,   #Turquoise
    'rgb(65, 191, 83)',     #Decred Green
    'rgb(153, 51, 255)',    #PoS Purple
    'rgb(250, 38, 53)' ,    #PoW Red
    'rgb(239, 125, 50)',    #Price Orange
    ]
dash_data = [
    'solid','solid','solid','solid','dot',
    ]
width_data = [
    2,2,2,2,2
    ]
opacity_data = [
    1,1,1,1,1
    ]
legend_data = [
    True,True,True,True,True,
    ]
title_data = [
    'Stakeholder Commitments in BTC',
    'date',
    'Value (BTC)',
    '']
range_data = [['2016-01-01','2021-01-01'],[3,6],[2,8]]
autorange_data = [False,False,True]
type_data = ['date','log','log']#
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
#fig.update_xaxes(dtick=0.1)
fig.show()


"""
#############################################################################
                    TICKET METRICS
#############################################################################
"""

loop_data = [[0,1,],[]]
x_data = [
    DCR_data['date'],
    DCR_data['date'],
    DCR_data['date'],
    DCR_data['date'],
    DCR_data['date'],
    ]
y_data = [
    DCR_data['PriceUSD'],
    DCR_data['CapTicPriceUSD'],
    DCR_data['PoS_income_btc'].cumsum(),
    DCR_data['PoW_income_btc'].cumsum(),
    DCR_data['PriceRealUSD']/DCR_data['PriceUSD_BTC']*DCR_data['SplyCur'],
    ]
name_data = [
    'Market Cap',
    'Cumulative Ticket Lockup',
    'Cumulative PoS Block Reward',
    'Cumulative PoW Block Reward',
    'Realised Cap',
    ]
color_data = [
    'rgb(46, 214, 161)' ,   #Turquoise
    'rgb(65, 191, 83)',     #Decred Green
    'rgb(153, 51, 255)',    #PoS Purple
    'rgb(250, 38, 53)' ,    #PoW Red
    'rgb(239, 125, 50)',    #Price Orange
    ]
dash_data = [
    'solid','solid','solid','solid','dot',
    ]
width_data = [
    2,2,2,2,2
    ]
opacity_data = [
    1,1,1,1,1
    ]
legend_data = [
    True,True,True,True,True,
    ]
title_data = [
    'Stakeholder Commitments in BTC',
    'date',
    'Value (BTC)',
    'DCRUSD Price']
range_data = [['2016-01-01','2021-01-01'],[3,6],[2,8]]
autorange_data = [False,False,True]
type_data = ['date','log','log']#
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
#fig.update_xaxes(dtick=0.1)
fig.show()



"""
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                    BUILDERS AND TREASURY
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
"""


DCR_fund = pd.read_csv(r"D:\code_development\checkonchain\checkonchain\dcronchain\resources\data\treasury_20200212.csv")
#Sort by timestamp - oldest to newest
DCR_fund = DCR_fund.sort_values(by='time_stamp')
#Reset Index
DCR_fund = DCR_fund.reset_index(drop=True)
#Convert timestamp to datetime
DCR_fund['date'] = pd.to_datetime(DCR_fund['time_stamp'],unit='s',utc=True)
#Calculate Transaction value * direction (+ve = inflow)
DCR_fund['funds'] = DCR_fund['value'] * DCR_fund['direction']
#Treasury Balance = cumulative sum of funds
DCR_fund['balance'] = DCR_fund['funds'].cumsum()
#Incoming and Outgoing = cumulative sum in +ve and negative direction
DCR_fund['incoming'] = DCR_fund['funds'].clip(lower=0)
DCR_fund['outgoing'] = DCR_fund['funds'].clip(upper=0)
#Treasury Spend Rate
DCR_fund['spend_rate'] = DCR_fund['outgoing'].cumsum()*-1/DCR_fund['balance']
DCR_fund['spend_rate_final'] = DCR_fund['outgoing'].cumsum()/(-19.32e6*0.1)
#Combine with Price USD and BTC Data
DCR_fund = pd.merge_asof(
    DCR_fund,
    DCR_data[['date','PriceUSD','PriceBTC','tic_pool_avg','tic_day','tic_price_avg']],
    left_on='date',
    right_on='date'
    )
#Calculate Expenditure
DCR_fund['balance_usd'] = DCR_fund['balance'] * DCR_fund['PriceUSD']
DCR_fund['incoming_usd'] = DCR_fund['incoming'] * DCR_fund['PriceUSD']
DCR_fund['outgoing_usd'] = DCR_fund['outgoing'] * DCR_fund['PriceUSD']
DCR_fund['expenditure_usd'] = DCR_fund['outgoing_usd'].cumsum()*-1



"""
#############################################################################
                    TREASURY INFLOW OUTFLOW - DCR
#############################################################################
"""
loop_data = [[0,1,2],[3]]
x_data = [
    DCR_fund['date'],
    DCR_fund['date'],
    DCR_fund['date'],
    DCR_fund['date'],
    DCR_fund['date'],
    DCR_fund['date'],
    DCR_fund['date'],
    DCR_fund['date'],
    DCR_fund['date'],
    ]
y_data = [
    #Chart 1 - INFLOW/OUTFLOW DCR
    DCR_fund['balance'],
    DCR_fund['incoming'].cumsum(),
    DCR_fund['outgoing'].cumsum()*-1,
    DCR_fund['PriceUSD'],
    #Chart 2 - INFLOW/OUTFLOW USD
    DCR_fund['balance_usd'],
    DCR_fund['incoming_usd'].cumsum(),
    DCR_fund['outgoing_usd'].cumsum()*-1,
    #Chart 3 - SPEND RATIO
    DCR_fund['spend_rate'],
    DCR_fund['spend_rate_final'],
    ]
name_data = [
    #Chart 1
    'Treasury Balance DCR',
    'Treasury Inflows DCR',
    'Treasury Outflows DCR',
    'PriceUSD',
    #Chart 2
    'Treasury Balance USD',
    'Treasury Inflows USD',
    'Treasury Outflows USD',
    #Chart 3
    'Treasury Spend Ratio (Actual)',
    'Treasury Spend Ratio (Final)'
    ]
color_data = [
    #Chart 1
    'rgb(65, 191, 83)',     #Decred Green
    'rgb(46, 214, 161)' ,   #Turquoise
    'rgb(250, 38, 53)' ,    #PoW Red
    'rgb(255,255,255)',     #White
    #Chart 2
    'rgb(65, 191, 83)',     #Decred Green
    'rgb(46, 214, 161)' ,   #Turquoise
    'rgb(250, 38, 53)' ,    #PoW Red
    #Chart 3
    'rgb(46, 214, 161)' ,   #Turquoise
    'rgb(250, 38, 53)' ,    #PoW Red
    ]
dash_data = [
    'solid','solid','solid','dot',
    'dot','dot','dot',
    'solid','dash'
    ]
width_data = [
    2,2,2,1,
    2,2,2,
    2,2
    ]
opacity_data = [
    1,1,1,1,
    1,1,1,
    1,1
    ]
legend_data = [
    True,True,True,True,
    True,True,True,
    True,True,
    ]
title_data = [
    'Decred Treasury Flows - DCR',
    'Date',
    'Treasury Flows (DCR)',
    'DCR Price (USD)']
range_data = [['2016-01-01','2021-01-01'],[0,1e6],[-1,3]]
autorange_data = [False,False,False]
type_data = ['date','linear','log']
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_yaxes(dtick=1e5,secondary_y=False)
fig.show()

"""
#############################################################################
                    TREASURY INFLOW OUTFLOW - USD
#############################################################################
"""
loop_data = [[0,1,2],[4,5,6]]
range_data = [['2016-01-01','2021-01-01'],[0,1e6],[4,7]]
autorange_data = [False,False,True]
type_data = ['date','linear','log']
title_data = [
    'Decred Treasury Flows',
    'Date',
    'Treasury Flows (DCR)',
    'Treasury Flows (USD)']
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()

"""
#############################################################################
                    TREASURY SPEND RATIO
#############################################################################
"""
loop_data = [[7,8],[]]
range_data = [['2016-01-01','2021-01-01'],[0,0.5],[]]
autorange_data = [False,False,False]
type_data = ['date','linear','log']
title_data = [
    'Decred Treasury Spend Ratio',
    'date',
    'Spend Ratio',
    '']
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.update_yaxes(tickformat = "%",dtick=0.1)
fig.show()



"""
#############################################################################
                    TICKET VOTE POWER
#############################################################################
"""
#Calculate USD Power per Ticket in Pool
DCR_fund['vote_power_usd'] = DCR_fund['balance_usd']/DCR_fund['tic_pool_avg']
#Calculate DCR Power per Ticket in Pool
DCR_fund['vote_power_dcr'] = DCR_fund['balance']/DCR_fund['tic_pool_avg']
#Calculate Relative Proportion
DCR_fund['vote_power'] = DCR_fund['vote_power_dcr']/DCR_fund['tic_price_avg']


loop_data = [[1],[2]]
x_data = [
    DCR_fund['date'],
    DCR_fund['date'],
    DCR_fund['date'],
    ]
y_data = [
    DCR_fund['vote_power_usd'],
    DCR_fund['vote_power_dcr'],
    DCR_fund['vote_power'],
    ]
name_data = [
    'Vote Power USD',
    'Vote Power DCR',
    'Vote Power Ratio',
    ]
color_data = [
    #Chart 1
    'rgb(65, 191, 83)',     #Decred Green
    'rgb(46, 214, 161)' ,   #Turquoise
    'rgb(250, 38, 53)' ,    #PoW Red
    'rgb(255,255,255)',     #White
    #Chart 2
    'rgb(65, 191, 83)',     #Decred Green
    'rgb(46, 214, 161)' ,   #Turquoise
    'rgb(250, 38, 53)' ,    #PoW Red
    #Chart 3
    'rgb(255,255,255)',     #White
    'rgb(65, 191, 83)'      #Decred Green
    ]
dash_data = [
    'solid','solid','solid','solid',
    ]
width_data = [
    2,2,1,2,
    2,2,2,
    2,2
    ]
opacity_data = [
    1,1,1,1,
    1,1,1,
    1,1
    ]
legend_data = [
    True,True,True,True,
    True,True,True,
    True,True,
    ]
title_data = [
    'Vote Power per Ticket (DCR)',
    'Date',
    'Vote Power per Ticket (DCR)',
    'Vote Power to Ticket Price Ratio']
range_data = [['2016-01-01','2021-01-01'],[-1,2],[-2,0]]
autorange_data = [False,False,False]
type_data = ['date','log','log']
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.update_yaxes(tickformat = "%",secondary_y=True)
fig.show()