# Elaborated based on the wonderful tutorial by codebliss (https://youtu.be/Ldp3RmUxtOQ)

import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import requests
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data 
import yfinance as yf
yf.pdr_override()

# Start and end dates
start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

# Function that updates financial market news
def update_news():
	url = 'https://cloud.iexapis.com/stable/stock/market/news/last/5?token=pk_9ed15be4e74b454d8436a2cc86c8254b&period=annual'
	r = requests.get(url)
	json_string = r.json()

	df = pd.DataFrame(json_string)
	df = pd.DataFrame(df[['headline', 'url']])
	return(df)

# Function that generates the financial news table
def generate_html_table(max_rows = 10):
	df = update_news()

	return html.Div(
		[
			html.Div(
				html.Table(
					# Header
					[html.Tr([html.Th()])]
					+
					# Body
					[
						html.Tr(
							[
								html.Td(
									html.A(
										df.iloc[i]['headline'],
										href = df.iloc[i]['url'],
										target = '_blank'
									)
								)
							]
						)
						for i in range(min(len(df), max_rows))
					]
				),
				style = {'height' : '300px', 'overflowY' : 'scroll'},
			),
		],
		style = {'height' : '100%'},)

# Define the external CSS stylesheet to be used
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initiate the app
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# App layout (everything that's visible on the app)
app.layout = html.Div([
	html.Div([
		html.H2('Stock app'),
		html.Img(src = '/assets/Investing.jpeg')
	], className = 'banner'),

	html.Div([
		dcc.Input(id = 'stock-input', value = 'SPY', type = 'text'),
		html.Button(id = 'submit-button', n_clicks = 0, children = 'Submit')
		]),

		html.Div([
			html.Div([
				dcc.Graph(
					id = 'graph_close',
				)
			],className = 'six columns'),

			html.Div([
				html.H3('Market news'),
				generate_html_table()
			],className = 'six columns'),


	],className = 'row')
])

# Append the external CSS stylesheet
app.css.append_css({
	'external_url' : 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# App callback (Stock input search bar)
@app.callback(Output('graph_close', 'figure'),
			 [Input('submit-button', 'n_clicks')],
			 [State('stock-input', 'value')]
			 )

# This function updates the stock figure type (line / candle / bar)
def update_fig(n_clicks, input_value):
	df = pdr.get_data_yahoo(input_value, start, end)

	data = []
	trace_line = go.Scatter(x = list(df.index),
							 y = list(df.Close),
							 name='Close',
							 line=dict(color = 'red')
							 )

	trace_candle = go.Candlestick(x = df.index,
							 open = df.Open,
							 high = df.High,
							 low = df.Low,
							 close = df.Close,
							 visible = False,
							 name='Close',
							 showlegend = False
							 )

	trace_bar = go.Ohlc(x = df.index,
							 open = df.Open,
							 high = df.High,
							 low = df.Low,
							 close = df.Close,
							 visible = False,
							 name='Close',
							 showlegend = False
							 )



	data = [trace_line, trace_candle, trace_bar]

# Update figure drop-down menu
	updatemenus = list([
		dict(
			buttons = list([
				dict(
					args=[{'visible' : [True, False, False]}],
					label = 'Line',
					method = 'update'
				),
				dict(
					args=[{'visible' : [False, True, False]}],
					label = 'Candle',
					method = 'update'
				),
				dict(
					args=[{'visible' : [False, False, True]}],
					label = 'Bar',
					method = 'update'
				)

			]),
			direction = 'down',
			pad = {'r' : 10, 't' : 10},
			x = 0,
			xanchor = 'left',
			y = 1.05,
			yanchor = 'top'
		)
	])

# Final graph layout
	layout = dict(title = input_value,
				  updatemenus = updatemenus,
				  autosize = False,
				  xaxis = dict(
					rangeselector=dict(
			            buttons=list([
			                dict(count=1,
			                     label="1m",
			                     step="month",
			                     stepmode="backward"),
			                dict(count=6,
			                     label="6m",
			                     step="month",
			                     stepmode="backward"),
			                dict(count=1,
			                     label="YTD",
			                     step="year",
			                     stepmode="todate"),
			                dict(count=1,
			                     label="1y",
			                     step="year",
			                     stepmode="backward"),
			                dict(step="all")
            		])
    			),
        rangeslider=dict(
			visible=True
        )
        			)
  	)
# The function returns data and layout for the plotly graph
	return {
		'data': data,
		'layout': layout
	}
		
# This section maintains the code running with debug mode
if(__name__ == '__main__'):
	app.run_server(debug=True)
