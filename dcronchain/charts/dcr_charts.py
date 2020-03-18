#Suite of pre-built charts for analysing Decred On-chain and price performance
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.general.standard_charts import *
from checkonchain.general.regression_analysis import *
from datetime import date, datetime, time, timedelta

class dcr_chart_suite():

    def __init__(self):
        self.today = datetime.combine(date.today(), time())
        self.last = pd.to_datetime(self.today + pd.to_timedelta(90,unit='D'))
        self.start = '2016-01-01'
        self.df = dcr_add_metrics().dcr_ticket_models()
        #Create dataframe with key events like market tops, btms and halvings
        events = pd.DataFrame(
            data = [
                [np.datetime64('2016-02-08'),'genesis',0],
                [np.datetime64('2016-12-26'),'btm',0],
                [np.datetime64('2018-01-13'),'top',0],
            ],
            columns = ['date_event','event','epoch']
        )
        #Convert to UTC Timezone
        events['date_event'] = events['date_event'].dt.tz_localize('UTC')
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
        """"Decred Realised Price and MVRV"""
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
            [0.5,0.5],
            [0.7,0.7],
            [1.8,1.8],
            [2.4,2.4],
        ]
        name_data = [
            'DCR Price (USD)',
            'Realised Price (USD)',
            'MVRV Ratio',
            'STRONG BUY (0.5)',
            'BUY (0.7)',
            'SELL (1.8)',
            'STRONG SELL (2.4)'
        ]
        width_data      = [2,2,1,2,2,2,2]
        opacity_data    = [1,1,1,1,1,1,1]
        dash_data = ['solid','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(255, 255, 255)',   #White
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True,True,]
        title_data = [
            '<b>Decred MVRV Ratio</b>',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>MVRV Ratio</b>']
        range_data = [[self.start,self.last],[-1,3],[-0.522878745,1.301029996]]
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

    def block_subsidy_usd(self):
        """
        #############################################################################
                            DCR USD BLOCK SUBSIDY MODELS
        #############################################################################
        """
        df = self.df

        loop_data=[[0,1,2,3,4],[5]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
        ]
        y_data = [
            df['PoW_income_usd'].cumsum()/df['SplyCur'],
            df['PoS_income_usd'].cumsum()/df['SplyCur'],
            df['Fund_income_usd'].cumsum()/df['SplyCur'],
            df['Total_income_usd'].cumsum()/df['SplyCur'],
            df['PriceUSD'],
            df['DiffMean'],
        ]
        name_data = [
            'POW-USD',
            'POS-USD',
            'Treasury-USD',
            'Total-USD',
            'DCR/USD Price', 
            'Difficulty Ribbon   ',
            ]
        color_data = [
            'rgb(250, 38, 53)',     #POW Red
            'rgb(114, 49, 163)',    #POS Purple
            'rgb(255, 192, 0)',     #Treasury Yellow
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(46, 214, 161)',    #Turquoise
            #'rgb(156,225,143)',     #Turquoise Green
        ]
        dash_data = ['solid','solid','solid','solid','solid','solid']
        width_data = [2,2,2,2,2,1,]
        opacity_data = [1,1,1,1,1,1,]
        legend_data = [True,True,True,True,True,True,]#
        title_data = [
            'Decred Miner Subsidy Models',
            'Date',
            'DCR/USD Pricing',
            'Difficulty']
        range_data = [['01-02-2016','01-02-2020'],[-2,3],[5,11]]
        autorange_data = [True,False,False]
        type_data = ['date','log','log']#
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')

        """ =================================
            ADD DIFFICULTY RIBBON
        ================================="""
        for i in [9,14,25,40,60,90,128,200]:
            fig.add_trace(go.Scatter(
                mode='lines',
                x=df['date'], 
                y=df['DiffMean'].rolling(i).mean(),
                name='Difficulty '+str(i),
                opacity=0.5,
                showlegend=False,
                line=dict(
                    width=i/200*2,
                    color='rgb(46, 214, 161)',#Turquoise
                    dash='solid'
                    )),
                secondary_y=True)
        """ =================================
            ADD VOLUME BAR CHARTS
        ================================="""
        x_data = [
            df['date'],
            df['date']
        ]
        y_data = [
            100000+df['dcr_tic_vol'],
            100000+df['dcr_tfr_vol']
        ]
        color_data = ['rgb(237,96,136)','rgb(37,187,217)']
        loop_data = [0,1]
        name_data = ['Ticket Vol (DCR)','Transfer Vol (DCR)']

        for i in loop_data:
            fig.add_trace(
                go.Bar(x=x_data[i],y=y_data[i],name=name_data[i],opacity=0.5,marker_color=color_data[i],yaxis="y2"))
        fig.update_layout(barmode='stack',bargap=0.01,yaxis2=dict(side="right",position=0.15))

        self.add_slider(fig)
        fig.show()

    def block_subsidy_btc(self):
        """
        #############################################################################
                            DCR BTC BLOCK SUBSIDY MODELS
        #############################################################################
        """
        df = self.df

        loop_data = [[0,1,2,3,4],[5]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            ]
        y_data = [
            df['PoW_income_btc'].cumsum()/df['SplyCur'],
            df['PoS_income_btc'].cumsum()/df['SplyCur'],
            df['Fund_income_btc'].cumsum()/df['SplyCur'],
            df['Total_income_btc'].cumsum()/df['SplyCur'],
            df['PriceBTC'],
            df['dcr_tic_sply_avg'],
            ]
        name_data = [
            'POW (BTC)',
            'POS (BTC)',
            'Treasury (BTC)',
            'Total (BTC)',
            'DCR/BTC Price',
            'Ticket Pool Value (DCR)',
            ]
        color_data = [
            'rgb(250, 38, 53)' , #POW Red
            'rgb(114, 49, 163)', #POS Purple
            'rgb(255, 192, 0)',  #Treasury Yellow
            'rgb(20, 169, 233)', #Total Blue
            'rgb(239, 125, 50)', #Price Orange
            'rgb(46, 214, 161)',    #Turquoise
            #'rgb(156,225,143)',  #Turquoise Green
            ]
        dash_data = ['solid','solid','solid','solid','solid','solid','solid']
        width_data = [2,2,2,2,2,2,1]
        opacity_data = [1,1,1,1,1,1,1]
        legend_data = [True,True,True,True,True,True,True]#
        title_data = ['Decred Stakeholder Subsidy Models','Date','Network Valuation (BTC)','Total DCR in Tickets']
        range_data = [['01-02-2016','01-02-2020'],[-4,-1],[0,1]]
        autorange_data = [True,False,True]
        type_data = ['date','log','linear']#
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,
            x_data,
            y_data,
            name_data,
            color_data,
            dash_data,
            width_data,
            opacity_data,
            legend_data
        )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')

        """ =================================
            ADD VOLUME BAR CHARTS
        ================================="""
        x_data = [
            df['date'],
            df['date']
        ]
        y_data = [
            df['dcr_tic_vol'],
            df['dcr_tfr_vol']
        ]
        color_data = ['rgb(237,96,136)','rgb(37,187,217)']
        loop_data = [0,1]
        name_data = ['Ticket Vol (DCR)','Transfer Vol (DCR)']
        for i in loop_data:
            fig.add_trace(
                go.Bar(x=x_data[i],y=y_data[i],name=name_data[i],marker_color=color_data[i]),secondary_y=True)
        fig.update_layout(barmode='stack',bargap=0.01)
        fig.show()

    def mayer_multiple(self):
        """"Decred Mayer Multiple"""
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
            [0.4,0.4],
            [0.5,0.5],
            [1.6,1.6],
            [2.8,2.8],
        ]
        name_data = [
            'DCR Market Cap (USD)',
            '200DMA',
            'Mayer Multiple',
            'STRONG BUY (0.4)',
            'BUY (0.5)',
            'SELL (1.6)',
            'STRONG SELL (2.8)'
        ]
        width_data      = [1,1,1,2,2,2,2]
        opacity_data    = [1,1,1,1,1,1,1]
        dash_data = ['solid','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(255, 255, 255)',   #White
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True,True]
        title_data = [
            '<b>Decred Mayer Multiple</b>',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>Mayer Multiple</b>']
        range_data = [[self.start,self.last],[-1,3],[-1,2]]
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
        df['Mayer_SBUY']    = df['200DMA'] * 0.4
        df['Mayer_BUY']     = df['200DMA'] * 0.5
        df['Mayer_SELL']    = df['200DMA'] * 1.6
        df['Mayer_SSELL']   = df['200DMA'] * 2.8

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
            'DCR Price (USD)',
            '200DMA',
            '128DMA',
            'STRONG BUY (0.4)',
            'BUY (0.5)',
            'SELL (1.6)',
            'STRONG SELL (2.8)'
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
            'rgb(237, 109, 71)',    #Decred Orange
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 204, 102)',   #Gradient Yellow
            'rgb(255, 153, 102)',   #Gradient Orange
            'rgb(255, 80, 80)',     #Gradient Red  
        ]
        legend_data = [True,True,True,True,True,True,True,]
        title_data = [
            '<b>Decred Mayer Multiple Bands</b>',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b></b>']
        range_data = [['2016-01-01',self.last],[-1,3],[]]
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

        #Calculate Puell Multiple expanding from 0 to 365 day MA
        df['Puell_Multiple'] = 0
        for i in df.index:
            _a = min(i,364)
            _b = df['DailyIssuedUSD'].rolling(_a).mean().loc[i]
            _c = df.loc[i,'DailyIssuedUSD']
            df['Puell_Multiple'].loc[i] = _c / _b

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
            'DCR Market Cap (USD)',
            'Puell Multiple',
            'STRONG BUY (0.4)',
            'BUY (0.6)',
            'SELL (2.5)',
            'STRONG SELL (5.0)'
        ]
        width_data      = [2,1,2,2,2,2]
        opacity_data    = [1,1,1,1,1,1]
        dash_data = ['solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(255, 255, 255)',   #White
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True]
        title_data = [
            '<b>Decred Puell Multiple</b>',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>Puell Multiple</b>']
        range_data = [[self.start,self.last],[-1,3],[-1,2]]
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
            _b = df['PriceUSD'].rolling(_a).mean().loc[i] * 0.4
            _c = df.loc[i,'PriceUSD']
            df.loc[i,'BEAM'] = np.log(_c / _b) / 1
            df.loc[i,'BEAM_lower'] = _b
            df.loc[i,'BEAM_upper'] = _b * 15.2281175

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
            [0.05,0.05],
            [1.0,1.0],
            [1.2,1.2],
        ]
        name_data = [
            'BTC Price (USD)',
            'BEAM Lower Band',
            'BEAM Upper Band',
            'BEAM Indicator',
            'STRONG BUY (0.0)',
            'BUY (0.05)',
            'SELL (1.0)',
            'STRONG SELL (1.2)'
        ]
        width_data      = [2,2,2,1,2,2,2,2]
        opacity_data    = [1,1,1,1,1,1,1,1]
        dash_data = ['solid','solid','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(46, 214, 161)',    #Turquoise
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
            '<b>Decred BEAM Indicator<b>',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>BEAM Indicator</b>']
        range_data = [[self.start,self.last],[-1,3],[-0.2,2.4]]
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
        #print(df.columns)
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
            'Epoch 1 (Genesis-2016)',
            'Epoch 2 (2016-2020)',
            'Epoch 3 (X)',
            'Epoch 4 (X)',
        ]
        width_data      = [2,2,2,2]
        opacity_data    = [1,1,1,1]
        dash_data = ['solid','solid','solid','solid',]
        color_data = [
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(78,205,233)',      #Total Blue
            'rgb(255, 80, 80)',      #Gradient Red
            'rgb(153, 255, 102)',      #Gradient Green
        ]
        legend_data = [True,True,True,True,]
        title_data = [
            '<b>Decred Price Growth Since Cycle Low</b>',
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
            'Epoch 1 (2018-20)',
            'Epoch 2 (X)',
            'Epoch 3 (X)',
            'Epoch 4 (X)',
        ]
        width_data      = [2,2,2,2]
        opacity_data    = [1,1,1,1]
        dash_data = ['solid','solid','solid','solid',]
        color_data = [
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(78,205,233)',      #Total Blue
            'rgb(255, 80, 80)',      #Gradient Red
            'rgb(153, 255, 102)',      #Gradient Green
        ]
        legend_data = [True,True,True,True,]
        title_data = [
            '<b>Decred Drawdown Since Market Top</b>',
            '<b>Days Since Market Top</b>',
            '<b>Drawdown Since Top</b>',
            '<b></b>']
        range_data = [[0,1500],[-1.301029996,0],[-1,2]]
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
        btc_s2f_model = regression_analysis().ln_regression(df,'S2F','CapMrktCurUSD','date')['model_params']
        df['S2FCapMrktUSD_CM'] = (
            np.exp(float(btc_s2f_model['intercept']))
            * df['S2F']**float(btc_s2f_model['coefficient'])
            )
        df['S2FPriceUSD_CM'] = df['S2FCapMrktUSD_CM'] / df['SplyCur']
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
            [0.1,0.1],
            [0.4,0.4],
            [5,5],
            [20,20],
        ]
        name_data = [
            'BTC Price (USD)',
            'S2F Model (Checkmate)',
            'S2F Model (Plan B)',
            'S2F Multiple (Checkmate)',
            'S2F Multiple (Plan B)',
            'STRONG BUY (0.1)',
            'BUY (0.4)',
            'SELL (5.0)',
            'STRONG SELL (20.0)',
        ]
        width_data      = [2,2,2,1,1,2,2,2,2]
        opacity_data    = [1,0.5,0.5,1,1,1,1,1,1]
        dash_data = ['solid','dot','dot','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(255,255,255)',    #White
            #'rgb(239, 125, 50)',    #Price Orange
            'rgb(112, 203, 255)',   #Decred L Blue
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(112, 203, 255)',   #Decred L Blue
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True,True,True,True,]
        title_data = [
            '<b>Decred Stock-to-Flow Models</b>',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>S2F Multiple</b>']
        range_data = [[self.start,self.last],[-1,3],[-2,5]]
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


fig = dcr_chart_suite()


#fig.mvrv()
#fig.block_subsidy_usd()
#fig.block_subsidy_btc()
#fig.mayer_multiple()
#fig.mayer_multiple_bands()



#fig.puell_multiple()
fig.beam_indicator()

#fig.bottom_cycle()
#fig.top_cycle()
fig.s2f_model()


#df = dcr_add_metrics().dcr_ticket_models()

#df[['DailyIssuedUSD','DailyIssuedNtv','PriceUSD']]



