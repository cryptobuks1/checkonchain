#Compare the Unforgeable Costliness of Bitcoin and Decred
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.dcronchain.dcr_security_model import *


"""
CONCEPT: 
Unforgeable costliness is the cost required to produce each coin.
1. Calculate block subsidy models (Natv and USD terms)
2. Cummulative sum --> assuming marginal reward = marginal cost
    PoW = Cummulative Sum (100% for BTC and 60% for DCR)
    PoS = Cummulative Sum (30% for DCR)
3. For Decred, there is a balance between PoS and PoW as described 
in Stafford (2019)
    Assume an attacker portion of ticket stake owned 
        P_y = (1%, 5%, 30%, 50% and 95%)
    Probability of honest tickets having 3/5 votes
        sig_y = 1 - P_y
    Proportion of Hashrate attacker needs
        x_y = (1 / P_y) - 1
4. Decred cost to attack = P_y(PoS) + x_y(PoW)
"""

#Compile Input Dataframes
BTC_subs = btc_add_metrics().btc_subsidy_models()
DCR_subs = dcr_add_metrics().dcr_ticket_models()
BTC_fee = btc_add_metrics().btc_coin()

#Calculate Unforgeable Costliness (cummulative Sum)
BTC_subs['Unforg_Cost'] = BTC_subs['PoW_income_usd'].cumsum()
DCR_subs['PoW_Cost'] = DCR_subs['PoW_income_usd'].cumsum()
DCR_subs['PoS_Cost'] = DCR_subs['PoS_income_usd'].cumsum()

#Calculate Unforgeable Costliness (cummulative Sum)
BTC_subs['Unforg_Cost_Daily'] = BTC_subs['PoW_income_usd']
DCR_subs['PoW_Cost_Daily'] = DCR_subs['PoW_income_usd']
DCR_subs['PoS_Cost_Daily'] = DCR_subs['PoS_income_usd']

#Calculate Range of Decred Security Conditions
for y in range(5,105,5): #Assume range of Attacker ticket stake ownership
    y       = y/100       #Probability attacker tickets make block
    i = 0
    _total = 0
    while i < 3:
        _bincoef = (
            math.factorial(5)
            / (math.factorial(5-i) 
            * math.factorial(i))
        )
        _calc = _bincoef * y**(5-i)*((1-y)*1)**i
        _total = _total + _calc
        i += 1
    P_y     = _total
    sig_y   = 1-P_y         #Probability honest tickets  make valid block
    x_y     = (1 / P_y) - 1 #Attacker required hashpower for given stake
    col_name = 'Unforg_Cost_'+str(int(y*100))+'%' #Set column name
    DCR_subs[col_name] = (  #Cummulative Unforgeable Cost
        P_y * DCR_subs['PoS_Cost'] + x_y * DCR_subs['PoW_Cost']
    )
    DCR_subs[col_name+'_Daily'] = ( #Daily Unforgeable Cost
        P_y * DCR_subs['PoS_Cost_Daily'] #PoS Reward
        #+ P_y * DCR_subs['dcr_tic_sply_avg'] * DCR_subs['PriceUSD'] #Buy Tickets
        + x_y * DCR_subs['PoW_Cost_Daily'] #Hashpower reward
    )

#Calculate monetary premium over pure PoW Energy Expendature
BTC_subs['PoW_Premium'] = BTC_subs['CapMrktCurUSD'] / BTC_subs['Unforg_Cost']
DCR_subs['PoW_Premium'] = DCR_subs['CapMrktCurUSD'] / DCR_subs['Unforg_Cost_100%']



#Set Toggle to 1 for Market Cap, XXX_subs['SplyCur'] for Price
toggle_btc = 1#BTC_subs['SplyCur']
toggle_dcr = 1#DCR_subs['SplyCur']
"""
#############################################################################
                    UNFORGEABLE COSTLINESS - CUMMULATIVE
#############################################################################
"""
loop_data = [[0,1,2,3,4,5,6,7,8],[9,10]]
x_data = [
    BTC_subs['age_sply'],DCR_subs['age_sply'],  #Market Caps
    BTC_subs['age_sply'],                       #BTC UC
    DCR_subs['age_sply'],DCR_subs['age_sply'],  #DCR UC
    DCR_subs['age_sply'],DCR_subs['age_sply'],  #DCR UC
    DCR_subs['age_sply'],DCR_subs['age_sply'],  #DCR UC
    BTC_subs['age_sply'],DCR_subs['age_sply'],   #Pow Premium Secondary
    ]
