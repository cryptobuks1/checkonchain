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
DCR_data = DCR_data.merge(BTC_data[['age_days','AdrActCnt']],on='age_days',how='left',suffixes=('', '_BTC'))
#DCR_data.rename(columns={'AdrActCnt_y':'AdrActCnt_BTC'}, inplace=True)
DCR_data['DCRBTC_AdrActCnt'] = DCR_data['AdrActCnt'] / DCR_data['AdrActCnt_BTC']

loop_data = [[0,1,2],[3,4,5]]
x_data = [
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_data['age_days'],DCR_data['age_days'],
    BTC_half['age_days'],    
    ]
y_data = [
    BTC_data['AdrActCnt'],DCR_data['AdrActCnt'],DCR_data['tic_day'].rolling(7).mean()*4,
    BTC_data['PriceUSD'],DCR_data['PriceUSD'],
    BTC_half['y_arb'],
    ]
name_data = [
    'BTC AdrActCnt','DCR AdrActCnt','4x Ticket Buys',
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
    'Active Addresses',
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
loop_data = [[1,2,0,3,4],[]]
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
    DCR_data['tic_day'].rolling(3).mean(),
    BTC_data['TxTfrCnt'].cumsum(),
    DCR_data['TxTfrCnt'].cumsum(),
    DCR_data['tic_day'].cumsum(),
    BTC_half['y_arb'],
    ]
name_data = [
    'BTC TxTfrCnt','DCR TxTfrCnt','DCR Ticket Buys',
    'BTC Cumulative TxTfr','DCR Cumulative TxTfr','Ticket Buys Cumulative',
    'Bitcoin Halvings'
    ]
color_data = [
    'rgb(254, 150, 70)', 'rgb(65, 191, 83)','rgb(112, 203, 255)',
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

#Address Density
BTC_data['AdrDens'] = BTC_data['TxTfrValNtv']/BTC_data['AdrActCnt']
DCR_data['AdrDens'] = DCR_data['TxTfrValNtv']/DCR_data['AdrActCnt']
DCR_data['dcr_tic_buy'] = DCR_data['tic_day']*DCR_data['tic_price_avg']

loop_data = [[0,1,2],[3,4,5,6]]
x_data = [
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_data['age_days'],DCR_data['age_days'],DCR_data['age_days'],
    BTC_half['age_days'],    
    ]
y_data = [
    BTC_data['TxTfrValNtv'].rolling(14).mean(),
    DCR_data['TxTfrValNtv'].rolling(14).mean(),
    DCR_data['dcr_tic_buy'].rolling(14).mean(),
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
    'rgb(254, 150, 70)', 'rgb(65, 191, 83)','rgb(112, 203, 255)',
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
    'Native Units Transferred On-chain',
    'Protocol Age (days)',
    'Daily Native Units Transferred',
    'Cumulative Native Units Transferred']
range_data = [[0,4500],[2,7],[2,11]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
fig.show()