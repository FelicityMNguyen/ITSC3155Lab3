import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSSV file from Datasets folder
df = pd.read_csv('../Datasets/Weather2014-15.csv')

# Extrapolating the actual max temp per month
new_df = df.groupby(['day', 'month'], sort=False).agg(
    {'record_max_temp': 'max'}).reset_index()
#print(new_df)

# Preparing data
data = [go.Heatmap(x=new_df['day'],
                   y=new_df['month'],
                   z=new_df['record_max_temp'].values.tolist(),
                   colorscale='Jet')]

# Preparing layout
layout = go.Layout(title='Recorded Max Temperature (F) On Days Of The Week From July 2014 to June 2015',
                   xaxis_title="Day of Week",
                   yaxis_title="Week of Month"
                   )

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='WeatherHeatMap.html')