y_data = [
    BTC_subs['CapMrktCurUSD']/toggle_btc,DCR_subs['CapMrktCurUSD']/toggle_dcr,        #Market Caps
    (BTC_subs['Unforg_Cost']+BTC_fee['FeeTotUSD'].cumsum())/toggle_btc,                                    #BTC UC
    DCR_subs['Unforg_Cost_5%']/toggle_dcr,DCR_subs['Unforg_Cost_10%']/toggle_dcr,     #DCR UC
    DCR_subs['Unforg_Cost_15%']/toggle_dcr,DCR_subs['Unforg_Cost_30%']/toggle_dcr,    #DCR UC
    DCR_subs['Unforg_Cost_50%']/toggle_dcr,DCR_subs['Unforg_Cost_75%']/toggle_dcr,   #DCR UC
    BTC_subs['PoW_Premium'],DCR_subs['PoW_Premium'],            #Pow Premium Secondary
    ]
name_data = [
    'BTC Market Cap','DCR Market Cap',
    'BTC Unforgeable Cost',
    'DCR Unforgeable Cost 5%','DCR Unforgeable Cost 10%',
    'DCR Unforgeable Cost 15%','DCR Unforgeable Cost 30%',
    'DCR Unforgeable Cost 50%','DCR Unforgeable Cost 75%',
    'BTC Pure PoW Premium','DCR Pure PoW Premium',
    ]
color_data = [
    'rgb(255, 255,255)' ,'rgb(46, 214, 161)' ,
    'rgb(255, 102, 0)',
    'rgb(1, 255, 116)','rgb(156,225,43)',
    'rgb(255, 255, 102)','rgb(255, 153, 102)',
    'rgb(255, 102, 102)','rgb(255, 80, 80)',
    'rgb(255, 102, 0)', 'rgb(46, 214, 161)',
    ]
dash_data = [
    'solid','solid',
    'solid',
    'solid','solid',
    'solid','solid',
    'solid','solid',
    'solid','solid',
    ]
width_data = [
    2,2,2,2,2,2,2,2,2,1,1
    ]
opacity_data = [
    1,1,1,1,1,1,1,1,1,1,1
    ]
legend_data = [
    True,True,
    True,
    True,True,True,
    True,True,True,
    True,True
    ]#
title_data = [
    'Sound Money, Unforgeable Costliness',
    'Coin Age (Supply/21M)',
    'Cost to Attack Network (USD)',
    'Pure PoW Premium Ratio']
range_data = [[0,1],[4,12],[-1,5]]
autorange_data = [False,True,False]
type_data = ['linear','log','log']#
fig = check_standard_charts('dark').subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_xaxes(dtick=0.1)
fig.show()


#Set Toggle to 1 for Market Cap, XXX_subs['SplyCur'] for Price
toggle_btc = 1#BTC_subs['SplyCur']
toggle_dcr = 1#DCR_subs['SplyCur']


"""
#############################################################################
                    UNFORGEABLE COSTLINESS - DAILY
#############################################################################
"""
loop_data = [[0,1,2,3,4,5,6,7,8,9,10],[]]
x_data = [
    BTC_subs['age_sply'],DCR_subs['age_sply'],  #Market Caps
    BTC_subs['age_sply'],                       #BTC UC
    DCR_subs['age_sply'],DCR_subs['age_sply'],  #DCR UC
    DCR_subs['age_sply'],DCR_subs['age_sply'],  #DCR UC
    DCR_subs['age_sply'],DCR_subs['age_sply'],  #DCR UC
    BTC_subs['age_sply'],DCR_subs['age_sply'],   #Pow Premium Secondary
    ]
y_data = [
    BTC_subs['CapMrktCurUSD']/toggle_btc,DCR_subs['CapMrktCurUSD']/toggle_dcr,        #Market Caps
    (BTC_subs['Unforg_Cost_Daily']+BTC_fee['FeeTotUSD'])/toggle_btc,                                    #BTC UC
    DCR_subs['Unforg_Cost_5%_Daily']/toggle_dcr,DCR_subs['Unforg_Cost_10%_Daily']/toggle_dcr,     #DCR UC
    DCR_subs['Unforg_Cost_15%_Daily']/toggle_dcr,DCR_subs['Unforg_Cost_30%_Daily']/toggle_dcr,    #DCR UC
    DCR_subs['Unforg_Cost_50%_Daily']/toggle_dcr,DCR_subs['Unforg_Cost_75%_Daily']/toggle_dcr,   #DCR UC
    BTC_subs['TxTfrValUSD'].rolling(7).mean(),DCR_subs['TxTfrValUSD'].rolling(7).mean(),
    #BTC_subs['PoW_Premium'],DCR_subs['PoW_Premium'],            #Pow Premium Secondary
    ]
