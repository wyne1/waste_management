import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

from list_locations import list_of_locations
for i
app = dash.Dash(
	__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoiemVlcmFrd3luZSIsImEiOiJjazdyenBsbzAwaW9wM2ZudjFnbmZlNDBhIn0.yVq3jzmrcnc5QeUPCkKnLQ"

"""
1 - 33.731210 73.036416
2 - 33.731452, 73.036368
3 - 33.731668, 73.036330
4 - 33.732054, 73.036191
5 - 33.732324, 73.036164
6 - 33.732297, 73.035801
7 - 33.732408, 73.035308
8 - 33.732493, 73.035042
9 - 33.732538, 73.034908
10 - 33.732578, 73.034755
"""


labels = ["Empty", "Full", "Normal", "Overflow"]
waste_data = [59,312,136,131]
colors = ['#29ECEC', '#EC7029', '#5E6B6B','#B6E44C']


trace1 = go.Pie(labels=labels, values=waste_data,
			   hoverinfo='label+percent', textinfo='value',
			   textfont=dict(size=20),
			   name = 'Waste',
			   # Create hole in pie where we will place day name
			   hole = 0.2,
			   marker=dict(colors=colors,
						   line=dict(color='#000000', width=2)
						   ),
			   # Set where first plot will be plotted
			   domain=dict(x=[0,0.5])
	   )

ann1 = dict(font=dict(size=20),
			showarrow=False,
			text='Waste',
			# Specify text position (place text in a hole of pie)
			x=0.23,
			y=0.5
			)

layout = go.Layout(title ='Pie chart subplots',
				   annotations=[ann1],
				   # Hide legend if you want
				   #showlegend=False
				   )

app.layout = html.Div(
	children = [
		# TOP ROW
		html.Div(
			[
				html.Div(
					className="one-third column",
					children = [
						html.Img(
							src=app.get_asset_url("dash-logo-new.png"),
							id="plotly-image",
							style={
								"height": "50px",
								"width": "auto",
								"margin-bottom": "25px",
							},
						)
					],
				),

				html.Div(
					className="one-half column",
					id="title",
					children = [
						html.Div(
							[
								html.H3(
									"Smart Waste Management",
									style={"margin-bottom": "0px"},
								),
								html.H5(
									"Smart Containers", style={"margin-top": "0px"}
								),
							]
						)
					],
				),
				html.Div(
					[
						html.A(
							html.Button("GitHub Page", id="learn-more-button"),
							href="https://github.com/abdylan/audioAnn_GUI",
						)
					],
					className="one-third column",
					id="button",
				),
			],
			id="header",
			className="row flex-display",
			style={"margin-bottom": "25px"},
		),

		# Middle Data Low
		html.Div(
			className = "row",
			children = [
				html.Div(
					className="div-for-dropdown",
					children=[
						dcc.DatePickerSingle(
							id="date-picker",
							min_date_allowed=dt(2014, 4, 1),
							max_date_allowed=dt(2014, 9, 30),
							initial_visible_month=dt(2014, 4, 1),
							date=dt(2014, 4, 1).date(),
							display_format="MMMM D, YYYY",
							style={"border": "0px solid black"},
						)
					],
				),

				dcc.Graph(id="map-graph"),

			]
		)
	]
)

@app.callback(
	Output("map-graph", "figure"),
	[
		Input("date-picker", "date"),
	],
)


def update_graph(datePicked):
	return go.Figure(
		data=[
			# Plot of important locations on the map
			Pie(labels=labels, values=waste_data,
						   hoverinfo='label+percent', textinfo='value',
						   textfont=dict(size=20),
						   name = 'Waste',
						   # Create hole in pie where we will place day name
						   hole = 0.2,
						   marker=dict(colors=colors,
									   line=dict(color='#000000', width=2)
									   ),
						   # Set where first plot will be plotted
						   domain=dict(x=[0,0.5])
			),
		],

		layout=Layout(
			height = 40%,
			autosize=True,
			# margin=go.layout.Margin(l=0, r=35, t=0, b=0),
			annotations = [ann1],
			showlegend=True,
			plot_bgcolor = "#1E1E1E",
			paper_bgcolor = "#1E1E1E",
			updatemenus=[
				dict(
					buttons=(
						[
							dict(
								args=[
									{
										"mapbox.zoom": 12,
										"mapbox.center.lon": "-73.991251",
										"mapbox.center.lat": "40.7272",
										"mapbox.bearing": 0,
										"mapbox.style": "dark",
									}
								],
								label="Reset Zoom",
								method="relayout",
							)
						]
					),
					direction="left",
					pad={"r": 0, "t": 0, "b": 0, "l": 0},
					showactive=False,
					type="buttons",
					x=0.45,
					y=0.02,
					xanchor="left",
					yanchor="bottom",
					bgcolor="#323130",
					borderwidth=1,
					bordercolor="#6d6d6d",
					font=dict(color="#FFFFFF"),
				)
			],
		),
	)

if __name__ == "__main__":
	app.run_server(debug=True, port = 5000)
