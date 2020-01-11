from checkonchain.general.__init__ import *
import os



class general_helpers():
    def __init__():
        os.chdir('D:\code_development\checkonchain\checkonchain')

    def df_to_csv(df,filename):
        """Inputs
        df      = dataframe to write to csv
        path    = filepath of output csv
        """
        path = 'misc\data_exports'
        path = path + '\_' + filename + '.csv'
        df.to_csv(path)
