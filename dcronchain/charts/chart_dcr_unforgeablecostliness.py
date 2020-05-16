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












