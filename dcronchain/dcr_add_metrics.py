# Calculate a Suite of Decred Specific Metrics
#Data Science
import pandas as pd
import numpy as np
import math
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

from checkonchain.general.coinmetrics_api import * #Coinmetrics.io
from checkonchain.general.regression_analysis import *
from checkonchain.dcronchain.dcr_schedule import * #DCR Schedule
from checkonchain.dcronchain.dcr_dcrdata_api import * #DCRdata.org
from checkonchain.general.general_helpers import *

import os
os.getcwd()
os.chdir('D:\code_development\checkonchain\checkonchain')


class dcr_add_metrics():
    """
    Functions for building Pandas DataFrames of Decred specific metrics
    Aggregates data from supported APIs and calculates Decred specific metrics
        - Coinmetrics Community
        - dcrdata

    Functions Available
    dcr_coin            = coinmetrics community with supplemented price data from early data sources
    dcr_sply            = theoretical supply curve with added S2F model
    dcr_sply_curtailed  = dcr_sply curtailed to 0.667 days to reduce df size (reduce load on charts)
    dcr_diff            = dcrdata difficulty for PoS and PoW. Data setup in 144 block windows 
                            ['blk','window','time','tic_cnt_window','tic_price','tic_miss','pow_diff']
    dcr_perf            = dcrdata blockchain performance 
                            ['blk','time','dcr_sply','dcr_tic_sply','tic_part','tic_pool','tic_blk',
                            'pow_hashrate_THs','pow_work_EH']
    dcr_natv            = dcrdata blockchain combination of dcr_perf and dcr_diff (by block) 
                            ['blk', 'window','tic_cnt_window', 'tic_price', 'tic_blk', 'tic_pool',
                            'dcr_tic_sply', 'dcr_sply','pow_diff','pow_hashrate_THs', 'pow_work_TH']
    dcr_real            = Compiles Coinmetrics (dcr_coin) and dcrdata (dcr_natv) for general data analytics
    dcr_subsidy_models  = Follows dcr_real, adds income for PoW, PoS, Fund and Total priced in dcr, btc and usd
    dcr_ticket_models   = Follows dcr_subsidy_models, ticket based transaction models
    """
    
    def __init__(self):
        self.topcapconst    = 12 #Top Cap = topcapconst * Avg Cap
        self.blkrew_ratio   = [0.6,0.3,0.1] #PoW,PoS,Fund Block Reward Fraction
        self.sply_curtail   = 6144 / 4 #reduce dataset = 5.33days
        self.dust_limit     = 100 #set Decred dust limit in bytes

    def dcr_coin(self): 
        """
        Pulls Coinmetrics v2 API Community
            - adds coin age metric (days)
            - adds coin age metric (supply) = Supply / 21M
            - adds Bittrex early price data not included in coinmetrics from csv

            OUTPUT DATAFRAME COLUMNS:
            'date', 'blk','age_days','age_sply','btc_blk_est',
            'BlkSizeByte', BlkSizeMeanByte',
            'DailyIssuedNtv', 'DailyIssuedUSD', 'inf_pct_ann', 'S2F',
            'AdrActCnt', 'BlkCnt', 'BlkSizeByte', 'BlkSizeMeanByte',
            'CapMVRVCur', 'CapMrktCurUSD', 'CapRealUSD','CapRealBTC', 'DiffMean', 'CapMVRVCur',
            'FeeMeanNtv','FeeMeanUSD', 'FeeMedNtv', 'FeeMedUSD', 'FeeTotNtv', 'FeeTotUSD',
            'PriceBTC', 'PriceUSD', 'PriceRealUSD','PriceRealBTC', 'BTC_PriceUSD', 'SplyCur',
            'TxCnt', 'TxTfrCnt', 'TxTfrValAdjNtv', 'TxTfrValAdjUSD',
            'TxTfrValMeanNtv', 'TxTfrValMeanUSD', 'TxTfrValMedNtv',
            'TxTfrValMedUSD', 'TxTfrValNtv', 'TxTfrValUSD',
            'notes'
        """    
        df = Coinmetrics_api('dcr',"2016-02-08",today).convert_to_pd()
        #Calculate coin age since launch in days
        df['age_days'] = (df[['date']] - df.loc[0,['date']])/np.timedelta64(1,'D')
        #Calculate coin age since launch in terms of supply
        df['age_sply'] = df['SplyCur'] / 21e6
        print('...adding PriceUSD and CapMrktCurUSD for $0.49 (founders, 8/9-Feb-2016)')
        print('and Bittrex (10-02-2016 to 16-05-2016)...')
        #Import Early price data --> 
        #   founders $0.49 for 8/9 Feb 2016  
        #   Bitrex up to 16-May-2016 (saved in relative link csv)
        df_early = pd.read_csv(r"dcronchain\\resources\\data\\dcr_pricedata_2016-02-08_2016-05-16.csv")
        df_early['date'] = pd.to_datetime(df_early['date'],utc=True) #Convert to correct datetime format
        df['notes'] = str('') # add notes for storing data
        for i in df_early['date']: #swap in early price data
            #Add Early PriceUSD Data
            df.loc[df.date==i,'PriceUSD'] = float(
                df_early.loc[df_early.date==i,'PriceUSD']
            )
            #Add Early PriceBTC Data
            df.loc[df.date==i,'PriceBTC'] = float(
                df_early.loc[df_early.date==i,'PriceBTC']
            )
            #Add Early MarketCap Data
            df.loc[df.date==i,'CapMrktCurUSD'] = (
                df.loc[df.date==i,'PriceUSD'] * 
                df.loc[df.date==i,'SplyCur']
            )
            #Add Notes
            df.loc[df.date==i,'notes'] = df_early.loc[df_early.date==i,'notes']
        #Populate Columns which early prices feed into
        df = general_helpers.early_price_metric(df,'DailyIssuedUSD','DailyIssuedNtv')
        df = general_helpers.early_price_metric(df,'FeeTotUSD','FeeTotNtv')
        df = general_helpers.early_price_metric(df,'FeeMeanUSD','FeeMeanNtv')
        df = general_helpers.early_price_metric(df,'FeeMedUSD','FeeMedNtv')
        df = general_helpers.early_price_metric(df,'TxTfrValAdjUSD','TxTfrValAdjNtv')
        df = general_helpers.early_price_metric(df,'TxTfrValUSD','TxTfrValNtv')
        df = general_helpers.early_price_metric(df,'TxTfrValMeanUSD','TxTfrValMeanNtv')
        df = general_helpers.early_price_metric(df,'TxTfrValMedUSD','TxTfrValMedNtv')
        
        #Calculate Realised Cap and Price in BTC
        df['BTC_PriceUSD'] = df['PriceUSD'] / df['PriceBTC'] #BTC Price USD
        df['CapMrktCurBTC'] = df['SplyCur'] * df['PriceBTC']
        df['CapRealBTC']   = df['CapRealUSD'].diff(periods=1) / df['BTC_PriceUSD']
        df['CapRealBTC']   = df['CapRealBTC'].cumsum()
        df['PriceRealBTC'] = df['CapRealBTC'] / df['SplyCur']

        # Restructure final dataset
        df = df[[
            'date', 'blk','age_days','age_sply','btc_blk_est',
            'BlkSizeByte', 'BlkSizeMeanByte',
            'DailyIssuedNtv', 'DailyIssuedUSD', 'inf_pct_ann', 'S2F',
            'AdrActCnt', 'BlkCnt', 'BlkSizeByte', 'BlkSizeMeanByte',
            'CapMVRVCur', 'CapMrktCurUSD', 'CapMrktCurBTC', 'CapRealUSD','CapRealBTC', 'DiffMean', 
            'FeeMeanNtv','FeeMeanUSD', 'FeeMedNtv', 'FeeMedUSD', 'FeeTotNtv', 'FeeTotUSD',
            'PriceBTC', 'PriceUSD', 'PriceRealUSD','PriceRealBTC', 'BTC_PriceUSD', 'SplyCur',
            'TxCnt', 'TxTfrCnt', 'TxTfrValAdjNtv', 'TxTfrValAdjUSD',
            'TxTfrValMeanNtv', 'TxTfrValMeanUSD', 'TxTfrValMedNtv',
            'TxTfrValMedUSD', 'TxTfrValNtv', 'TxTfrValUSD',
            'notes'
            ]]
        #Reformat datetime
        #df['date'] = df['date'].dt.strftime('%d-%m-%y')
        return df

    def dcr_diff(self):
        """
        Pulls dcrdata Difficulty data
        Data is arranged by difficulty window (144 blocks)
        OUTPUT COLUMNS:
            'blk'           - block height
            'window'        - windoc count (count if 144 windows)
            'time'          - time (timestamp)
            'tic_cnt_window'- Tickets bought in window (max 2880)
            'tic_price'     - Ticket Price | Stake Difficulty (DCR)
            'tic_miss'      - Tickets missed in window
            'pow_diff'      - PoW Difficulty
        """
        df = dcrdata_api().dcr_difficulty()
        return df

    def dcr_perf(self):
        """
        Pulls dcrdata Performance data
        Data is arranged by block
        OUTPUT COLUMNS:
            'blk'               - block height
            'time'              - time (timestamp)
            'dcr_sply'          - circulating supply (DCR)
            'dcr_tic_sply'      - ticket pool value (DCR)
            'tic_blk'           - Tickets bought per block (max 20)
            'tic_pool'          - Tickets in the pool (40,960 target)
            'pow_hashrate_THs'  - PoW Hashrate in Terahash/s
            'pow_work_TH'       - Cummulative work (TH/s)
        """
        df = dcrdata_api().dcr_performance()
        return df

    def dcr_priv(self):
        """
        Pulls dcrdata Privacy data
        Data is arranged by day
        OUTPUT COLUMNS:
            'blk'               - block height
            'time'              - time (timestamp)
            'dcr_sply'          - circulating supply (DCR)
            'dcr_anon_sply'     - anonymity pool value (DCR)
            'dcr_anon_part'     - Anonymity participation (anon pool / circ. supply)
            'dcr_anon_mix_vol'  - Daily DCR mixed
        """
        df = dcrdata_api().dcr_privacy()
        return df
    
    def dcr_natv(self):
        """
        Compile dcrdata sets dcr_diff and dcr_perf (Final dataset is by block)
            Difficulty is filled backwards (step function)
        OUTPUT COLUMNS:
            As per dcr_diff and ddcr_perf (not repeated for brevity)
            Dropped 'time' and 'tic_miss'
        """
        _diff = self.dcr_diff() #Pull dcrdata difficulty
        _perf = self.dcr_perf() #Pull dcrdata performance
        # DCR_natv = merge _diff (by window) to _perf (by blk)
        df = pd.merge(
            _perf.drop(['time'],axis=1),
            _diff.drop(['time','tic_miss'],axis=1),
            on='blk',how='left')
        # Fill backwards for difficulty metrics
        df[['tic_price','pow_diff','window']] = df[
            ['tic_price','pow_diff','window']
            ].fillna(method='bfill')
        # Restructure final dataset
        df = df[[
            'blk', 'window',
            'tic_cnt_window', 'tic_price', 'tic_blk', 'tic_pool',
            'dcr_tic_sply', 'dcr_sply',
            'pow_diff','pow_hashrate_THs', 'pow_work_TH'
        ]]
        return df

    def dcr_sply(self,to_blk): #Calculate Theoretical Supply Curve
        """
        Calculates the theoretical supply curve by block height
        INPUTS:
            to_blk      = Integer, block height to calcuate up to (from 0)
        OUTPUT COLUMNS:
            'blk'               - block height
            'blk_reward'        - Total block reward
            'Sply_ideal'        - Ideal Total Supply (DCR)
            'PoWSply_ideal'     - Ideal PoW Issued Supply (DCR)
            'PoSSply_ideal'     - Ideal PoS Issued Supply incl. 4% Premine (DCR)
            'FundSply_ideal'    - Ideal Treasury Issued Supply incl. 4% Premine (DCR)
            'inflation_ideal'   - Idealised Inflation Rate
            'S2F_ideal'         - Idealised Stock-to-Flow Ratio
        """
        df = dcr_supply_schedule(to_blk).dcr_supply_function()
        return df

    def dcr_sply_curtailed(self,to_blk):
        """
        Curtail theoretical supply curve (dcr_sply) to reduce load on charting packages
        INPUTS:
            to_blk      = Integer, block height to calcuate up to (from 0)
        OUTPUT COLUMNS:
            As per dcr_sply (not repeated for brevity)
        """
        df = self.dcr_sply(to_blk)
        df = df.iloc[::int(self.sply_curtail), :] #Select every 
        return  df

    def dcr_real(self):
        """
        Compiles Coinmetrics (dcr_coin) and dcrdata (dcr_natv) for general data analytics
        OUTPUT COLUMNS:
            TIME VARIABLES
                'date'                  - Datetime 
                'blk'                   - Block Height
                'age_days'              - Coin Age in Days
                'age_sply'              - Coin age in Supply (SplyCur/21M)
                'window'                - Count of difficulty window
                'BlkSizeByte'           - Daily Total Block Size (bytes)
                'BlkSizeMeanByte'       - Avg Block Size (bytes)
                'CapMrktCurUSD'         - Market Cap (USD)
                'CapMrktCurBTC'         - Market Cap (BTC)
                'CapRealUSD'            - Realised Cap (USD)
                'CapRealBTC'            - Realised Cap (BTC)
                'CapMVRVCur'            - MVRV Ratio
                'PriceBTC'              - Price in BTC
                'PriceUSD'              - Price in USD
                'PriceRealUSD'          - Realised Price (USD)
                'PriceRealBTC'          - Realised Price (BTC)
                'BTC_PriceUSD'          - BTC Price
                'DailyIssuedNtv'        - Daily DCR Issued
                'DailyIssuedUSD'        - Daily Issued USD
                'AdrActCnt'             - Active Address Count
                'TxTfrValNtv'           - Daily Transferred DCR
                'TxTfrValUSD'           - Daily Transferred USD
                'TxTfrValAdjNtv'        - Daily Transferred DCR (Adjusted for noise)
                'TxTfrValAdjUSD'        - Daily Transferred USD (Adjusted for noise)
                'TxTfrValMedNtv'        - Median DCR Transaction
                'TxTfrValMeanNtv'       - Mean DCR Transaction
                'TxCnt'                 - Daily transaction count (Full count incl 0 DCR Tx)
                'TxTfrCnt'              - Daily Transfer count (transfer of non-zero DCR)
                'FeeTotNtv'             - Total Fees DCR
                'FeeTotUSD'             - Total Fees USD
                'S2F'                   - Actual Stock-to-Flow Ratio
                'inf_pct_ann'           - Annual Inflation Rate
                'SplyCur'               - DCR Supply (Coinmetrics)
                'dcr_sply'              - DCR Supply (dcrdata)
                'dcr_tic_sply_avg'      - Average DCR Supply locked in Tickets over day
                'tic_day'               - Number of Tickets purchased that day
                'tic_price_avg'         - Average ticket price over the day
                'tic_pool_avg'          - Number of tickets in Pool (Target 40,960)
                'DiffMean'              - Average PoW Difficulty on day (Coinmetrics)
                'pow_diff_avg'          - Average PoW Difficulty on day (dcrdata)
                'pow_hashrate_THs_avg'  - Average PoW Hashrate on day (TH/s)
                'pow_work_TH'           - Cumulative PoW in TH
                'dcr_anon_sply'         - Total DCR in anonymity set
                'dcr_anon_part'         - Privacy Participation (dcr_anon_sply/dcr_sply)
                'dcr_anon_mix_vol'      - Daily mixing volume (DCR)
        """
        print('...Combining Decred specific metrics - (coinmetrics + dcrdata)...')
        _coin = self.dcr_coin() #Coinmetrics by date
        _natv = self.dcr_natv() #dcrdata API by block
        _priv = self.dcr_priv() #Pull dcrdata privacy
        #_blk_max = int(_coin['blk'][_coin.index[-1]])
        #Cull _coin to Key Columns
        _coin = _coin[[
            'date','blk','age_days','age_sply',
            'BlkSizeByte', 'BlkSizeMeanByte',
            'CapMrktCurUSD','CapMrktCurBTC','CapRealUSD','CapRealBTC','CapMVRVCur',
            'DiffMean','PriceBTC','PriceUSD','PriceRealUSD','PriceRealBTC','BTC_PriceUSD',
            'SplyCur','DailyIssuedNtv','DailyIssuedUSD','S2F',
            'inf_pct_ann','TxCnt','TxTfrCnt','TxTfrValMedNtv','TxTfrValMeanNtv',
            'TxTfrValNtv','TxTfrValUSD','TxTfrValAdjNtv','TxTfrValAdjUSD',
            'FeeTotNtv','FeeTotUSD','AdrActCnt']]
        
        #Add new columns for transferring _natv data to_coin
        _coin['tic_day']                = 0.0
        _coin['tic_price_avg']          = 0.0
        _coin['tic_pool_avg']           = 0.0
        _coin['dcr_tic_sply_avg']       = 0.0
        _coin['pow_diff_avg']           = 0.0
        _coin['pow_hashrate_THs_avg']   = 0.0
        blk_from = 0    #Captures last _coin block (block from)
        _row = 0        #Captures current block height (natv is by block)
        for i in _coin['blk']:
            #Sum tickets bought on the day
            _coin.loc[_row,['tic_day']]         = (
                float(_natv.loc[blk_from:i,['tic_blk']].sum()) #tickets bought that day
            )
            #Average Ticket price over day
            _coin.loc[_row,['tic_price_avg']]   = (
                float(_natv.loc[blk_from:i,['tic_price']].mean()) #avg tic price that day
            )
            #Average Tickets in Pool over day
            _coin.loc[_row,['tic_pool_avg']]   = (
                float(_natv.loc[blk_from:i,['tic_pool']].mean()) #avg tic price that day
            )
            #Average DCR Locked in Tickets over day
            _coin.loc[_row,['dcr_tic_sply_avg']]   = (
                float(_natv.loc[blk_from:i,['dcr_tic_sply']].mean()) #avg tic price that day
            )
            #Average PoW Difficulty
            _coin.loc[_row,['pow_diff_avg']]= (
                float(_natv.loc[blk_from:i,['pow_diff']].mean()) #avg hashrate that day
            )
            #Average PoW Hashrate in TH/s
            _coin.loc[_row,['pow_hashrate_THs_avg']]= (
                float(_natv.loc[blk_from:i,['pow_hashrate_THs']].mean()) #avg hashrate that day
            )
            blk_from = i
            _row += 1
        #Merge _coin and _natv
        df = pd.merge(
            _coin,
            _natv.drop(
                ['tic_cnt_window','pow_diff','pow_hashrate_THs','tic_pool','dcr_tic_sply'],axis=1
                ),on='blk',how='left'
            )
        #Merge df with _priv (on date)
        df = pd.merge(
            df,
            _priv.drop(['time','dcr_sply'],axis=1),
            on='date',how='left')
        #Compile into final ordered dataframe
        df = df[[
            'date', 'blk', 'age_days','age_sply','window',                              #Time Metrics
            'BlkSizeByte', 'BlkSizeMeanByte',                                           #Blockchain Size Metrics
            'CapMrktCurUSD', 'CapMrktCurBTC', 'CapRealUSD','CapRealBTC','CapMVRVCur',   #Value Metrics
            'PriceBTC', 'PriceUSD', 'PriceRealBTC',  'PriceRealUSD','BTC_PriceUSD',     #Price Metrics
            'DailyIssuedNtv','DailyIssuedUSD','AdrActCnt','TxCnt','TxTfrCnt',           #Block Reward Metrics
            'TxTfrValNtv','TxTfrValUSD','TxTfrValAdjNtv','TxTfrValAdjUSD',              #Global Transaction Metrics
            'TxTfrValMedNtv','TxTfrValMeanNtv',                                         #Local Transaction Metrics
            'FeeTotNtv','FeeTotUSD',                                                    #Fee Metrics
            'S2F', 'inf_pct_ann','SplyCur', 'dcr_sply',                                 #Supply Metrics
            'dcr_tic_sply_avg','tic_day', 'tic_price_avg', 'tic_pool_avg',              #Ticket Metrics
            'DiffMean','pow_diff_avg', 'pow_hashrate_THs_avg', 'pow_work_TH',           #PoW Metrics
            'dcr_anon_sply', 'dcr_anon_part','dcr_anon_mix_vol'                        #Privacy Metrics
            ]]
        general_helpers.df_to_csv(df,'DCR_data')
        return df

    def dcr_subsidy_models(self):
        """
        Calculates DataFrame Cols for Decred block subsidy Models (Permabull Nino, 2019)
            Note 'X' in col name can be replaced by dcr, usd, btc for different metrics
            Results are daily, applying .cumsum() will provide lifetime aggregate
            Starting df = dcr_real
        OUTPUT COLUMNS: 
            'PoW_income_X'      = Daily subsidy paid to PoW Miners
            'PoS_income_X'      = Daily subsidy paid to PoS Stakeholders
            'Fund_income_X'     = Daily subsidy paid to Treasury Fund
            'Total_income_X'    = Total Daily subsidy paid by protocol
        """

        print('...Calculating Decred block subsidy models...')
        df = self.dcr_real()
        #Calculate Block Subsidy Models
        df['PoW_income_dcr']    = df['DailyIssuedNtv'] * self.blkrew_ratio[0] + df['FeeTotNtv']
        df['PoS_income_dcr']    = df['DailyIssuedNtv'] * self.blkrew_ratio[1]
        df['Fund_income_dcr']   = df['DailyIssuedNtv'] * self.blkrew_ratio[2]
        df['Total_income_dcr']  = df['DailyIssuedNtv'] + df['FeeTotNtv']
        
        df['PoW_income_usd']    = df['PoW_income_dcr']   * df['PriceUSD']
        df['PoS_income_usd']    = df['PoS_income_dcr']   * df['PriceUSD']
        df['Fund_income_usd']   = df['Fund_income_dcr']  * df['PriceUSD']
        df['Total_income_usd']  = df['Total_income_dcr'] * df['PriceUSD']

        df['PoW_income_btc']    = df['PoW_income_dcr']   * df['PriceBTC']
        df['PoS_income_btc']    = df['PoS_income_dcr']   * df['PriceBTC']
        df['Fund_income_btc']   = df['Fund_income_dcr']  * df['PriceBTC']
        df['Total_income_btc']  = df['Total_income_dcr'] * df['PriceBTC']
        return df

    def dcr_ticket_models(self):  #Calculate Ticket Based Valuation Metrics
        """
        Calculates Ticket specific metrics for Decred
            Starting df = dcr_subsidy_models
        OUTPUT COLUMNS:
            'dcr_tic_vol'       = Daily DCR Transaction Volume associated with ticket purchases
            'dcr_tfr_vol'       = Daily DCR Transaction Volume Not associated with tickets
            'tic_tfr_vol_ratio' = Ratio of tickets to total DCR transaction volume
            'tic_usd_cost'      = Total Daily USD Spend on Tickets
            'tic_btc_cost'      = Total Daily BTC Spend on Tickets
            'CapTicUSD'         = Ticket Cap, cumulative USD spend on tickets
            'CapTicBTC'         = Ticket Cap, cumulative BTC spend on tickets
            'CapTicPriceUSD'    = Ticket Investment Price (USD) = Ticket Cap / Circulating Supply
            'CapTicPriceBTC'    = Ticket Investment Price (BTC) = Ticket Cap / Circulating Supply
        """
        print('...Calculating Decred Ticket models...')
        df = self.dcr_subsidy_models()
        #Calculate Ticket Volumes On-chain
        #   Daily DCR Transaction Volume associated with ticket purchases
        df['dcr_tic_vol'] = df['tic_day'] * df['tic_price_avg']
        #   Daily DCR Transaction Volume Not associated with tickets
        df['dcr_tfr_vol'] = df['TxTfrValNtv'] - df['dcr_tic_vol']
        #   Ratio of tickets to total DCR transaction volume
        df['tic_tfr_vol_ratio'] = df['dcr_tic_vol'] / df['TxTfrValNtv']

        #Ticket Investment Metrics
        #   Daily USD and BTC Spent on Tickets
        df['tic_usd_cost']  = df['dcr_tic_vol'] * df['PriceUSD']
        df['tic_btc_cost']  = df['dcr_tic_vol'] * df['PriceBTC']
        #   Ticket Cap = cummulative spend on tickets
        df['CapTicUSD']     = df['tic_usd_cost'].cumsum()
        df['CapTicBTC']     = df['tic_btc_cost'].cumsum()
        #   Ticket Investment Price = Ticket Cap / Circulating Supply
        df['CapTicPriceUSD']   = df['CapTicUSD'] / df['SplyCur']
        df['CapTicPriceBTC']   = df['CapTicBTC'] / df['SplyCur']

        #Write to csv for others
        general_helpers.df_to_csv(df,'DCR_tics')
        return df


#DCR_coin = dcr_add_metrics().dcr_coin()
#DCR_diff = dcr_add_metrics().dcr_diff()
#DCR_perf = dcr_add_metrics().dcr_perf()
#DCR_natv = dcr_add_metrics().dcr_natv()
#DCR_priv = dcr_add_metrics().dcr_priv()
#DCR_real = dcr_add_metrics().dcr_real()
#DCR_sply = dcr_add_metrics().dcr_sply(500000)
#DCR_tics = dcr_add_metrics().dcr_ticket_models()