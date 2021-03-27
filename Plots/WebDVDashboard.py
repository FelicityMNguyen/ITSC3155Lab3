import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/Olympic2016Rio with Continents.csv')
df2 = pd.read_csv('../Datasets/Weather2014-15.csv')

app = dash.Dash()

# Bar chart data
# Sorting values and select first 20 countries
new_barchart_df = df1.sort_values(by=['Total'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=new_barchart_df['NOC'], y=new_barchart_df['Total'])]

# Stack bar chart data
# Creating sum of number of cases group by NOC Column
stackbarchart_df = df1.groupby(['NOC']).agg(
    {'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum', 'Total': 'sum'}).reset_index()
stackbarchart_df = stackbarchart_df.sort_values(by=['Total'],
                                                ascending=[False]).head(20).reset_index()

trace1_stackbarchart = go.Bar(x=stackbarchart_df['NOC'],
                              y=stackbarchart_df['Bronze'], name='Bronze',
                              marker={'color': '#CD7F32'})

trace2_stackbarchart = go.Bar(x=stackbarchart_df['NOC'],
                              y=stackbarchart_df['Silver'], name='Silver',
                              marker={'color': '#9EA0A1'})

trace3_stackbarchart = go.Bar(x=stackbarchart_df['NOC'],
                              y=stackbarchart_df['Gold'], name='Gold',
                              marker={'color': '#FFD700'})

data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# Line Chart
# Extrapolating the actual max temp per month
line_df = df2.groupby('month', sort=False).agg(
    {'actual_max_temp': 'max'}).reset_index()
data_linechart = [go.Scatter(x=line_df['month'], y=line_df['actual_max_temp'], mode='lines',
                   name='Record Max Temperature')]

# Multi Line Chart
multiline_df = df2.groupby('month', sort=False).agg(
    {'actual_mean_temp': 'mean', 'actual_min_temp': 'min',
     'actual_max_temp': 'max'}).reset_index()
trace1_multiline = go.Scatter(x=multiline_df['month'], y=multiline_df['actual_mean_temp'],
                              mode='lines', name='Actual Mean Temp')
trace2_multiline = go.Scatter(x=multiline_df['month'], y=multiline_df['actual_min_temp'],
                              mode='lines', name='Actual Min Temp')
trace3_multiline = go.Scatter(x=multiline_df['month'], y=multiline_df['actual_max_temp'],
                              mode='lines', name='Actual Max Temp')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# Bubble chart
bubble_df = df2.groupby('month', sort=False).agg(
    {'average_min_temp': 'mean',
     'average_max_temp': 'mean'}).reset_index()
data_bubblechart = [
    go.Scatter(x=bubble_df['average_min_temp'],
               y=bubble_df['average_max_temp'], text=bubble_df['month'],
               mode='markers')  # , marker=dict(size=new_df['Confirmed'] / 100,
    #            color=new_df['Confirmed'] / 100,
    #            showscale=True))
]

# Heatmap
heatmap_df = df2.groupby(['day', 'month'], sort=False).agg(
    {'record_max_temp': 'max'}).reset_index()
data_heatmap = [go.Heatmap(x=heatmap_df['day'],
                           y=heatmap_df['month'],
                           z=heatmap_df['record_max_temp'].values.tolist(),
                           colorscale='Jet')]

# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python',
             style={'textAlign': 'center'}),
    html.Div('Medals Won By National Olympic Committees in 2016 Olympic',
             style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the number of medals won by the top 20 '
             'National Olympic Committees in the chosen continent in the 2016 Olympic.'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a continent', style={'color': '#ef3e18', 'margin': '10px'}),
    dcc.Dropdown(
        id='select-continent',
        options=[
            {'label': 'Asia', 'value': 'Asia'},
            {'label': 'Africa', 'value': 'Africa'},
            {'label': 'Europe', 'value': 'Europe'},
            {'label': 'North America', 'value': 'North America'},
            {'label': 'Oceania', 'value': 'Oceania'},
            {'label': 'South America', 'value': 'South America'}
        ],
        value='Europe'
    ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the number of medals won by the global top 20 '
             'National Olympic Committees in the 2016 Olympic.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Medals Won',
                                      xaxis={'title': 'National Olympic Committee'},
                                      yaxis={'title': 'Total Medals Won'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represents types of medal won by the top 20 National Olympic '
        'Committees in the 2016 Olympic.'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Types of Medals Won In The Top 20 '
                                            'National Olympic Committees in the '
                                            '2016 Olympic',
                                      xaxis={'title': 'National Olympic Committee'},
                                      yaxis={'title': 'Types Of Medals Won'},
                                      barmode='stack')
              }
              ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.Br(),
    html.Br(),
    html.Div('Recorded Temperatures Between 2014-07-01 And 2015-06-30',
             style={'textAlign': 'center'}),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represents the record max temperature of each month '
             'between 2014-07-01 and 2015-06-30'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Record Max Temperature Of Each Month '
                                            'Between 2014-07-01 And 2015-06-30',
                                      xaxis={'title': 'Month'},
                                      yaxis={'title': 'Temperature (F)'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This line chart represents the actual mean, minimum, and max temperatures of each '
        'month between 2014-07-01 and 2015-06-30.'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='The Actual Mean, Minimum, And Maximum Temperatures '
                            'Between 2014-07-01 And 2015-06-30.',
                      xaxis={'title': 'Month'}, yaxis={'title': 'Temperature (F)'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represents the average minimum and maximum temperatures of each '
        'month between 2014-07-01 and 2015-06-30.'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='Average Minimum And Maximum Temperatures Of '
                                            'Each Month Between 2014-07-01 And 2015-06-30',
                                      xaxis={'title': 'Month'},
                                      yaxis={'title': 'Temperature (F)'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'This heat map represents the recorded max temperature of each day of the week and '
        'each week of the month between 2014-07-01 and 2015-06-30.'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_heatmap,
                  'layout': go.Layout(title='Recorded Max Temperature (F) On Days Of The Week '
                                            'Of Each Month Between 2014-07-01 And 2015-06-30',
                                      xaxis={'title': 'Day of Week'},
                                      yaxis={'title': 'Week of Month'})
              }
              )
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-continent', 'value')])
def update_figure(selected_continent):
    filtered_df = df1[df1['Continent'] == selected_continent]

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df = filtered_df.groupby(['NOC'])['Total'].sum().reset_index()
    new_df = new_df.sort_values(by=['Total'], ascending=[False]).head(20)
    data_interactive_barchart = [go.Bar(x=new_df['NOC'], y=new_df['Total'])]
    return {'data': data_interactive_barchart,
            'layout': go.Layout(title='Olympic Medals Won In ' + selected_continent,
                                xaxis={'title': 'National Olympic Committee'},
                                yaxis={'title': 'Number of Medals Won'})}


if __name__ == '__main__':
    app.run_server()