#Parametric model for the cost to attack a PoW and Hybrid PoW/PoS blockchain
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import*
from checkonchain.btconchain.btc_add_metrics import *


class dcr_security_model():

    def __init__(self,asset,atk_blk,atk_type,y,H_net,blk,price,Z,p_t):
        """
        Decred security model calculation for specific data point
        INPUTS:
            asset   = str, 'btc' for pure PoW or 'dcr' for Hybrid PoW/PoS
            atk_blk = int, depth of block reorg/double spend
            atk_type= str, 'attack type = 'internal' or 'external'
            y       = float, Portion of the ticket pool owned by an attacker (0 to 1)
            H_net   = float, Hashrate measured in TH/s
            price   = float, Price of coin in USD
            Z       = int, Tickets in pool (target is 40960)
            p_t     = float, Ticket price (DCR)
        """
        # Input Params
        self.asset = asset # 'btc' or 'dcr' supported
        self.atk_blk = atk_blk # depth of blocks to attack | double spend
        self.atk_type = atk_type #attack type = 'internal' or 'external'
        self.y = y # portion of stake owned by attacker
        self.H_net = H_net # network total hashrate (TH/s)
        self.blk = blk # blk height
        self.price = price # DCR/Fiat Exchange Rate
        self.Z = Z # Ticket pool size (~40960)
        self.p_t = p_t # Ticket price (DCR)
        #self.fee = fee # total Fees paid in native unit

        #Ticket Constants for Decred
        self.N = 5 # Tickets called per block
        self.k = 3 # Tickets required to vote yes
        self.p = 1 # stake pool online rate (0-1) (relate to missed)

        """Set Constants for specific model"""
        if asset ==str('btc'):
            self.y = 1e-15 # Hard reset of tic pool to near zero
            self.t_b = 10*60 # blk time (s)
            #PoW rentability constants
            self.a = (217.2838 + 129.5275)/1000 # total rentable hsh (TH/s)
            # https://www.nicehash.com/my/marketplace/SHA256
            self.r_e = 143.25/1000 # rental price (fiat / TH/s)
            #PoW ASIC capital constants
            #ASSUMES ANTMINER S19 Pro (May 2020)
            self.h_d = 110 # ASIC hashrate (TH/s)
            self.w_d = 3.25 # ASIC power draw (kW)
            self.p_d = 3140 # ASIC capital (fiat/ASIC Device)

        elif asset ==str('dcr'):
            self.t_b = 5*60 # blk time (s)
            #PoW rentability constants
            self.a = (0.0077 + 0.0044)/1000 # total rentable hashrate (TH/s)
            self.r_e = 0.73/1000 # rental price (fiat / TH/s)
            #https://www.nicehash.com/my/marketplace/DECRED
            #PoW ASIC capital constants
            #if blk < 114424: #genesis to 10/Mar/2017 =  NVIDIA GeForce GTX 1070
            #    self.h_d = 0.00283 # GPU hashpower (TH/s)
            #    self.w_d = 0.15 # GPU power draw (kW)
            #    self.p_d = 379 # GPU capital (fiat/GPU Device)
            #else:
            #ASSUMES StrongU STU-U1++ or MicroBT Whatsminer D1 (May 2020)
            self.h_d = 52 # ASIC hashpower (TH/s)
            self.w_d = 2.2 # ASIC power draw (kW)
            self.p_d = 1130 # ASIC capital (fiat/ASIC Device)
            
        # Duration of attack based on blocks to be wound back - compare finality
        self.t_a = self.atk_blk * self.t_b # time of attack (time in s)

        #PoW power constants
        self.adj_d = 0.05 # adjustment factor for other PoW overheads (multiple on Device cost)
        self.c = 0.05 # cost per power ($/KWh)
        self.rho = (self.p_d / self.h_d) # (ASIC ($/unit)/(TH/s)) = ASIC relative cost
        self.nu = self.h_d/self.w_d # (ASIC (TH/s)/kWh) = ASIC power efficiency

    def R(self): # calc total block reward for btc and dcr
        if self.asset == str('btc'):
            R_tot = 50*0.5**(math.floor(self.blk/210000))
            R_pow = R_tot
            R_pos = 0
            R_fnd = 0
        elif self.asset =='dcr':
            R_tot = 31.19582664*(100/101)**(math.floor(self.blk/6144))
            R_pow = 0.6 * R_tot
            R_pos = 0.3 * R_tot
            R_fnd = 0.1 * R_tot
        else:
            R_tot = 0
            R_pow = 0
            R_pos = 0
            R_fnd = 0
        return R_tot,R_pow,R_pos,R_fnd


    def p_y(self): 
        #Probability attacker holds required tickets to make valid block
        i = 0
        _total = 0
        while i < self.k:
            _bincoef = (
                math.factorial(self.N)
                / (math.factorial(self.N-i) 
                * math.factorial(i))
            )
            _calc = _bincoef * self.y**(self.N-i)*((1-self.y)*self.p)**i
            _total = _total + _calc
            i += 1
        return _total

    def sig_y(self): 
        #Probability honest party required tickets to make valid block (1-p_y)
        return 1 - self.p_y()

    def x_y(self): # attacker factor of hashpower required (assuming attacker hash is not already active)
        return 1/self.p_y() - 1

    """Proof-of-Work Term"""
    def pow_prof(self): # Daily pow profitability factor
        # beta = Daily USD income
        # 86400 * R_pow / blk time (s*units/blk time in s = daily units)
        beta = 86400*self.R()[1] / self.t_b 
        #PoW profitability a_w
        # a_w = beta / (network hashrate H_net) - cost of ASIC and Power 
        # --> Aggregate Income - Costs
        a_w = ((beta * self.price)/(self.H_net) - (0.024*self.c/self.nu))/self.rho
        return a_w
        #Note - pow_prof calcs based on H_net --> H_a calc. Thus a_w links H_net and H_a


    def N_d(self): #Number of Devices on Network
        # H_net / h_d
        N_d = self.H_net / self.h_d
        return N_d


    def H_a(self): # attackers proportion of total hashrate
        # relating H_a to miner profitability --> 0 in the long term
        # Attackers hashrate = Prob Honest Tickest * Daily PoW USD Reward / (blk_time(ASIC + power costs))
        H_a = (self.sig_y() 
        * (86400*self.R()[1]*self.price) 
        / (self.t_b*(self.pow_prof()*self.rho + 0.024*self.c/self.nu))
        )
        return H_a

    def pow_term_rent(self):
        # Rental Costs
        R = self.a * self.r_e * self.t_a # TH/s * price/TH * time
        return R

    def pow_term_asic(self):
        # ASIC Capital
        # (attack hash - rent hash) * (ASIC relative cost) * Overhead adjustment factor
        D = (self.H_a() - self.a) * self.rho * self.adj_d 
        return D

    def pow_term_power(self):        
        # Power Costs
        P = (self.H_a()- self.a)/self.nu * self.c * self.t_a
        return P

    def pow_term(self): 
        #Calculate aggregate PoW cost
        W = self.pow_term_rent() + self.pow_term_asic() + self.pow_term_power()
        return W #Return Total Proof-of-Work Cost

   
    """Proof-of-Stake Term"""
    def pos_prof(self): # annual stake yield %
        # 
        return ((self.p_t+(self.R()[2]/self.N))/self.p_t)**(365.25/28)-1
    
    def pos_term(self):
        # Stake share * tic pool * tic diff (units) * price ($/unit)
        S_a = (self.y * self.Z * self.R()[2] * self.price) / (self.N*((self.pos_prof()+1)**(28/365.25)-1))
        return S_a
    
    """Total Cost to Attack"""
    def pca(self): # Total attack cost
        return self.pow_term() + self.pos_term()





