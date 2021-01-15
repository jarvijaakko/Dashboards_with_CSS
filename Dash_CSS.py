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
import yfinance as yf
yf.pdr_override()

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

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
