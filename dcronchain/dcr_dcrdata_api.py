#Extract key ticket data from dcrdata

""" DATA IS EXTRACTED FROM DCRDATA.ORG IN TWO MODULES
1) dcr_difficulty()  ---> For both PoS and PoW. Rows by Ticket window
blk, window, time, ticket_count, ticket_price, missed, pow_diff

2) dcr_performance() ---> data by block height on actual blockchain performance 
  blk, time, circulation, ticket_pool, ticket_count, pow_hashrate, pow_work, pow_offset
"""
#Data Science
import pandas as pd
import numpy as np

#Project specific modules
import json
from tinydecred.pydecred.dcrdata import DcrdataClient

client = DcrdataClient("https://alpha.dcrdata.org/")


"""
NOTES:
            Difficulty (by Window)
blk                 = Block Height
window              = Counter of Difficulty Window
time                = time (fomart unknown)
tic_cnt_window      = Tickets bought per window
tic_price           = Ticket Price DCR
tic_miss            = Tickets missed in window
pow_diff            = PoW difficulty

            Performance (by Block)
blk                 = Block Height
time                = time (fomart unknown)
dcr_sply            = Circulating DCR Supply
dcr_tic_sply        = Total DCR in tickets
tic_part            = PoS Participation Rate (dcr_tic / dcr_sply)
tic_pool            = Ticket Pool Count (target 40,960)
tic_blk             = Tickets bought in each block (calculated)
pow_hashrate_THs    = PoW Hashrate in TH/s
pow_work_EH         = PoW Cummulative Chainwork (Exahash --> TeraHash)
"""
class dcrdata_api():

    def __init__(self):
        self.window = 144 #blocks per window
        self.atoms = 1e8 #atoms per DCR
        self.votes = 5 #PoS votes per block
    
    def dcr_difficulty(self):
        print('...Fetching dcrdata - Difficulty metrics...')
        #Extract Ticket Price - WINDOW (~2600)
        tic_pce = pd.DataFrame(client.chart("ticket-price", bin="block")) #Pull dcrdata
        tic_pce.columns = ['tic_cnt_window','tic_price','time','window'] #Rename Columns
        tic_pce['tic_price']= tic_pce['tic_price']/ self.atoms #Change from Atoms to DCR
        tic_pce['window'] = tic_pce.index #Set window to a counter rather than 144
        #Missed Votes - WINDOW (~2600)
        tic_miss = pd.DataFrame(client.chart("missed-votes", bin="block", axis="time"))
        tic_miss.columns = ['tic_miss','offset','time','window']
        #Extract Mining Difficulty - WINDOW (~2600)
        pow_dif = pd.DataFrame(client.chart("pow-difficulty", bin="block", axis="time"))
        pow_dif.columns = ['pow_diff','time','window']
        #Combine into single dataset
        response=tic_pce.join(pow_dif['pow_diff'],how='outer')
        response=response.join(tic_miss['tic_miss'],how='outer')
        #Add block height and rearrange
        response['blk'] = (response.index+1)*self.window
        response=response[['blk','window','time','tic_cnt_window','tic_price','tic_miss','pow_diff']]
        #response['blk']=response.astype({'blk':'int64'}) #Ensure blk is int64
        return response


    def dcr_performance(self):
        print('...Fetching dcrdata - Performance metrics...')
        #Ticket Staked  - Output dataframe by block
        pos_stake = pd.DataFrame(client.chart("stake-participation", bin="block", axis="time")) #Pull dcrdata
        pos_stake.columns = ['axis','bin','dcr_sply','dcr_tic_sply','time'] #Rename columns
        pos_stake['dcr_sply']= pos_stake['dcr_sply']/ self.atoms #Atoms to DCR
        pos_stake['dcr_tic_sply']= pos_stake['dcr_tic_sply']/ self.atoms #Atoms to DCR
        pos_stake['tic_part'] = pos_stake['dcr_tic_sply']/pos_stake['dcr_sply'] #PoS Participation
        pos_stake['blk'] = pos_stake.index
        #Ticket Pool Size in DCR
        pos_pool = pd.DataFrame(client.chart("ticket-pool-size", bin="block", axis="time"))
        pos_pool.columns = ['axis','bin','tic_pool','time']
        pos_pool['tic_blk'] = pos_pool['tic_pool'].diff() + self.votes #Calculate number of tickets purchased in that block (+5 votes)
        #Mining Hashrate
        pow_hash = pd.DataFrame(client.chart("hashrate", bin="block", axis="time"))
        pow_hash.columns = ['axis','bin','pow_offset','pow_hashrate_THs','time']
        #Total Work
        tot_work = pd.DataFrame(client.chart("chainwork", bin="block", axis="time"))
        tot_work.columns = ['axis','bin','time','pow_work_TH'] #Note pow_work is in EH, to be converted to TH
        #Combine into single dataset
        response=pos_stake.join(pos_pool[['tic_blk','tic_pool']],how='outer') #Join
        response=response.join(pow_hash[['pow_hashrate_THs']],how='outer') #Join
        response=response.join(tot_work[['pow_work_TH']]*1000000,how='outer') #Join + Convert EH to TH
        #Restructure dataframe
        response=response[[
            'blk','time',
            'dcr_sply','dcr_tic_sply',
            'tic_blk','tic_pool',
            'pow_hashrate_THs','pow_work_TH'
            ]]
        #response['blk']=response.astype({'blk':'int64'}) #Ensure blk is int64
        return response


#a = dcrdata_api().dcr_difficulty()
#a.head(10)

#b = dcrdata_api().dcr_performance()
#b.tail(10)