class dcr_security_analyse():
    """Calculates a dataframe from dcr_security model using user defined inputs (e.g real performance)
    Modules:
        dcr_security_curve      = returns DataFrame with key points to plot Decred Security Curve
        calculate_df            = returns dataframe with complete security model calculations
    """
    def __init__(self):
        pass

    def dcr_security_curve(self,chart):
        """
        Calculates the Decred security curve (hashrate multiplier) for incremental stake capture
        INPUT:
            chart   0 = do not print chart
                    1 = print chart
        OUTPUT:
            df  = DataFrame, containsthe following columns
                y   = Percentage of PoS ticket pool held by attacker
                p_y = probability attacker 
        """
        df = pd.DataFrame(columns=['y','p_y','sig_y','x_y','days_buy_y'])
        for i in range(1,101,1):
            y = i/100
            #Attacker share of Ticket Pool
            df.loc[i,['y']] = y
            #Probability Attacker validates block p_y
            j = p_y = _calc = _bincoef = 0
            while j < 3:
                _bincoef = (
                    math.factorial(5)
                    / (math.factorial(5-j) 
                    * math.factorial(j))
                )
                _calc = _bincoef * y**(5-j) * ((1-y)*1)**j
                p_y = p_y + _calc
                j += 1
            df.loc[i,['p_y']]   = p_y
            #Probability Honest Ticket validates block sig_y
            df.loc[i,['sig_y']] = 1 - p_y
            #Proportion of Hashpower needed by Attacker
            df.loc[i,['x_y']]   = 1 / p_y - 1
            df.loc[i,['days_buy_y']] = y * 40960 / 20 * 5 / 60 / 24

        #if chart flag = 1, print Decred Security Curve Chart
        if chart ==1:
            """
            #############################################################################
                                PLOT DECRED SECURITY CURVE
            #############################################################################
            """
            loop_data = [[0],[2]]
            x_data = [df['y'],[0,1],df['y']]
            y_data = [df['x_y'],[1,1],df['days_buy_y']]
            name_data = [
                '<b>Decred Security Curve</b>',
                '<b>Bitcoin Security Curve</b>',
                '<b>Days to Buy Tickets in Full Blocks</b>']
            title_data = [
                '<b>Decred Security Curve</b>',
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

        return df

    def calculate_df(self,asset,atk_blk,atk_type):
        """
        Calculates the Decred security performance and parameters based on a set of REAL inputs
            INPUTS:
                asset           = str, 'btc' for pure PoW or 'dcr' for Hybrid PoW/PoS
                atk_blk         = int, depth of block reorg/double spend
                atk_type        = str, 'attack type = 'internal' or 'external'
            Auto Calculated: 
                df              = DataFrame structured with the following columns
                df['blk']       = Block Height (time variable)
                df['H_net']     = Hashrate measured in TH/s
                df['price']     = Price of coin in USD
                df['tic_pool']  = Tickets in pool (target is 40960)
                df['tic_price'] = Ticket Price in DCR
                df['y']         = Portion of the ticket pool owned by an attacker (0 to 1)
            OUTPUTS: df = Dataframe with appended columns
                df['sig_y']     = Probability honest party required tickets to make valid block (1-p_y)
                df['p_y']       = Probability attacker holds required tickets to make valid block
                df['x_y']       = Attacker factor of hashpower required (assuming attacker hash is not already active)
                df['H_a']       = Attackers proportion of total hashrate
                df['pow_rent'] = PoW Cost to Attack (Rental Component, %age)
                df['pow_asic'] = PoW Cost to Attack (ASIC Capital Component, %age)
                df['pow_power'] = PoW Cost to Attack (Power Component, %age)
                df['pow_term']  = PoW Cost to Attack Total (USD)
                df['pos_term']  = PoS Cost to Attack Total (USD)
                df['pow_term']  = PoW Cost to Attack Total (USD)
                df['pca']       = Total Cost to Attack (USD)
                df['pow_ratio'] = Ratio of PoW contribution to PCA pow/term / pca
                df['pow_prof']  = Miner profitability
                df['pos_prof']  = Staker profitability
        """
        #Pull Real Data from Coinmetrics / dcrdata
        if asset == 'btc':
            df  = btc_add_metrics().btc_subsidy_models()
            df         = df[['blk','HashRate','PriceUSD']]
            df.columns = ['blk','H_net','price'] #rename for security model
            #BTC PARAMS NOT CHECKED!!!
            df['tic_pool']  = 1
            df['tic_price'] = 1
            y_list = 100
        else:
            df  = dcr_add_metrics().dcr_subsidy_models()
            #restructure and rename to plug into security model
            df         = df[['blk','pow_work_TH','PriceUSD','tic_pool_avg','tic_price_avg']]
            df.columns = ['blk','H_net','price','tic_pool','tic_price'] #rename for security model
            #Add PoS ticket pool held by attacker y = 0 to 1
            y_list = np.array([1,2,3,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75])
            y_list = y_list/100
        #add attackers PoS ticket share
        _df = df
        for i in y_list:
            _df['y'] = i
            df = df.append(_df)
        df = df.reset_index()
        df = df.dropna(axis=0)

        print('sig_y')
        df['sig_y'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).sig_y(),axis=1)
        print('p_y') 
        df['p_y'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).p_y(),axis=1) 
        print('x_y')
        df['x_y'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).x_y(),axis=1) 
        print('Ha')
        df['H_a'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).H_a(),axis=1) 
        print('pow_rent')
        df['pow_rent'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pow_term_rent(),axis=1)
        print('pow_asic')
        df['pow_asic'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pow_term_asic(),axis=1)
        print('pow_power')
        df['pow_power'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pow_term_power(),axis=1)
        print('pow_term')
        df['pow_term'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pow_term(),axis=1) / 1e6
        print('pos_term')
        df['pos_term'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pos_term(),axis=1) / 1e6
        print('pca')
        df['pca'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pca(),axis=1) / 1e6
        df['pow_ratio'] = df['pow_term'] / df['pca']
        df['pow_prof'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pow_prof(),axis=1)
        df['pos_prof'] = df.apply(
            lambda row : dcr_security_model(
                asset,atk_blk,atk_type,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pos_prof(),axis=1)
        return df

    class charts_unforgeable_costliness():

        def __init__(self,theme):
            self.BTC = btc_add_metrics().btc_subsidy_models()
            self.DCR = dcr_add_metrics().dcr_subsidy_models()
            self.theme = theme

        def unforgeable_cost_cum(self):

            """
            #############################################################################
            UNFORGEABLE COSTLINESS - CUMULATIVE       
            Assumptions - No honest security provider is willing to expend more than the available block reward
                        - Considers PoS security influence over PoW hash-power multiple
            #############################################################################
            """
            BTC = self.BTC
            DCR = self.DCR

            #Calculate Unforgeable Costliness (Cumulative Sum)
            BTC['Unforg_Cost']  = BTC['PoW_income_usd'].cumsum() + BTC['FeeTotUSD'].cumsum()
            DCR['PoW_Cost']     = DCR['PoW_income_usd'].cumsum() + DCR['FeeTotUSD'].cumsum()
            DCR['PoS_Cost']     = DCR['PoS_income_usd'].cumsum()

            #Calculate Decred security curve
            _df = dcr_security_analyse().dcr_security_curve(0)
            #Calculate Range of Decred Security Conditions
            for y in [5,10,15,30,50,75]:                                            #Assume range of Attacker ticket stake ownership
                y   = y/100                                                     #Probability attacker tickets make block
                p_y = float(_df[_df['y']==y]['p_y'])                            #Probability attacker holds required tickets to make valid block
                x_y = float(_df[_df['y']==y]['x_y'])                            #hash-power multiple
                col_name = 'Unforg_Cost_'+str(int(y*100))+'%'                   #Set column name e.g 'Unforg_Cost_5%'
                DCR[col_name] = (p_y * DCR['PoS_Cost'] + x_y * DCR['PoW_Cost']) #Cumulative Unforgeable Cost

            #build chart
            loop_data = [[0,1,2,3,4,5,6,7,8],[]]
            x_data = [
                BTC['age_sply'],
                DCR['age_sply'],
                BTC['age_sply'],
                DCR['age_sply'],
                DCR['age_sply'],
                DCR['age_sply'],
                DCR['age_sply'],
                DCR['age_sply'],
                DCR['age_sply'],
                ]
            y_data = [
                BTC['CapMrktCurUSD'],
                DCR['CapMrktCurUSD'],
                BTC['Unforg_Cost'],
                DCR['Unforg_Cost_5%'],
                DCR['Unforg_Cost_10%'],
                DCR['Unforg_Cost_15%'],
                DCR['Unforg_Cost_30%'],
                DCR['Unforg_Cost_50%'],
                DCR['Unforg_Cost_75%'],
                ]
            name_data = [
                'BTC Market Cap',
                'DCR Market Cap',
                'BTC Unforgeable Cost',
                'DCR Unforgeable Cost 5%',
                'DCR Unforgeable Cost 10%',
                'DCR Unforgeable Cost 15%',
                'DCR Unforgeable Cost 30%',
                'DCR Unforgeable Cost 50%',
                'DCR Unforgeable Cost 75%',
                ]
            color_data = [
                'rgb(255, 255,255)',
                'rgb(46, 214, 161)',
                'rgb(255, 102, 0)',
                'rgb(1, 255, 116)',
                'rgb(156,225,43)',
                'rgb(255, 255, 102)',
                'rgb(255, 153, 102)',
                'rgb(255, 102, 102)',
                'rgb(255, 80, 80)',
                ]
            color_data = check_standard_charts(self.theme).color_invert(color_data)
            dash_data = [
                'solid','solid','solid','solid','solid','solid','solid','solid','solid',
                ]
            width_data = [
                2,2,2,2,2,2,2,2,2,
                ]
            opacity_data = [
                1,1,1,1,1,1,1,1,1,
                ]
            legend_data = [
                True,True,True,True,True,True,True,True,True,
                ]#
            title_data = [
                '<b>Sound Money, Unforgeable Costliness</b>',
                '<b>Coin Age (Supply/21M)</b>',
                '<b>Cost to Attack Network (USD)</b>',
                '<b></b>']
            range_data = [[0,1],[5,12],[0,0]]
            autorange_data = [False,False,False]
            type_data = ['linear','log','log']#
            fig = check_standard_charts(self.theme).subplot_lines_singleaxis(
                title_data, range_data ,autorange_data ,type_data,
                loop_data,x_data,y_data,name_data,color_data,
                dash_data,width_data,opacity_data,legend_data
                )
            #Increase tick spacing
            fig.update_xaxes(dtick=0.1,showgrid=True)
            fig.update_yaxes(showgrid=True)
            fig.show()

        def unforgeable_cost_daily(self):
            """
            #############################################################################
            UNFORGEABLE COSTLINESS - DAILY
            Assumptions - No honest security provider is willing to expend more than the available block reward
                        - Considers PoS security influence over PoW hash-power multiple
            #############################################################################
            """
            BTC = self.BTC
            DCR = self.DCR

            #Calculate Unforgeable Costliness (Daily Sum)
            BTC['Unforg_Cost']  = BTC['PoW_income_usd'] + BTC['FeeTotUSD']
            DCR['PoW_Cost']     = DCR['PoW_income_usd'] + DCR['FeeTotUSD']
            DCR['PoS_Cost']     = DCR['PoS_income_usd']

            #Calculate Decred security curve
            _df = dcr_security_analyse().dcr_security_curve(0)
            #Calculate Range of Decred Security Conditions
            for y in [5,10,15,30,50,75]:                                        #Assume range of Attacker ticket stake ownership
                y   = y/100                                                     #Probability attacker tickets make block
                p_y = float(_df[_df['y']==y]['p_y'])                            #Probability attacker holds required tickets to make valid block
                x_y = float(_df[_df['y']==y]['x_y'])                            #hash-power multiple
                col_name = 'Unforg_Cost_'+str(int(y*100))+'%'                   #Set column name e.g 'Unforg_Cost_5%'
                DCR[col_name] = (p_y * DCR['PoS_Cost'] + x_y * DCR['PoW_Cost']) #Cumulative Unforgeable Cost
            
            
            loop_data = [[0,1,2,3,4,5,6,7,8,9,10],[]]
            x_data = [
                BTC['age_sply'],
                DCR['age_sply'],
                BTC['age_sply'],
                DCR['age_sply'],
                DCR['age_sply'],
                DCR['age_sply'],
                DCR['age_sply'],
                DCR['age_sply'],
                DCR['age_sply'],
                BTC['age_sply'],
                DCR['age_sply'],
                ]
            y_data = [
                BTC['CapMrktCurUSD'],
                DCR['CapMrktCurUSD'],
                BTC['Unforg_Cost'],
                DCR['Unforg_Cost_5%'],
                DCR['Unforg_Cost_10%'],
                DCR['Unforg_Cost_15%'],
                DCR['Unforg_Cost_30%'],
                DCR['Unforg_Cost_50%'],
                DCR['Unforg_Cost_75%'],
                BTC['TxTfrValUSD'].rolling(7).mean(),
                DCR['TxTfrValUSD'].rolling(7).mean(),
            ]
            name_data = [
                'BTC Market Cap',
                'DCR Market Cap',
                'BTC Attack Cost',
                'DCR Attack Cost 5%',
                'DCR Attack Cost 10%',
                'DCR Attack Cost 15%',
                'DCR Attack Cost 30%',
                'DCR Attack Cost 50%',
                'DCR Attack Cost 75%',
                'BTC Daily USD Settled',
                'DCR Daily USD Settled',
            ]
            color_data = [
                'rgb(255, 255,255)' ,
                'rgb(46, 214, 161)' ,
                'rgb(255, 102, 0)',
                'rgb(1, 255, 116)',
                'rgb(156,225,43)', 
                'rgb(255, 255, 102)',
                'rgb(255, 153, 102)',
                'rgb(255, 102, 102)',
                'rgb(255, 80, 80)',
                'rgb(255, 255, 255)', 
                'rgb(112, 203, 255)',
            ]
            color_data = check_standard_charts(self.theme).color_invert(color_data)
            dash_data = [
                'solid','solid','dot','dot','dot','dot','dot','dot','dot','solid','solid',
            ]
            width_data = [
                2,2,1,1,1,1,1,1,1,3,3
            ]
            opacity_data = [
                1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,1
            ]
            legend_data = [
                True,True,True,True,True,True,True,True,True,True,True
            ]
            title_data = [
                '<b>Daily Security and Tx Settlement</b>',
                '<b>Coin Age (Supply/21M)</b>',
                '<b>Cost to Attack Network (USD)</b>',
                '<b>Pure PoW Premium Ratio</b>'
            ]
            range_data = [[0,1],[2,12],[-1,5]]
            autorange_data = [False,False,False]
            type_data = ['linear','log','log']#
            fig = check_standard_charts(self.theme).subplot_lines_singleaxis(
                title_data, range_data ,autorange_data ,type_data,
                loop_data,x_data,y_data,name_data,color_data,
                dash_data,width_data,opacity_data,legend_data
                )
            #Increase tick spacing
            fig.update_xaxes(dtick=0.1,showgrid=True)
            fig.update_yaxes(showgrid=True)
            fig.show()

        def unforgeable_cost_compare(self):
            """
            #############################################################################
            COMPARE TOP CAP PROJECTS
            Compares the cumulative unforgeable costliness of top market cap projects
            Case 1: BTC, BCH, XMR, ZEC, ETH
                Cumulative Total USD block reward (incl fees)
            Case 2: Dash
                Cumulative Total USD block reward (incl fees) + Cost of one Masternode (1000DASH)
            Case 3: DCR
                Cumulative Total USD block reward (incl fees) modified by PoS/PoW Security Curve
            #############################################################################
            """
            BTC = self.BTC
            DCR = self.DCR

            #Calculate Unforgeable Costliness (Cumulative Sum)
            BTC['Unforg_Cost']  = BTC['PoW_income_usd'].cumsum() + BTC['FeeTotUSD'].cumsum()
            DCR['PoW_Cost']     = DCR['PoW_income_usd'].cumsum() + DCR['FeeTotUSD'].cumsum()
            DCR['PoS_Cost']     = DCR['PoS_income_usd'].cumsum()

            #Calculate Decred security curve
            _df = dcr_security_analyse().dcr_security_curve(0)
            #Calculate Range of Decred Security Conditions
            for y in [5,10,15,30,50,75]:                                            #Assume range of Attacker ticket stake ownership
                y   = y/100                                                     #Probability attacker tickets make block
                p_y = float(_df[_df['y']==y]['p_y'])                            #Probability attacker holds required tickets to make valid block
                x_y = float(_df[_df['y']==y]['x_y'])                            #hash-power multiple
                col_name = 'Unforg_Cost_'+str(int(y*100))+'%'                   #Set column name e.g 'Unforg_Cost_5%'
                DCR[col_name] = (p_y * DCR['PoS_Cost'] + x_y * DCR['PoW_Cost']) #Cumulative Unforgeable Cost

            LTC = Coinmetrics_api('ltc',"2011-10-07",today).convert_to_pd().set_index('date',drop=False)
            BCH = Coinmetrics_api('bch',"2017-08-01",today).convert_to_pd().set_index('date',drop=False)
            DASH = Coinmetrics_api('dash',"2014-01-19",today).convert_to_pd().set_index('date',drop=False)
            XMR = Coinmetrics_api('xmr',"2014-04-18",today).convert_to_pd().set_index('date',drop=False)
            ZEC = Coinmetrics_api('zec',"2016-10-28",today).convert_to_pd().set_index('date',drop=False)
            ETH = Coinmetrics_api('eth',"2015-07-30",today).convert_to_pd().set_index('date',drop=False)

            LTC['age_sply'] = LTC['SplyCur']/84e6
            BCH['age_sply'] = BCH['SplyCur']/21e6
            DASH['age_sply'] = DASH['SplyCur']/17.6e6
            XMR['age_sply'] = XMR['SplyCur']/22.466e6
            ZEC['age_sply'] = ZEC['SplyCur']/21e6
            ETH['age_sply'] = ETH['SplyCur']/135e6

            LTC['Unforg_Cost'] = LTC['DailyIssuedNtv'] *LTC['PriceUSD'] + LTC['FeeTotUSD']
            BCH['Unforg_Cost'] = BCH['DailyIssuedNtv'] *BCH['PriceUSD'] + BCH['FeeTotUSD']
            DASH['Unforg_Cost']= DASH['DailyIssuedNtv']*DASH['PriceUSD'] + DASH['FeeTotUSD'] + 1000*DASH['PriceUSD'] #1x MN
            XMR['Unforg_Cost'] = XMR['DailyIssuedNtv'] *XMR['PriceUSD'] + XMR['FeeTotUSD']
            ZEC['Unforg_Cost'] = ZEC['DailyIssuedNtv'] *ZEC['PriceUSD'] + ZEC['FeeTotUSD']
            ETH['Unforg_Cost'] = ETH['DailyIssuedNtv'] *ETH['PriceUSD'] + ETH['FeeTotUSD']


            loop_data = [[0,1,2,3,4,5,6,7,8,9,10,11,12],[]]
            x_data = [
                BTC['age_sply'],
                DCR['age_sply'],DCR['age_sply'],DCR['age_sply'],
                DCR['age_sply'],DCR['age_sply'],DCR['age_sply'],
                LTC['age_sply'], 
                BCH['age_sply'], 
                DASH['age_sply'],
                XMR['age_sply'], 
                ZEC['age_sply'], 
                ETH['age_sply'], 
                ]
            y_data = [
                BTC['Unforg_Cost'],
                DCR['Unforg_Cost_5%'],DCR['Unforg_Cost_10%'],  
                DCR['Unforg_Cost_15%'],DCR['Unforg_Cost_30%'], 
                DCR['Unforg_Cost_50%'],DCR['Unforg_Cost_75%'],
                LTC['Unforg_Cost'].cumsum(),
                BCH['Unforg_Cost'].cumsum(),
                DASH['Unforg_Cost'].cumsum(),
                XMR['Unforg_Cost'].cumsum(),
                ZEC['Unforg_Cost'].cumsum(),
                ETH['Unforg_Cost'].cumsum()
                ]
            name_data = [
                'BTC',
                'DCR 5%','DCR 10%','DCR 15%',
                'DCR 30%','DCR 50%','DCR 75%',
                'LTC',
                'BCH',
                'DASH',
                'XMR',
                'ZEC',
                'ETH',
                ]
            color_data = [
                'rgb(255, 102, 0)',
                'rgb(1, 255, 116)','rgb(156,225,43)', 
                'rgb(255, 255, 102)','rgb(255, 153, 102)',
                'rgb(255, 102, 102)','rgb(255, 80, 80)',
                'rgb(214, 214, 194)',
                'rgb(0, 153, 51)',  
                'rgb(51, 204, 255)',
                'rgb(255, 153, 0)',  
                'rgb(255, 255, 0)',  
                'rgb(153, 51, 255)' 
                ]
            color_data = check_standard_charts(self.theme).color_invert(color_data)
            dash_data = [
                'solid',
                'solid','solid','solid',
                'solid','solid','solid',
                'dot',
                'dot',
                'dot',
                'dot',
                'dot',
                'dot',
                ]
            width_data = [
                2,
                2,2,2,2,2,2,
                2,2,2,2,2,2]
            opacity_data = [
                1,
                1,1,1,1,1,1,
                1,1,1,1,1,1,
                ]
            legend_data = [
                True,
                True,True,True,True,True,True,
                True,True,True,True,True,True]#
            title_data = [
                '<b>Compare Unforgeable Costliness</b>',
                '<b>Coin Age (Supply / 2050 Supply)</b>',
                '<b>Cost to Attack Network (USD)</b>']
            range_data = [[0,1],[4,12],[-1,5]]
            autorange_data = [False,False,False]
            type_data = ['linear','log','log']
            fig = check_standard_charts(self.theme).subplot_lines_singleaxis(
                title_data, range_data ,autorange_data ,type_data,
                loop_data,x_data,y_data,name_data,color_data,
                dash_data,width_data,opacity_data,legend_data
                )
            #Increase tick spacing
            fig.update_xaxes(dtick=0.1,showgrid=True)
            fig.update_yaxes(showgrid=True)
            fig.show()

        def dcr_btc_pow_growth(self):
            """
            #############################################################################
            BITCOIN AND DECRED POW GROWTH
            Presents the relative growth and performance of 
            PoW metrics for Difficulty and Hashrate
            #############################################################################
            """

            BTC = self.BTC
            DCR = self.DCR[self.DCR['pow_hashrate_THs_avg']>1]


            loop_data = [[0,1,4,5],[2,3]]
            x_data = [
                BTC['age_days'],DCR['age_days'],
                BTC['age_days'],DCR['age_days'],
                BTC['age_days'],DCR['age_days'],
                ]
            y_data = [
                BTC['DiffMean'],                DCR['DiffMean'],
                BTC['HashRate']*1000,           DCR['pow_hashrate_THs_avg'],
                BTC['CapMrktCurUSD'],           DCR['CapMrktCurUSD'],
                ]
            name_data = [
                'Bitcoin Difficulty','Decred Difficulty',
                'Bitcoin Hashrate','Decred Hashrate',
                'Bitcoin Market Cap','Decred Market Cap',
                ]
            color_data = [
                'rgb(255, 102, 0)' , 'rgb(46, 214, 161)' ,
                'rgb(65, 191, 83)','rgb(254, 215, 140)',
                'rgb(255, 102, 0)' , 'rgb(46, 214, 161)' ,
                ]
            color_data = check_standard_charts(self.theme).color_invert(color_data)
            dash_data = [
                'solid','solid','solid','solid','dot','dot',
                ]
            width_data = [
                2,2,1,1,1,1
                ]
            opacity_data = [
                1,1,1,1,0.5,0.5
                ]
            legend_data = [
                True,True,True,True,True,True,
                ]#
            title_data = [
                '<b>Proof of Work Growth</b>',
                '<b>Coin Age (Days since Launch)</b>',
                '<b>Protocol Difficulty</b>',
                '<b>Network Hashrate (TH/s)</b>']
            range_data = [[0,14*365],[0,14],[-6,9]]
            autorange_data = [True,False,True]
            type_data = ['linear','log','log']#
            fig = check_standard_charts(self.theme).subplot_lines_doubleaxis(
                title_data, range_data ,autorange_data ,type_data,
                loop_data,x_data,y_data,name_data,color_data,
                dash_data,width_data,opacity_data,legend_data
                )
            #Increase tick spacing
            fig.update_xaxes(dtick=365,showgrid=True)
            fig.update_yaxes(secondary_y=False,showgrid=True)
            fig.show()

        def finality_ratio(self):
            """
            #############################################################################
            FINALITY RATIO
            Calculate and plot the real time difference in protocol finality between Bitcoin and Decred
            DCR Daily cost / BTC Daily Cost --> block for block (x2 for time for time or btc blocks)
            #############################################################################
            """
            BTC = self.BTC
            DCR = self.DCR

            #Calculate daily unforgeable costliness
            BTC['BTC_Unforg_Cost']  = BTC['PoW_income_usd'] + BTC['FeeTotUSD']
            BTC = BTC[['date','BTC_Unforg_Cost']]
            DCR['PoW_Cost']     = DCR['PoW_income_usd'] + DCR['FeeTotUSD']
            DCR['PoS_Cost']     = DCR['PoS_income_usd']

            #Calculate Decred security curve
            _df = dcr_security_analyse().dcr_security_curve(0)
            #Calculate Range of Decred Security Conditions
            for y in [5,10,15,30,50,75]:                                        #Assume range of Attacker ticket stake ownership
                y   = y/100                                                     #Probability attacker tickets make block
                p_y = float(_df[_df['y']==y]['p_y'])                            #Probability attacker holds required tickets to make valid block
                x_y = float(_df[_df['y']==y]['x_y'])                            #hash-power multiple
                col_name = 'Unforg_Cost_'+str(int(y*100))+'%'                   #Set column name e.g 'Unforg_Cost_5%'
                DCR[col_name] = (p_y * DCR['PoS_Cost'] + x_y * DCR['PoW_Cost']) #Cumulative Unforgeable Cost

            #Calculate Finality Ratio
            #Finality Ratio = Decred Daily Security / Bitcoin Daily Security
            DCR = DCR.merge(BTC,left_on='date',right_on='date')

            DCR['Finality_Ratio_5%']  = (
                DCR['Unforg_Cost_5%'] / DCR['BTC_Unforg_Cost']
            )
            DCR['Finality_Ratio_10%'] = (
                DCR['Unforg_Cost_10%'] / DCR['BTC_Unforg_Cost']
            )
            DCR['Finality_Ratio_15%'] = (
                DCR['Unforg_Cost_15%'] / DCR['BTC_Unforg_Cost']
            )
            DCR['Finality_Ratio_30%'] = (
                DCR['Unforg_Cost_30%'] / DCR['BTC_Unforg_Cost']
            )
            DCR['Finality_Ratio_50%'] = (
                DCR['Unforg_Cost_50%'] / DCR['BTC_Unforg_Cost']
            )
            DCR['Finality_Ratio_75%'] = (
                DCR['Unforg_Cost_75%'] / DCR['BTC_Unforg_Cost']
            )

            loop_data = [[0,1,2,3,4,5],[]]
            x_data = [
                DCR['date'],
                DCR['date'],
                DCR['date'],
                DCR['date'],
                DCR['date'],
                DCR['date'],
                ]
            y_data = [
                DCR['Finality_Ratio_5%'].rolling(7).mean(),
                DCR['Finality_Ratio_10%'].rolling(7).mean(),
                DCR['Finality_Ratio_15%'].rolling(7).mean(),
                DCR['Finality_Ratio_30%'].rolling(7).mean(),
                DCR['Finality_Ratio_50%'].rolling(7).mean(),
                DCR['Finality_Ratio_75%'].rolling(7).mean(),
                ]
            name_data = [
                'DCR Finality Ratio 5%',
                'DCR Finality Ratio 10%',
                'DCR Finality Ratio 15%',
                'DCR Finality Ratio 30%',
                'DCR Finality Ratio 50%',
                'DCR Finality Ratio 75%',
                ]
            color_data = [
                'rgb(1, 255, 116)',
                'rgb(156,225,43)', 
                'rgb(255, 255, 102)',
                'rgb(255, 153, 102)',
                'rgb(255, 102, 102)',
                'rgb(255, 80, 80)',
                ]
            color_data = check_standard_charts(self.theme).color_invert(color_data)
            dash_data = [
                'solid','solid',
                'solid','solid',
                'solid','solid',
                ]
            width_data = [
                2,2,2,2,2,2,
                ]
            opacity_data = [
                1,1,1,1,1,1,
                ]
            legend_data = [
                True,True,True,
                True,True,True,
                ]#
            title_data = [
                '<b>Decred Finality Ratio</b>',
                '<b>Date</b>',
                '<b>DCR/BTC Daily Attack Cost Ratio</b>',
                '<b>Pure PoW Premium Ratio</b>']
            range_data = [[0,1],[4,12],[-1,5]]
            autorange_data = [True,True,False]
            type_data = ['date','log','log']#
            fig = check_standard_charts(self.theme).subplot_lines_singleaxis(
                title_data, range_data ,autorange_data ,type_data,
                loop_data,x_data,y_data,name_data,color_data,
                dash_data,width_data,opacity_data,legend_data
                )
            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(secondary_y=False,showgrid=True)
            #Increase tick spacing
            #fig.update_xaxes(dtick=0.1)
            fig.show()

    class charts_security_performance():

        def __init__(self,theme):
            self.df = dcr_security_analyse().calculate_df('dcr',12,'internal') 
            self.theme = theme

        def pow_profitability(self):
            """
            #############################################################################
            Decred PoW Miner Profitability
            #############################################################################
            """
            df = self.df

            df1 = df[df['y']==0.01]
            df2 = df[df['y']==0.15]
            
            loop_data = [[0,1],[2,3]]
            x_data = [
                df1['blk'],
                df2['blk'],
                df1['blk'],
                df2['blk'],
                ]
            y_data = [
                df1['H_net'],
                df2['H_net'],
                df1['pow_prof'],
                df2['pow_prof'],
                ]
            name_data = [
                'HashRate (0.01%)',
                'HashRate (0.01%)',
                ]
            color_data = [
                'rgb(255, 102, 0)' , 
                'rgb(46, 214, 161)',
                'rgb(65, 191, 83)',
                'rgb(254, 215, 140)',
                'rgb(255, 102, 0)', 
                'rgb(46, 214, 161)',
                ]
            color_data = check_standard_charts(self.theme).color_invert(color_data)
            dash_data = [
                'solid','solid','solid','solid','dot','dot',
                ]
            width_data = [
                2,2,1,1,1,1
                ]
            opacity_data = [
                1,1,1,1,0.5,0.5
                ]
            legend_data = [
                True,True,True,True,True,True,
                ]#
            title_data = [
                '<b>Proof of Work Growth</b>',
                '<b>Coin Age (Days since Launch)</b>',
                '<b>Protocol Difficulty</b>',
                '<b>Network Hashrate (TH/s)</b>']
            range_data = [[0,14*365],[0,14],[-6,9]]
            autorange_data = [True,False,True]
            type_data = ['linear','log','log']#
            fig = check_standard_charts(self.theme).subplot_lines_doubleaxis(
                title_data, range_data ,autorange_data ,type_data,
                loop_data,x_data,y_data,name_data,color_data,
                dash_data,width_data,opacity_data,legend_data
                )
            #Increase tick spacing
            fig.update_xaxes(dtick=365,showgrid=True)
            fig.update_yaxes(secondary_y=False,showgrid=True)
            fig.show()


            
#Decred Security Curve
#model = 1 prints Decred Security Curve chart
#df_1 = dcr_security_analyse().dcr_security_curve(0)

#Decred full security analysis DataFrame
#asset, atk_blk,atk_type
df_2 = dcr_security_analyse().calculate_df('dcr',12,'internal')



#Plot Unforgeable Costliness Charts
fig = dcr_security_analyse().charts_unforgeable_costliness('dark')
#Unforgeable Costliness
fig.unforgeable_cost_cum()
fig.unforgeable_cost_daily()
fig.unforgeable_cost_compare()
fig.dcr_btc_pow_growth()
fig.finality_ratio()












df = df_2
"""
#############################################################################
Decred PoW Miner Profitability
#############################################################################
"""
#df = dcr_security_analyse().calculate_df('dcr',12,'internal') 

df1 = df[df['y']==0.01]
df2 = df[df['y']==0.15]

loop_data = [[0,1],[2,3]]
x_data = [
    df1['blk'],
    df2['blk'],
    df1['blk'],
    df2['blk'],
    ]
y_data = [
    df1['H_net'],
    df2['H_net'],
    df1['pow_prof'],
    df2['pow_prof'],
    ]
name_data = [
    'HashRate (0.01%)',
    'HashRate (0.15%)',
    'PoW Profitability (0.01%)',
    'PoW Profitability (0.15%)',
    ]
color_data = [
    'rgb(255, 102, 0)' , 
    'rgb(46, 214, 161)',
    'rgb(65, 191, 83)',
    'rgb(254, 215, 140)',
    'rgb(255, 102, 0)', 
    'rgb(46, 214, 161)',
    ]
#color_data = check_standard_charts(self.theme).color_invert(color_data)
dash_data = [
    'solid','solid','solid','solid','dot','dot',
    ]
width_data = [
    2,2,1,1,1,1
    ]
opacity_data = [
    1,1,1,1,0.5,0.5
    ]
legend_data = [
    True,True,True,True,True,True,
    ]#
title_data = [
    '<b>Proof of Work Growth</b>',
    '<b>Coin Age (Days since Launch)</b>',
    '<b>Protocol Difficulty</b>',
    '<b>Network Hashrate (TH/s)</b>']
range_data = [[0,14*365],[0,14],[-6,9]]
autorange_data = [True,True,True]
type_data = ['linear','linear','linear']#
fig = check_standard_charts('dark').subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
#fig.update_xaxes(dtick=365,showgrid=True)
#fig.update_yaxes(secondary_y=False,showgrid=True)
fig.show()







































#df_sec[df_sec['y']==0.15]
#
#
#df_sec.columns
#df_sec['pos_term'] = df_sec['y']*df_sec['tic_pool']*df_sec['price']*df_sec['tic_price']
#df_sec['pca'] = df_sec['pca'] + df_sec['pos_term']
#
#import plotly.graph_objects as go
#fig = go.Figure(data=[go.Scatter3d(
#    x=df_sec['blk'], 
#    y=df_sec['y'], 
#    z=df_sec['pca'],
#    mode='markers',
#    marker=dict(
#        size=12,
#        color=df_sec['pca']/1e6,                # set color to an array/list of desired values
#        colorscale='Electric',   # choose a colorscale
#        opacity=0.8
#    )
#)])
#fig.show()
#
#fig.update_layout(scene = dict(
#    xaxis = dict(
#        type = 'linear',
#        backgroundcolor="rgb(200, 200, 230)",
#        gridcolor="white",
#        showbackground=True,
#        zerolinecolor="white",),
#    yaxis = dict(
#        type = 'linear',
#        backgroundcolor="rgb(230, 200,230)",
#        gridcolor="white",
#        showbackground=True,
#        zerolinecolor="white"),
#    zaxis = dict(
#        type = 'log',
#        backgroundcolor="rgb(230, 230,200)",
#        gridcolor="white",
#        showbackground=True,
#        zerolinecolor="white",),),
#    width=1500,
#    height=1500,
#    margin=dict(
#    r=10, l=10,
#    b=10, t=10)
#    )
#fig.show()

