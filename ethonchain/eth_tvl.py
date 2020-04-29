import pandas as pd
from checkonchain.general.standard_charts import *


class ethonchain():

    def __init__(self):
        pass

    def tvl(self):
        df = pd.read_csv(r"ethonchain\data\dh_tvl_20200420.csv")
        df['date'] = pd.to_datetime(df['date'],utc=True)

        loop_data=[[0],[1,2]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
        ]
        y_data = [
            df['PriceUSD'],
            df['TVL_eth '],
            df['TVL_usd '],
        ]
        name_data = [
            'ETH Price (USD)',
            'TVL ETH (USD)',
            'TVL (USD)',
        ]

        width_data      = [2,2,2,]
        opacity_data    = [1,1,1,]
        dash_data = ['solid','solid','solid']
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(239, 125, 50)',    #Price Orange
        ]
        legend_data = [True,True,True]
        title_data = [
            'Ethereum TVL in DeFi',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>TVL (USD)</b>'
        ]

        range_data = [['2018-01-01','2020-06-01'],[0,1500],[0,0]]

        autorange_data = [False,False,False]
        type_data = ['date','linear','linear']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data,
            )
        fig = check_standard_charts().add_annotation(fig,"@checkmatey<br />@TrustlessState")
        fig.update_xaxes(dtick='M3',tickformat='%d-%b-%y')
        fig.update_yaxes(showgrid=True,secondary_y=False,dtick=100)
        fig.update_yaxes(showgrid=False,secondary_y=True,dtick=1e8)

    def lindy(self):
        df = pd.read_csv(r"ethonchain\data\dh_tvl_20200420.csv")
        df['date'] = pd.to_datetime(df['date'],utc=True)

        loop_data=[[0],[1,2]]
        x_data = [
            df['date'],
            df['date'],
            df['date'],
        ]
        y_data = [
            df['PriceUSD'],
            df['TCVL_eth'],
            df['TCVL_usd'],
        ]
        name_data = [
            'ETH Price (USD)',
            'Cumulative TVL ETH (USD)',
            'Cumulative TVL (USD)',
        ]
        width_data      = [2,2,2,]
        opacity_data    = [1,1,1,]
        dash_data = ['solid','solid','solid']
        color_data = [
            'rgb(255, 255, 255)',    #White
            'rgb(20, 169, 233)',    #Total Blue
            'rgb(239, 125, 50)',    #Price Orange
        ]
        legend_data = [True,True,True]
        title_data = [
            'Ethereum TVL in DeFi',
            '<b>Date</b>',
            '<b>Price (USD)</b>',
            '<b>TVL (USD)</b>'
        ]
        range_data = [['2018-01-01','2020-06-01'],[0,1500],[0,0]]
        autorange_data = [True,True,True]
        type_data = ['date','linear','linear']
        fig = check_standard_charts().subplot_lines_doubleaxis(
            title_data, range_data ,autorange_data ,type_data,
            loop_data,x_data,y_data,name_data,color_data,
            dash_data,width_data,opacity_data,legend_data,
            )
        fig = check_standard_charts().add_annotation(fig,"@checkmatey<br />@TrustlessState")
        fig.update_xaxes(dtick='M3',tickformat='%d-%b-%y')
        #fig.update_yaxes(showgrid=True,secondary_y=False,dtick=100)
        #ig.update_yaxes(showgrid=False,secondary_y=True,dtick=1e8)
        fig.show()

ethonchain().lindy()



df = pd.read_csv(r"ethonchain\data\dh_tvl_20200420.csv")
df.columns