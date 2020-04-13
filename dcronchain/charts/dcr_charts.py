#Suite of pre-built charts for analysing Decred On-chain and price performance
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.general.standard_charts import *
from checkonchain.general.regression_analysis import *
from datetime import date, datetime, time, timedelta

class dcr_chart_suite():

    def __init__(self):
        self.today = datetime.combine(date.today(), time())
        self.last = pd.to_datetime(self.today + pd.to_timedelta(90,unit='D'))
        self.start = '2016-01-01'

        #USD RANGE LEVELS (USD)
        self.cap_lb     = 5     #Market Cap Lower Bound (log)
        self.cap_ub     = 10    #Market Cap Upper Bound (log)
        self.price_lb   = -1    #Price Lower Bound (log)
        self.price_ub   = 3     #Price Lower Bound (log)

        #BTC RANGE LEVELS (BTC)
        self.cap_lb_btc     = 2     #Market Cap Lower Bound (log)
        self.cap_ub_btc     = 6     #Market Cap Upper Bound (log)
        self.price_lb_btc   = -4    #Price Lower Bound (log)
        self.price_ub_btc   = -1     #Price Lower Bound (log)
        
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
        """
        Adds x-axis slider to chart
        INPUT: fig = Plotly figure item to add slider
        """
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True,
                    thickness=0.05
                )
            )
        )
        fig.update_yaxes(fixedrange=False)

    def write_html(self,fig,filename):
        "Writes chart to checkmatey.github.io"
        html_path = "D:\code_development\checkonchain\checkmatey.github.io\dcr_charts"
        html_path = html_path + str('\\') + filename + '.html'
        pio.write_html(fig, file=html_path, auto_open=True)

    def mvrv(self,model):
        """"Decred Realised Price and MVRV
            model = 0   = Network Valuation (Market Cap, Realised Cap etc)
            model = 1   = Pricing Model (Coin price, realised price etc)
        """
        df = self.df
        mvrv_lb = -0.522878745
        mvrv_ub = 1.301029996

        #STANDARD SETTINGS
        loop_data=[[0,1],[2,3,4,5,6]]
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
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            ['2016-01-01','2022-01-01'],    #Strong BUY
            ['2016-01-01','2022-01-01'],    #BUY
            ['2016-01-01','2022-01-01'],    #SELL
            ['2016-01-01','2022-01-01'],    #Strong SELL
        ]

        #MARKET CAP SETTINGS
        if model ==0:
            loop_data=[[0,1],[2]]
            y_data = [
                df['CapMrktCurUSD'],
                df['CapRealUSD'],
                df['CapMVRVCur'],
                [0.5,0.5],
                [0.7,0.7],
                [1.8,1.8],
                [2.4,2.4],
            ]
            name_data = [
                'Market Cap',
                'Realised Cap',
                'MVRV Ratio',
                'STRONG BUY (0.5)',
                'BUY (0.7)',
                'SELL (1.8)',
                'STRONG SELL (2.4)'
            ]
            title_data = [
                '<b>Decred MVRV Ratio Valuation</b>',
                '<b>Date</b>',
                '<b>Network Valuation (USD)</b>',
                '<b>MVRV Ratio</b>']
            range_data = [[self.start,self.last],[self.cap_lb,self.cap_ub],[mvrv_lb,mvrv_ub]]
        
        #MARKET CAP SETTINGS
        elif model ==1:
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
                'DCR Price',
                'Realised Price',
                'MVRV Ratio',
                'STRONG BUY (0.5)',
                'BUY (0.7)',
                'SELL (1.8)',
                'STRONG SELL (2.4)'
            ]
            title_data = [
                '<b>Decred MVRV Ratio Pricing</b>',
                '<b>Date</b>',
                '<b>Price (USD)</b>',
                '<b>MVRV Ratio</b>']
            range_data = [[self.start,self.last],[-1,3],[mvrv_lb,mvrv_ub]]
        
        #BUILD CHART
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True)
        self.add_slider(fig)
        
        #Write out html chart
        if model == 0:
            chart_name = '\\valuation_models\\mvrv_valuation'
        elif model ==1:
            chart_name = '\\pricing_models\\mvrv_pricing'
        self.write_html(fig,chart_name)

    def difficulty_ribbon(self):
        """Decred Difficulty Ribbon and Block Subsidy Model

        Block Subsidy model paid after @permabullnino
        Realised cap after @Coinmetrics
        Difficulty Ribbon after @woonomic

        """
        df = self.df

        loop_data=[[0,1,2,3,4,5,],[6]]
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
            df['CapMrktCurUSD'],
            df['CapRealUSD'],
            df['PoW_income_usd'].cumsum(),
            df['PoS_income_usd'].cumsum(),
            df['Fund_income_usd'].cumsum(),
            df['Total_income_usd'].cumsum(),
            df['DiffMean'],
        ]
        name_data = [
            'Market Cap',
            'Realised Cap',
            'POW-USD',
            'POS-USD',
            'Treasury-USD',
            'Total-USD',
            'Difficulty',
            ]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(250, 38, 53)',     #POW Red
            'rgb(114, 49, 163)',    #POS Purple
            'rgb(255, 192, 0)',     #Treasury Yellow
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(46, 214, 161)',    #Turquoise
        ]
        dash_data = [
            'solid','dash','solid','solid','solid','solid','solid',
            ]
        width_data = [2,2,2,2,2,2,2]
        opacity_data = [1,1,1,1,1,1,1]
        legend_data = [True,True,True,True,True,True,True]#
        autorange_data = [True,False,True]
        type_data = ['date','log','log']#
        title_data = [
            '<b>Decred Difficulty Ribbon</b>',
            '<b>Date</b>',
            '<b>Network Valuation</b>',
            '<b>Difficulty</b>']
        range_data = [[self.start,self.last],[self.cap_lb,self.cap_ub],[0,0]]

        #BUILD FINAL CHART
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
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
                showlegend=True,
                line=dict(
                    width=i/200*2,
                    color='rgb(46, 214, 161)',#Turquoise
                    dash='solid'
                    )),
                secondary_y=True)
        
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\valuation_models\\difficulty_ribbon'
        self.write_html(fig,chart_name)

    def block_subsidy_usd(self,model):
        """Decred Block Subsidy Models priced in USD with Difficulty Ribbon
        after @permabullnino
        INPUTS:
            model = 0   = Network Valuation (Market Cap, Realised Cap etc)
            model = 1   = Pricing Model (Coin price, realised price etc)
        """
        df = self.df

        #Block Subsidy Models
        df['SubsidyPoWCapUSD']   = df['PoW_income_usd'].cumsum()
        df['SubsidyPoSCapUSD']   = df['PoS_income_usd'].cumsum()
        df['SubsidyFundCapUSD']  = df['Fund_income_usd'].cumsum()
        df['SubsidyCapUSD']      = df['Total_income_usd'].cumsum()

        #Adjusted Supply Issued Cap (EXPERIMENTAL)
        df['AdjSubsidyCapUSD'] = df['SubsidyCapUSD'] *10*(101/100)**(np.floor(df['blk']/6144))
        df['AdjSubsidyPriceUSD'] = df['AdjSubsidyCapUSD'] / df['SplyCur']

        #STANDARD SETTINGS
        loop_data=[[0,1,2,3,5,4],[]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
        ]
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(250, 38, 53)',     #POW Red
            'rgb(114, 49, 163)',    #POS Purple
            'rgb(255, 192, 0)',     #Treasury Yellow
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(20, 169, 233)',    #Total Blue
        ]
        dash_data = ['solid','solid','solid','solid','solid','solid','dash']
        width_data = [2,2,2,2,2,2]
        opacity_data = [1,1,1,1,1,1]
        legend_data = [True,True,True,True,True,True]#
        autorange_data = [True,False,False]
        type_data = ['date','log','log']#
        
        #MARKET CAP SETTINGS
        if model ==0:
            y_data = [
                df['CapMrktCurUSD'],
                df['SubsidyPoWCapUSD'],
                df['SubsidyPoSCapUSD'],
                df['SubsidyFundCapUSD'],
                df['SubsidyCapUSD'],
                df['AdjSubsidyCapUSD']
            ]
            name_data = [
                'Market Cap',
                'POW-USD',
                'POS-USD',
                'Treasury-USD',
                'Total-USD', 
                'Supply Issued Cap (USD)'
            ]
            title_data = [
                'Decred Block Subsidy Valuation Models (USD)',
                'Date',
                'Network Valuation (USD)',
                'N/A'
            ]
            range_data = [[self.start,self.last],[self.cap_lb,self.cap_ub],[5,11]]
        #MARKET CAP SETTINGS
        elif model == 1:
            y_data = [
                df['PriceUSD'],
                df['PoW_income_usd'].cumsum()/df['SplyCur'],
                df['PoS_income_usd'].cumsum()/df['SplyCur'],
                df['Fund_income_usd'].cumsum()/df['SplyCur'],
                df['Total_income_usd'].cumsum()/df['SplyCur'],
                df['IssuedPriceUSD']
            ]
            name_data = [
                'DCR/USD Price', 
                'POW-USD',
                'POS-USD',
                'Treasury-USD',
                'Total-USD',
                'Supply Issued Price (USD)'
                ]
            title_data = [
                'Decred Block Subsidy Pricing Models (USD)',
                'Date',
                'DCR Price (USD)',
                'Difficulty'
            ]
            range_data = [[self.start,self.last],[self.price_lb,self.price_ub],[5,11]]
        
        #BUILD CHARTS
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')
        
        #Only Add Volume Bars and Difficulty Ribbon to PRICING MODELS
        if model == 1:
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


        #FINALISE CHART
        self.add_slider(fig)
        fig = check_standard_charts().add_annotation(fig,"@checkmatey<br />@permabullnino")

        #Write out html chart
        if model == 0:
            chart_name = '\\valuation_models\\block_subsidy_usd_valuation'
        elif model ==1:
            chart_name = '\\pricing_models\\block_subsidy_usd_pricing'
        self.write_html(fig,chart_name)

    def block_subsidy_btc(self,model):
        """Decred Block Subsidy Models priced in BTC with Difficulty Ribbon
        after @permabullnino
        INPUTS:
            model = 0   = Network Valuation (Market Cap, Realised Cap etc)
            model = 1   = Pricing Model (Coin price, realised price etc)
        """
        df = self.df

        #Block Subsidy Models
        df['SubsidyPoWCapBTC']   = df['PoW_income_btc'].cumsum()
        df['SubsidyPoSCapBTC']   = df['PoS_income_btc'].cumsum()
        df['SubsidyFundCapBTC']  = df['Fund_income_btc'].cumsum()
        df['SubsidyCapBTC']      = df['Total_income_btc'].cumsum()

        #Adjusted Supply Issued Cap (EXPERIMENTAL)
        df['AdjSubsidyCapBTC'] = df['SubsidyCapBTC'] *10*(101/100)**(np.floor(df['blk']/6144))
        df['AdjSubsidyPriceBTC'] = df['AdjSubsidyCapBTC'] / df['SplyCur']

        #STANDARD SETTINGS
        loop_data = [[0,1,2,3,6,4],[5]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            ]
        color_data = [
            'rgb(250, 38, 53)' , #POW Red
            'rgb(114, 49, 163)', #POS Purple
            'rgb(255, 192, 0)',  #Treasury Yellow
            'rgb(20, 169, 233)', #Total Blue
            'rgb(255, 255, 255)', #White
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(20, 169, 233)', #Total Blue
            ]
        dash_data = ['solid','solid','solid','solid','solid','solid','dash']
        width_data = [2,2,2,2,2,2,2]
        opacity_data = [1,1,1,1,1,1,1]
        legend_data = [True,True,True,True,True,True,True,True]#
        autorange_data = [False,False,False]
        type_data = ['date','log','linear']#

        #NETWORK VALUATION SETTINGS
        if model == 0:
            y_data = [
                df['SubsidyPoWCapBTC'],
                df['SubsidyPoSCapBTC'],
                df['SubsidyFundCapBTC'],
                df['SubsidyCapBTC'],
                df['CapMrktCurBTC'],
                df['dcr_tic_sply_avg'],
                df['AdjSubsidyCapBTC'],
                ]
            name_data = [
                'POW (BTC)',
                'POS (BTC)',
                'Treasury (BTC)',
                'Total (BTC)',
                'Market Cap (BTC)',
                'Ticket Pool Value (DCR)',
                'Supply Issued Cap (BTC)'
                ]
            title_data = [
                'Decred Block Subsidy Valuation Models (BTC)',
                'Date',
                'Network Valuation (BTC)',
                'Total DCR in Tickets'
                ]
            range_data = [[self.start,self.last],[self.cap_lb_btc,self.cap_ub_btc],[0,1]]

        #PRICING SETTINGS
        elif model == 1:
            y_data = [
                df['SubsidyPoWCapBTC']/df['SplyCur'],
                df['SubsidyPoSCapBTC']/df['SplyCur'],
                df['SubsidyFundCapBTC']/df['SplyCur'],
                df['SubsidyCapBTC']/df['SplyCur'],
                df['PriceBTC'],
                df['dcr_tic_sply_avg'],
                df['IssuedPriceBTC'],
                ]
            name_data = [
                'POW (BTC)',
                'POS (BTC)',
                'Treasury (BTC)',
                'Total (BTC)',
                'DCR Price (BTC)',
                'Ticket Pool Value (DCR)',
                'Supply Issued Price (BTC)'
                ]
            title_data = [
                'Decred Block Subsidy Pricing Models (BTC)',
                'Date',
                'DCR Price (BTC)',
                'Total DCR in Tickets'
                ]
            range_data = [[self.start,self.last],[self.price_lb_btc,self.price_ub_btc],[0,1]]
        

        #BUILD CHARTS
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

        #ADD VOLUME BARS ONLY TO PRICING MODELS
        if model == 1:
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
        
        #FINALISE CHART
        fig = check_standard_charts().add_annotation(fig,"@checkmatey<br />@permabullnino")
        self.add_slider(fig)

        #Write out html chart
        if model == 0:
            chart_name = '\\valuation_models\\block_subsidy_btc_valuation'
        elif model ==1:
            chart_name = '\\pricing_models\\block_subsidy_btc_pricing'
        self.write_html(fig,chart_name)

    def commitment_usd(self,model):
        """Decred USD Stakeholder Commitment Models

        Block Subsidy model paid after @permabullnino
        Cumulative ticket value locked after @checkmatey
        Realised cap after @Coinmetrics

        INPUTS:
            model = 0   = Network Valuation (Market Cap, Realised Cap etc)
            model = 1   = Pricing Model (Coin price, realised price etc)
        """
        df = self.df

        df['IssuedCapUSD'] = df['DailyIssuedNtv'] * df['PriceUSD']
        df['IssuedCapUSD'] = df['IssuedCapUSD'].cumsum()
        df['IssuedCapUSD'] = df['IssuedCapUSD'] *10*(101/100)**(np.floor(df['blk']/6144))
        df['IssuedPriceUSD'] = df['IssuedCapUSD'] / df['SplyCur']

        #STANDARD SETTINGS
        loop_data=[[0,1,2,3,4,5,6,7],[]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
        ]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(250, 38, 53)',     #POW Red
            'rgb(114, 49, 163)',    #POS Purple
            'rgb(255, 192, 0)',     #Treasury Yellow
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(156,225,143)',     #Turquoise Green
        ]
        dash_data = ['solid','dash','solid','solid','solid','solid','solid','dash']
        width_data = [2,2,2,2,2,2,3,2]
        opacity_data = [1,1,1,1,1,1,1,1]
        legend_data = [True,True,True,True,True,True,True,True,]#
        autorange_data = [True,False,False]
        type_data = ['date','log','log']#

        #NETWORK VALUATION SETTINGS
        if model == 0:
            y_data = [
                df['CapMrktCurUSD'],
                df['CapRealUSD'],
                df['PoW_income_usd'].cumsum(),
                df['PoS_income_usd'].cumsum(),
                df['Fund_income_usd'].cumsum(),
                df['Total_income_usd'].cumsum(),
                df['tic_usd_cost'].cumsum(),
                df['IssuedCapUSD'],
                df['IssuedCapUSD']
            ]
            name_data = [
                'Market Cap',
                'Realised Cap',
                'POW-USD',
                'POS-USD',
                'Treasury-USD',
                'Total-USD',
                'Tickets Bound Cap',
                'Supply Issued Cap',
                ]
            title_data = [
                '<b>Decred Stakeholder Commitments Valuations (USD)</b>',
                '<b>Date</b>',
                '<b>Network Valuation</b>',
                '<b></b>']
            range_data = [[self.start,self.last],[self.cap_lb,self.cap_ub],[0,0]]

        #PRICING MODELS SETTINGS
        if model == 1:
            y_data = [
                df['PriceUSD'],
                df['PriceRealUSD'],
                df['PoW_income_usd'].cumsum()/df['SplyCur'],
                df['PoS_income_usd'].cumsum()/df['SplyCur'],
                df['Fund_income_usd'].cumsum()/df['SplyCur'],
                df['Total_income_usd'].cumsum()/df['SplyCur'],
                df['tic_usd_cost'].cumsum()/df['SplyCur'],
                df['IssuedPriceUSD'],
            ]
            name_data = [
                'DCR/USD Price',
                'Realised Price',
                'POW-USD',
                'POS-USD',
                'Treasury-USD',
                'Total-USD',
                'Tickets Bound Price',
                'Supply Issued Price'
                ]
            title_data = [
                '<b>Decred Stakeholder Commitments Pricing Models (USD)</b>',
                '<b>Date</b>',
                '<b>DCR/USD Pricing</b>',
                '<b></b>']
            range_data = [[self.start,self.last],[self.price_lb,self.price_ub],[0,0]]


        #BUILD FINAL CHART
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')

        self.add_slider(fig)

        #Write out html chart
        if model == 0:
            chart_name = '\\valuation_models\\commitments_usd_valuation'
        elif model ==1:
            chart_name = '\\pricing_models\\commitments_usd_pricing'
        self.write_html(fig,chart_name)

    def commitment_btc(self,model):
        """Decred BTC Stakeholder Commitment Models

        Block Subsidy model paid after @permabullnino
        Cumulative ticket value locked after @checkmatey
        Realised cap after @Coinmetrics
        
        INPUTS:
            model = 0   = Network Valuation (Market Cap, Realised Cap etc)
            model = 1   = Pricing Model (Coin price, realised price etc)
        """
        df = self.df

        df['IssuedCapBTC'] = df['DailyIssuedNtv'] * df['PriceBTC']
        df['IssuedCapBTC'] = df['IssuedCapBTC'].cumsum()
        df['IssuedCapBTC'] = df['IssuedCapBTC'] *10*(101/100)**(np.floor(df['blk']/6144))
        df['IssuedPriceBTC'] = df['IssuedCapBTC'] / df['SplyCur']

        #STANDARD SETTINGS
        loop_data=[[0,1,2,3,4,5,6,7],[]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
        ]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(250, 38, 53)',     #POW Red
            'rgb(114, 49, 163)',    #POS Purple
            'rgb(255, 192, 0)',     #Treasury Yellow
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(156,225,143)',     #Turquoise Green
        ]
        dash_data = ['solid','dash','solid','solid','solid','solid','solid','dash']
        width_data = [2,2,2,2,2,2,3,2]
        opacity_data = [1,1,1,1,1,1,1,1]
        legend_data = [True,True,True,True,True,True,True,True,]#
        autorange_data = [True,False,False]
        type_data = ['date','log','log']


        #NETWORK VALUATION SETTINGS
        if model == 0:
            y_data = [
                df['CapMrktCurBTC'],
                df['CapRealBTC'],
                df['PoW_income_btc'].cumsum(),
                df['PoS_income_btc'].cumsum(),
                df['Fund_income_btc'].cumsum(),
                df['Total_income_btc'].cumsum(),
                df['tic_btc_cost'].cumsum(),
                df['IssuedCapBTC'],
            ]
            name_data = [
                'Market Cap',
                'Realised Cap',
                'POW-BTC',
                'POS-BTC',
                'Treasury-BTC',
                'Total-BTC',
                'Tickets Bound Cap',
                'Supply Issued Cap'
                ]
            title_data = [
                '<b>Decred Stakeholder Commitments Valuations (BTC)</b>',
                '<b>Date</b>',
                '<b>Network Valuation</b>',
                '<b></b>']
            range_data = [[self.start,self.last],[self.cap_lb_btc,self.cap_ub_btc],[0,0]]
        #PRICING MODELS SETTINGS
        if model == 1:
            y_data = [
                df['PriceBTC'],
                df['PriceRealBTC'],
                df['PoW_income_btc'].cumsum()/df['SplyCur'],
                df['PoS_income_btc'].cumsum()/df['SplyCur'],
                df['Fund_income_btc'].cumsum()/df['SplyCur'],
                df['Total_income_btc'].cumsum()/df['SplyCur'],
                df['tic_btc_cost'].cumsum()/df['SplyCur'],
                df['IssuedPriceBTC']
            ]
            name_data = [
                'DCR/BTC Price',
                'Realised Price',
                'POW-BTC',
                'POS-BTC',
                'Treasury-BTC',
                'Total-BTC',
                'Tickets Bound Price',
                'Supply Issued Price',
                ]
            title_data = [
                '<b>Decred Stakeholder Commitments Pricing Models (BTC)</b>',
                '<b>Date</b>',
                '<b>DCR/BTC Pricing</b>',
                '<b></b>']
            range_data = [[self.start,self.last],[self.price_lb_btc,self.price_ub_btc],[0,0]]

        #BUILD FINAL CHART
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')

        self.add_slider(fig)

        #Write out html chart
        if model == 0:
            chart_name = '\\valuation_models\\commitment_btc_valuation'
        elif model ==1:
            chart_name = '\\pricing_models\\commitment_btc_pricing'
        self.write_html(fig,chart_name)

    def s2f_model(self,model):
        """Decred Stock to Flow Models

        Linear Regression for Price OR Market Cap after @checkmatey
        Stock to flow model by PlanB @100TrillionUSD for Bitcoin applied to DCR S2F for ref
        
        INPUTS:
            model = 0   = Network Valuation (Market Cap, Realised Cap etc)
            model = 1   = Pricing Model (Coin price, realised price etc)
        """
        df = self.df[['date','age_sply','S2F','PriceUSD','SplyCur','CapMrktCurUSD']]
        df = df.dropna(axis=0)
     
        #Run OLS Linear Regression for full dataset
        x = 'S2F'
        y = 'CapMrktCurUSD'

        analysis    = regression_analysis().ln_regression_OLS(df,x,y,True)
        df          = analysis['df']
        reg_model   = analysis['model']
        df['S2F_Price_predict'] = df['S2F_CapMr_predict'] / df['SplyCur']

        #Calc S2F Model - Bitcoins Plan B Model
        df['S2F_Price_predict_PB']    = np.exp(-1.84)*df['S2F']**3.36
        df['S2F_CapMr_predict_PB']    = df['S2F_Price_predict_PB'] * df['SplyCur']
        df['S2F_Price_multiple_PB']   = df['PriceUSD'] / df['S2F_Price_predict_PB']
        #Trim first value due to genesis spiking S2F results
        df = df[1:]

        #df_sply = dcr_add_metrics().dcr_sply_curtailed(1051200)
        #
        #df_sply['S2FCap'] = np.exp(
        #    reg_model.params['const'] 
        #    + reg_model.params[x]
        #    * df_sply['S2F_ideal']
        #)

        #STANDARD SETTINGS
        loop_data=[[0,2,1],[4,3,5,6,7,8]]
        x_data = [
            df['date'], #Price
            df['date'], #CM S2F Model
            df['date'], #PB S2F Model
            #Secondary
            df['date'], #CM Multiple
            df['date'], #PB Multiple
            ['2016-01-01','2022-01-01'],    #Strong BUY
            ['2016-01-01','2022-01-01'],    #BUY
            ['2016-01-01','2022-01-01'],    #SELL
            ['2016-01-01','2022-01-01'],    #Strong SELL
        ]
        width_data      = [2,0.5,0.5,    1,0.5,   2,2,2,2]
        opacity_data    = [1,1,0.45,  1,0.45,  1,1,1,1]
        dash_data = ['solid','dot','dot','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(255,255,255)',    #White
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True,True,True,True,True,True,]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']

        #NETWORK VALUATION SETTINGS
        if model == 0:
            y_data = [
                df['CapMrktCurUSD'],
                df['S2F_CapMr_predict'],
                df['S2F_CapMr_predict_PB'],
                #Secondary
                df['S2F_CapMr_multiple'],
                df['S2F_Price_multiple_PB'],
                [0.1,0.1],
                [0.4,0.4],
                [3,3],
                [8,8],
            ]
            name_data = [
                'Market Cap (USD)',
                'S2F Model (Checkmate)',
                'S2F Model (Plan B)',
                'S2F Multiple (Checkmate)',
                'S2F Multiple (Plan B)',
                'STRONG BUY (0.1)',
                'BUY (0.4)',
                'SELL (3.0)',
                'STRONG SELL (8.0)',
            ]
            title_data = [
                '<b>Decred Stock-to-Flow Network Valuation (USD)</b>',
                '<b>Date</b>',
                '<b>Network Valuation (USD)</b>',
                '<b>S2F Multiple</b>']
            range_data = [[self.start,self.last],[self.cap_lb,self.cap_ub],[-2,5]]
        
        elif model == 1:
            y_data = [
                df['PriceUSD'],
                df['S2F_Price_predict'],
                df['S2F_Price_predict_PB'],
                #Secondary
                df['S2F_CapMr_multiple'],
                df['S2F_Price_multiple_PB'],
                [0.1,0.1],
                [0.4,0.4],
                [3,3],
                [8,8],
            ]
            name_data = [
                'DCR Price (USD)',
                'S2F Model (Checkmate)',
                'S2F Model (Plan B)',
                'S2F Multiple (Checkmate)',
                'S2F Multiple (Plan B)',
                'STRONG BUY (0.1)',
                'BUY (0.4)',
                'SELL (3.0)',
                'STRONG SELL (8.0)',
            ]
            title_data = [
                '<b>Decred Stock-to-Flow Price Model (USD)</b>',
                '<b>Date</b>',
                '<b>Price (USD)</b>',
                '<b>S2F Multiple</b>']
            range_data = [[self.start,self.last],[self.price_lb,self.price_ub],[-2,5]]
        
        
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True)
        self.add_slider(fig)

        #Write out html chart
        if model == 0:
            chart_name = '\\valuation_models\\s2f_model_valuation'
        elif model ==1:
            chart_name = '\\pricing_models\\s2f_model_pricing'
        self.write_html(fig,chart_name)

    def s2f_model_residuals(self):
        """Decred Stock to Flow Models - Residuals

        Shows the distance Price or Market Cap have moved away from the mean
        """
        df = self.df[['date','age_sply','S2F','PriceUSD','SplyCur','CapMrktCurUSD']]
        df = df.dropna(axis=0)

        #Run OLS Linear Regression for Decred dataset
        df = regression_analysis().ln_regression_OLS(df,'S2F','CapMrktCurUSD',True)['df']
        df['S2F_Price_predict'] = df['S2F_CapMr_predict'] / df['SplyCur']
        #Trim first value due to genesis spiking S2F results
        df = df[1:]

        #Run OLS Linear Regression for Bitcoin dataset
        df2 = btc_add_metrics().btc_coin()
        df2 = df2[['date','age_sply','S2F','PriceUSD','SplyCur','CapMrktCurUSD']]
        df2['CapMrktCurUSD'] = df2['PriceUSD'] * df2['SplyCur']
        df2 = df2.dropna(axis=0)
        df2 = regression_analysis().ln_regression_OLS(df2,'S2F','CapMrktCurUSD',True)['df']
        
        #Add Bitcoin Halvings
        df3 = btc_add_metrics().btc_sply_halvings_step()
        df3 = df3[:10]
        df3['y_arb'].replace(to_replace=0,value=-10,inplace=True)
        df3['y_arb'].replace(to_replace=1e20,value=10,inplace=True)
        
        #STANDARD SETTINGS
        loop_data=[[3,4,5,6],[0,1,2]]
        x_data = [
            df['age_sply'],     #DCR Price
            df2['age_sply'],    #BTC Price
            df3['age_sply'],    #Halvings
            [-1,2],    # Arbitrary Ceiling for Sell Fill
            [-1,2],    # BUY
            [-1,2],    # Arbitrary Ceiling for Sell Fill
            [-1,2],    # SELL
        ]
        y_data = [
            df['S2F_CapMr_residual'].rolling(14).mean(),
            df2['S2F_CapMr_residual'].rolling(14).mean(),
            df3['y_arb'],
            [-10,-10],
            [-1.5,-1.5],
            [10,10],
            [1.5,1.5],
        ]
        name_data = [
            'Decred S2F Residuals',
            'Bitcoin S2F Residuals',
            'Bitcoin Halvings',
            'N/A',
            'BUY ZONE (-1.5 stdev)',
            'N/A',
            'SELL ZONE (-1.5 stdev)',
        ]
        title_data = [
            '<b>Decred Stock-to-Flow Model Residuals</b>',
            '<b>Coin Age (% of 21M Supply Mined)</b>',
            '<b>Standard Deviations from Mean</b>',
            '<b></b>'
        ]
        width_data      = [4,1.5,1,  2,2,2,2]
        opacity_data    = [1,0.75,1,  0.25,0.25,0.25,0.25]
        fill_data       = ['none','none','none','none','tonexty','none','tonexty',]
        dash_data = ['solid','solid','dash','dash','dash','dash','dash']
        color_data = [
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(255, 255, 255)',    #White
            'rgb(50, 50, 50)',    #Background
            'rgba(153, 255, 102,0.25)',   #Gradient Green
            'rgb(50, 50, 50)',    #Background
            'rgba(255, 80, 80,0.25)',     #Gradient Red
        ]
        legend_data = [True,True,True,False,True,False,True]
        autorange_data = [False,False,False]
        type_data = ['linear','linear','linear']
        range_data = [[0,1],[-4,4],[-4,4]]      
        fig = check_standard_charts().subplot_lines_doubleaxis_1st_area(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data,
            fill_data
            )
        fig.update_xaxes(dtick='0.1',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True)
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\oscillators\\s2f_residuals'
        self.write_html(fig,chart_name)

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
            ['2016-01-01','2022-01-01'],    #Strong BUY
            ['2016-01-01','2022-01-01'],    #BUY
            ['2016-01-01','2022-01-01'],    #SELL
            ['2016-01-01','2022-01-01'],    #Strong SELL
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
        width_data      = [2,2,1,2,2,2,2]
        opacity_data    = [1,1,1,1,1,1,1]
        dash_data = ['solid','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(46, 214, 161)',    #Turquoise
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

        #Write out html chart
        chart_name = '\\oscillators\\mayer_multiple'
        self.write_html(fig,chart_name)

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
        range_data = [[self.start,self.last],[-1,3],[]]
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
        chart_name = '\\pricing_models\\mayer_multiple_pricing'
        self.write_html(fig,chart_name)

    def puell_multiple(self):
        """"Puell Multiple"""
        df = self.df

        #Calculate Puell Multiple expanding from 0 to 365 day MA
        df['Puell_Multiple'] = 0
        for i in df.index:
            _a = min(i,364)
            _b = df['DailyIssuedUSD'].rolling(_a).mean().loc[i]
            _c = df.loc[i,'DailyIssuedUSD']
            df.loc[i,'Puell_Multiple'] = _c / _b

        loop_data=[[0],[1,2,3,4,5]]
        x_data = [
            df['date'],
            df['date'],
            ['2016-01-01','2022-01-01'],    #Strong BUY
            ['2016-01-01','2022-01-01'],    #BUY
            ['2016-01-01','2022-01-01'],    #SELL
            ['2016-01-01','2022-01-01'],    #Strong SELL
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
            'DCR Price (USD)',
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
            'rgb(255, 255, 255)',   #White
            'rgb(46, 214, 161)',    #Turquoise
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

        #Write out html chart
        chart_name = '\\oscillators\\puell_multiple'
        self.write_html(fig,chart_name)

    def contractor_multiple(self):
        """"Contractor Multiple"""
        df = self.df

        #Calculate Contractor Multiple expanding from 0 to 30 day MA
        df['Contractor_Multiple'] = df['PriceUSD'] / df['PriceUSD'].rolling(30).mean()

        loop_data=[[0,1],[2,3,4]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            ['2016-01-01','2022-01-01'],    #BUY
            ['2016-01-01','2022-01-01'],    #SELL
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceUSD'].rolling(30).mean(),
            df['Contractor_Multiple'],
            [0.6,0.6],
            [1.7,1.7],
        ]
        name_data = [
            'DCR Price (USD)',
            'DCR Price 30DMA (USD)',
            'Contractor_Multiple',
            'BUY (0.6)',
            'SELL (1.7)'
        ]
        width_data      = [2,1,1,2,2]
        opacity_data    = [1,1,1,1,1,1,1]
        dash_data = ['solid','solid','solid','dash','dash']
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(46, 214, 161)',    #Turquoise
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True]
        title_data = [
            '<b>Decred Contractor Multiple</b>',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>Contractor Multiple</b>']
        range_data = [[self.start,self.last],[-1,3],[-0.6931471805599453,3]]
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
        chart_name = '\\oscillators\\contractor_multiple'
        self.write_html(fig,chart_name)

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
            [-0.2,-0.2],
            [0.05,0.05],
            [1.0,1.0],
            [1.2,1.2],
        ]
        name_data = [
            'BTC Price (USD)',
            'BEAM Lower Band',
            'BEAM Upper Band',
            'BEAM Indicator',
            'STRONG BUY (-0.2)',
            'BUY (0.05)',
            'SELL (1.0)',
            'STRONG SELL (1.2)'
        ]
        width_data      = [2,2,2,1,2,2,2,2]
        opacity_data    = [1,1,1,1,1,1,1,1]
        dash_data = ['solid','solid','solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 80, 80)',     #Gradient Red
            'rgb(46, 214, 161)',    #Turquoise
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
        range_data = [[self.start,self.last],[-1,3],[-1,10]]
        autorange_data = [False,False,False]
        type_data = ['date','log','linear']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True,dtick=0.5)
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\pricing_models\\BEAM_indicator'
        self.write_html(fig,chart_name)

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

        #Write out html chart
        chart_name = '\\cycle_charts\\bottom_cycle'
        self.write_html(fig,chart_name)
    
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

        #Write out html chart
        chart_name = '\\cycle_charts\\top_cycle'
        self.write_html(fig,chart_name)

    def TVWAP(self):
        """
        #############################################################################
                            REALISED CAP + 142DAY CAP
        #############################################################################
        """
        df = self.df
        #14 Day TVWAP
        df['14day_TVWAP'] = (
            (df['tic_usd_cost'].rolling(14).sum()
            / df['dcr_tic_vol'].rolling(14).sum())
        )
        df['14day_TVWAP_Ratio'] = df['14day_TVWAP'] / df['PriceUSD']
        df['14day_TVWAP_Cap']   = df['14day_TVWAP'] * df['dcr_sply']


        #28 Day TVWAP
        df['28day_TVWAP'] = (
            (df['tic_usd_cost'].rolling(28).sum()
            / df['dcr_tic_vol'].rolling(28).sum())
        )
        df['28day_TVWAP_Ratio'] = df['28day_TVWAP'] / df['PriceUSD']
        df['28day_TVWAP_Cap']   = df['28day_TVWAP'] * df['dcr_sply']


        #142 Day TVWAP
        df['142day_TVWAP'] = (
            (df['tic_usd_cost'].rolling(142).sum()
            / df['dcr_tic_vol'].rolling(142).sum())
        )
        df['142day_TVWAP_Ratio'] = df['142day_TVWAP'] / df['PriceUSD']
        df['142day_TVWAP_Cap']   = df['142day_TVWAP'] * df['dcr_sply']


        loop_data=[[0,1,2,3,4],[5,6,7,   8,9,10,11]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            #Ratios
            df['date'],
            df['date'],
            df['date'],

            ['2015-01-01','2021-01-01'],    #Strong BUY
            ['2015-01-01','2021-01-01'],    #BUY
            ['2015-01-01','2021-01-01'],    #SELL
            ['2015-01-01','2021-01-01'],    #Strong SELL
        ]
        y_data = [
            df['CapMrktCurUSD'],
            df['CapRealUSD'],
            df['14day_TVWAP_Cap'],
            df['28day_TVWAP_Cap'],
            df['142day_TVWAP_Cap'],
            #Ratios
            df['14day_TVWAP_Ratio'],
            df['28day_TVWAP_Ratio'],
            df['142day_TVWAP_Ratio'],

            [0.65,0.65],    #Strong BUY
            [0.90,0.90],    #BUY
            [1.20,1.20],    #SELL
            [1.45,1.45],    #Strong SELL
        ]
        name_data = [
            'DCR/USD Price',
            'Realised Price',
            '14-Day TVWAP',
            '28-Day TVWAP',
            '142-Day TVWAP',
            #Ratios
            '14 Day Ratio',
            '28 Day Ratio',
            '142 Day Ratio',
            'STRONG BUY (0.65)',
            'BUY (0.90)',
            'SELL (1.20)',
            'STRONG SELL (1.45)'
            ]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(17, 255, 125)',    #Powerpoint Green
            'rgb(255, 192, 0)',     #Treasury Yellow
            'rgb(250, 38, 53)',     #POW Red
            'rgb(20, 169, 233)',    #Total Blue
            #Ratios
            'rgb(255, 192, 0)',     #Treasury Yellow
            'rgb(250, 38, 53)',     #POW Red
            'rgb(20, 169, 233)',    #Total Blue
            
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 255, 102)',   #Gradient Lime
            'rgb(255, 102, 102)',   #Gradient L.Red
            'rgb(255, 80, 80)',     #Gradient Red

        ]
        dash_data = ['solid','solid','solid','solid','solid',   'solid','solid','solid' ,'dash','dash','dash','dash']
        width_data = [2,2,1,1,2,  1,1,1,   2,2,2,2]
        opacity_data = [1,1,1,1,1,   1,1,1,   0.75,0.75,0.75,0.75,]
        legend_data = [True,True,True,True,True,     True,True,True,     True,True,True,True,]#
        title_data = [
            '<b>Decred TVWAP Capitalisation</b>',
            '<b>Date</b>',
            '<b>Decred Valuation</b>',
            '<b>TVWAP Ratios</b>']
        range_data = [['2016-01-01','2020-06-01'],[6,9],[0,5]]
        autorange_data = [False,False,False]
        type_data = ['date','log','linear']#
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')
        fig = check_standard_charts().add_annotation(fig,"@checkmatey<br />@permabullnino")
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\valuation_models\\TVWAP'
        self.write_html(fig,chart_name)

    def hodler_conversion(self):
        """"Decred Hodler COnversion Rates
            after @permabullnino"""
        df = self.df

        #142 Day TVWAP
        df['142day_TVWAP'] = (
            (df['tic_usd_cost'].rolling(142).sum()
            / df['dcr_tic_vol'].rolling(142).sum())
        )
        df['142day_TVWAP_Ratio'] = df['142day_TVWAP'] / df['PriceUSD']
        df['142day_TVWAP_Cap']   = df['142day_TVWAP'] * df['dcr_sply']

        #Calculate Hodler Conversion Rate
        df['hconv142d'] = (
            (df['dcr_tic_vol'].rolling(142).sum() 
                / df['TxTfrValNtv'].rolling(142).sum())
            -
            (df['dcr_tic_vol'].rolling(28).sum() 
                / df['dcr_sply'])
        )

        #Create positive and Negative datasets
        df['hconv142d_pos'] = np.where(df['hconv142d'] >= 0, df['hconv142d'], 0)
        df['hconv142d_neg'] = np.where(df['hconv142d'] < 0, df['hconv142d'], 0)

        #CHART
        loop_data=[[0,1,2],[3,4]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceRealUSD'],
            df['142day_TVWAP'],
            df['hconv142d_pos'],
            df['hconv142d_neg'],

        ]
        name_data = [
            'DCR Price (USD)',
            'Realised Price (USD)',
            '142-Day TVWAP',
            'Hodler Conversion Rate +ve',
            'Hodler Conversion Rate -ve',
        ]
        fill_data = ['','','','tozeroy','tozeroy']
        width_data      = [2,2,2,2,2]
        opacity_data    = [1,1,1,1,1]
        dash_data = ['solid','solid','solid','solid','solid',]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(17, 255, 125)',    #Powerpoint Green
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(255, 80, 80)',     #Gradient Red
            'rgb(153, 255, 102)',   #Gradient Green
        ]
        legend_data = [True,True,True,True,True,]
        title_data = [
            '<b>Decred HODLer Converstion Rate</b>',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>HODLer Conversion Rate</b>']
        range_data = [[self.start,self.last],[-2,3],[-0.5,1.5]]
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
        fig.update_yaxes(showgrid=False,secondary_y=True,tickformat=',.0%',dtick=0.25)
        self.add_slider(fig)

        fig = check_standard_charts().add_annotation(fig,"@checkmatey<br />@permabullnino")     
        
        #Write out html chart
        chart_name = '\\oscillators\\hodler_conversion'
        self.write_html(fig,chart_name)

    def ticket_overunder(self):
        """"Decred Ticket Over/Under Measure
            after @permabullnino"""
        df = self.df

        df['tic_overunder'] = (
            df['dcr_tic_vol'].rolling(28).sum()
            /
            df['dcr_tic_vol'].rolling(142).sum()
        )

        #CHART
        loop_data=[[0,1],[2,3,4]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            ['2016-01-01','2022-01-01','2022-01-01','2016-01-01'],    #BUY ZONE
            ['2016-01-01','2022-01-01','2022-01-01','2016-01-01'],    #SELL ZONE
        ]
        y_data = [
            df['PriceBTC'],
            df['PriceRealBTC'],
            df['tic_overunder'],
            [0.199,0.199,0.200,0.200],
            [0.210,0.210,0.211,0.211],
        ]
        name_data = [
            'DCR Price (BTC)',
            'Realised Price (BTC)',
            'Ticket Over/Under Measure',
            'Buy Zone',
            'Sell Zone',
        ]
        width_data      = [2,2,2,1,1]
        opacity_data    = [1,1,1,1,1]
        dash_data = ['solid','solid','solid','dash','dash',]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(17, 255, 125)',    #Powerpoint Green
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,]
        title_data = [
            '<b>Decred Ticket Over/Under Measure</b>',
            '<b>Date</b>',
            '<b>Price (BTC)</b>',
            '<b>Ticket Over/Under Measure</b>']
        range_data = [['2018-01-01',self.last],[-3.698970004,-1.698970004],[0.190,0.240]]
        autorange_data = [False,False,False]
        type_data = ['date','log','linear']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True,dtick=0.005)
        self.add_slider(fig)

        fig = check_standard_charts().add_annotation(fig,"@checkmatey<br />@permabullnino")     

        #Write out html chart
        chart_name = '\\oscillators\\ticket_overunder'
        self.write_html(fig,chart_name)

    def tic_vol_sum_142day(self):
        """"Decred 142-day sum of tickets with Fibonacci multiple bands 
            after @permabullnino"""
        df = self.df

        df['tic_usd_cost_142sum'] = df['tic_usd_cost'].rolling(142).sum()/df['dcr_sply']

        loop_data=[[0,1,2,3,4],[]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            df['date'],
        ]
        y_data = [
            df['PriceUSD'],
            df['tic_usd_cost_142sum'],
            df['tic_usd_cost_142sum']*0.236,
            df['tic_usd_cost_142sum']*0.382,
            df['tic_usd_cost_142sum']*0.618,
        ]
        name_data = [
            'DCR/USD Price',
            '142d Ticket USD Sum',
            '142d Ticket USD Sum x23.6%',
            '142d Ticket USD Sum x38.2%',
            '142d Ticket USD Sum x61.8%',
            ]
        color_data = [
            'rgb(255, 255, 255)',    #WHite
            'rgb(255, 80, 80)',     #Gradient Red
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 204, 102)',   #Gradient Yellow
            'rgb(255, 204, 102)',   #Gradient Yellow
        ]
        dash_data = ['solid','solid','solid','dash','dash']
        width_data = [2,2,2,1,1]
        opacity_data = [1,1,1,1,1]
        legend_data = [True,True,True,True,True]#
        title_data = [
            '<b>Decred 142-Day Ticket USD Sum</b>',
            '<b>Date</b>',
            '<b>DCR/USD Pricing</b>',
            '']
        range_data = [[self.start,self.last],[-1,3],[5,11]]
        autorange_data = [True,False,False]
        type_data = ['date','log','log']#
        fig = check_standard_charts().subplot_lines_singleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')

        self.add_slider(fig)
        fig = check_standard_charts().add_annotation(fig,"@checkmatey<br />@permabullnino")

        #Write out html chart
        chart_name = '\\pricing_models\\142day_ticket_volume'
        self.write_html(fig,chart_name)

    def tx_volatility_ratio(self):
        """"Decred Transactional Volatility Ratio
            after @permabullnino"""
        df = self.df

        df['tx_volatile_ratio'] = (
            df['dcr_tfr_vol'].rolling(28).sum()
            /
            df['dcr_tfr_vol'].rolling(142).sum()
        )

        df['tx_volatile_ratio_Ntv'] = (
            df['TxTfrValAdjNtv'].rolling(28).sum()
            /
            df['TxTfrValAdjNtv'].rolling(142).sum()
        )

        #CHART
        loop_data=[[0,1],[2,3,4,5]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            ['2016-01-01','2022-01-01','2022-01-01','2016-01-01'],    #BUY ZONE
            ['2016-01-01','2022-01-01','2022-01-01','2016-01-01'],    #SELL ZONE
        ]
        y_data = [
            df['PriceBTC'],
            df['PriceRealBTC'],
            df['tx_volatile_ratio'],
            df['tx_volatile_ratio_Ntv'],
            [0.15,0.15,0.17,0.17],
            [0.26,0.26,0.28,0.28],
        ]
        name_data = [
            'DCR Price (BTC)',
            'Realised Price (BTC)',
            'Transaction Volatility (dcrdata)',
            'Transaction Volatility (CoinMetrics)',
            'Buy Zone',
            'Sell Zone',
        ]
        width_data      = [2,2,2,2,1,1]
        opacity_data    = [1,1,1,1,1,1]
        dash_data = ['solid','solid','dash','solid','dash','dash',]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(17, 255, 125)',    #Powerpoint Green
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True]
        title_data = [
            '<b>Decred Transactional Volatility</b>',
            '<b>Date</b>',
            '<b>Price (BTC)</b>',
            '<b>Transaction Volatility Ratio</b>'
            ]
        range_data = [[self.start,self.last],[-4,-1.698970004],[0,1]]
        autorange_data = [False,False,False]
        type_data = ['date','log','linear']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True,dtick=0.05)
        self.add_slider(fig)

        fig = check_standard_charts().add_annotation(fig,"@checkmatey<br />@permabullnino")     

        #Write out html chart
        chart_name = '\\oscillators\\tx_volatility_ratio'
        self.write_html(fig,chart_name)

    def tx_sum_adjsply_142d(self):
        """"Decred 142day Sum of coins moved, adjusted for supply
        after @permabullnino"""
        df = self.df

        #df['tx_dcr_142sum']     = df['TxTfrValNtv'].rolling(142).sum() / df['SplyCur']
        df['tx_dcr_142sum_adj'] = df['TxTfrValAdjNtv'].rolling(142).sum() / df['SplyCur']

        loop_data=[[0],[1,2,3,4,5]]
        x_data = [
            df['date'],
            df['date'],
            [self.start,self.last],    #BUY ZONE Ceiling
            [self.start,self.last],    #BUY ZONE Floor
            [self.start,self.last],    #SELL ZONE Ceiling
            [self.start,self.last],    #SELL ZONE Floor
        ]
        y_data = [
            df['PriceUSD'],
            df['tx_dcr_142sum_adj'],
            [1.1,1.1],
            [0.75,0.75],
            [2.1,2.1],
            [1.7,1.7],
        ]
        name_data = [
            'DCR Price (USD)',
            'tx_dcr_142sum_adj',
            'LOW ACTIVITY',
            'N/A',
            'HIGH ACTIVITY',
            'N/A',
        ]
        width_data      = [2,2,2,2,2,2]
        opacity_data    = [1,1,1,1,1,1]
        dash_data = ['solid','solid','dash','dash','dash','dash']
        color_data = [
            'rgb(46, 214, 161)',    #Turquoise
            #'rgb(239, 125, 50)',    #Price Orange
            'rgb(255, 255, 255)',   #White
            'rgba(0,255,255,0.3)', #Retro Blue
            'rgba(0,255,255,0.3)', #Retro Blue
            'rgba(255,0,255,0.3)', #Retro Pink
            'rgba(255,0,255,0.3)', #Retro Pink
        ]
        legend_data = [True,True,True,False,True,False,]
        fill_data       = ['none','none','none','tonexty','none','tonexty',]
        title_data = [
            '<b>Decred 142-Day Moved Coins Adjusted for Supply</b>',
            '<b>Date</b>',
            '<b>Price USD</b>',
            '<b>142-day DCR Sum Moved / Supply</b>']
        range_data = [[self.start,self.last],[self.price_lb,self.price_ub],[0,3.5]]
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
        fig.update_yaxes(showgrid=False,secondary_y=True)
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\oscillators\\tx_sum_adjsply_142d'
        self.write_html(fig,chart_name)

    def max_vol_ratio(self):
        """"Decred Maximum Volume Ratio
            after @permabullnino"""
        df = self.df

        df['max_vol_ratio_USD'] = (
            df['CapMrktCurUSD']
            /
            df['tic_usd_cost'].rolling(28).sum()
        )

        df['max_vol_ratio_BTC'] = (
            df['CapMrktCurBTC']
            /
            df['tic_btc_cost'].rolling(28).sum()
        )

        #CHART
        loop_data=[[0,1],[2,3,4,5]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            df['date'],
            [self.start,self.last,self.last,self.start],    #BUY ZONE
            [self.start,self.last,self.last,self.start],    #SELL ZONE
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceRealUSD'],
            df['max_vol_ratio_USD'],
            df['max_vol_ratio_BTC'],
            [0.15,0.15,0.17,0.17],
            [0.26,0.26,0.28,0.28],
        ]
        name_data = [
            'DCR Price (BTC)',
            'Realised Price (BTC)',
            'max_vol_ratio_USD',
            'max_vol_ratio_BTC',
            'Buy Zone',
            'Sell Zone',
        ]
        width_data      = [2,2,2,2,1,1]
        opacity_data    = [1,1,1,1,1,1]
        dash_data = ['solid','solid','solid','dash','dash','dash',]
        color_data = [
            'rgb(255, 255, 255)',   #White
            'rgb(17, 255, 125)',    #Powerpoint Green
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(153, 255, 102)',   #Gradient Green
            'rgb(255, 80, 80)',     #Gradient Red
        ]
        legend_data = [True,True,True,True,True,True]
        title_data = [
            '<b>Decred Max Vol Ratio</b>',
            '<b>Date</b>',
            '<b>Price (BTC)</b>',
            '<b>Transaction Volatility Ratio</b>'
            ]
        range_data = [[self.start,self.last],[-3.698970004,-2.522878745],[0.0,5.0]]
        autorange_data = [False,False,False]
        type_data = ['date','log','linear']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        fig.update_yaxes(showgrid=False,secondary_y=True,dtick=0.05)
        self.add_slider(fig)

        fig = check_standard_charts().add_annotation(fig,"@checkmatey<br />@permabullnino")     

        #Write out html chart
        chart_name = '\\oscillators\\max_volume_ratio'
        self.write_html(fig,chart_name)

    def nvt_rvt(self):
        """"Bitcoin NVT and RVT Ratio"""
        df = pd.DataFrame()
        df = self.df

        #Calculate NVT and RVT 28 and 90DMA
        
        for i in [28,90]:
            name_nvt = 'NVT_' + str(i)
            name_rvt = 'RVT_' + str(i)

            df[name_nvt] = (
                df['CapMrktCurUSD'].rolling(i).mean()
                / df['TxTfrValAdjUSD'].rolling(i).mean()
            )

            df[name_rvt] = (
                df['CapRealUSD'].rolling(i).mean()
                / df['TxTfrValAdjUSD'].rolling(i).mean()
            )
            
            #Calculate NVTS and RVTS (28DMA on Tx only)
            if i == 28:
                df['NVTS'] = (
                    df['CapMrktCurUSD']
                    / df['TxTfrValAdjUSD'].rolling(i).mean()
                )
                
                df['RVTS'] = (
                    df['CapRealUSD']
                    / df['TxTfrValAdjUSD'].rolling(i).mean()
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
            [250,250],
            [175,175],
            [100,100],
            [50,50],
            [50,50]
        ]
        name_data = [
            'DCR Price (USD)',
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
            '<b>Decred NVT and RVT Ratio</b>',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>NVT or RVT Ratio</b>']
        range_data = [[self.start,self.last],[-2,3],[0,500]]
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
        fig.update_yaxes(showgrid=False,secondary_y=True,dtick=50)
        self.add_slider(fig)

        #Write out html chart
        chart_name = '\\oscillators\\nvt_rvt'
        self.write_html(fig,chart_name)


"""MODEL"""
fig_dcr = dcr_chart_suite()

fig_dcr.difficulty_ribbon()

"""NETWORK VALUATION"""
fig_dcr.mvrv(0)

fig_dcr.block_subsidy_usd(0)
fig_dcr.block_subsidy_btc(0)

fig_dcr.commitment_usd(0)
fig_dcr.commitment_btc(0)

fig_dcr.s2f_model(0)
fig_dcr.s2f_model_residuals()

fig_dcr.nvt_rvt()

"""PRICING MODELS"""
fig_dcr.mvrv(1)

fig_dcr.block_subsidy_usd(1)
fig_dcr.block_subsidy_btc(1)

fig_dcr.commitment_usd(1)
fig_dcr.commitment_btc(1)

fig_dcr.s2f_model(1)

fig_dcr.mayer_multiple()
fig_dcr.mayer_multiple_bands()

fig_dcr.beam_indicator()

fig_dcr.puell_multiple()
fig_dcr.contractor_multiple()

"""Market Cycle Metrics"""


fig_dcr.bottom_cycle()
fig_dcr.top_cycle()


"""PermabullNino Metrics"""

fig_dcr.TVWAP()
fig_dcr.hodler_conversion()
fig_dcr.ticket_overunder()
fig_dcr.tic_vol_sum_142day()
fig_dcr.tx_volatility_ratio()
fig_dcr.tx_sum_adjsply_142d()
fig_dcr.max_vol_ratio()
