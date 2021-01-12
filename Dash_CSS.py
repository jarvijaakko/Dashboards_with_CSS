import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import yfinance as yf
yf.pdr_override()

input_stock = 'VZ'

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

df = pdr.get_data_yahoo('GE', start, end)

trace_close = go.Scatter(
	x = list(df.index),
	y = list(df.Close),
	name='Close',
	line=dict(color = 'red'))

trace_high = go.Scatter(
	x = list(df.index),
	y = list(df.High),
	name='Close',
	line=dict(color = 'red'))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([

	html.Div([
		html.H2('Stock app'),
		html.Img(src = '/assets/Investing.jpeg')
	], className = 'banner'),

		html.Div([
			html.Div([
				html.H3('Column 1'),
				dcc.Graph(
					id = 'graph_close',
					figure = {
						'data' : [trace_close],
						'layout' : {
							'title' : 'Close Graph'
						}
				})
			],className = 'six columns'),

			html.Div([
				html.H3('Column 2'),
				dcc.Graph(
					id = 'graph_high',
					figure = {
						'data' : [trace_close],
						'layout' : {
							'title' : 'High Graph'
						}
					}
				)
			],className = 'six columns'),
	],className = 'row')
])

app.css.append_css({
	'external_url' : 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if(__name__ == '__main__'):
	app.run_server(debug=True)
