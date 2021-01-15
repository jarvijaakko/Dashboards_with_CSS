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

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

def update_news():
	url = 'https://cloud.iexapis.com/stable/stock/market/news/last/5?token=pk_9ed15be4e74b454d8436a2cc86c8254b&period=annual'
	r = requests.get(url)
	json_string = r.json()

	df = pd.DataFrame(json_string)
	df = pd.DataFrame(df[['headline', 'url']])
	return(df)

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
				style = {'height' : '150px', 'overflowY' : 'scroll'},
			),
		],
		style = {'height' : '100%'},)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

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

app.css.append_css({
	'external_url' : 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

@app.callback(Output('graph_close', 'figure'),
			 [Input('submit-button', 'n_clicks')],
			 [State('stock-input', 'value')]
			 )

def update_fig(n_clicks, input_value):
	df = pdr.get_data_yahoo(input_value, start, end)

	data = []
	trace_close = go.Scatter(x = list(df.index),
							 y = list(df.Close),
							 name='Close',
							 line=dict(color = 'red')
							 )

	data.append(trace_close)

	layout = {'title' : input_value}

	return {
		'data': data,
		'layout': layout
	}
		

if(__name__ == '__main__'):
	app.run_server(debug=True)
