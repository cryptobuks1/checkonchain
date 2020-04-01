#Modules for Linear Regression Analysis
from checkonchain.general.__init__ import *
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

from checkonchain.dcronchain.dcr_add_metrics import *

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
    
    def ln_regression(self,df,x_metric,y_metric,time_metric):
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
        print('...Calculating ln-ln Linear Regression for '+x_metric+'-'+y_metric+'...')

        #Subset of dataset, drop na values
        df = df[[
            time_metric,
            x_metric,
            y_metric
        ]].dropna(axis=0)
        df = df.reset_index(drop=True)

        #Create arrays for x and y in regression
        x=np.array(np.log(df[x_metric])).reshape((-1,1))
        y=np.array(np.log(df[y_metric]))
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
        
    def rsq_progression(self,df,x_metric,y_metric,time_metric):
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
        print('...Calculating R-Square Progression for '+x_metric+'-'+y_metric+'...')
        #Calculate progression of rsq over time
        df = df[[time_metric,x_metric,y_metric]].dropna(axis=0)
        df = df.reset_index(drop=True)
        df['rsq_'+x_metric]=0

        for i in range(0,len(df.index)):
            #Calculate S2F RSQ development
            df.loc[i,['rsq_'+x_metric]]=LinearRegression().fit(
                np.log(df.loc[:i,[x_metric]]),
                np.log(df.loc[:i,[y_metric]])
                ).score(
                    np.log(df.loc[:i,[x_metric]]),
                    np.log(df.loc[:i,[y_metric]])
                    )
        print('RSQ Complete')
        return {
            'rsq_develop':df
            }


    def ln_regression_OLS(self,df,x_metric,y_metric,const):
        """Linear Regression Analysis OLS statsmodels - Automatically calcs ln(x) and ln(y)
        Takes in dataframe columns, 
            applies natural log, 
            performs regression analysis, 
            returns result in linear space (exp(result))
        INPUTS:
            Dataframe       = Pandas dataframe containing relevant datasets
            x_metric        = String - column heading of x_metric
            y_metric        = String - column heading of y_metric
            const           = Boolean, add intercept or not
        OUTPUT:
            dataframe with the following additional columns:
            'xy_predict'  - Predicted model based on x_metric (in linear space)
            'xy_multiple' - Predicted model based on x_metric
            'xy_residual' - Predicted model Residuals (y_metric - xy_predict) / std_error
        """
        print('...Calculating OLS ln-ln Linear Regression for '+x_metric+'-'+y_metric+'...')
        #set x and y params for regression
        x = df[x_metric].apply(np.log)
        if const == True:
            x = sm.add_constant(x)
        y = df[y_metric].apply(np.log)
        #Calculate regression model and print results
        model = sm.OLS(y, x).fit()
        predictions = model.predict(x).apply(np.exp)
        print(model.summary())
        #Create string names for model outputs
        xy_predict      = x_metric[:3] + '_' + y_metric[:5] + '_predict'
        xy_multiple     = x_metric[:3] + '_' + y_metric[:5] + '_multiple'
        xy_residual     = x_metric[:3] + '_' + y_metric[:5] + '_residual'

        df[xy_predict]      = model.predict(x).apply(np.exp)
        df[xy_multiple]     = df[y_metric] / df[xy_predict]
        df[xy_residual]     = (y - df[xy_predict].apply(np.log)) / np.exp(float(model.bse[x_metric]))
        print('...Returning df with added cols: ' + xy_predict + ' ' + xy_multiple + ' ' + xy_residual)
        return {'df':df,'model':model}


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

#df = dcr_add_metrics().dcr_coin()
#x_metric = 'S2F'
#y_metric = 'PriceUSD'
#const = True
#
#print('...Calculating OLS ln-ln Linear Regression for '+x_metric+'-'+y_metric+'...')
##set x and y params for regression
#x = df[x_metric].apply(np.log)
#if const == True:
#    x = sm.add_constant(x)
#y = df[y_metric].apply(np.log)
##Calculate regression model and print results
#model = sm.OLS(y, x).fit()
#predictions = model.predict(x).apply(np.exp)
#print(model.summary())
##Create string names for model outputs
#xy_predict      = x_metric[:3] + '_' + y_metric[:5] + '_predict'
#xy_multiple     = x_metric[:3] + '_' + y_metric[:5] + '_multiple'
#xy_residual     = x_metric[:3] + '_' + y_metric[:5] + '_residual'
#
#df[xy_predict]      = model.predict(x).apply(np.exp)
#df[xy_multiple]     = df[y_metric] / df[xy_predict]
#df[xy_residual]     = (y - df[xy_predict].apply(np.log)) / np.exp(float(model.bse[x_metric]))
#print('...Returning df with added cols: ' + xy_predict + ' ' + xy_multiple + ' ' + xy_residual)
#
#name = xy_predict + '_2'
#df[name] = np.exp(x[x_metric]*model.params[x_metric] + x['const']*model.params['const'])
#
#df[[xy_predict,name]]
#
#model.params