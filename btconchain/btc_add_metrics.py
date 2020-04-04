# Calculate a Suite of Bitcoin Specific Metrics
#Data Science
import pandas as pd
import numpy as np
import math
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

import quandl

from checkonchain.general.coinmetrics_api import *
from checkonchain.general.regression_analysis import *
from checkonchain.btconchain.btc_schedule import *
from checkonchain.general.general_helpers import *


class btc_add_metrics():

    def __init__(self):
        self.topcapconst = 35 #Top Cap = topcapconst * Avg Cap
        self.blkrew_ratio = [1.0] #PoW Reward Fraction
        self.sply_curtail = 144 #Supply curtailed to once a day

    def btc_coin(self):
        """Pulls Coinmetrics v2 API Community,
            adds early price data by Plan B (fills backwards)
        """
        df = Coinmetrics_api('btc',"2009-01-03",today).convert_to_pd()
        #Coin age in days
        df['age_days'] = (df[['date']] - df.loc[0,['date']])/np.timedelta64(1,'D')
        #Coin age in supply issuance
        df['age_sply'] = df['SplyCur'] / 21e6
        #Add in Plan B Data for Price and Market Cap
        #Create dataframe with Plan B price data before Coinmetrics has it
        print('...adding monthly Plan B PriceUSD and CapMrktCurUSD 2009-10...')
        planB_data = [
            ['01-10-2009',0.000763941940412529],
            ['01-11-2009',0.002],
            ['01-12-2009',0.002],
            ['01-01-2010',0.002],
            ['01-02-2010',0.002],
            ['01-03-2010',0.003],
            ['01-04-2010',0.0035],
            ['01-05-2010',0.0041],
            ['01-06-2010',0.04],
            ['01-07-2010',0.07]
            ]
        df_planB = pd.DataFrame(data=planB_data,columns=['date','PriceUSD'])
        df_planB['date'] = pd.to_datetime(df_planB['date'],utc=True)
        #Populate Price and fill backwards
        df['notes'] = str('')
        for i in df_planB['date']:
            df.loc[df.date==i,'PriceUSD'] = float(df_planB.loc[df_planB.date==i,'PriceUSD'])
        df['PriceUSD'] = df['PriceUSD'].fillna(method='bfill')
        for i in df_planB['date']:
            df.loc[df.date==i,'CapMrktCurUSD'] = df.loc[df.date==i,'PriceUSD'] * df.loc[df.date==i,'SplyCur']
            df.loc[df.date==i,'notes'] = 'PriceUSD and CapMrktCurUSD from Plan B data (@100TrillionUSD)'
        #Restructure final dataset
        df = df[[
            'date', 'blk','age_days','age_sply',
            'DailyIssuedNtv', 'DailyIssuedUSD', 'inf_pct_ann', 'S2F',
            'AdrActCnt', 'BlkCnt', 'BlkSizeByte', 'BlkSizeMeanByte',
            'CapMVRVCur', 'CapMrktCurUSD', 'CapRealUSD', 'DiffMean', 'HashRate',
            'FeeMeanNtv','FeeMeanUSD', 'FeeMedNtv', 'FeeMedUSD', 'FeeTotNtv', 'FeeTotUSD',
            'PriceBTC', 'PriceUSD', 'PriceRealUSD', 'SplyCur',
            'TxCnt', 'TxTfrCnt', 'TxTfrValAdjNtv', 'TxTfrValAdjUSD',
            'TxTfrValMeanNtv', 'TxTfrValMeanUSD', 'TxTfrValMedNtv',
            'TxTfrValMedUSD', 'TxTfrValNtv', 'TxTfrValUSD',
            'notes'
            ]]
        return df


    def btc_sply(self,to_blk):
        df = btc_supply_schedule(to_blk).btc_supply_function()
        #Calculate projected S2F Models Valuations
        btc_s2f_model = regression_analysis().regression_constants()['btc_s2f']
        df['CapS2Fmodel'] = np.exp(
            float(btc_s2f_model['coefficient'])
            * np.log(df['S2F_ideal'])
            + float(btc_s2f_model['intercept'])
        )
        df['PriceS2Fmodel'] = df['CapS2Fmodel']/df['Sply_ideal']
        #Calc S2F Model - Bitcoins Plan B Model
        planb_s2f_model = regression_analysis().regression_constants()['planb']
        df['PricePlanBmodel'] = np.exp(
            float(planb_s2f_model['coefficient'])
            * np.log(df['S2F_ideal'])
            + float(planb_s2f_model['intercept'])
        )
        df['CapPlanBmodel'] = df['PricePlanBmodel']*df['Sply_ideal']
        return df
    

    def btc_sply_curtailed(self,to_blk):
        """Curtail theoretical supply curve for charting"""
        btc_sply_interval = self.sply_curtail
        df = self.btc_sply(to_blk)
        return df.iloc[::btc_sply_interval,:] #Select every 144 blocks

    def btc_sply_halvings_step(self):
        """Calculate btc supply halvings for plotting"""
        df = btc_supply_schedule(0).btc_halvings_stepped()
        df['age_sply'] = df['end_sply']/21e6
        return df #Select every 144 blocks


    def btc_real(self):
        """Coinmetrics + Hashrate from QUANDL"""
        print('...compiling Bitcoin specific metrics (coinmetrics + supply curve)...')
        _coin = self.btc_coin()
        _blk_max = int(_coin['blk'][_coin.index[-1]])
        df = _coin[[
            'date', 'blk','BlkCnt', 'age_days','age_sply',                                   #Time Metrics
            'CapMrktCurUSD', 'CapRealUSD', 'PriceUSD', 'PriceRealUSD',              #Value Metrics
            'DailyIssuedNtv', 'DailyIssuedUSD','AdrActCnt','TxCnt', 'TxTfrCnt',     #Block Reward Metrics
            'TxTfrValAdjNtv', 'TxTfrValAdjUSD', 'TxTfrValNtv', 'TxTfrValUSD',       #Global Transaction Metrics
            'TxTfrValMeanNtv', 'TxTfrValMeanUSD', 'TxTfrValMedNtv','TxTfrValMedUSD',#Local Transaction Metrics             
            'FeeTotNtv','FeeTotUSD',                                                #Fee Metrics
            'S2F','inf_pct_ann', 'SplyCur',                                         #Supply Metrics
            'DiffMean', 'HashRate','notes'                                          #PoW Metrics
        ]]
        general_helpers.df_to_csv(df,'BTC_data')
        return df

    def btc_hash(self):
        #QUANDL has 50 daily query limit
        #Hashrate (GH/s --> 0.001 TH/s)
        _real = self.btc_real()
        df = pd.DataFrame()
        df['pow_hashrate_THs'] = quandl.get("BCHAIN/HRATE")['Value'] #Pull hashrate data
        df['date'] = df.index 
        df = df.reset_index(drop=True)
        df['date'] = pd.to_datetime(df['date'],utc=True)
        df = pd.merge(_real,df,on='date')
        return df

    def btc_subsidy_models(self):
        print('...Calculating Bitcoin block subsidy models...')
        df = self.btc_real()
        #Calculate PoS Return on Investment
        df['PoW_income_btc']    = df['DailyIssuedNtv']
        df['PoW_income_usd']    = df['PoW_income_btc'] * df['PriceUSD']
        return df

    def btc_pricing_models(self):
        print('...Calculating Bitcoin pricing models...')
        _real = self.btc_subsidy_models()
        df = _real

        # Average Cap and Average Price
        df['CapAvg'] = df['CapMrktCurUSD'].fillna(0.0001) #Fill not quite to zero for Log charts/calcs
        df['CapAvg'] = df['CapAvg'].expanding().mean()
        df['PriceAvg'] = df['CapAvg']/df['SplyCur']
        # Delta Cap and Delta Price
        df['CapDelta'] = df['CapRealUSD'] - df['CapAvg']
        df['PriceDelta'] =df['CapDelta']/df['SplyCur']
        # Top Cap and Top Price
        df['CapTop'] = df['CapAvg']*self.topcapconst
        df['PriceTop'] =df['CapTop']/df['SplyCur']

        #Calc S2F Model - Specific to Bitcoin
        btc_s2f_model = regression_analysis().ln_regression(df,'S2F','PriceUSD','date')['model_params']
        df['PriceS2Fmodel'] = (
            np.exp(float(btc_s2f_model['intercept']))
            * df['S2F']**float(btc_s2f_model['coefficient'])
            )
        df['CapS2Fmodel'] = df['PriceS2Fmodel']*df['SplyCur']
        #Calc S2F Model - Bitcoins Plan B Model
        planb_s2f_model = regression_analysis().regression_constants()['planb']
        df['PricePlanBmodel'] = np.exp(-1.84)*df['S2F']**3.36
        df['CapPlanBmodel'] = df['PricePlanBmodel']/df['SplyCur']

        #Calc Diff Model - Specific to Bitcoin
        btc_diff_model = regression_analysis().ln_regression(df,'DiffMean','CapMrktCurUSD','date')['model_params']
        df['CapDiffmodel'] = np.exp(float(btc_diff_model['coefficient'])*np.log(df['DiffMean'])+float(btc_diff_model['intercept']))
        df['PriceDiffmodel'] = df['CapDiffmodel']/df['SplyCur']

        # Inflow Cap and Inflow Price
        df['CapInflow'] = df['DailyIssuedUSD'].expanding().sum()
        df['PriceInflow'] =df['CapInflow']/df['SplyCur']
        
        # Fee Cap and Fee Price
        df['CapFee'] = df['FeeTotUSD'].expanding().sum()
        df['PriceFee'] =df['CapFee']/df['SplyCur']

        #Calculate Miner Income
        df['MinerIncome'] = df['CapInflow'] + df['CapFee']
        df['FeesPct'] =  df['CapFee']/df['MinerIncome']
        df['MinerCap'] = df['MinerIncome'].expanding().sum()

        #Moving Averages (Magic Lines)
        df['PriceUSD_128DMA'] = df['PriceUSD'].rolling(128).mean()
        df['PriceUSD_200DMA'] = df['PriceUSD'].rolling(200).mean()
        df['PriceUSD_128WMA'] = df['PriceUSD'].rolling(896).mean()
        df['PriceUSD_200WMA'] = df['PriceUSD'].rolling(1400).mean()
        return df

    def btc_oscillators(self):
        print('...Calculating Bitcoin Oscillators...')
        _pricing = self.btc_pricing_models()
        df = _pricing        
        #Calc - NVT_28, NVT_90, NVTS, RVT_28, RVT_90, RVTS
        df['NVT_28'] = df['CapMrktCurUSD'].rolling(28).mean()/ df['TxTfrValUSD'].rolling(28).mean()
        df['NVT_90'] = df['CapMrktCurUSD'].rolling(90).mean()/df['TxTfrValUSD'].rolling(90).mean()
        df['NVTS']   = df['CapMrktCurUSD']/ df['TxTfrValUSD'].rolling(28).mean()
        df['RVT_28'] = df['CapRealUSD'].rolling(28).mean()/ df['TxTfrValUSD'].rolling(28).mean()
        df['RVT_90'] = df['CapRealUSD'].rolling(90).mean()/df['TxTfrValUSD'].rolling(90).mean()
        df['RVTS']   = df['CapRealUSD']/ df['TxTfrValUSD'].rolling(28).mean()

        #Mayer Multiple
        df['MayerMultiple'] = df['PriceUSD']/df['PriceUSD_200DMA']
        df['S2FMultiple'] = df['PriceUSD']/df['PricePlanBmodel']
        df['DiffMultiple'] = df['PriceUSD']/df['PriceDiffmodel']

        df['Puell_Multiple'] = (
            df['DailyIssuedUSD']
            / df['DailyIssuedUSD'].rolling(365).mean()
        )
        return df

#BTC_subs = btc_add_metrics().btc_oscillators()
#BTC_real = btc_add_metrics().btc_real()

