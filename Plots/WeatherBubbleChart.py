import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('../Datasets/Weather2014-15.csv')

# Extrapolating the average max and min temps per month
new_df = df.groupby('month', sort=False).agg(
    {'average_min_temp': 'mean',
     'average_max_temp': 'mean'}).reset_index()

# Preparing data
data = [
    go.Scatter(x=new_df['average_min_temp'],
               y=new_df['average_max_temp'], text=new_df['month'],
               mode='markers')#, marker=dict(size=new_df['Confirmed'] / 100,
                               #            color=new_df['Confirmed'] / 100,
                               #            showscale=True))
]

# Preparing layout
layout = go.Layout(title='The Average Min And Max Of Each Month From ',
                   xaxis_title="Average Min Temperature",
                   yaxis_title="Average Max Temperature",
                   hovermode='closest')

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename="WeatherBubleChart.html")