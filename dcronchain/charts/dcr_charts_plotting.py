#Module for printing charts contained in dcr_charts
from checkonchain.dcronchain.charts.dcr_charts import *

"""MODEL"""
#fig_dcr = dcr_chart_suite('dark')
fig_dcr = dcr_chart_suite('light')


"""NETWORK VALUATION"""
fig_dcr.mvrv(0)

fig_dcr.block_subsidy_usd(0)
fig_dcr.block_subsidy_btc(0)

fig_dcr.commitment_usd(0)
fig_dcr.commitment_btc(0)

fig_dcr.s2f_model(0)
fig_dcr.s2f_model_residuals()

fig_dcr.nvt_rvt()
fig_dcr.difficulty_ribbon()

"""PRICING MODELS"""
fig_dcr.mvrv(1)

fig_dcr.block_subsidy_usd(1)
fig_dcr.block_subsidy_btc(1)

fig_dcr.commitment_usd(1)
fig_dcr.commitment_btc(1)

fig_dcr.s2f_model(1)

"""Oscillators"""

fig_dcr.mayer_multiple()

fig_dcr.beam_indicator()

fig_dcr.puell_multiple()
fig_dcr.contractor_multiple()

fig_dcr.unrealised_PnL()
fig_dcr.MACD(0)

fig_dcr.mrkt_real_gradient(30)

"""Market Cycle Metrics"""

fig_dcr.dcr_vs_btc()
fig_dcr.bottom_cycle()
fig_dcr.top_cycle()

"""PermabullNino Metrics"""

fig_dcr.TVWAP()
fig_dcr.hodler_conversion()
fig_dcr.ticket_overunder()
fig_dcr.tic_vol_sum_142day()
fig_dcr.tx_volatility_ratio()
fig_dcr.tx_sum_adjsply_142d()
fig_dcr.max_vol_ratio()
fig_dcr.mining_pulse()

"""Performance Metrics"""
fig_dcr.privacy()
fig_dcr.privacy_volume()