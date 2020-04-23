#Suite of pre-built charts for analysing Bitcoin On-chain and price performance
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.general.standard_charts import *
from checkonchain.general.regression_analysis import *
from datetime import date, datetime, time, timedelta

class btc_chart_suite():

    def __init__(self):
        self.today = datetime.combine(date.today(), time())
        self.last = pd.to_datetime(self.today + pd.to_timedelta(90,unit='D'))
        self.start = '2010-01-01'
        self.df_init = btc_add_metrics().btc_coin()
        self.df_clean = self.df_init
        #Create dataframe with key events like market tops, btms and halvings
        events = pd.DataFrame(
            data = [
                [np.datetime64('2011-06-08'),'top',0],
                [np.datetime64('2011-11-18'),'btm',0],
                [np.datetime64('2012-11-28'),'halving',0],
                [np.datetime64('2013-11-29'),'top',1],
                [np.datetime64('2015-01-14'),'btm',1],
                [np.datetime64('2016-07-09'),'halving',1],
                [np.datetime64('2017-12-16'),'top',2],
                [np.datetime64('2018-12-15'),'btm',2],
                [np.datetime64('2020-05-09'),'halving',2],
            ],
            columns = ['date_event','event','epoch']
        )
        #Convert to UTC Timezone
        events['date_event'] = events['date_event'].dt.tz_localize('UTC')
        self.halvings = events[events['event']=='halving']
        #Merge to add Price feed (keep date_event to calc deltas)
        events = pd.merge(
            events,
            self.df_init[['date','PriceUSD']],
            left_on='date_event',right_on='date'
        )
        #Rename price column
        events = events.rename(columns={'PriceUSD':'PriceUSD_event'})
        #Finalise into self and drop additional date column
        self.events = events.drop(columns='date')

    def write_html(self,fig,filename):
        "Writes chart to checkmatey.github.io"
        html_path = "D:\\code_development\\checkonchain\\checkonchain\\hosted_charts\\btconchain"
        html_path = html_path + str('\\') + filename + '.html'
        pio.write_html(fig, file=html_path, auto_open=True)


    def add_slider(self,fig):
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True,
                    thickness=0.05
                )
            )
        )
        fig.update_yaxes(fixedrange=False)

    def mvrv(self):
        """"Bitcoin Realised Price and MVRV"""
        df = pd.DataFrame()
        df = self.df_init

        #Calculate Unrealised Profit max((Mrkt - Real),0)
        df['UnrealisedProfit'] = (
            df['CapMrktCurUSD'] - df['CapRealUSD']
        ) / df['CapMrktCurUSD']

        #Calculate Unrealised Loss max((Real - Mrkt),0)
        df['UnrealisedLoss'] = (
            df['CapRealUSD'] - df['CapMrktCurUSD']
        ) / df['CapMrktCurUSD']
        #Max of value and 0
        df.loc[df['UnrealisedProfit']<0,'UnrealisedProfit'] = 0
        df.loc[df['UnrealisedLoss']<0,'UnrealisedLoss'] = 0

        df['UnrealisedPnL_Net'] = df['UnrealisedProfit'] - df['UnrealisedLoss']

        df['UnrealisedProfit'] = df['CapRealUSD'] - df['CapMrktCurUSD']

        loop_data=[[0,1],[2,3,4,5,6,7,8]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            [self.start,self.last], #NA Ceiling
            [self.start,self.last], #STRONG SELL
            [self.start,self.last], #SELL
            [self.start,self.last], #NORMAL
            [self.start,self.last], #BUY
            [self.start,self.last], #STRONG BUY
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceRealUSD'],
            df['CapMVRVCur'],
            [10,10],   #NA Ceiling
            [5.0,5.0], #STRONG SELL
            [2.6,2.6], #SELL
            [1.0,1.0], #NORMAL
            [0.7,0.7], #BUY
            [0.7,0.7], #STRONG BUY
        ]
        name_data = [
            'BTC Price (USD)',
            'Realised Price (USD)',
            'MVRV Ratio',
            'N/A',
            'STRONG SELL (5.0)',
            'SELL (2.6)',
            'N/A',
            'BUY (1.0)',
            'STRONG BUY (0.7)',
        ]
        fill_data = [
            'none','none','none',
            'none','tonexty','tonexty','none','tonexty','tozeroy',
        ]
        width_data      = [2,2,1,1,1,1,1,1,1]
        opacity_data    = [1,1,1,1,1,1,1,1,1]
        dash_data = [
            'solid','solid','solid',
            'dash','dash','dash','dash','dash','dash',
            ]
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(239, 125, 50)',    #Price Orange
            'rgba(255, 80, 80, 0.2)',     #Gradient Red
            'rgba(255, 80, 80, 0.2)',     #Gradient Red
            'rgba(255, 80, 80, 0.1)',     #Gradient Red
            'rgba(55 ,55, 55, 0)',        #NA
            'rgba(36, 255, 136, 0.1)',    #Gradient Green
            'rgba(36, 255, 136, 0.2)',    #Gradient Green

        ]
        legend_data = [
            True,True,True,
            False,True,True,False,True,True,
        ]
        title_data = [
            'Bitcoin MVRV Ratio',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>MVRV Ratio</b>'
        ]

        a = np.log10(0.3)
        b = np.log10(1e5)
        range_data = [[self.start,self.last],[-1,5],[a,b]]
        
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis_2nd_area(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data,
            fill_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=False,secondary_y=False)
        fig.update_yaxes(showgrid=True,secondary_y=True)
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\valuation_models\\mvrv_pricing'
        self.write_html(fig,chart_name)

    def unrealised_PnL(self):
        """"Bitcoin Realised Price and MVRV"""
        df = pd.DataFrame()
        df = self.df_init

        #Calculate Unrealised Profit max((Mrkt - Real),0)
        df['UnrealisedProfit'] = (
            df['CapMrktCurUSD'] - df['CapRealUSD']
        ) / df['CapMrktCurUSD']

        #Calculate Unrealised Loss max((Real - Mrkt),0)
        df['UnrealisedLoss'] = (
            df['CapRealUSD'] - df['CapMrktCurUSD']
        ) / df['CapMrktCurUSD']

        #Max of value and 0
        #df.loc[df['UnrealisedProfit']<0,'UnrealisedProfit'] = 0
        #df.loc[df['UnrealisedLoss']>0,'UnrealisedLoss'] = 0

        df['UnrealisedPnL_Net'] = (df['CapMrktCurUSD'] - df['CapRealUSD']) / df['CapMrktCurUSD']
        
        
        for i in [0.00,0.25,0.50,0.75,0.75]:
            a = -0.05
            if i == 0.00:
                name = 'UPnL_capitulation'
                df[name] = df['UnrealisedPnL_Net'] #set equal to net PnL
                df.loc[df[name]>=i - a,name] = np.nan #set >= 0 to nan
            elif j == 0.75:
                name = 'UPnL_euphoria'
                df[name] = df['UnrealisedPnL_Net'] #set equal to net PnL
                df.loc[df[name]<=i + a,name] = np.nan #set < 1.0 to nan
            else:
                if i == 0.25:
                    name = 'UPnL_fear'
                elif i == 0.50:
                    name = 'UPnL_optimism'
                elif i == 0.75:
                    name = 'UPnL_belief'
                df[name] = df['UnrealisedPnL_Net'] #set equal to net PnL
                df.loc[df[name]<=j + a, name] = np.nan #set Outside range to nan
                df.loc[df[name]>=i - a, name] = np.nan #set Outside range to nan
            j = i
            


        loop_data=[[0,1],[2,3,4,5,6]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceRealUSD'],
            df['UPnL_capitulation'],
            df['UPnL_fear'],
            df['UPnL_optimism'],
            df['UPnL_belief'],
            df['UPnL_euphoria'],
        ]
        name_data = [
            'BTC Price (USD)',
            'Realised Price (USD)',
            'Capitulation',
            'Hope-Fear',
            'Optimism-Anxiety',
            'Belief-Denial',
            'Euphoria-Greed'
        ]
        width_data      = [2,2,3,3,3,3,3]
        opacity_data    = [1,1,1,1,1,1,1]
        dash_data = [
            'solid','solid','solid','solid','solid','solid','solid']
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(233, 68, 68)',     #Capitulation Red
            'rgb(247, 132, 16)',    #Fear Orange
            'rgb(255, 192, 0)',     #Optimism Yellow
            'rgb(38, 200, 17)',     #Belief Green
            'rgb(68, 103, 235)',    #Greed Blue
        ]
        legend_data = [
            True,True,True,True,True,True,True,
            ]
        title_data = [
            'Bitcoin Unrealised Profit and Loss',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>Unrealised PnL</b>'
        ]

        range_data = [[self.start,self.last],[-1,5],[-1.5,1.5]]
        
        autorange_data = [False,False,False]
        type_data = ['date','log','linear']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=False,secondary_y=False)
        fig.update_yaxes(showgrid=True,secondary_y=True)
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\oscillators\\unrealised_pnl'
        self.write_html(fig,chart_name)

    def magic_lines_full(self):
        """"Prints Bitcoin Full History Magic Lines 200D, 128D, 200W and 128W (log)"""
        df = pd.DataFrame()
        df = self.df_init
        
        df['Mayer_Multiple'] = (
            df['PriceUSD']
            / df['PriceUSD'].rolling(200).mean()
        )

        df['200DMA'] = df['PriceUSD'].rolling(200).mean()
        df['128DMA'] = df['PriceUSD'].rolling(128).mean()
        df['200WMA'] = df['PriceUSD'].rolling(1400).mean()
        df['128WMA'] = df['PriceUSD'].rolling(896).mean()

        loop_data=[[0,1,2,3,4,5],[6]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceRealUSD'],
            df['200DMA'],
            df['128DMA'],
            df['200WMA'],
            df['128WMA'],
            df['Mayer_Multiple']
        ]
        name_data = [
            'BTC Price (USD)',
            'Realised Price (USD)',
            '200DMA',
            '128DMA',
            '200WMA',
            '128WMA',
            'Mayer Multiple'
        ]
        width_data      = [2,1,1,1,1,1,1]
        opacity_data    = [1,1,1,1,1,1,0.5]
        dash_data = ['solid','dot','dash','dash','solid','solid','dot']
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(255, 80, 80)',   #Gradient Red
            'rgb(153, 255, 102)', #Gradient Green
            'rgb(255, 80, 80)',   #Gradient Red
            'rgb(153, 255, 102)', #Gradient Green
            'rgb(239, 125, 50)',    #Price Orange
        ]
        legend_data = [True,True,True,True,True,True,True,True]
        title_data = [
            'Bitcoin Magic Lines',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>Mayer Multiple</b>']
        range_data = [[self.start,self.last],[-1,5],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\pricing_models\\magic_lines_full_pricing'
        self.write_html(fig,chart_name)

    def magic_lines(self):
        """"Prints Bitcoin Full History Magic Lines 200D, 128D, 200W and 128W (log)"""
        df = pd.DataFrame()
        df = self.df_init
        
        df['200DMA'] = df['PriceUSD'].rolling(200).mean()
        df['128DMA'] = df['PriceUSD'].rolling(128).mean()
        df['200WMA'] = df['PriceUSD'].rolling(1400).mean()
        df['128WMA'] = df['PriceUSD'].rolling(896).mean()

        loop_data=[[0,1,2,3,4,5],[]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceRealUSD'],
            df['200DMA'],
            df['128DMA'],
            df['200WMA'],
            df['128WMA']
        ]
        name_data = [
            'BTC Price (USD)',
            'Realised Price (USD)',
            '200DMA',
            '128DMA',
            '200WMA',
            '128WMA',
        ]
        width_data      = [2,1,1,1,1,1]
        opacity_data    = [1,1,1,1,1,1]
        dash_data = ['solid','dot','dash','dash','solid','solid']
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(255, 80, 80)',   #Gradient Red
            'rgb(153, 255, 102)', #Gradient Green
            'rgb(255, 80, 80)',   #Gradient Red
            'rgb(153, 255, 102)', #Gradient Green
        ]
        legend_data = [True,True,True,True,True,True,True]
        title_data = [
            'Bitcoin Magic Lines',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b></b>']
        range_data = [['2017-01-01',self.last],[00,20000],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','linear','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(dtick=1000)
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\pricing_models\\magic_lines_pricing'
        self.write_html(fig,chart_name)

    def mayer_multiple(self):
        """"Mayer Multiple Bands"""
        df = pd.DataFrame()
        df = self.df_init

        df['Mayer_Multiple'] = df['PriceUSD']/df['PriceUSD'].rolling(200).mean()
        df['200DMA']        = df['PriceUSD'].rolling(200).mean()
        df['128DMA']     = df['PriceUSD'].rolling(128).mean()
        df['Mayer_SBUY']    = df['200DMA'] * 0.6
        df['Mayer_BUY']     = df['200DMA'] * 0.8
        df['Mayer_CAUTION']   = df['200DMA'] * 1.6
        df['Mayer_SELL']    = df['200DMA'] * 2.4
        df['Mayer_SSELL']   = df['200DMA'] * 3.4

        loop_data=[[0,1,2,3,4,5,6],[7,8,9,10,11,12,13,14]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            #Secondary
            [self.start,self.last],    #N/A CEILING
            [self.start,self.last],    #STRONG SELL
            [self.start,self.last],    #SELL
            [self.start,self.last],    #CAUTION
            [self.start,self.last],    #N/A CEILING
            [self.start,self.last],    #BUY
            [self.start,self.last],    #BUY
            df['date'],
        ]
        y_data = [
            df['PriceUSD'],
            df['200DMA'],
            df['Mayer_SSELL'],
            df['Mayer_SELL'],
            df['Mayer_CAUTION'],
            df['Mayer_BUY'],
            df['Mayer_SBUY'],
            #Secondary
            [6,6],
            [3.4,3.4],
            [2.4,2.4],
            [1.6,1.6],
            [0.8,0.8],
            [0.6,0.6],
            [0.6,0.6],
            df['Mayer_Multiple'],
        ]
        fill_data = [
            'none','none','none','none','none','none','none',
            'none','tonexty','tonexty','tonexty','none','tonexty','tozeroy','none'
        ]
        name_data = [
            'BTC Price (USD)',
            '200DMA',
            'STRONG SELL (3.4)',
            'SELL (2.4)',
            'CAUTION (1.6)',
            'BUY (0.8)',
            'STRONG BUY (0.6)',
            #Secondary
            'N/A',
            'STRONG SELL (3.4)',
            'SELL (2.4)',
            'CAUTION (1.6)',
            'N/A',
            'BUY (0.8)',
            'STRONG BUY (0.6)',
            'Mayer Multiple',
        ]
        width_data      = [2,1,1,1,1,1,1,             1,1,1,1,1,1,1,1]
        opacity_data    = [1,1,0.7,0.7,0.7,0.7,0.7,   1,1,1,1,1,1,1,1]
        dash_data = [
            'solid','solid','dash','dash','dash','dash','dash',
            'dash','dash','dash','dash','dash','dash','dash','solid',
            ]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(255, 80, 80)',     #Gradient Red  
            'rgb(255, 153, 102)',   #Gradient Orange
            'rgb(255, 153, 102)',   #Gradient Orange
            'rgb(255, 204, 102)',   #Gradient Yellow
            'rgb(153, 255, 102)',   #Gradient Green
            #Secondary
            'rgba(255, 80, 80, 0.2)',     #Gradient Red
            'rgba(255, 80, 80, 0.2)',     #Gradient Red
            'rgba(255, 80, 80, 0.1)',     #Gradient Red
            'rgba(255, 153, 102, 0.1)',   #Gradient Orange
            'rgba(55 ,55, 55, 0)',        #NA
            'rgba(36, 255, 136, 0.1)',    #Gradient Green
            'rgba(36, 255, 136, 0.2)',    #Gradient Green
            'rgb(46, 214, 161)',    #Turquoise
        ]
        legend_data = [
            True,True,True,True,True,True,True,
            False,False,False,False,False,False,False,True,
            ]
        title_data = [
            'Bitcoin Mayer Multiple Bands',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>Mayer Multiple</b>']
        range_data = [['2011-01-01',self.last],[-1,5],[np.log10(0.3),4]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis_2nd_area(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data,
            fill_data
            )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\pricing_models\\mayer_multiple_bands_pricing'
        self.write_html(fig,chart_name)

    def puell_multiple(self):
        """"Puell Multiple"""
        df = pd.DataFrame()
        df = self.df_init
        
        df['Puell_Multiple'] = (
            df['DailyIssuedUSD']
            / df['DailyIssuedUSD'].rolling(365).mean()
        )

        loop_data=[[0,1,2],[3,4,5,6,7]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            ['2008-01-01','2022-01-01'],    #Strong BUY
            ['2008-01-01','2022-01-01'],    #BUY
            ['2008-01-01','2022-01-01'],    #SELL
            ['2008-01-01','2022-01-01'],    #Strong SELL
        ]
        y_data = [
            df['PriceUSD'],
            df['DailyIssuedUSD']/df['SplyCur']*1000*2**(np.floor(df['blk']/210000)),
            df['DailyIssuedUSD'].rolling(365).mean()/df['SplyCur']*1000*2**(np.floor(df['blk']/210000)),
            df['Puell_Multiple'],
            [0.4,0.4],
            [0.6,0.6],
            [2.5,2.5],
            [5,5],
        ]
        name_data = [
            'BTC Price (USD)',
            'Issued/Supply *1000*2^halving_epoch',
            'Issued/Supply *factor (365DMA)',
            'Puell Multiple',
            'STRONG BUY (0.4)',
            'BUY (0.6)',
            'SELL (2.5)',
            'STRONG SELL (5.0)'
        ]
        width_data      = [1,0.5,0.5,1,2,2,2,2]
        opacity_data    = [1,0.75,0.75,1,1,1,1,1]
        dash_data = ['solid','solid','dash','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True,True,True]
        title_data = [
            'Bitcoin Puell Multiple',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>Puell Multiple</b>']
        range_data = [[self.start,self.last],[-1,5],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\oscillators\\puell_multiple_pricing'
        self.write_html(fig,chart_name)

    def block_subsidy(self):
        """"Block Subsidy Models"""
        df = pd.DataFrame()
        df = self.df_init
        
        df['Puell_Multiple'] = (
            df['DailyIssuedUSD']
            / df['DailyIssuedUSD'].rolling(365).mean()
        )

        df['DailyIssuedUSD'] = df['DailyIssuedNtv'] * df['PriceUSD']

        df['DailyIssuedUSDAdj'] = df['DailyIssuedUSD']*10*2**(np.floor(df['blk']/210000))

        df['FeeTotUSD'] = df['FeeTotNtv'] * df['PriceUSD']
        df['PoW_cap'] = df['DailyIssuedUSDAdj'].cumsum()
        df['miner_cap'] = df['DailyIssuedUSDAdj'].cumsum() + df['FeeTotUSD'].cumsum()


        loop_data=[[0,1,2],[]]#3,4,5,6,7
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            ['2008-01-01','2022-01-01'],    #Strong BUY
            ['2008-01-01','2022-01-01'],    #BUY
            ['2008-01-01','2022-01-01'],    #SELL
            ['2008-01-01','2022-01-01'],    #Strong SELL
        ]
        y_data = [
            df['CapMrktCurUSD'],
            df['miner_cap'],
            df['miner_cap']*0.236,
            df['Puell_Multiple'],
            [0.4,0.4],
            [0.6,0.6],
            [2.5,2.5],
            [5,5],
        ]
        name_data = [
            'Market Cap (USD)',
            'PoW Block Reward Cap',
            'PoW Block Reward Cap * 23.6%',
            'Puell Multiple',
            'STRONG BUY (0.4)',
            'BUY (0.6)',
            'SELL (2.5)',
            'STRONG SELL (5.0)'
        ]
        width_data      = [2,2,2,1,2,2,2,2]
        opacity_data    = [1,1,1,1,1,1,1,1]
        dash_data = ['solid','dash','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(250, 38, 53)',     #PoW Red
            'rgb(250, 38, 53)',     #PoW Red
            'rgb(255, 255, 255)',   #White
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True,True,True]
        title_data = [
            'Bitcoin Block Subsidy Models',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>Puell Multiple</b>']
        range_data = [[self.start,self.last],[5,12],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\valuation_models\\block_subsidy_valuation'
        self.write_html(fig,chart_name)

    def difficulty_ribbon(self):
        """"Difficulty Ribbon and Miner Income"""
        df = pd.DataFrame()
        df = self.df_init

        df['PoW_Income_btc'] = df['DailyIssuedNtv'] + df['FeeTotNtv']
        df['PoW_Income_usd'] = df['DailyIssuedUSD'] + df['FeeTotUSD']
        df['Miner_Multiple'] = df['CapMrktCurUSD'] / df['PoW_Income_usd'].cumsum()

        #Calc Difficulty Model - Specific to Bitcoin (CHECKMATE)
        btc_diff_model = regression_analysis().ln_regression(df,'DiffMean','CapMrktCurUSD','date')['model_params']
        df['CapDiffUSD'] = (
            np.exp(float(btc_diff_model['intercept']))
            * df['DiffMean']**float(btc_diff_model['coefficient'])
            )
        df['DiffMultiple'] = df['CapMrktCurUSD']/df['CapDiffUSD']

        #Calculate Difficulty Model Price
        diff_price = (
            float(df['CapDiffUSD'].iloc[-1])
            / float(df['SplyCur'].iloc[-1])
        )

        loop_data=[[2,0,4,1],[5,  6,7,8,9,10,11,12]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            [self.start,self.last], #NA Ceiling
            [self.start,self.last], #STRONG SELL
            [self.start,self.last], #SELL
            [self.start,self.last], #UNITY
            [self.start,self.last], #NORMAL
            [self.start,self.last], #BUY
            [self.start,self.last], #STRONG BUY
        ]
        y_data = [
            df['CapMrktCurUSD'],
            df['CapDiffUSD'],
            df['PoW_Income_usd'].cumsum(),
            df['TxTfrValUSD'],
            df['DiffMean'],
            df['DiffMultiple'],
            [25,25], #NA Ceiling
            [5,5], #STRONG SELL (95%)
            [2,2], #SELL (85%)
            [1,1], #Unity
            [0.5,0.5], #NORMAL
            [0.3,0.3], #BUY (20%)
            [0.3,0.3], #STRONG BUY (10%)
        ]
        name_data = [
            'Market Cap (USD)',
            'Difficulty Cap',
            'Cumulative PoW Reward',
            'On-chain Transaction Value',
            'Difficulty Ribbon',
            'Difficulty Multiple',
            'N/A',
            'STRONG SELL (95%)',
            'SELL (85%)',
            'N/A','N/A',
            'BUY (80%)',
            'STRONG BUY (90%)'
        ]
        fill_data = [
            'none','none','none','none','none','none',
            'none','tonexty','tonexty','none','none','tonexty','tozeroy'
        ]
        width_data      = [2,2,2,1,2,1,      1,1,1,1,1,1,1]
        opacity_data    = [1,1,1,0.75,1,1,   1,1,1,1,1,1,1]
        dash_data = [
            'solid','solid','solid','solid','solid','solid',
            'dash','dash','dash','dash','dash','dash','dash',]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(255, 102, 0)',     #Burnt Orange
            'rgb(250, 38, 53)',     #POW Red
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(254, 215, 140)',   #Matte Yellow
            'rgb(255, 102, 0)',     #Burnt Orange

            'rgba(255, 80, 80, 0.2)',     #Gradient Red
            'rgba(255, 80, 80, 0.2)',     #Gradient Red
            'rgba(255, 80, 80, 0.1)',     #Gradient Red
            'rgba(255, 255, 255, 0.2)',   #White
            'rgba(55 ,55, 55, 0)',        #NA
            'rgba(36, 255, 136, 0.1)',    #Gradient Green
            'rgba(36, 255, 136, 0.2)',    #Gradient Green
        ]
        legend_data = [
            True,True,True,True,True,True,
            False,True,True,False,False,True,True,]
        title_data = [
            'Bitcoin Difficulty Ribbon',
            '<b>Date</b>',
            '<b>Bitcoin Valuation (USD)<br />Protocol Difficulty</b>',
            '<b>Difficulty Multiple</b>'
        ]
        range_data = [[self.start,self.last],[4,14],[-1,6]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis_2nd_area(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data,
            fill_data
            )

        """ =================================
            ADD DIFFICULTY RIBBON
        ================================="""
        for i in [9,14,25,40,60,90,128,200]:
            fig.add_trace(go.Scatter(
                mode='lines',
                x=df['date'], 
                y=df['DiffMean'].rolling(i).mean(),
                name='D_ '+str(i),
                opacity=0.5,
                showlegend=False,
                line=dict(
                    width=i/200*2,
                    color='rgb(254, 215, 140)',#Matte Yellow
                    dash='solid'
                    )),
                secondary_y=False)
  
        self.add_slider(fig)
        fig.update_xaxes(dtick='M12')
        #Remove Gridlines
        fig.update_yaxes(showgrid=False,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True)

        #Write out html chart
        chart_name = '\\pricing_models\\difficulty_ribbon_pricing'
        self.write_html(fig,chart_name)

    def beam_indicator(self):
        """"BEAM Indicator (Bitcoin Economics Adaptive Multiple) 
        after https://bitcoineconomics.io/beam.html"""
        df = pd.DataFrame()
        df = self.df_init

        for i in df.index:
            _a = min(i,1400)
            _b = df['PriceUSD'].rolling(_a).mean().loc[i]
            _c = df.loc[i,'PriceUSD']
            df.loc[i,'BEAM'] = np.log(_c / _b) / 2.5
            df.loc[i,'BEAM_lower'] = _b
            df.loc[i,'BEAM_upper'] = _b * 12.182494

        loop_data=[[0,1,2],[3,4,5,6,7]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            ['2008-01-01','2022-01-01'],    #Strong BUY
            ['2008-01-01','2022-01-01'],    #BUY
            ['2008-01-01','2022-01-01'],    #SELL
            ['2008-01-01','2022-01-01'],    #Strong SELL
        ]
        y_data = [
            df['PriceUSD'],
            df['BEAM_lower'],
            df['BEAM_upper'],
            df['BEAM'],
            [0.0,0.0],
            [0.07,0.07],
            [0.96,0.96],
            [1.0,1.0],
        ]
        name_data = [
            'BTC Price (USD)',
            'BEAM Lower Band',
            'BEAM Upper Band',
            'BEAM Indicator',
            'STRONG BUY (0.0)',
            'BUY (0.07)',
            'SELL (0.96)',
            'STRONG SELL (1.0)'
        ]
        width_data      = [2,2,2,1,2,2,2,2]
        opacity_data    = [1,1,1,1,1,1,1,1]
        dash_data = ['solid','solid','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 80, 80)',     #Gradient Red
            'rgb(255, 255, 255)',   #White
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True,True,True,]
        title_data = [
            '<b>Bitcoin BEAM Indicator<b>',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>BEAM Indicator</b>']
        range_data = [[self.start,self.last],[-1,5],[-0.2,2.4]]
        autorange_data = [False,False,False]
        type_data = ['date','log','linear']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True,dtick=0.2)
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\pricing_models\\BEAM_indicator_pricing'
        self.write_html(fig,chart_name)

    def investor_tool(self):
        """"Bitcoin Investor Tool 730DMA after @PositiveCrypto"""
        df = pd.DataFrame()
        df = self.df_init

        df['730DMA'] = df['PriceUSD'].rolling(730).mean()
        df['730DMAx5'] = df['730DMA']*5

        df['upper'] = np.where(df['PriceUSD'] >= df['730DMAx5'], df['PriceUSD'], df['730DMAx5'])
        df['lower'] = np.where(df['PriceUSD'] <= df['730DMA']  , df['PriceUSD'], df['730DMA'])

        #Block Subsidy Model
        df['DailyIssuedUSD'] = df['DailyIssuedNtv'] * df['PriceUSD']
        df['DailyIssuedUSDAdj'] = df['DailyIssuedUSD']*10*2**(np.floor(df['blk']/210000))
        df['FeeTotUSD'] = df['FeeTotNtv'] * df['PriceUSD']
        df['PoW_cap'] = df['DailyIssuedUSDAdj'].cumsum()
        df['miner_cap'] = df['DailyIssuedUSDAdj'].cumsum() + df['FeeTotUSD'].cumsum()
        df['miner_price'] = df['miner_cap'] / df['SplyCur']


        loop_data=[[0,1,2,3,4],[]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date']
        ]
        y_data = [
            df['PriceUSD'],
            df['lower'], #N/A Price for Fill
            df['730DMA'],
            df['upper'], #N/A Price for Fill
            df['730DMAx5'],
            df['miner_price'],
            df['miner_price']*0.236,
        ]
        name_data = [
            'BTC Price (USD)',
            'N/A',
            'BUY Zone (2yr MA)',
            'N/A',
            'SELL Zone (2yr MA x5)',
            'PoW Block Reward Price',
            'PoW Block Reward Price * 23.6%',
        ]
        width_data      = [2,1,2,1,2,1,1]
        opacity_data    = [1,0,1,0,1,1,1]
        fill_data = ['none','none','tonexty','none','tonexty','none','none']
        dash_data = ['solid','solid','solid','solid','solid','solid','solid']
        color_data = [
            'rgb(255, 255, 255)',           #White
            'rgb(255, 255, 255)',           #White
            'rgba(17, 255, 125,0.8)',             #Strong Green
            'rgb(255, 255, 255)',           #White
            'rgba(250, 38, 53,0.8)',             #PoW Red
            'rgb(255, 255, 0)',             #Retro Pink
            'rgb(0, 255, 255)',             #Retro Blue
        ]
        legend_data = [True,False,True,False,True,True,True]
        title_data = [
            'Bitcoin Investor Tool',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b></b>']
        range_data = [[self.start,self.last],[-1,5],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis_1st_area(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data,
            fill_data
            )
        
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=False,secondary_y=False)
        fig.update_yaxes(showgrid=True,secondary_y=True)
        self.add_slider(fig)
        
        fig = check_standard_charts().add_annotation(fig,"@checkmatey<br />after @PositiveCrypto") 

        #Write out html chart
        chart_name = '\\pricing_models\\investor_tool_pricing'
        self.write_html(fig,chart_name)

    def golden_ratio(self):
        """"Bitcoin Golden Ratio and Fib Levels after @PositiveCrypto"""
        df = pd.DataFrame()
        df = self.df_init

        df['365DMA'] = df['PriceUSD'].rolling(365).mean()
        df['365DMA_golden'] = df['365DMA'] * 1.61803398875
        df['365DMA_2']      = df['365DMA'] * 2.0
        df['365DMA_3']      = df['365DMA'] * 3.0
        df['365DMA_5']      = df['365DMA'] * 5.0
        df['365DMA_8']      = df['365DMA'] * 8.0
        df['365DMA_13']     = df['365DMA'] * 13.0
        df['365DMA_21']     = df['365DMA'] * 21.0
        #Fib Extensions
        df['365DMA_p236']      = df['365DMA'] * 0.236
        df['365DMA_p382']      = df['365DMA'] * 0.382
        df['365DMA_p500']      = df['365DMA'] * 0.500
        df['365DMA_p618']      = df['365DMA'] * 0.618
        df['365DMA_p786']     = df['365DMA'] * 0.786
        df['365DMA_p900']     = df['365DMA'] * 0.900

        df['116DMA']     = df['PriceUSD'].rolling(116).mean()

        loop_data=[[0,1,2   ,3,4,5,6,7,8,     9,10,11,12,13,14,   15],[]]
        x_data = [
            df['date'],df['date'],
            df['date'],
            #Fib Extensions
            df['date'],df['date'],
            df['date'],df['date'],
            df['date'],df['date'],
            #Fib Levels
            df['date'],df['date'],
            df['date'],df['date'],
            df['date'],df['date'],

            df['date'],
        ]
        y_data = [
            df['PriceUSD'], df['365DMA'],
            df['365DMA_golden'],
            #Fib Extensions
            df['365DMA_2'], df['365DMA_3'],     
            df['365DMA_5'], df['365DMA_8'],     
            df['365DMA_13'],df['365DMA_21'],
            #Fib Levels
            df['365DMA_p236'],df['365DMA_p382'],
            df['365DMA_p500'],df['365DMA_p618'],
            df['365DMA_p786'],df['365DMA_p900'],

            df['116DMA'] 
        ]
        name_data = [
            'BTC Price (USD)','365DMA',
            'Golden Ratio 1.618',
            'x2','x3','x5','x8','x13','x21',
            'x0.236','x0.382','x0.500','x0.618','x0.786','x0.900',
            '116DMA'
        ]
        width_data      = [2,2,2,   1,1,1,1,1,1,   1,1,1,2,1,1,   2]
        opacity_data    = [1,1,1,   1,1,1,1,1,1,   0.5,0.5,0.5,1,0.5,0.5,   1]
        dash_data = [
            'solid','solid','solid',
            'dash','dash','dash','dash','dash','dash',
            'dot','dot','dot','dot','dot','dot',
            'solid'
            ]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(102, 255, 153)', #Turquoise Green
            'rgb(239, 125, 50)',    #Price Orange
            #Fib Extensions
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 204, 102)',   #Gradient Yellow
            'rgb(255, 153, 102)',   #Gradient Orange
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
            #Fib Levels
            'rgb(255, 80, 80)',     #Gradient Red
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 153, 102)',   #Gradient Orange
            'rgb(239, 125, 50)',    #Price Orange    'rgb(255, 204, 102)',   #Gradient Yellow
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(153, 255, 102)',   #Gradient Green

            'rgb(20, 169, 233)',    #Total Blue
        ]
        legend_data = [True,True,True,    True,True,True,True,True,True,   True,True,True,True,True,True,  True]
        title_data = [
            'Bitcoin Golden Ratio',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b></b>']
        range_data = [['2017-01-01',self.last],[2.698970004,5.397940009],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M3',tickformat='%d-%b-%y')
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\pricing_models\\golden_ratio_pricing'
        self.write_html(fig,chart_name)

    def golden_ratio_full(self):
        """"Bitcoin Golden Ratio and Fib Levels after @PositiveCrypto"""
        df = pd.DataFrame()
        df = self.df_init

        df['365DMA'] = df['PriceUSD'].rolling(365).mean()
        df['365DMA_golden'] = df['365DMA'] * 1.61803398875
        df['365DMA_2']      = df['365DMA'] * 2.0
        df['365DMA_3']      = df['365DMA'] * 3.0
        df['365DMA_5']      = df['365DMA'] * 5.0
        df['365DMA_8']      = df['365DMA'] * 8.0
        df['365DMA_13']     = df['365DMA'] * 13.0
        df['365DMA_21']     = df['365DMA'] * 21.0
        #Fib Extensions
        df['365DMA_p236']      = df['365DMA'] * 0.236
        df['365DMA_p382']      = df['365DMA'] * 0.382
        df['365DMA_p500']      = df['365DMA'] * 0.500
        df['365DMA_p618']      = df['365DMA'] * 0.618
        df['365DMA_p786']     = df['365DMA'] * 0.786
        df['365DMA_p900']     = df['365DMA'] * 0.900

        df['116DMA']     = df['PriceUSD'].rolling(116).mean()

        loop_data=[[0,1,2   ,3,4,5,6,7,8,     9,10,11,12,13,14,   ],[15]]
        x_data = [
            df['date'],df['date'],
            df['date'],
            #Fib Extensions
            df['date'],df['date'],
            df['date'],df['date'],
            df['date'],df['date'],
            #Fib Levels
            df['date'],df['date'],
            df['date'],df['date'],
            df['date'],df['date'],

            df['date'],
        ]
        y_data = [
            df['PriceUSD'], df['365DMA'],
            df['365DMA_golden'],
            #Fib Extensions
            df['365DMA_2'], df['365DMA_3'],     
            df['365DMA_5'], df['365DMA_8'],     
            df['365DMA_13'],df['365DMA_21'],
            #Fib Levels
            df['365DMA_p236'],df['365DMA_p382'],
            df['365DMA_p500'],df['365DMA_p618'],
            df['365DMA_p786'],df['365DMA_p900'],

            df['116DMA'] 
        ]
        name_data = [
            'BTC Price (USD)','365DMA',
            'Golden Ratio 1.618',
            'x2','x3','x5','x8','x13','x21',
            'x0.236','x0.382','x0.500','x0.618','x0.786','x0.900',
            '116DMA'
        ]
        width_data      = [2,2,2,   1,1,1,1,1,1,   1,1,1,2,1,1,   0.5]
        opacity_data    = [1,1,1,   1,1,1,1,1,1,   0.5,0.5,0.5,1,0.5,0.5,   0.5]
        dash_data = [
            'solid','solid','solid',
            'dash','dash','dash','dash','dash','dash',
            'dot','dot','dot','dot','dot','dot',
            'solid'
            ]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(102, 255, 153)', #Turquoise Green
            'rgb(239, 125, 50)',    #Price Orange
            #Fib Extensions
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 204, 102)',   #Gradient Yellow
            'rgb(255, 153, 102)',   #Gradient Orange
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
            #Fib Levels
            'rgb(255, 80, 80)',     #Gradient Red
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 153, 102)',   #Gradient Orange
            'rgb(239, 125, 50)',    #Price Orange    'rgb(255, 204, 102)',   #Gradient Yellow
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(153, 255, 102)',   #Gradient Green

            'rgb(20, 169, 233)',    #Total Blue
        ]
        legend_data = [True,True,True,    True,True,True,True,True,True,   True,True,True,True,True,True,  True]
        title_data = [
            'Bitcoin Golden Ratio',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b></b>']
        range_data = [[self.start,self.last],[-2,6],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M3',tickformat='%d-%b-%y')
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\pricing_models\\golden_ratio_full_pricing'
        self.write_html(fig,chart_name)

    def catch_btm_top(self):
        """"Catching the Bottom and the Top"""
        df = pd.DataFrame()
        df = self.df_init
        
        #128W and 200W MA
        df['200WMA'] = df['PriceUSD'].rolling(1400).mean()
        df['128WMA'] = df['PriceUSD'].rolling(896).mean()
        #Average Cap
        df['CapAvg'] = df['CapMrktCurUSD'].fillna(0.0001)
        df['CapAvg'] = df['CapAvg'].expanding().mean()
        df['PriceAvg'] = df['CapAvg']/df['SplyCur']
        # Delta Cap and Delta Price
        df['CapDelta'] = df['CapRealUSD'] - df['CapAvg']
        df['PriceDelta'] =df['CapDelta']/df['SplyCur']
        # Top Cap and Top Price
        df['CapTop'] = df['CapAvg']*32
        df['PriceTop'] =df['CapTop']/df['SplyCur']
        #Investor Tool
        df['730DMA'] = df['PriceUSD'].rolling(730).mean()
        df['730DMAx5'] = df['730DMA']*5
        #Mayer Multiple
        df['200DMA'] = df['PriceUSD'].rolling(200).mean()
        df['Mayer_BUY'] = df['200DMA']*0.8
        df['Mayer_SBUY'] = df['200DMA']*0.6
        df['Mayer_SSELL'] = df['200DMA']*3.4


        loop_data=[[0,1,2,3,4,5,6,7,8,9,10],[]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
        ]
        y_data = [
            df['PriceUSD'],
            #Bottoming Signals
            df['200WMA'],
            df['PriceDelta'],
            df['Mayer_SBUY'],
            #Accumulation Signals
            df['PriceRealUSD'],
            df['128WMA'],
            df['730DMA'],
            df['Mayer_BUY'],
            #Topping Signals
            df['730DMAx5'],
            df['PriceTop'],        
            df['Mayer_SSELL'],
        ]
        name_data = [
            'BTC Price (USD)',
            #Bottoming Signals
            '200WMA',
            'Delta Price',
            'Mayer Strong Buy (0.6)',
            #Accumulation Signals
            'Realised Price (USD)',
            '128WMA',
            '730DMA',
            'Mayer Buy (0.8)',
            #Topping Signals
            '730DMA x 5',
            'Top Cap',
            'Mayer Strong Sell (3.4)',         
        ]
        width_data      = [2,1,1,1,2,1,1,1,1,1,1]
        opacity_data    = [
            1,
            1,1,0.5,
            1,1,1,0.5,
            1,1,0.5
            ]
        dash_data = [
            'solid',
            'solid','dash','dash',
            'solid','dash','dot','dash',
            'solid','dash','dash',
            ]
        color_data = [
            #'rgb(239, 125, 50)',    #Price Orange
            #'rgb(20, 169, 233)',    #Total Blue
            'rgb(255, 255, 255)',    #White
            #Bottoming Signals
            'rgb(153, 255, 102)', #Gradient Green
            'rgb(153, 255, 102)', #Gradient Green
            'rgb(153, 255, 102)', #Gradient Green
            #Accumulation Signals
            'rgb(255, 204, 102)', #Gradient Yellow
            'rgb(255, 204, 102)', #Gradient Yellow
            'rgb(255, 204, 102)', #Gradient Yellow
            'rgb(255, 204, 102)', #Gradient Yellow
            #Topping Signals
            'rgb(255, 80, 80)',   #Gradient Red
            'rgb(255, 80, 80)',   #Gradient Red
            'rgb(255, 80, 80)',   #Gradient Red
            #Mayer Bands
        ]
        legend_data = [True,True,True,True,True,True,True,True,True,True,True]
        title_data = [
            'Bitcoin Topping and Bottoming',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b></b>']
        range_data = [['2017-01-01',self.last],[2.698970004,5.397940009],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        #fig.update_yaxes(dtick=1000)
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\pricing_models\\catch_btm_top'
        self.write_html(fig,chart_name)

    def s2f_model(self):
        """"Stock-to-flow Model(s) and multiple"""
        df = pd.DataFrame()
        df = self.df_init

        #Calc S2F Model - Specific to Bitcoin (CHECKMATE)
        btc_s2f_model = regression_analysis().ln_regression(df,'S2F','PriceUSD','date')['model_params']
        df['S2FPriceUSD_CM'] = (
            np.exp(float(btc_s2f_model['intercept']))
            * df['S2F']**float(btc_s2f_model['coefficient'])
            )
        df['S2FMultiple_CM'] = df['PriceUSD']/df['S2FPriceUSD_CM'].rolling(10).mean()

        #Calc S2F Model - Bitcoins Plan B Model
        planb_s2f_model = regression_analysis().regression_constants()['planb']
        df['S2FPriceUSD_PB'] = np.exp(-1.84)*df['S2F']**3.36
        df['S2FMultiple_PB'] = df['PriceUSD']/df['S2FPriceUSD_PB'].rolling(10).mean()


        loop_data=[[1,2,0],[3,4,5,6,7,8,9,10,11]]
        x_data = [
            df['date'], #Price
            df['date'], #CM S2F Model
            df['date'], #PB S2F Model
            df['date'], #CM Multiple
            df['date'], #PB Multiple
            [self.start,self.last], #NA Ceiling
            [self.start,self.last], #STRONG SELL
            [self.start,self.last], #SELL
            [self.start,self.last], #UNITY
            [self.start,self.last], #NORMAL
            [self.start,self.last], #BUY
            [self.start,self.last], #STRONG BUY
        ]
        y_data = [
            df['PriceUSD'],
            df['S2FPriceUSD_CM'].rolling(10).mean(),
            df['S2FPriceUSD_PB'].rolling(10).mean(),
            df['S2FMultiple_CM'],
            df['S2FMultiple_PB'],
            [20,20], #NA Ceiling
            [3.6,3.6], #STRONG SELL (95%)
            [1.6,1.6], #SELL (85%)
            [1.0,1.0], #Unity
            [0.4,0.4], #NORMAL
            [0.2,0.2], #BUY (20%)
            [0.2,0.2], #STRONG BUY (10%)
        ]
        name_data = [
            'BTC Price (USD)',
            'S2F Model (Checkmate)',
            'S2F Model (Plan B)',
            'S2F Multiple (Checkmate)',
            'S2F Multiple (Plan B)',
            'N/A',
            'STRONG SELL (95%)',
            'SELL (85%)',
            'N/A',
            'N/A',
            'BUY (80%)',
            'STRONG BUY (90%)'
        ]
        fill_data = [
            'none','none','none','none','none',
            'none','tonexty','tonexty','none','none','tonexty','tozeroy'
        ]
        width_data      = [2,2,  2,  1,1,   1,1,1,1,1,1,1]
        opacity_data    = [1,0.5,0.5,1,1,   1,1,1,1,1,1,1]
        dash_data = [
            'solid','dot','dot','solid','solid',
            'dash','dash','dash','dash','dash','dash','dash'
            ]
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(239, 125, 50)',    #Price Orange
            'rgba(255, 80, 80, 0.2)',     #Gradient Red
            'rgba(255, 80, 80, 0.2)',     #Gradient Red
            'rgba(255, 80, 80, 0.1)',     #Gradient Red
            'rgba(255, 255, 255, 0.2)',   #White
            'rgba(55 ,55, 55, 0)',        #NA
            'rgba(36, 255, 136, 0.1)',    #Gradient Green
            'rgba(36, 255, 136, 0.2)',    #Gradient Green
        ]
        legend_data = [
            True,True,True,True,True,
            False,True,True,False,False,True,True
            ]
        title_data = [
            'Bitcoin Stock-to-Flow Models',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>S2F Multiple</b>']
        range_data = [[self.start,self.last],[-2.995732273553991,5],[-2.995732273553991,5]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis_2nd_area(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data,
            fill_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True)
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\pricing_models\\s2f_model_pricing'
        self.write_html(fig,chart_name)

    def nvt_rvt(self):
        """"Bitcoin NVT and RVT Ratio"""
        df = pd.DataFrame()
        df = self.df_init

        #Calculate NVT and RVT 28 and 90DMA
        
        for i in [28,90]:
            name_nvt = 'NVT_' + str(i)
            name_rvt = 'RVT_' + str(i)

            df[name_nvt] = (
                df['CapMrktCurUSD'].rolling(i).mean()
                / df['TxTfrValUSD'].rolling(i).mean()
            )

            df[name_rvt] = (
                df['CapRealUSD'].rolling(i).mean()
                / df['TxTfrValUSD'].rolling(i).mean()
            )
            
            #Calculate NVTS and RVTS (28DMA on Tx only)
            if i == 28:
                df['NVTS'] = (
                    df['CapMrktCurUSD']
                    / df['TxTfrValUSD'].rolling(i).mean()
                )
                
                df['RVTS'] = (
                    df['CapRealUSD']
                    / df['TxTfrValUSD'].rolling(i).mean()
                )
        

        loop_data=[[0,1],[2,3,4,5,6,7,   8,9,10,11,12]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            [self.start,self.last],    #N/A CEILING
            [self.start,self.last],    #SELL
            [self.start,self.last],    #NORMAL 1
            [self.start,self.last],    #NORMAL 2
            [self.start,self.last],    #BUY
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceRealUSD'],
            df['NVT_28'],
            df['NVT_90'],
            df['NVTS'],
            df['RVT_28'],
            df['RVT_90'],
            df['RVTS'],
            [40,40],
            [27,27],
            [18,18],
            [10,10],
            [10,10]
        ]
        name_data = [
            'BTC Price (USD)',
            'Realised Price (USD)',
            'NVT 28DMA',
            'NVT 90DMA',
            'NVTS',
            'RVT 28DMA',
            'RVT 90DMA',
            'RVTS',
            'N/A','N/A','N/A','N/A','N/A',
        ]
        width_data      = [2,2,1,1,1,1,1,1,1,1,1,1,1]
        opacity_data    = [1,1,1,1,1,1,1,1,0,0,0,0,0]
        dash_data = [
            'solid','solid','dot','dash','solid','dot','dash','solid',
            'solid','solid','solid','solid','solid'
            ]
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(20, 169, 233)',     #Total Blue
            'rgb(153, 255, 102)',
            'rgb(255, 255, 102)',
            'rgb(255, 204, 102)',
            'rgb(255, 153, 102)',
            'rgb(255, 102, 102)',
            'rgb(255, 80, 80)',
            'rgb(55,55,55)',              #N/A
            'rgba(255, 80, 80, 0.2)',     #Gradient Red
            'rgba(255, 153, 102, 0.2)',   #Gradient Orange
            'rgba(255, 204, 102, 0.2)',   #Gradient Yellow
            'rgba(36, 255, 136, 0.2)',    #Gradient Green
        ]
        legend_data = [
            True,True,True,True,True,True,True,True,
            False,False,False,False,False,
            ]
        fill_data = [
            'none','none','none','none','none','none','none','none',
            'none','tonexty','tonexty','tonexty','tozeroy',
            ]
        title_data = [
            'Bitcoin NVT and RVT Ratio',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>NVT or RVT Ratio</b>']
        range_data = [[self.start,self.last],[-1,5],[0,150]]
        autorange_data = [False,False,False]
        type_data = ['date','log','linear']
        fig = check_standard_charts().subplot_lines_doubleaxis_2nd_area(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data,
            fill_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True,dtick=10)
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\oscillators\\nvt_rvt_ratio'
        self.write_html(fig,chart_name)

    def halving_cycle(self):
        """"Price Growth over Days since halving for each cycle"""
        df = self.df_init
        df['epoch'] = 0
        df = df.drop(['epoch'],axis=1)

        #Calculate halving epoch
        df['epoch'] = df['blk']/210000
        df['epoch'] = df['epoch'].apply(np.floor)
        #Filter events to halving events
        df2 = self.halvings
        #Merge events onto df
        df = pd.merge(
            df,df2[['epoch','event','date_event']],
            how='left',
            left_on='epoch',
            right_on='epoch',
            copy=False
        )
        #Calculate days until event
        df['days_to_event'] = 1460 - (df['date_event'] - df['date']) / np.timedelta64(1, 'D')

        loop_data=[[0,1,2,3],[]]
        x_data = [
            df[df['epoch']==0]['days_to_event'],
            df[df['epoch']==1]['days_to_event'],
            df[df['epoch']==2]['days_to_event'],
            df[df['epoch']==3]['days_to_event'],
        ]
        y_data = [
            df[df['epoch']==0]['PriceUSD']/0.084,
            df[df['epoch']==1]['PriceUSD']/12.33,
            df[df['epoch']==2]['PriceUSD']/651.94,
            df[df['epoch']==3]['PriceUSD']/8250,
        ]
        name_data = [
            'Epoch 1 (2009-12)',
            'Epoch 2 (2012-16)',
            'Epoch 3 (2016-20)',
            'Epoch 4 (2020-24)',
        ]
        width_data      = [2,2,2,2]
        opacity_data    = [1,1,1,1]
        dash_data = ['solid','solid','solid','solid',]
        color_data = [
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(78,205,233)',      #Total Blue
            'rgb(255, 80, 80)',      #Gradient Red
            'rgb(153, 255, 102)',      #Gradient Green
        ]
        legend_data = [True,True,True,True,]
        title_data = [
            'Bitcoin Days to Halving',
            '<b>Days since Halving</b>',
            '<b>Growth Multiple Since Halving</b>',
            '<b></b>']
        range_data = [[0,1460],[-0.301029996,3],[-1,2]]
        autorange_data = [False,True,False]
        type_data = ['linear','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick=30,tickformat='1./0f')
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\cycle_charts\\halving_cycle'
        self.write_html(fig,chart_name)

    def bottom_cycle(self):
        """"Price Growth over Days since capitulation for each cycle"""
        df = self.df_init
        df['epoch'] = 0
        df = df.drop(['epoch'],axis=1)
        
        #Filter events to market capitulation event
        df2 = self.events[self.events['event']=='btm']
        #Merge events onto df, fill backwards
        df = pd.merge(
            df,df2,
            how='left',
            left_on='date',
            right_on='date_event',
            copy=False
        )
        #Fill forwards for all event data
        df[['date_event','epoch','event','PriceUSD_event']] = (
            df[['date_event','epoch','event','PriceUSD_event']].fillna(method='ffill')
        )
        
        #Calculate days since event
        df['days_since_event'] = (df['date'] - df['date_event']) / np.timedelta64(1, 'D')
        #Calculate drawdown since event
        df['event_delta'] = df['PriceUSD']/df['PriceUSD_event']

        loop_data=[[0,1,2,3],[]]
        x_data = [
            df[df['epoch']==0]['days_since_event'],
            df[df['epoch']==1]['days_since_event'],
            df[df['epoch']==2]['days_since_event'],
            df[df['epoch']==3]['days_since_event'],
        ]
        y_data = [
            df[df['epoch']==0]['event_delta'],
            df[df['epoch']==1]['event_delta'],
            df[df['epoch']==2]['event_delta'],
            df[df['epoch']==3]['event_delta'],
        ]
        name_data = [
            'Epoch 1 (2009-12)',
            'Epoch 2 (2012-16)',
            'Epoch 3 (2016-20)',
            'Epoch 4 (2020-24)',
        ]
        width_data      = [2,2,2,2]
        opacity_data    = [1,1,1,1]
        dash_data = ['solid','solid','solid','solid',]
        color_data = [
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(78,205,233)',      #Total Blue
            'rgb(255, 80, 80)',      #Gradient Red
            'rgb(153, 255, 102)',      #Gradient Green
        ]
        legend_data = [True,True,True,True,]
        title_data = [
            'Bitcoin Price Growth Since Cycle Low',
            '<b>Days Since Capitulation</b>',
            '<b>Growth Multiple Since Low</b>',
            '<b></b>']
        range_data = [[0,1500],[0,3],[-1,2]]
        autorange_data = [False,True,False]
        type_data = ['linear','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick=30)
        #fig.update_yaxes(tickformat='.0%')
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\cycle_charts\\bottom_cycle'
        self.write_html(fig,chart_name)
    
    def top_cycle(self):
        """"Price Drawdown over since market top for each cycle"""
        df = self.df_init
        df['epoch'] = 0
        df = df.drop(['epoch'],axis=1)

        #Filter events to market top event
        df2 = self.events[self.events['event']=='top']
        #Merge events onto df, fill forwards
        df = pd.merge(
            df,df2,
            how='left',
            left_on='date',
            right_on='date_event',
            copy=False
        )
        #Fill forwards for all event data
        df[['date_event','epoch','event','PriceUSD_event']] = (
            df[['date_event','epoch','event','PriceUSD_event']].fillna(method='ffill')
        )
        #print(df.columns)
        #Calculate days since event
        df['days_since_event'] = (df['date'] - df['date_event']) / np.timedelta64(1, 'D')
        #Calculate drawdown since event
        df['event_delta'] = df['PriceUSD']/df['PriceUSD_event']

        loop_data=[[0,1,2,3],[]]
        x_data = [
            df[df['epoch']==0]['days_since_event'],
            df[df['epoch']==1]['days_since_event'],
            df[df['epoch']==2]['days_since_event'],
            df[df['epoch']==3]['days_since_event'],
        ]
        y_data = [
            df[df['epoch']==0]['event_delta'],
            df[df['epoch']==1]['event_delta'],
            df[df['epoch']==2]['event_delta'],
            df[df['epoch']==3]['event_delta'],
        ]
        name_data = [
            'Epoch 1 (2009-12)',
            'Epoch 2 (2012-16)',
            'Epoch 3 (2016-20)',
            'Epoch 4 (2020-24)',
        ]
        width_data      = [2,2,2,2]
        opacity_data    = [1,1,1,1]
        dash_data = ['solid','solid','solid','solid',]
        color_data = [
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(78,205,233)',      #Total Blue
            'rgb(255, 80, 80)',      #Gradient Red
            'rgb(153, 255, 102)',      #Gradient Green
        ]
        legend_data = [True,True,True,True,]
        title_data = [
            'Bitcoin Drawdown Since Market Top',
            '<b>Days Since Market Top</b>',
            '<b>Drawdown Since Top</b>',
            '<b></b>']
        range_data = [[0,1500],[0,3],[-1,2]]
        autorange_data = [False,True,False]
        type_data = ['linear','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick=30)
        #fig.update_yaxes(tickformat='.0%')
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\cycle_charts\\top_cycle'
        self.write_html(fig,chart_name)

    def yearly_cycle(self):
        """"Price Growth over Days since halving for each cycle"""
        df = self.df_init
        #drop dates prior to first pricing for clean charts
        df = df[df.date > '18-06-2010']

        #Calculate Year
        df['year'] = pd.DatetimeIndex(df['date']).year
        #Calculate days into year
        df['days_to_event'] = df.date.dt.dayofyear

        loop_data=[[0,1,2,3,4,5,6,7,8,9,10],[]]

        df['refPriceUSD'] = 1
        df['yearly_roi'] = 0
        for i in range(2010,2021,1):
            #calculate price at start of period
            df.loc[df.year == i,'refPriceUSD'] = (
                float(df[df['year'] == i].reset_index().loc[0,['PriceUSD']])
            )

        #calculate roi from start of year
        df['yearly_roi'] = df['PriceUSD'] / df['refPriceUSD']

        x_data = [
            df[df['year']==2010]['days_to_event'],
            df[df['year']==2011]['days_to_event'],
            df[df['year']==2012]['days_to_event'],
            df[df['year']==2013]['days_to_event'],
            df[df['year']==2014]['days_to_event'],
            df[df['year']==2015]['days_to_event'],
            df[df['year']==2016]['days_to_event'],
            df[df['year']==2017]['days_to_event'],
            df[df['year']==2018]['days_to_event'],
            df[df['year']==2019]['days_to_event'],
            df[df['year']==2020]['days_to_event'],
        ]
        y_data = [
            df[df['year']==2010]['yearly_roi'],
            df[df['year']==2011]['yearly_roi'],
            df[df['year']==2012]['yearly_roi'],
            df[df['year']==2013]['yearly_roi'],
            df[df['year']==2014]['yearly_roi'],
            df[df['year']==2015]['yearly_roi'],
            df[df['year']==2016]['yearly_roi'],
            df[df['year']==2017]['yearly_roi'],
            df[df['year']==2018]['yearly_roi'],
            df[df['year']==2019]['yearly_roi'],
            df[df['year']==2020]['yearly_roi'],
        ]
        name_data = [
            '2010','2011','2012',
            '2013','2014','2015',
            '2016','2017','2018',
            '2019','2020',
        ]
        width_data      = [
            2,2,2,  2,2,2,  2,2,2,  2,2,
            ]
        opacity_data    = [
            1,1,1,  1,1,1,  1,1,1,  1,1,
            ]
        dash_data = [
            'solid','solid','solid',
            'solid','solid','solid',
            'solid','solid','solid',
            'solid','solid',]
        color_data = [
            '#ff0000','#ff8000','#ffff00',
            '#80ff00','#00ff00','#00ff80',
            '#00ffff','#0080ff','#0000ff',
            '#8000ff','#ff00ff',
        ]
        legend_data = [True,True,True,True,True,True,True,True,True,True,True,True,]
        title_data = [
            'Bitcoin Yearly Returns',
            '<b>Days into Year</b>',
            '<b>Growth Multiple Since Halving</b>',
            '<b></b>']
        range_data = [[0,370],[0,0],[0,0]]
        autorange_data = [False,True,False]
        type_data = ['linear','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick=30,tickformat='1./0f')
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\cycle_charts\\yearly_cycle'
        self.write_html(fig,chart_name)



#""" =================================
#    ADD VOLUME BAR CHARTS
#================================="""
#x_data = [
#    df['date'],
#]
#y_data = [
#    df['TxTfrValNtv'],
#]
#color_data = ['rgb(255, 102, 0)',]#Burnt Orange
#loop_data = [0]
#name_data = ['On-chain Vol (BTC)',]
#
#for i in loop_data:
#    fig.add_trace(
#        go.Bar(x=x_data[i],y=y_data[i],name=name_data[i],opacity=0.5,marker_color=color_data[i],yaxis="y2"))
#fig.update_layout(barmode='stack',bargap=0.01,yaxis2=dict(side="right",position=0.15))
#
#fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')


fig_btc = btc_chart_suite()

fig_btc.unrealised_PnL()


"""FAIR VALUE MODELS"""
fig_btc.difficulty_ribbon()






"""VALUATION MODELS"""
fig_btc.mvrv()
fig_btc.magic_lines_full()
fig_btc.magic_lines()
fig_btc.mayer_multiple()
fig_btc.puell_multiple()
fig_btc.block_subsidy()
fig_btc.difficulty_ribbon()
fig_btc.beam_indicator()
fig_btc.investor_tool()
fig_btc.golden_ratio()
fig_btc.golden_ratio_full()
fig_btc.catch_btm_top()
fig_btc.s2f_model()
fig_btc.nvt_rvt()


"""CYCLE MODELS"""
fig_btc.halving_cycle()
fig_btc.bottom_cycle()
fig_btc.top_cycle()
fig_btc.yearly_cycle()



