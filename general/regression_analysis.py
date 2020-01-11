#Modules for Linear Regression Analysis
from checkonchain.general.__init__ import *
from sklearn.linear_model import LinearRegression


class regression_analysis():
    """
    Modules for calculating the linear regression between two parameters
    Modules available:
        regression_constants() = Contains constants from saved analysis
        ln_regression() = Linear Regression Analysis - Automatically calcs ln(x) and ln(y)
        rsq_progression() = Calculates progression of R-squared coefficient quality over a dataset
        
    """

    def __init__(self):
        pass

    def regression_constants(self):
        """regression_constants() = contains constants from saved analysis
            Module --> .regression_constants()['model']
                'planb'     = BTC, Market Cap vs S2F, after Plan B 2018
                'btc_s2f'   = BTC, Market Cap vs S2F, after Checkmate 2019
                'btc_diff'  = BTC, Difficulty vs S2F, after Checkmate (unpublished)
                'dcr_s2f'   = DCR, Market Cap vs S2F, after Checkmate 2019
                'dcr_diff'  = DCR, Difficulty vs S2F, after Checkmate (unpublished)
                'ltc_s2f'   = LTC, Market Cap vs S2F, after Checkmate 2019
                'ltc_diff'  = LTC, Difficulty vs S2F, after Checkmate (unpublished)
        """
        planb = pd.DataFrame(data={
            'Details':['BTC_PlanBModel'],
            'rsq':[0.947328],
            'intercept':[-1.84],
            'coefficient':[3.36]
            })
        btc_s2f = pd.DataFrame(data={
            'Details':['BTC_S2F_MrktCap_20191013'],
            'rsq':[0.8992],
            'intercept':[13.1286],
            'coefficient':[3.9880]
            })
        btc_diff = pd.DataFrame(data={
            'Details':['BTC_DiffMean_MrktCap_20191013'],
            'rsq':[0.934309],
            'intercept':[10.697469],
            'coefficient':[0.498638]
            })

        dcr_s2f = pd.DataFrame(data={
            'Details':['DCR_S2F_MrktCap_20191014'],
            'rsq':[0.7050],
            'intercept':[15.7692],
            'coefficient':[2.5750]
            })
        dcr_diff = pd.DataFrame(data={
            'Details':['DCR_DiffMean_MrktCap_20191013'],
            'rsq':[0.50967],
            'intercept':[12.310519],
            'coefficient':[0.322534]
            })

        ltc_s2f = pd.DataFrame(data={
            'Details':['LTC_S2F_MrktCap_20191013'],
            'rsq':[0.4622],
            'intercept':[16.9544],
            'coefficient':[1.6934]
            })
        ltc_diff = pd.DataFrame(data={
            'Details':['LTC_DiffMean_MrktCap_20191013'],
            'rsq':[0.745483],
            'intercept':[14.193707],
            'coefficient':[0.494897]
            })
        return {
            'planb':planb,
            'btc_s2f':btc_s2f,
            'btc_diff':btc_diff,
            'dcr_s2f':dcr_s2f,
            'dcr_diff':dcr_diff,
            'ltc_s2f':ltc_s2f,
            'ltc_diff':ltc_diff,            
            }
    
    def ln_regression(self,dataframe,x_metric,y_metric,time_metric):
        """Linear Regression Analysis - Automatically calcs ln(x) and ln(y)
        INPUTS:
            Dataframe       = Pandas dataframe containing relevant datasets
            x_metric        = String - column heading of x_metric
            y_metric        = String - column heading of y_metric
            time_metric     = String - column heading of time metric (not part of in calc)
        OUTPUT:
            'model'         = Regression model
            'model_params   = Dataframe containing RSQ, Intercept and Coefficient Params
        """
        self.dataframe = dataframe
        self.x_metric = x_metric
        self.y_metric = y_metric
        self.time_metric = time_metric #arbitrary for charting
        print('...Calculating ln-ln Linear Regression for '+self.x_metric+'-'+self.y_metric+'...')

        #Subset of dataset, drop na values
        df = self.dataframe[[
            self.time_metric,
            self.x_metric,
            self.y_metric
        ]].dropna(axis=0)
        df = df.reset_index(drop=True)

        #Create arrays for x and y in regression
        x=np.array(np.log(df[self.x_metric])).reshape((-1,1))
        y=np.array(np.log(df[self.y_metric]))
        regression_model = LinearRegression().fit(x, y)
        
        #Calculate r_sq, intercept and coefficient of model
        model_params = pd.DataFrame(
            index=['regression_model'],
            data={
                'rsq':[regression_model.score(x,y)], 
                'intercept': [regression_model.intercept_],
                'coefficient':[float(regression_model.coef_)]
                })
        print(model_params)
        return {
            'model': regression_model, 
            'model_params':model_params
            }
        
    def rsq_progression(self,dataframe,x_metric,y_metric,time_metric):
        """
        Calculates progression of R-squared coefficient quality over a dataset
        INPUTS:
            Dataframe       = Pandas dataframe containing relevant datasets
            x_metric        = String - column heading of x_metric
            y_metric        = String - column heading of y_metric
            time_metric     = String - column heading of time metric (not part of in calc)
        OUTPUTS:
            'rsq_develop'   = DataFrame with 'rsq_x_metric' column represents RSQ
        """
        self.dataframe = dataframe
        self.x_metric = x_metric
        self.y_metric = y_metric
        self.time_metric = time_metric #arbitrary for charting
        print('...Calculating R-Square Progression for '+self.x_metric+'-'+self.y_metric+'...')
        #Calculate progression of rsq over time
        df = self.dataframe[[self.time_metric,self.x_metric,self.y_metric]].dropna(axis=0)
        df = df.reset_index(drop=True)
        df['rsq_'+self.x_metric]=0

        for i in range(0,len(df.index)):
            #Calculate S2F RSQ development
            df.loc[i,['rsq_'+self.x_metric]]=LinearRegression().fit(
                np.log(df.loc[:i,[self.x_metric]]),
                np.log(df.loc[:i,[self.y_metric]])
                ).score(
                    np.log(df.loc[:i,[self.x_metric]]),
                    np.log(df.loc[:i,[self.y_metric]])
                    )
        print('RSQ Complete')
        return {
            'rsq_develop':df
            }


#from checkonchain.general.coinmetrics_api import *
#BTC_coin = Coinmetrics_api('btc',"2009-01-03",today).convert_to_pd()
#BTC_regr = regression_analysis().ln_regression(BTC_coin,'DiffMean','CapMrktCurUSD','date')
#BTC_rsq = regression_analysis().rsq_progression(BTC_coin,'DiffMean','CapMrktCurUSD','date')
#BTC_rsq
#
#DCR_coin = Coinmetrics_api('dcr',"2016-02-08",today).convert_to_pd()
#DCR_regr = regression_analysis().ln_regression(DCR_coin,'DiffMean','CapMrktCurUSD','date')
#DCR_rsq = regression_analysis().rsq_progression(DCR_coin,'DiffMean','CapMrktCurUSD','date')
#DCR_rsq
#
#LTC_coin = Coinmetrics_api('ltc',"2011-10-07",today).convert_to_pd()
#LTC_regr = regression_analysis().ln_regression(LTC_coin,'S2F','CapMrktCurUSD','date')
#LTC_rsq = regression_analysis().rsq_progression(LTC_coin,'DiffMean','CapMrktCurUSD','date')
#LTC_rsq

