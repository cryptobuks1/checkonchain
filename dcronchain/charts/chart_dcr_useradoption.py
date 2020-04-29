#Compare the Usage adoption metrics for Decred and Bitcoin
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.general.general_helpers import *


class dcr_user_adoption():
    """
    GOVERNANCE, USER ADOPTION AND RESILIENCE:
    Establish user adoption metrics for the Decred chain
    Three parties involved
    """
    def __init__(self):
        #Chart Theme
        self.chart = check_standard_charts('dark')
        #Compile Input Dataframes
        self.btc = btc_add_metrics().btc_subsidy_models()
        self.dcr = dcr_add_metrics().dcr_ticket_models()
        #Calculate halving lines
        self.btc_half = btc_add_metrics().btc_sply_halvings_step()
        #Cull to first 3 halvings and add nearest date column
        self.btc_half = pd.merge_asof(
            self.btc_half[self.btc_half.index<=6],
            self.btc[['date','SplyCur']],
            left_on='end_sply',
            right_on='SplyCur'
            )
        #Update 2020 Halving
        self.btc_half.loc[5:6,['date']] = pd.to_datetime(np.datetime64('2020-05-13'),utc=True)
        #Add column for coin age in days
        self.btc_half['age_days'] = (
            pd.Series(delta.days for delta in (
                self.btc_half['date'] 
                - pd.to_datetime(np.datetime64('2009-01-09'),utc=True)
            )
        ))
        #Calculate btc hashrate (ss by Coinmetrics 'HashRate' bu author is lazy)
        self.btc['pow_hashrate_THs'] = self.btc['HashRate']
            

    def dcr_user_active_address(self):
        """
        #############################################################################
                            USER METRICS - ACTIVE ADDRESSES
        #############################################################################
        """
        #Adjust Active address by removing extra use of tickets (50% use 4x, 50% use 2x)
        self.dcr['AdrActCntAdj'] = self.dcr['AdrActCnt'] - self.dcr['tic_day'].rolling(7).mean()*3

        loop_data = [[0,1,2],[3,4,5]]
        x_data = [
            self.btc['age_days'],self.dcr['age_days'],self.dcr['age_days'],
            self.btc['age_days'],self.dcr['age_days'],
            self.btc_half['age_days'],    
            ]
        y_data = [
            self.btc['AdrActCnt'],self.dcr['AdrActCntAdj'].rolling(7).mean(),self.dcr['tic_day'].rolling(7).mean()*3,
            self.btc['PriceUSD'],self.dcr['PriceUSD'],
            self.btc_half['y_arb'],
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
        fig = self.chart.subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.show()
        return fig

    def dcr_user_active_address_ratio(self):
        """
        #############################################################################
                        USER METRICS - DCRBTC ACTIVE ADDRESS RATIO (AGE_DAYS)
        #############################################################################
        """

        self.dcr = self.dcr.merge(self.btc[['age_days','AdrActCnt','TxTfrCnt']],on='age_days',how='left',suffixes=('', '_BTC'))
        #DCR_data.rename(columns={'AdrActCnt_y':'AdrActCnt_BTC'}, inplace=True)
        self.dcr['DCRBTC_AdrActCnt'] = self.dcr['AdrActCnt'] / self.dcr['AdrActCnt_BTC']
        self.dcr['DCRBTC_TxTfrCnt'] = self.dcr['TxTfrCnt'] / self.dcr['TxTfrCnt_BTC']


        loop_data = [[1,2,3,0],[]]
        x_data = [
            self.dcr['age_days'],
            [0,5000],[0,5000],[0,5000],
            self.btc_half['age_days']
        ]
        y_data = [
            self.dcr['DCRBTC_AdrActCnt'].rolling(7).mean(),
            [1,1],[0.5,0.5],[0.25,0.25],
            self.btc_half['y_arb']
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
        autorange_data = [False,False,False]
        fig = self.chart.subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )

        fig.show()
        return fig

    def dcr_user_tx_count(self):
        """
        #############################################################################
                            USER METRICS - TRANSACTION COUNTS
        #############################################################################
        """

        loop_data = [[0,1,2],[3,4,5,6]]
        x_data = [
            self.btc['age_days'],self.dcr['age_days'],self.dcr['age_days'],
            self.btc['age_days'],self.dcr['age_days'],self.dcr['age_days'],
            self.btc_half['age_days'],    
            ]
        y_data = [
            self.btc['TxTfrCnt'].rolling(1).mean(),
            self.dcr['TxTfrCnt'].rolling(3).mean(),
            self.dcr['tic_day'].rolling(3).mean()*3,
            self.btc['TxTfrCnt'].cumsum(),
            self.dcr['TxTfrCnt'].cumsum(),
            self.dcr['tic_day'].cumsum()*3,
            self.btc_half['y_arb'],
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
        fig = self.chart.subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.show()
        return fig

    def dcr_user_global_txflow(self):
        """
        #############################################################################
                    USER METRICS - GLOBAL NATIVE UNITS TRANSFERRED
        #############################################################################
        """
        self.dcr['dcr_tic_buy'] = self.dcr['tic_day']*self.dcr['tic_price_avg']

        loop_data = [[0,1,2],[3,4,5,6]]
        x_data = [
            self.btc['age_days'],self.dcr['age_days'],self.dcr['age_days'],
            self.btc['age_days'],self.dcr['age_days'],self.dcr['age_days'],
            self.btc_half['age_days'],    
            ]
        y_data = [
            self.btc['TxTfrValNtv'].rolling(7).mean(),
            self.dcr['TxTfrValNtv'].rolling(7).mean(),
            self.dcr['dcr_tic_buy'].rolling(7).mean(),
            self.btc['TxTfrValNtv'].cumsum(),
            self.dcr['TxTfrValNtv'].cumsum(),
            self.dcr['dcr_tic_buy'].cumsum(),
            self.btc_half['y_arb'],
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
        fig = self.chart.subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.show()
        return fig

    def dcr_user_cum_txval(self):
        """
        #############################################################################
                    USER METRICS - CUMULATIVE VALUE TRANSFERRED
        #############################################################################
        """

        loop_data = [[0,1,2,3,4,5],[7,8,6]]
        x_data = [
            self.btc['age_days'],self.dcr['age_days'],self.dcr['age_days'],
            self.btc['age_days'],self.dcr['age_days'],self.dcr['age_days'],
            self.btc_half['age_days'],
            self.btc['age_days'],self.dcr['age_days']    
            ]
        y_data = [
            self.btc['TxTfrValNtv'].cumsum(),
            self.dcr['TxTfrValNtv'].cumsum(),
            self.dcr['dcr_tic_buy'].cumsum(),
            self.btc['TxTfrValUSD'].cumsum(),
            self.dcr['TxTfrValUSD'].cumsum(),
            self.dcr['tic_usd_cost'].cumsum(),
            self.btc_half['y_arb'],
            self.btc['PriceUSD'],self.dcr['PriceUSD']
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
        fig = self.chart.subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.show()
        return fig

    def dcr_user_daily_txval(self):
        """
        #############################################################################
                    USER METRICS - DAILY VALUE TRANSFERRED
        #############################################################################
        """

        loop_data = [[0,1,2,3,4,5],[7,8,6]]
        x_data = [
            self.btc['age_days'],self.dcr['age_days'],self.dcr['age_days'],
            self.btc['age_days'],self.dcr['age_days'],self.dcr['age_days'],
            self.btc_half['age_days'],
            self.btc['age_days'],self.dcr['age_days']    
            ]
        y_data = [
            self.btc['TxTfrValNtv'].rolling(7).mean(),
            self.dcr['TxTfrValNtv'].rolling(7).mean(),
            self.dcr['dcr_tic_buy'].rolling(7).mean(),
            self.btc['TxTfrValUSD'].rolling(7).mean(),
            self.dcr['TxTfrValUSD'].rolling(7).mean(),
            self.dcr['tic_usd_cost'].rolling(7).mean(),
            self.btc_half['y_arb'],
            self.btc['PriceUSD'],self.dcr['PriceUSD']
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
        fig = self.chart.subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.show()
        return fig

    def dcr_user_local_txflow(self):
        """
        #############################################################################
                    USER METRICS - LOCAL TRANSACTION FLOWS
        #############################################################################
        """

        loop_data = [[0,1,2,3,4],[5,6,7]]
        x_data = [
            #Transaction Volume
            self.btc['age_days'],
            self.btc['age_days'],
            self.dcr['age_days'],
            self.dcr['age_days'],
            self.dcr['age_days'],
            #Address Density
            self.btc['age_days'],
            self.dcr['age_days'],
            self.btc_half['age_days'],
            ]
        y_data = [
            self.btc['TxTfrValMedNtv'].rolling(2).mean(),
            self.btc['TxTfrValMeanNtv'],
            self.dcr['TxTfrValMedNtv'].rolling(2).mean(),
            self.dcr['TxTfrValMeanNtv'],
            self.dcr['tic_price_avg'],
            #Address Density
            self.btc['PriceUSD'],
            self.dcr['PriceUSD'],
            self.btc_half['y_arb']
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
        fig = self.chart.subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.show()


    def dcr_miner_pow_growth(self):
        """
        #############################################################################
                            BITCOIN AND DECRED POW GROWTH
        #############################################################################
        """
        dcr_hash = self.dcr[self.dcr['pow_hashrate_THs_avg']>1]

        loop_data = [[0,1,2,3],[4,5]]
        x_data = [
            self.btc['age_days'],dcr_hash['age_days'],
            self.btc['age_days'],dcr_hash['age_days'],
            self.btc['age_days'],dcr_hash['age_days'],
            ]
        y_data = [
            self.btc['DiffMean'],dcr_hash['DiffMean'],
            self.btc['pow_hashrate_THs'],dcr_hash['pow_hashrate_THs_avg'],
            self.btc['PriceUSD'],dcr_hash['PriceUSD'],
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
        fig = self.chart.subplot_lines_doubleaxis(
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
                x=dcr_hash['age_days'], 
                y=dcr_hash['DiffMean'].rolling(i).mean(),
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
                x=self.btc['age_days'], 
                y=self.btc['DiffMean'].rolling(i).mean(),
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
        return fig

    def dcr_miner_cum_income(self):
        """
        #############################################################################
                            MINER CUMULATIVE INCOMES
        #############################################################################
        """

        self.btc['PoW_income_usd'] = self.btc['DailyIssuedUSD'] + self.btc['FeeTotUSD']
        self.btc['FeeRatio'] = self.btc['FeeTotUSD']/self.btc['PoW_income_usd']
        self.dcr['FeeRatio'] = self.dcr['FeeTotUSD']/self.dcr['PoW_income_usd']

        loop_data = [[0,2,6,4,1,3,7,5],[]]
        x_data = [
            self.btc['age_sply'],self.dcr['age_sply'],
            self.btc['age_sply'],self.dcr['age_sply'],
            self.btc['age_sply'],self.dcr['age_sply'],
            self.btc['age_sply'],self.dcr['age_sply'],
            #Second Chart
            self.btc['age_sply'],self.dcr['age_sply'],
            ]
        y_data = [
            self.btc['PoW_income_usd'].cumsum(),
            self.dcr['PoW_income_usd'].cumsum(),
            self.btc['FeeTotUSD'].cumsum(),
            self.dcr['FeeTotUSD'].cumsum(),
            self.btc['PoW_income_usd'],
            self.dcr['PoW_income_usd'],
            self.btc['CapMrktCurUSD'],
            self.dcr['CapMrktCurUSD'],
            #Second Chart
            self.btc['FeeRatio'],   #Fee Ratio
            self.dcr['FeeRatio'],   #Fee Ratio
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
        fig = self.chart.subplot_lines_doubleaxis(
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
        fig = self.chart.subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        #Increase tick spacing
        fig.update_xaxes(dtick=0.1)
        fig.update_yaxes(tickformat = ".2%")
        fig.show()

    def dcr_stakers_ticlock_usd(self):
        """
        #############################################################################
                            STAKEHOLDER TOTAL LOCKED IN TICKETS - USD
        #############################################################################
        """

        loop_data = [[0,1,2,3],[]]
        x_data = [
            self.dcr['date'],
            self.dcr['date'],
            self.dcr['date'],
            self.dcr['date'],
            ]
        y_data = [
            self.dcr['CapMrktCurUSD'],
            self.dcr['tic_usd_cost'].cumsum(),
            self.dcr['PoW_income_usd'].cumsum(),
            self.dcr['CapRealUSD'],
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
        fig = self.chart.subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        #Increase tick spacing
        #fig.update_xaxes(dtick=0.1)
        fig.show()

    def dcr_stakers_ticlock_btc(self):
        """
        #############################################################################
                            STAKEHOLDER TOTAL LOCKED IN TICKETS - BTC
        #############################################################################
        """
        self.dcr = self.dcr.merge(self.btc[['date','PriceUSD',]],on='date',how='left',suffixes=('', '_BTC'))
        self.dcr['CapRealBTC'] = self.dcr['CapRealUSD'].diff(periods=1)/self.dcr['PriceUSD_BTC']
        self.dcr['CapRealBTC'] = self.dcr['CapRealBTC'].cumsum()


        loop_data = [[0,1,2,3,4],[]]
        x_data = [
            self.dcr['date'],
            self.dcr['date'],
            self.dcr['date'],
            self.dcr['date'],
            self.dcr['date'],
            ]
        y_data = [
            self.dcr['SplyCur']*self.dcr['PriceBTC'],
            self.dcr['tic_btc_cost'].cumsum(),
            self.dcr['PoS_income_btc'].cumsum(),
            self.dcr['PoW_income_btc'].cumsum(),
            self.dcr['CapRealBTC'],
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
        fig = self.chart.subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        #Increase tick spacing
        #fig.update_xaxes(dtick=0.1)
        fig.show()

    def dcr_stakers_ticmetric(self):
        """
        #############################################################################
                            TICKET METRICS
        #############################################################################
        """
        loop_data = [[0,1,],[]]
        x_data = [
            self.dcr['date'],
            self.dcr['date'],
            self.dcr['date'],
            self.dcr['date'],
            self.dcr['date'],
            ]
        y_data = [
            self.dcr['PriceUSD'],
            self.dcr['CapTicPriceUSD'],
            self.dcr['PoS_income_btc'].cumsum(),
            self.dcr['PoW_income_btc'].cumsum(),
            self.dcr['PriceRealUSD']/self.dcr['PriceUSD_BTC']*self.dcr['SplyCur'],
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
        fig = self.chart.subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        #Increase tick spacing
        #fig.update_xaxes(dtick=0.1)
        fig.show()

    def dcr_fund(self):

        dcr_fund = pd.read_csv(r"D:\code_development\checkonchain\checkonchain\dcronchain\resources\data\treasury_20200212.csv")
        #Sort by timestamp - oldest to newest
        dcr_fund = dcr_fund.sort_values(by='time_stamp')
        #Reset Index
        dcr_fund = dcr_fund.reset_index(drop=True)
        #Convert timestamp to datetime
        dcr_fund['date'] = pd.to_datetime(dcr_fund['time_stamp'],unit='s',utc=True)
        #Calculate Transaction value * direction (+ve = inflow)
        dcr_fund['funds'] = dcr_fund['value'] * dcr_fund['direction']
        #Treasury Balance = cumulative sum of funds
        dcr_fund['balance'] = dcr_fund['funds'].cumsum()
        #Incoming and Outgoing = cumulative sum in +ve and negative direction
        dcr_fund['incoming'] = dcr_fund['funds'].clip(lower=0)
        dcr_fund['outgoing'] = dcr_fund['funds'].clip(upper=0)
        #Treasury Spend Rate
        dcr_fund['spend_rate'] = dcr_fund['outgoing'].cumsum()*-1/dcr_fund['incoming'].cumsum()
        dcr_fund['spend_rate_final'] = dcr_fund['outgoing'].cumsum()/(-19.32e6*0.1)
        #Combine with Price USD and BTC Data
        dcr_fund = pd.merge_asof(
            dcr_fund,
            self.dcr[['date','PriceUSD','PriceBTC','tic_pool_avg','tic_day','tic_price_avg']],
            left_on='date',
            right_on='date'
            )
        #Calculate Expenditure
        dcr_fund['balance_usd'] = dcr_fund['balance'] * dcr_fund['PriceUSD']
        dcr_fund['incoming_usd'] = dcr_fund['incoming'] * dcr_fund['PriceUSD']
        dcr_fund['outgoing_usd'] = dcr_fund['outgoing'] * dcr_fund['PriceUSD']
        dcr_fund['expenditure_usd'] = dcr_fund['outgoing_usd'].cumsum()*-1

        return dcr_fund

    def dcr_fund_IOflow(self):
        """
        #############################################################################
                            TREASURY INFLOW OUTFLOW - DCR
        #############################################################################
        """
        DCR_fund = self.dcr_fund()
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
        fig = self.chart.subplot_lines_doubleaxis(
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
        dcr_fund = self.dcr_fund()
        loop_data = [[0,1,2],[4,5,6]]
        range_data = [['2016-01-01','2021-01-01'],[0,1e6],[4,7]]
        autorange_data = [False,False,True]
        type_data = ['date','linear','log']
        title_data = [
            'Decred Treasury Flows',
            'Date',
            'Treasury Flows (DCR)',
            'Treasury Flows (USD)']
        fig = self.chart.subplot_lines_doubleaxis(
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
        fig = self.chart.subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_yaxes(tickformat = "%",dtick=0.1)
        fig.show()

    def dcr_fund_votepower(self):
        """
        #############################################################################
                            TICKET VOTE POWER
        #############################################################################
        """
        DCR_fund = self.dcr_fund()
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
        fig = self.chart.subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_yaxes(tickformat = "%",secondary_y=True)
        fig.show()

dcr_class = dcr_user_adoption()

#USER ADOPTION
dcr_class.dcr_user_tx_count()
dcr_class.dcr_user_global_txflow()
dcr_class.dcr_user_local_txflow()
dcr_class.dcr_user_daily_txval()
dcr_class.dcr_user_cum_txval()
dcr_class.dcr_user_active_address()
dcr_class.dcr_user_active_address_ratio()

#MINERS
dcr_class.dcr_miner_pow_growth()
dcr_class.dcr_miner_cum_income()

#STAKERS
dcr_class.dcr_stakers_ticlock_btc()
dcr_class.dcr_stakers_ticlock_usd()
dcr_class.dcr_stakers_ticmetric()

#TREASURY FUND
dcr_class.dcr_fund_IOflow()
dcr_class.dcr_fund_votepower()