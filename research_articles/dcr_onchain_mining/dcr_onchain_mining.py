#Module for printing charts contained in dcr_charts
from checkonchain.dcronchain.charts.dcr_charts import *
from checkonchain.dcronchain.dcr_security_model import *

class dcr_mining_chart_suite():

    def __init__(self,theme):
        """
        Modules for producing standard check-onchain charts for Decred
        INPUT = theme (string)
            theme = 'light' = light theme chart
            theme = 'dark'  = dark theme chart (default)
        """
        self.theme = theme
        self.chart = check_standard_charts(self.theme)
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

    def color_invert(self,color_data):
        """Inverts colors in a list
        INPUT
            color_data = list of 'rgb(rrr,ggg,bbb)' or 'rgba(rrr,ggg,bbb,a.aa)'
        """
        j = 0
        for i in color_data: #cycle through all colors
            if self.theme == 'light': #if light theme
                #split rbg and invert colors
                text = i.split('(')[1]
                text = text.split(')')[0]
                text = text.split(',')
                r = 255-int(text[0])
                g = 255-int(text[1])
                b = 255-int(text[2])
                if len(text) ==3:
                    text = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b) + ')'
                if len(text) ==4:
                    a = float(text[3])
                    text = 'rgba(' + str(r) + ',' + str(g) + ',' + str(b) + ',' + str(a) + ')'
                color_data[j] = text
            j = j + 1
        return color_data

    def difficulty_ribbon(self):
        """Decred Difficulty Ribbon and Block Subsidy Model

        Block Subsidy model paid after @permabullnino
        Realised cap after @Coinmetrics
        Difficulty Ribbon after @woonomic

        """
        df = self.df

        loop_data=[[0,],[6]]
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
        #Invert Colors for Light Theme
        color_data = self.color_invert(color_data)
        dash_data = [
            'solid','dash','solid','solid','solid','solid','solid',
            ]
        width_data = [2,2,2,2,2,2,2]
        opacity_data = [1,0.5,0.5,0.5,0.5,0.5,1]
        legend_data = [True,True,True,True,True,True,True]#
        autorange_data = [False,False,False]
        type_data = ['date','log','log']#
        title_data = [
            '<b>Decred Difficulty Ribbon</b>',
            '<b>Date</b>',
            '<b>Network Valuation</b>',
            '<b>Difficulty</b>']
        range_data = [[self.start,self.last],[self.cap_lb,self.cap_ub],[6,11]]

        #BUILD FINAL CHART
        fig = self.chart.subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_yaxes(showgrid=True,secondary_y=False)
        
        """ =================================
            ADD DIFFICULTY RIBBON
        ================================="""
        color_ribbon = str(color_data[6])
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
                    color=color_ribbon,#Turquoise
                    dash='solid'
                    )),
                secondary_y=True)
        
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')
        self.add_slider(fig)

        fig.show()

        #return fig

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

        loop_data=[[0,1],[2,3,4,5,6,7,8]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
            [self.start,self.last],    #N/A CEILING
            [self.start,self.last],    #STRONG SELL
            [self.start,self.last],    #SELL
            [self.start,self.last],    #NORMAL
            [self.start,self.last],    #BUY
            [self.start,self.last],    #BUY
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceUSD'].rolling(365).mean(),
            df['Puell_Multiple'],
            [10,10],
            [5,5],
            [2.5,2.5],
            [0.6,0.6],            
            [0.4,0.4],
            [0.4,0.4],
        ]
        name_data = [
            'DCR Price (USD)',
            '365-day MA',
            'Puell Multiple',
            'N/A',
            'STRONG SELL (2.8)',
            'SELL (2.0)',
            'N/A',
            'BUY (0.6)',
            'STRONG BUY (0.4)',
        ]
        width_data      = [2,2,1,1,1,1,1,1,1]
        opacity_data    = [1,1,1,1,1,1,1,1,1]
        dash_data = ['solid','solid','solid','dash','dash','dash','dash','dash','dash']
        color_data = [
            'rgb(255, 255, 255)',         #White
            'rgb(237, 109, 71)',          #Decred Orange
            'rgb(46, 214, 161)',          #Turquoise
            'rgba(255, 80, 80, 0.2)',     #Gradient Red
            'rgba(255, 80, 80, 0.2)',     #Gradient Red
            'rgba(255, 80, 80, 0.1)',     #Gradient Red
            'rgba(55 ,55, 55, 0)',        #NA
            'rgba(36, 255, 136, 0.1)',    #Gradient Green
            'rgba(36, 255, 136, 0.2)',    #Gradient Green
        ]
        #Invert Colors for Light Theme
        color_data = self.color_invert(color_data)
        fill_data = [
            'none','none','none',
            'none','tonexty','tonexty','none','tonexty','tozeroy',
        ]
        legend_data = [True,True,True,False,True,True,False,True,True]
        title_data = [
            '<b>Decred Puell Multiple</b>',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>Puell Multiple</b>']
        range_data = [[self.start,self.last],[-1,3],[-1,5]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = self.chart.subplot_lines_doubleaxis_2nd_area(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data,
            fill_data
            )
        fig.update_xaxes(dtick='M6',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False)
        self.add_slider(fig)

        fig.show()

    def security_curve(self):
        """
        #############################################################################
                            DECRED SECURITY CURVE
        #############################################################################
        """

        df = dcr_security_calculate_df().dcr_security_curve()
        df[50:100]

        loop_data = [[0],[1]]
        x_data = [df['y'],df['y']]
        y_data = [df['x_y'],df['days_buy_y']]
        name_data = [
            '<b>Decred Security Curve</b>',
            '<b>Days to Buy Tickets in Full Blocks</b>']
        title_data = [
            '<b>DCR Security Curve</b>',
            '<b>Attacker Share of Ticket Pool</b>',
            '<b>Required Multiple of Honest Hashpower</b>',
            '<b>Days to Buy Tickets in Full Blocks</b>'
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


fig_dcr_mine = dcr_mining_chart_suite('dark')

#fig_dcr_mine.difficulty_ribbon()

#fig_dcr_mine.puell_multiple()

fig_dcr_mine.security_curve()