name_data = [
    'BTC Market Cap','DCR Market Cap',
    'BTC Attack Cost',
    'DCR Attack Cost 5%','DCR Attack Cost 10%',
    'DCR Attack Cost 15%','DCR Attack Cost 30%',
    'DCR Attack Cost 50%','DCR Attack Cost 75%',
    'BTC Daily USD Settled','DCR Daily USD Settled',
    ]
color_data = [
    'rgb(255, 255,255)' ,'rgb(46, 214, 161)' ,
    'rgb(255, 102, 0)',
    'rgb(1, 255, 116)','rgb(156,225,43)', 
    'rgb(255, 255, 102)','rgb(255, 153, 102)',
    'rgb(255, 102, 102)','rgb(255, 80, 80)',
    'rgb(255, 255, 255)', 'rgb(112, 203, 255)',
    ]
dash_data = [
    'dot','dot',
    'solid',
    'solid','solid',
    'solid','solid',
    'solid','solid',
    'solid','solid',
    ]
width_data = [
    2,2,
    2,
    1,1,1,
    1,1,1,
    3,3
    ]
opacity_data = [
    1,1,
    1,
    1,1,1,
    1,1,1,
    1,1
    ]
legend_data = [
    True,True,
    True,
    True,True,True,
    True,True,True,
    True,True
    ]#
title_data = [
    'Daily Security and Tx Settlement',
    'Coin Age (Supply/21M)',
    'Cost to Attack Network (USD)',
    'Pure PoW Premium Ratio']
