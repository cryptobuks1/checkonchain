# checkonchain
Python Modules for studying the on-chain behavior of Bitcoin and Decred

## Purpose of repo
This repo is a collection of analysis code, tools and published articles for analysing the blockchains of Bitcoin and Decred. 

Tools in this repo are structured as follows
- General - scripts for calling standard APIs for blockchain and market data (e.g. coinmetrics Community)
- btconchain - Modules related to Bitcoin
- dcronchain - Modules related to Decred
- ltconchain - Modules related to Litecoin
- Research Articles - working folder for papers to be published
- Misc - temp storage and misc files

*Note - I am not a developer, code unlikely to be perfect. Suggestions and ideas welcomed.*

## Goals for these studies
1. Establish additional rigor for fundamental investment thesis for Bitcoin and Decred
2. Analyse the characteristics of both Bitcoin and Decred monetary policy, security mechanisms, unforgeable costliness and performance
3. Analyse performance of PoW difficulty and DCR tickets
4. Assess the balance between supply issuance, scarcity, ticket behaviour and transaction flows
5. Establish a set of charting packages with which others can replicate and follow the analysis
6. Develop an online charting package similar to woobull.com for both Decred and Bitcion.


## Repo Structure
This repo is my coding project and thus structure will develop over time. All code will be Python unless otherwise noted

```
checkonchain
│---README.md
│---LICENCE    
│
└───general (general tools, calling APIs, coin comparisons etc)
│   │---coinmetrics.py (pulls community API data from coinmetrics) [100%]
│   │---regression_analysis.py (performs LR analysis + stores constants) [100%]
|   |---standard_charts.py (standard set of consistent charts) [Ongoing]
|
└───btconchain
│   │---btc_add_metrics.py (compilation of datasets) [WIP]
│   │---btc_dust_limit.py (analysis on dust limit of btc) [80% - needs clean]
|   |---btc_pricing_models.py (Woobull.com style charts) [WIP]
|   |---btc_schedule.py (theoretical supply schedule by block) [90% - Review]
|
|---|---charts
|   |   |---chart_comparemetric_sply.py (Compare coins metric vs coin-age)
|   
|---|---data
|       |---satoshi_history --> sergio nonce data
│   
└───dcronchain
    │---dcr_add_metrics.py (compilation of datasets) [WIP]
    |---dcr_dcrdata_api.py (extract DCR data from dcrdata) [100%]
    |---dcr_pricing_model.py (Woobull.com style charts) [WIP]
    │---dcr_schedule.py (theoretical supply schedule by block) [90% - Review]
    |---dcr_security_model.py (Cost to attack after Stafford, 2019) [WIP]
    |---dcr_treasury.py (analysis of the Decred treasury wallet) [WIP]
    |
    |---charts
    |   |---chart_dcr_comparemetric.py (compare ratio of DCR/coin) [100%]
    |   |---chart_dcr_mcap_powerlaw.py (x) [x%]
    |   |---chart_dcr_premine.py (x) [x%]
    |   |---chart_dcr_comparemetric.py (compare ratio of DCR/coin) [100%]
    |   |---chart_block_subsidy.py (PoW, PoS, Fund models) [100%]
    |
    |---|resources
            |---data
                |---dcr_pricedata_2016-02-08_2016-05-16.csv (early price data)


```

- **Monetary Premiums** - Article and data for [medium article located here.](https://medium.com/@_Checkmatey_/monetary-premiums-can-altcoins-compete-with-bitcoin-54c97a92c6d4)
- **Coinmetrics** - Contains all scripts for extracting data from Coinmetrics
- **Decred_Analysis** - Modules for analysing Decred specific metrics
- **Bitcoin_Analysis** - Modules for analysing Bitcoin specific metrics

## Dependencies
1. [Coinmetrics python toolkit by h4110w33n.](https://github.com/h4110w33n/coinmetrics)
2. [TinyDecred by buck54321](https://github.com/decred/tinydecred)
3. [Quandl](https://www.quandl.com/tools/python) (```pip install quandl```)



## Roadmap
**Phase 1 - Write supply curve scripts:**
- Bitcoin (90%)
- Decred (90%)

**Phase 2 - Establish API Calls and Modules for:**
- Coinmetrics V2 (50%)
- dcrdata (via TinyDecred) (50%)
- CoinAPI (0%)
- Glassnode (0%)

**Phase 3 - Compile datasets from API calls into specific analysis**
- Decred staking Distribution - PoW, PoS and Ticket pool
- Transaction volumes and value vs Ticket behaviour
- PoW and PoS difficulty comparisons as driver for value
- Unforgeable costliness (Stock-to-flow, PoW Mining costs, PoS Capital costs, Treasury work cost)
- Realised Cap, Market Cap, Days destroyed


## Donations

**Bitcoin**
>![bc1q0a8r0jcf4natnmj2cun3nz3kwj5z5h2jsc9fk2](misc//images//btc_qr.png)

>[bc1q0a8r0jcf4natnmj2cun3nz3kwj5z5h2jsc9fk2](https://blockstream.info/address/bc1q0a8r0jcf4natnmj2cun3nz3kwj5z5h2jsc9fk2)

**Decred**
>![Dsmx4zrTuS6UJxGHNutc5pwH73VHx7JN5XE](misc//images//dcr_qr.png)

>[Dsmx4zrTuS6UJxGHNutc5pwH73VHx7JN5XE](https://explorer.dcrdata.org/address/Dsmx4zrTuS6UJxGHNutc5pwH73VHx7JN5XE?chart=balance&zoom=k5h3mcg0-k6ok9i80&bin=month)