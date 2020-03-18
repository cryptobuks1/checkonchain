from checkonchain.general.__init__ import *
import os


class general_helpers():
    
    def __init__():
        pass

    def df_to_csv(df,filename):
        os.chdir('D:\code_development\checkonchain\checkonchain')
        """Inputs
        df      = dataframe to write to csv
        path    = filepath of output csv
        """
        path = 'misc\data_exports'
        path = path + '\_' + filename + '.csv'
        print("EXPORTING " + filename + '.csv')
        print(path)
        df.to_csv(path)

    def early_price_metric(df,targetUSD,targetNtv):
        """
        When prices are added manually, this tool mutliplies
        some native coin value by price to create USD equivalent
        INPUTS:
            df = target dataframe
            targetUSD = str column name of target USD metric
            targetNtv = str column name of target Ntv value
        OUTPUTS:
            Returns df with targetUSD = PriceUSD * targetNtv
        """
        df[targetUSD] = df.apply(
            lambda row: row['PriceUSD']*row[targetNtv] if np.isnan(row[targetUSD]) else row[targetUSD],
            axis=1
        )
        return df
