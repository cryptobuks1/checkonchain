from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.charts.dcr_charts import *
from checkonchain.btconchain.charts.btc_charts import *

fig_btc = btc_chart_suite('dark')
fig_dcr = dcr_chart_suite('light')

"""Mayer Multiple"""

fig_btc.catch_btm_top()

fig_btc.mayer_multiple()
fig_dcr.mayer_multiple()


"""MVRV RATIO"""

fig_btc.mvrv()
fig_dcr.mvrv(0)

fig_btc.unrealised_PnL()
fig_dcr.unrealised_PnL()


"""DIFFICULTY RIBBON"""

fig_btc.difficulty_ribbon()
fig_dcr.difficulty_ribbon()

fig_btc.puell_multiple()
fig_dcr.puell_multiple()

"""NVT and RVT Ratio"""

fig_btc.nvt_rvt()
fig_dcr.nvt_rvt()


"""Block Subsidy"""

fig_btc.block_subsidy()
fig_dcr.commitment_usd(0)
fig_dcr.commitment_btc(0)