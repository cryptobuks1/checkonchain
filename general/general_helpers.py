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
