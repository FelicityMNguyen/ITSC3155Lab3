import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSSV file from Datasets folder
df = pd.read_csv('../Datasets/Weather2014-15.csv')

# Extrapolating the actual max temp per month
new_df = df.groupby('month', sort=False).agg(
    {'actual_max_temp': 'max'}).reset_index()

# Preparing data
data = [go.Scatter(x=new_df['month'], y=new_df['actual_max_temp'], mode='lines',
                   name='Record Max Temperature')]

# Preparing layout
layout = go.Layout(title='The Actual Max Temperature of Each Month From 2014 To 2015',
                   xaxis_title="Month", yaxis_title="Temperature (F)")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='WeatherLineChart.html')