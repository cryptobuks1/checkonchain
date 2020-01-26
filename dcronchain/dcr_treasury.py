#Analyse the Decred Treasury
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import *

treasury = pd.read_csv(r"D:\code_development\checkonchain\checkonchain\dcronchain\resources\data\treasury_20200126.csv")
treasury.columns


treasury['funds'] = treasury['value'] * treasury['direction']
treasury['balance'] = treasury['funds'].cumsum()
treasury['incoming'] = treasury[treasury['direction']==1]['value'].cumsum()
treasury['outgoing'] = treasury['incoming'] -  treasury['balance']

treasury['spend_rate'] = treasury['outgoing']/treasury['incoming']

treasury.loc[0,['time_stamp']]
treasury.loc[497330,['time_stamp']]

float(treasury['time_stamp'][0])-float(treasury['time_stamp'][-1:])



x_data = [treasury['time_stamp'],treasury['time_stamp'],treasury['time_stamp'],treasury['time_stamp']]
y_data = [treasury['balance'],treasury['incoming'],treasury['outgoing'],treasury['spend_rate']]
name_data = ['Treasury Balance','Incoming','Outgoing','Spending Rate']

fig = make_subplots(specs=[[{"secondary_y": True}]])
for i in range(0,3):
    fig.add_trace(go.Scatter(
        x=x_data[i], 
        y=y_data[i],
        mode='lines',
        name=name_data[i]),
        secondary_y=False)
for i in range(3,4):
    fig.add_trace(go.Scatter(
        x=x_data[i], 
        y=y_data[i],
        mode='lines',
        name=name_data[i]),
        secondary_y=True)

# Add figure title
fig.update_layout(title_text="Decred Treasury Balances")
fig.update_xaxes(
    title_text="<b>time_stamp</b>",
    autorange="reversed"
    )
fig.update_yaxes(
    title_text="<b>Treasury DCR balance</b>",
    secondary_y=False)
fig.update_yaxes(
    title_text="<b>Treasury Spend Ratio</b>",
    secondary_y=True)
fig.update_layout(template="plotly_dark")
fig.show()