range_data = [[0,1],[2,12],[-1,5]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts('dark').subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_xaxes(dtick=0.1)
fig.show()


"""
#############################################################################
                    COMPARE TOP CAP PROJECTS
#############################################################################
"""

LTC = Coinmetrics_api('ltc',"2011-10-07",today).convert_to_pd().set_index('date',drop=False)
BCH = Coinmetrics_api('bch',"2017-08-01",today).convert_to_pd().set_index('date',drop=False)
DASH = Coinmetrics_api('dash',"2014-01-19",today).convert_to_pd().set_index('date',drop=False)
DCR = Coinmetrics_api('dcr',"2016-02-08",today).convert_to_pd().set_index('date',drop=False)
XMR = Coinmetrics_api('xmr',"2014-04-18",today).convert_to_pd().set_index('date',drop=False)
ZEC = Coinmetrics_api('zec',"2016-10-28",today).convert_to_pd().set_index('date',drop=False)
ETH = Coinmetrics_api('eth',"2015-07-30",today).convert_to_pd().set_index('date',drop=False)

LTC['age_sply'] = LTC['SplyCur']/84e6
BCH['age_sply'] = BCH['SplyCur']/21e6
DASH['age_sply'] = DASH['SplyCur']/17.6e6
XMR['age_sply'] = XMR['SplyCur']/22.466e6
ZEC['age_sply'] = ZEC['SplyCur']/21e6
ETH['age_sply'] = ETH['SplyCur']/135e6

LTC['Unforg_Cost'] = LTC['DailyIssuedNtv'] *LTC['PriceUSD'] 
BCH['Unforg_Cost'] = BCH['DailyIssuedNtv'] *BCH['PriceUSD'] 
DASH['Unforg_Cost']= DASH['DailyIssuedNtv']*DASH['PriceUSD'] + 1000*DASH['PriceUSD'] #1x MN
XMR['Unforg_Cost'] = XMR['DailyIssuedNtv'] *XMR['PriceUSD'] 
ZEC['Unforg_Cost'] = ZEC['DailyIssuedNtv'] *ZEC['PriceUSD'] 
ETH['Unforg_Cost'] = ETH['DailyIssuedNtv'] *ETH['PriceUSD'] 


loop_data = [[0,1,2,3,4,5,6,7,8,9,10,11,12],[]]
x_data = [
    BTC_subs['age_sply'],
    DCR_subs['age_sply'],DCR_subs['age_sply'],DCR_subs['age_sply'],
    DCR_subs['age_sply'],DCR_subs['age_sply'],DCR_subs['age_sply'],
    LTC['age_sply'], 
    BCH['age_sply'], 
    DASH['age_sply'],
    XMR['age_sply'], 
    ZEC['age_sply'], 
    ETH['age_sply'], 
    ]
y_data = [
    BTC_subs['Unforg_Cost'],
    DCR_subs['Unforg_Cost_5%'],DCR_subs['Unforg_Cost_10%'],  
    DCR_subs['Unforg_Cost_15%'],DCR_subs['Unforg_Cost_30%'], 
    DCR_subs['Unforg_Cost_50%'],DCR_subs['Unforg_Cost_75%'],
    LTC['Unforg_Cost'].cumsum(),
    BCH['Unforg_Cost'].cumsum(),
    DASH['Unforg_Cost'].cumsum(),
    XMR['Unforg_Cost'].cumsum(),
    ZEC['Unforg_Cost'].cumsum(),
    ETH['Unforg_Cost'].cumsum()
    ]
name_data = [
    'BTC',
    'DCR 5%','DCR 10%','DCR 15%',
    'DCR 30%','DCR 50%','DCR 75%',
    'LTC',
    'BCH',
    'DASH',
    'XMR',
    'ZEC',
    'ETH',
    ]
color_data = [
    'rgb(255, 102, 0)',
    'rgb(1, 255, 116)','rgb(156,225,43)', 
    'rgb(255, 255, 102)','rgb(255, 153, 102)',
    'rgb(255, 102, 102)','rgb(255, 80, 80)',
    'rgb(214, 214, 194)',
    'rgb(0, 153, 51)',  
    'rgb(51, 204, 255)',
    'rgb(255, 153, 0)',  
    'rgb(255, 255, 0)',  
    'rgb(153, 51, 255)' 

    ]
dash_data = [
    'solid',
    'solid','solid','solid',
    'solid','solid','solid',
    'dot',
    'dot',
    'dot',
    'dot',
    'dot',
    'dot',
    ]
width_data = [
    2,
    2,2,2,2,2,2,
    2,2,2,2,2,2]
opacity_data = [
    1,
    1,1,1,1,1,1,
    1,1,1,1,1,1,
    ]
legend_data = [
    True,
    True,True,True,True,True,True,
    True,True,True,True,True,True]#
title_data = [
    'Compare Unforgeable Costliness',
    'Coin Age (Supply / 2050 Supply)',
    'Cost to Attack Network (USD)']
range_data = [[0,1],[4,12],[-1,5]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']
fig = check_standard_charts('dark').subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_xaxes(dtick=0.1)
fig.show()


"""
#############################################################################
                    DECRED SECURITY CURVE
#############################################################################
"""

DCR_Secure = dcr_security_calculate_df().dcr_security_curve()
DCR_Secure[50:100]

loop_data = [[0],[2]]
x_data = [DCR_Secure['y'],[0,1],DCR_Secure['y']]
y_data = [DCR_Secure['x_y'],[1,1],DCR_Secure['days_buy_y']]
name_data = [
    'Decred Security Curve',
    'Bitcoin Security Curve',
    'Days to Buy Tickets in Full Blocks']
title_data = [
    'DCR Security Curve',
    'Attacker Share of Ticket Pool',
    'Required Multiple of Honest Hashpower',
    'Days to Buy Tickets in Full Blocks'
    ]
color_data = [
    'rgb(255, 102, 0)',
    'rgb(46, 214, 161)' ,
    'rgb(51, 204, 255)',
]
dash_data = ['solid','solid','dash']
width_data = [2,2,2]
opacity_data = [1,1,1]
type_data = ['linear','log','linear']
range_data = [[0,0.75],[-1,5],[0,6]]
autorange_data = [False,False,False]
legend_data = [True,True,True]
fig = check_standard_charts('dark').subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_xaxes(dtick=0.05)
fig.update_yaxes(dtick=1,secondary_y=False)
fig.update_yaxes(dtick=1,secondary_y=True)
fig.update_layout(legend=dict(x=0.1, y=0.9))
fig.show()


"""
#############################################################################
                    BITCOIN AND DECRED POW GROWTH
#############################################################################
"""

BTC_hash = btc_add_metrics().btc_hash()
DCR_hash = DCR_subs[DCR_subs['pow_hashrate_THs_avg']>1]


loop_data = [[0,1,4,5],[2,3]]
x_data = [
    BTC_hash['age_days'],DCR_hash['age_days'],
    BTC_hash['age_days'],DCR_hash['age_days'],
    BTC_hash['age_days'],DCR_hash['age_days'],
    ]
y_data = [
    BTC_hash['DiffMean'],DCR_hash['DiffMean'],
    BTC_hash['pow_hashrate_THs']*1000,DCR_hash['pow_hashrate_THs_avg'],
    BTC_hash['CapMrktCurUSD'],DCR_hash['CapMrktCurUSD'],
    ]
name_data = [
    'Bitcoin Difficulty','Decred Difficulty',
    'Bitcoin Hashrate','Decred Hashrate',
    'Bitcoin Market Cap','Decred Market Cap',
    ]
color_data = [
    'rgb(255, 102, 0)' , 'rgb(46, 214, 161)' ,
    'rgb(65, 191, 83)','rgb(254, 215, 140)',
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
    1,1,1,1,0.5,0.5
    ]
legend_data = [
    True,True,True,True,True,True,
    ]#
title_data = [
    'Proof of Work Growth',
    'Coin Age (Days since Launch)',
    'Protocol Difficulty',
    'Network Hashrate (TH/s)']
range_data = [[0,12*365],[0,14],[-6,9]]
autorange_data = [True,False,True]
type_data = ['linear','log','log']#
fig = check_standard_charts('dark').subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_xaxes(dtick=365)
fig.show()



"""
#############################################################################
                    FINALITY RATIO
#############################################################################
Calculate and plot the real time difference in protocol finality between
Bitcoin and Decred
Ratio on date
DCR Daily cost / BTC Daily Cost --> block for block (x2 for time for time or btc blocks)
"""

BTC_final = BTC_subs[['date','Unforg_Cost_Daily']]
BTC_final.columns = ['date','BTC_Unforg_Cost_Daily']

DCR_final = DCR_subs.merge(BTC_final,left_on='date',right_on='date')

DCR_final['Finality_Ratio_5%']  = (
    DCR_final['Unforg_Cost_5%_Daily'] / DCR_final['BTC_Unforg_Cost_Daily']
)
DCR_final['Finality_Ratio_10%'] = (
    DCR_final['Unforg_Cost_10%_Daily'] / DCR_final['BTC_Unforg_Cost_Daily']
)
DCR_final['Finality_Ratio_15%'] = (
    DCR_final['Unforg_Cost_15%_Daily'] / DCR_final['BTC_Unforg_Cost_Daily']
)
DCR_final['Finality_Ratio_30%'] = (
    DCR_final['Unforg_Cost_30%_Daily'] / DCR_final['BTC_Unforg_Cost_Daily']
)
DCR_final['Finality_Ratio_50%'] = (
    DCR_final['Unforg_Cost_50%_Daily'] / DCR_final['BTC_Unforg_Cost_Daily']
)
DCR_final['Finality_Ratio_75%'] = (
    DCR_final['Unforg_Cost_75%_Daily'] / DCR_final['BTC_Unforg_Cost_Daily']
)


loop_data = [[0,1,2,3,4,5],[]]
x_data = [
    DCR_final['date'],
    DCR_final['date'],
    DCR_final['date'],
    DCR_final['date'],
    DCR_final['date'],
    DCR_final['date'],
    ]
y_data = [
    DCR_final['Finality_Ratio_5%'].rolling(7).mean(),
    DCR_final['Finality_Ratio_10%'].rolling(7).mean(),
    DCR_final['Finality_Ratio_15%'].rolling(7).mean(),
    DCR_final['Finality_Ratio_30%'].rolling(7).mean(),
    DCR_final['Finality_Ratio_50%'].rolling(7).mean(),
    DCR_final['Finality_Ratio_75%'].rolling(7).mean(),
    ]
name_data = [
    'DCR Finality Ratio 5%','DCR Finality Ratio 10%',
    'DCR Finality Ratio 15%','DCR Finality Ratio 30%',
    'DCR Finality Ratio 50%','DCR Finality Ratio 75%',
    ]
color_data = [
    'rgb(1, 255, 116)','rgb(156,225,43)', 
    'rgb(255, 255, 102)','rgb(255, 153, 102)',
    'rgb(255, 102, 102)','rgb(255, 80, 80)',
    ]
dash_data = [

    'solid','solid',
    'solid','solid',
    'solid','solid',
    ]
width_data = [
    2,2,2,2,2,2,
    ]
opacity_data = [
    1,1,1,1,1,1,
    ]
legend_data = [
    True,True,True,
    True,True,True,
    ]#
title_data = [
    'Decred Finality Ratio',
    'Date',
    'DCR/BTC Daily Attack Cost Ratio',
    'Pure PoW Premium Ratio']
range_data = [[0,1],[4,12],[-1,5]]
autorange_data = [True,True,False]
type_data = ['date','log','log']#
fig = check_standard_charts('dark').subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
#fig.update_xaxes(dtick=0.1)
fig.show()