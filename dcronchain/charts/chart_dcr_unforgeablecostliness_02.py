#Compare the Usage adoption metrics for Decred and Bitcoin
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.general.general_helpers import *


class dcr_unforgeable_costliness():

    def __init__(self):
        self.chart = check_standard_charts('light')
        #Calculate dataframes
        self.df_btc = btc_add_metrics().btc_real()
        self.DCR = dcr_add_metrics().dcr_ticket_models()

    def df_calcs(self):
        #Calculate Unforgeable Costliness (cummulative Sum)
        self.df_btc['Unforg_Cost'] = self.df_btc['DailyIssuedUSD'].cumsum()
        self.DCR['PoW_Cost'] = self.DCR['PoW_income_usd'].cumsum()
        self.DCR['PoS_Cost'] = self.DCR['PoS_income_usd'].cumsum()

        #Calculate Unforgeable Costliness (cummulative Sum)
        self.df_btc['Unforg_Cost_Daily'] = self.df_btc['PoW_income_usd']
        self.DCR['PoW_Cost_Daily'] = self.DCR['PoW_income_usd']
        self.DCR['PoS_Cost_Daily'] = self.DCR['PoS_income_usd']
