import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSSV file from Datasets folder
df = pd.read_csv('../Datasets/Weather2014-15.csv')

# Extrapolating the actual max, min, and mean temps per month
new_df = df.groupby('month', sort=False).agg(
    {'actual_mean_temp': 'mean', 'actual_min_temp': 'min',
     'actual_max_temp': 'max'}).reset_index()

# Preparing data
trace1 = go.Scatter(x=new_df['month'], y=new_df['actual_mean_temp'],
                    mode='lines', name='Actual Mean Temp')
trace2 = go.Scatter(x=new_df['month'], y=new_df['actual_min_temp'],
                    mode='lines', name='Actual Min Temp')
trace3 = go.Scatter(x=new_df['month'], y=new_df['actual_max_temp'],
                    mode='lines', name='Actual Max Temp')
data = [trace1, trace2, trace3]

# Preparing layout
layout = go.Layout(title='The Actual Mean, Min, And Max Temperatures of Each Month From July 2014 To June 2015',
                   xaxis_title="Month", yaxis_title="Temperature (F)")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='WeatherMultiLineChart.html')