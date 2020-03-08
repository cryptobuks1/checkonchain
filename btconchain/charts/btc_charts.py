#Calculate the dust limit and estimate future value
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.general.standard_charts import *
from checkonchain.general.regression_analysis import *
import datetime

class btc_chart_suite():

    def __init__(self):
        self.today = date.datetime.now().strftime('%Y-%m-%d')
        self.last = pd.to_datetime(df["date"].iloc[-1]) + pd.to_timedelta(90,unit='D')

    def mvrv(self):
        """"Prints Bitcoin Realised Price and MVRV"""
        df = btc_add_metrics().btc_coin()

        loop_data=[[0,1],[2,]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
        ]
        y_data = [
            df['PriceUSD'],
            df['PriceRealUSD'],
            df['CapMVRVCur'],
        ]
        name_data = [
            'BTC Price (USD)',
            'Realised Price (USD)',
            'MVRV Ratio',
        ]
        width_data      = [2,2,1]
        opacity_data    = [1,1,1]
        dash_data = ['solid','solid','solid']
        color_data = [
            'rgb(239, 125, 50)',    #Price Orange
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(255, 255, 255)',   #White
            #'rgb(255, 80, 80)',   #Gradient Red
            #'rgb(255, 80, 80)',   #Gradient Red
        ]
        legend_data = [True,True,True]
        title_data = [
            'Bitcoin MVRV Ratio',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>MVRV Ratio</b>']
        range_data = [['2010-01-01',self.last],[-1,5],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%b-%y')
        fig.show()

    def magic_lines_full(self):
        """"Prints Bitcoin Full History Magic Lines 200D, 128D, 200W and 128W (log)"""

        df = btc_add_metrics().btc_coin()
        
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
        range_data = [['2010-01-01',self.last],[-1,5],[-1,2]]
        autorange_data = [False,False,False]
        type_data = ['date','log','log']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data
            )
        fig.update_xaxes(dtick='M12',tickformat='%b-%y')
        fig.show()

    def magic_lines(self):
        """"Prints Bitcoin Full History Magic Lines 200D, 128D, 200W and 128W (log)"""

        df = btc_add_metrics().btc_coin()
        
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
        fig.update_xaxes(dtick='M12',tickformat='%b-%y')
        fig.update_yaxes(dtick=1000)
        fig.show()

    def mayer_multiple(self):
                """"Mayer Multiple"""
                df = btc_add_metrics().btc_coin()
                
                df['Mayer_Multiple'] = (
                    df['PriceUSD']
                    / df['PriceUSD'].rolling(200).mean()
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
                    df['Mayer_Multiple'],
                    [0.6,0.6],
                    [0.8,0.8],
                    [2.4,2.4],
                    [3.4,3.4],
                ]
                name_data = [
                    'BTC Market Cap (USD)',
                    'Mayer Multiple',
                    'STRONG BUY',
                    'BUY',
                    'SELL',
                    'STRONG SELL'
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
                    'Bitcoin Mayer Multiple',
                    '<b>Date</b>',
                    '<b>Price (USD)</b>',
                    '<b>Mayer Multiple</b>']
                range_data = [['2010-01-01',self.last],[-1,5],[-1,2]]
                autorange_data = [False,False,False]
                type_data = ['date','log','log']
                fig = check_standard_charts().subplot_lines_doubleaxis(
                    title_data, range_data ,autorange_data ,type_data,
                    loop_data,x_data,y_data,name_data,color_data,
                    dash_data,width_data,opacity_data,legend_data
                    )
                fig.update_xaxes(dtick='M12',tickformat='%b-%y')
                fig.show()

    def puell_multiple(self):
            """"Puell Multiple"""
            df = btc_add_metrics().btc_coin()
            
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
                'STRONG BUY',
                'BUY',
                'SELL',
                'STRONG SELL'
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
            range_data = [['2010-01-01',self.last],[-1,5],[-1,2]]
            autorange_data = [False,False,False]
            type_data = ['date','log','log']
            fig = check_standard_charts().subplot_lines_doubleaxis(
                title_data, range_data ,autorange_data ,type_data,
                loop_data,x_data,y_data,name_data,color_data,
                dash_data,width_data,opacity_data,legend_data
                )
            fig.update_xaxes(dtick='M12',tickformat='%b-%y')
            fig.show()




btc_chart_suite().mvrv()
btc_chart_suite().magic_lines_full()
btc_chart_suite().magic_lines()
btc_chart_suite().mayer_multiple()
btc_chart_suite().puell_multiple()


