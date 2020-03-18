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
        self.df = btc_add_metrics().btc_coin()
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
            self.df[['date','PriceUSD']],
            left_on='date_event',right_on='date'
        )
        #Rename price column
        events = events.rename(columns={'PriceUSD':'PriceUSD_event'})
        #Finalise into self and drop additional date column
        self.events = events.drop(columns='date')


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
        df = self.df

        loop_data=[[0,1],[2,3,4,5,6]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            ['2000-01-01','2100-01-01'],    #Strong BUY
            ['2000-01-01','2100-01-01'],    #BUY
            ['2000-01-01','2100-01-01'],    #SELL
            ['2000-01-01','2100-01-01'],    #Strong SELL
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceRealUSD'],
            df['CapMVRVCur'],
            [0.7,0.7],
            [1.0,1.0],
            [2.6,2.6],
            [5,5],
        ]
        name_data = [
            'BTC Price (USD)',
            'Realised Price (USD)',
            'MVRV Ratio',
            'STRONG BUY (0.7)',
            'BUY (1.0)',
            'SELL (2.6)',
            'STRONG SELL (5.0)'
        ]
        width_data      = [2,2,1,2,2,2,2]
        opacity_data    = [1,1,1,1,1,1,1]
        dash_data = ['solid','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(255, 255, 255)',   #White
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True,True,]
        title_data = [
            'Bitcoin MVRV Ratio',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>MVRV Ratio</b>']
        range_data = [[self.start,self.last],[-1,5],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=False,secondary_y=False)
        fig.update_yaxes(showgrid=True,secondary_y=True)
        self.add_slider(fig)
        fig.show()

    def magic_lines_full(self):
        """"Prints Bitcoin Full History Magic Lines 200D, 128D, 200W and 128W (log)"""

        df = self.df
        
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
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(255, 80, 80)',   #Gradient Red
            'rgb(153, 255, 102)', #Gradient Green
            'rgb(255, 80, 80)',   #Gradient Red
            'rgb(153, 255, 102)', #Gradient Green
            'rgb(255,255,255)'    #White
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
        fig.show()

    def magic_lines(self):
        """"Prints Bitcoin Full History Magic Lines 200D, 128D, 200W and 128W (log)"""

        df = self.df
        
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
            'rgb(239, 125, 50)',    #Price Orange
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
        fig.show()

    def mayer_multiple(self):
        """"Mayer Multiple"""
        df = self.df
        
        df['Mayer_Multiple'] = (
            df['PriceUSD']
            / df['PriceUSD'].rolling(200).mean()
        )

        loop_data=[[0,1],[2,3,4,5,6]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            ['2000-01-01','2100-01-01'],    #Strong BUY
            ['2000-01-01','2100-01-01'],    #BUY
            ['2000-01-01','2100-01-01'],    #SELL
            ['2000-01-01','2100-01-01'],    #Strong SELL
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceUSD'].rolling(200).mean(),
            df['Mayer_Multiple'],
            [0.6,0.6],
            [0.8,0.8],
            [2.4,2.4],
            [3.4,3.4],
        ]
        name_data = [
            'BTC Market Cap (USD)',
            '200DMA',
            'Mayer Multiple',
            'STRONG BUY (0.6)',
            'BUY (0.8)',
            'SELL (2.4)',
            'STRONG SELL (3.4)'
        ]
        width_data      = [1,1,1,2,2,2,2]
        opacity_data    = [1,1,1,1,1,1,1]
        dash_data = ['solid','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(255, 255, 255)',   #White
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True,True]
        title_data = [
            'Bitcoin Mayer Multiple',
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
        fig.show()

    def mayer_multiple_bands(self):
        """"Mayer Multiple Bands"""
        df = self.df

        df['200DMA']        = df['PriceUSD'].rolling(200).mean()
        df['128DMA']     = df['PriceUSD'].rolling(128).mean()
        df['Mayer_SBUY']    = df['200DMA'] * 0.6
        df['Mayer_BUY']     = df['200DMA'] * 0.8
        df['Mayer_SELL']    = df['200DMA'] * 2.4
        df['Mayer_SSELL']   = df['200DMA'] * 3.4

        loop_data=[[0,1,3,4,5,6],[]]
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
            df['200DMA'],
            df['128DMA'],
            df['Mayer_SBUY'],
            df['Mayer_BUY'] ,
            df['Mayer_SELL'], 
            df['Mayer_SSELL'],
        ]
        name_data = [
            'BTC Price (USD)',
            '200DMA',
            '128DMA',
            'STRONG BUY (0.6)',
            'BUY (0.8)',
            'SELL (2.4)',
            'STRONG SELL (3.4)'
        ]
        width_data      = [2,1,1,   1,1,1,1]
        opacity_data    = [1,1,1,   1,1,1,1]
        dash_data = [
            'solid','solid','solid',
            'dash','dash','dash','dash',
            ]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(20, 169, 233)',    #Total Blue
            #'rgb(102, 255, 153)',   #Turquoise Green
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 204, 102)',   #Gradient Yellow
            'rgb(255, 153, 102)',   #Gradient Orange
            'rgb(255, 80, 80)',     #Gradient Red  
        ]
        legend_data = [True,True,True,True,True,True,True,]
        title_data = [
            'Bitcoin Mayer Multiple Bands',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b></b>']
        range_data = [['2011-01-01',self.last],[-1,5.397940009],[]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M3',tickformat='%d-%b-%y')
        self.add_slider(fig)
        fig.show()

    def puell_multiple(self):
            """"Puell Multiple"""
            df = self.df
            
            df['Puell_Multiple'] = (
                df['DailyIssuedUSD']
                / df['DailyIssuedUSD'].rolling(365).mean()
            )

            loop_data=[[0],[1,2,3,4,5]]
            x_data = [
                df['date'],
                df['date'],
                ['2000-01-01','2100-01-01'],    #Strong BUY
                ['2000-01-01','2100-01-01'],    #BUY
                ['2000-01-01','2100-01-01'],    #SELL
                ['2000-01-01','2100-01-01'],    #Strong SELL
            ]
            y_data = [
                df['PriceUSD'],
                df['Puell_Multiple'],
                [0.4,0.4],
                [0.6,0.6],
                [2.5,2.5],
                [5,5],
            ]
            name_data = [
                'BTC Market Cap (USD)',
                'Puell Multiple',
                'STRONG BUY (0.4)',
                'BUY (0.6)',
                'SELL (2.5)',
                'STRONG SELL (5.0)'
            ]
            width_data      = [1,1,2,2,2,2]
            opacity_data    = [1,1,1,1,1,1]
            dash_data = ['solid','solid','dash','dash','dash','dash']
            color_data = [
                'rgb(239, 125, 50)',    #Price Orange
                'rgb(255, 255, 255)',   #White
                'rgb(153, 255, 102)',   #Gradient Green
                'rgb(255, 255, 102)',   #Gradient Lime
                'rgb(255, 102, 102)',   #Gradient L.Red
                'rgb(255, 80, 80)',     #Gradient Red
            ]
            legend_data = [True,True,True,True,True,True]
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
            fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
            self.add_slider(fig)
            fig.show()

    def beam_indicator(self):
        """"BEAM Indicator (Bitcoin Economics Adaptive Multiple) 
        after https://bitcoineconomics.io/beam.html"""
        df = self.df

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
            ['2000-01-01','2100-01-01'],    #Strong BUY
            ['2000-01-01','2100-01-01'],    #BUY
            ['2000-01-01','2100-01-01'],    #SELL
            ['2000-01-01','2100-01-01'],    #Strong SELL
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
            'rgb(239, 125, 50)',    #Price Orange
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
        fig.show()

    def investor_tool(self):
        """"Bitcoin Investor Tool 730DMA after @PositiveCrypto"""
        df = self.df

        df['730DMA'] = df['PriceUSD'].rolling(730).mean()
        df['730DMAx5'] = df['730DMA']*5

        loop_data=[[0,1,2],[]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
        ]
        y_data = [
            df['PriceUSD'],
            df['730DMA'],
            df['730DMAx5'],
        ]
        name_data = [
            'BTC Price (USD)',
            'BUY Zone',
            'SELL Zone',
        ]
        width_data      = [2,2,2]
        opacity_data    = [1,1,1]
        fill_data = ['none','tonexty','tonexty']
        dash_data = ['solid','solid','solid']
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(153, 255, 102)', #Gradient Green
            'rgb(255, 80, 80)',   #Gradient Red
        ]
        legend_data = [True,True,True]
        title_data = [
            'Bitcoin Investor Tool',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b></b>']
        range_data = [[self.start,self.last],[-1,5],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=False,secondary_y=False)
        fig.update_yaxes(showgrid=True,secondary_y=True)
        self.add_slider(fig)
        
        #fig.add_annotation(
        #    x=0.5,
        #    y=(1.05),
        #    text='after:@PostiveCrypto',
        #    showarrow=False,
        #    xref="paper",
        #    yref="paper",
        #    opacity=0.75,
        #    font=dict(
        #        family='Raleway',
        #        size=16,
        #        color='rgb(50,50,50)'
        #    )
        #)

        #check_standard_charts().add_annotation(fig,'after:@PostiveCrypto')
        fig.show()

    def golden_ratio(self):
            """"Bitcoin Golden Ratio and Fib Levels after @PositiveCrypto"""
            df = self.df

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
            fig.show()
            return fig

    def golden_ratio_full(self):
            """"Bitcoin Golden Ratio and Fib Levels after @PositiveCrypto"""
            df = self.df

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
            fig.show()

    def catch_btm_top(self):
        """"Catching the Bottom and the Top"""

        df = self.df
        
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
        fig.show()

    def halving_cycle(self):
        """"Price Growth over Days since halving for each cycle"""
        df = self.df
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
            right_on='epoch'
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
        autorange_data = [False,False,False]
        type_data = ['linear','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick=30,tickformat='1./0f')
        self.add_slider(fig)
        fig.show()

    def bottom_cycle(self):
        """"Price Growth over Days since capitulation for each cycle"""
        df = self.df
        #Filter events to market capitulation event
        df2 = self.events[self.events['event']=='btm']
        #Merge events onto df, fill backwards
        df = pd.merge(
            df,df2,
            how='left',
            left_on='date',
            right_on='date_event'
        )
        #Fill forwards for all event data
        print(df.columns)
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
        autorange_data = [False,False,False]
        type_data = ['linear','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick=30)
        #fig.update_yaxes(tickformat='.0%')
        self.add_slider(fig)
        fig.show()
    
    def top_cycle(self):
        """"Price Drawdown over since market top for each cycle"""
        df = self.df
        #Filter events to market top event
        df2 = self.events[self.events['event']=='top']
        #Merge events onto df, fill forwards
        df = pd.merge(
            df,df2,
            how='left',
            left_on='date',
            right_on='date_event'
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
        autorange_data = [False,False,False]
        type_data = ['linear','log','log']
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick=30)
        #fig.update_yaxes(tickformat='.0%')
        self.add_slider(fig)
        fig.show()

    def s2f_model(self):
        """"Stock-to-flow Model(s) and multiple"""
        df = self.df

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


        loop_data=[[1,2,0],[3,4,5,6,7,8]]
        x_data = [
            df['date'], #Price
            df['date'], #CM S2F Model
            df['date'], #PB S2F Model
            df['date'], #CM Multiple
            df['date'], #PB Multiple
            ['2000-01-01','2100-01-01'],    #Strong BUY
            ['2000-01-01','2100-01-01'],    #BUY
            ['2000-01-01','2100-01-01'],    #SELL
            ['2000-01-01','2100-01-01'],    #Strong SELL
        ]
        y_data = [
            df['PriceUSD'],
            df['S2FPriceUSD_CM'].rolling(10).mean(),
            df['S2FPriceUSD_PB'].rolling(10).mean(),
            df['S2FMultiple_CM'],
            df['S2FMultiple_PB'],
            [0.2,0.2],
            [0.4,0.4],
            [1.6,1.6],
            [3.6,3.6],
        ]
        name_data = [
            'BTC Price (USD)',
            'S2F Model (Checkmate)',
            'S2F Model (Plan B)',
            'S2F Multiple (Checkmate)',
            'S2F Multiple (Plan B)',
            'STRONG BUY (0.2)',
            'BUY (0.4)',
            'SELL (1.6)',
            'STRONG SELL (3.6)',
        ]
        width_data      = [2,2,2,1,1,2,2,2,2]
        opacity_data    = [1,0.5,0.5,1,1,1,1,1,1]
        dash_data = ['solid','dot','dot','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(255, 255, 255)',   #White
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(255, 255, 255)',   #White
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True,True,True,True,]
        title_data = [
            'Bitcoin Stock-to-Flow Models',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>S2F Multiple</b>']
        range_data = [[self.start,self.last],[-2,5],[-2,5]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True)
        self.add_slider(fig)
        fig.show()


fig = btc_chart_suite()


#fig.mvrv()
#fig.magic_lines_full()
#fig.magic_lines()
#fig.mayer_multiple()
#fig.mayer_multiple_bands()
#fig.puell_multiple()
#fig.beam_indicator()
#fig.investor_tool()
#fig.golden_ratio()
#fig.golden_ratio_full()
#fig.catch_btm_top()
#fig.halving_cycle()
#fig.bottom_cycle()
#fig.top_cycle()
#fig.s2f_model()
