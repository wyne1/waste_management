import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import math
from random import randrange, randint
import random

from plotly import graph_objs as go
from plotly.graph_objs import *
import plotly.express as px
import dash_table
import flask
from flask import request
import datetime
from datetime import datetime as dt
from list_locations import list_of_locations

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoiemVlcmFrd3luZSIsImEiOiJjazdyenBsbzAwaW9wM2ZudjFnbmZlNDBhIn0.yVq3jzmrcnc5QeUPCkKnLQ"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

date = dt.now()

data = pd.read_csv("waste.csv")
data['Date/Time'] = pd.to_datetime(data['Date/Time'], format = "%Y-%m-%d")
data.sort_values(by=['Date/Time'], inplace=True)

tab = data.drop(['lat','lon'], axis=1)

node_data = pd.DataFrame(columns=["Date/Time", "fill_value"])
for i in range(6):
    if i != 0:
        date1 = date + datetime.timedelta(seconds=i*10)
    else:
        date1 = date
    node_data.loc[i] = [str(date1)[:19], round(23/6.7 + i*2.5, 3)]

alert_toast = dbc.Toast(
            "SOMEONE IS TRYING TO STEAL THE DEVICE",
            id="alert-popup",
            header="    THEFT ALERT!   ",
            is_open=False,
            dismissable=True,
            icon="danger",
            duration=9000,
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 20, "right": 800, "width": 800},
        )

    

app.layout = dbc.Container([
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
    ),
    html.Div(children=[alert_toast]),
    #HEADER CONTAINER
    dbc.Container([dbc.Row([
        dbc.Col([
            html.Img(src=app.get_asset_url('waste-logo2.png'))
        ], width = 6, align="center", style={"align": "center"}),
        dbc.Col([
            html.A(
                html.Button("GitHub Page", id="learn-more-button"),
                href="https://github.com/abdylan/audioAnn_GUI",
				)
        ], width = 6, align="center"),
    ], justify='end', id="header")], fluid = True),
    
    html.Br(),
    
    #BODY CONTAINER
    dbc.Container([
        
        #FIRST ROW
        dbc.Row([
            dbc.Col([
                html.H4("Waste Management Demo"),
                html.P(
                    """Select different days using the date picker or by selecting
                    different time frames on the histogram."""
                ),
                html.Div(
                className="div-for-dropdown",
                children=[
                    dcc.DatePickerSingle(
                        id="date-picker",
                        min_date_allowed=dt(2018, 1, 1),
                        max_date_allowed=dt(2018, 9, 30),
                        initial_visible_month=dt(2014, 4, 1),
                        date=dt(2018, 1, 1).date(),
                        display_format="MMMM D, YYYY",
                        style={"border": "0px solid black"},
                    ),
                ],
            )], width=3, id='date-picker-col'),
            
            dbc.Col([
                html.Div(className="div-for-charts bg-grey",
                    children=[dcc.Graph(id="map-graph")])
            ], width=6, align='center'),
            
            dbc.Col([
                html.H4("Overview - Peshawar Waste"),
                dcc.Graph(id="pie-chart")
            ], width=3, align='center'),
        ], justify='center'),

        #SECOND ROW
        dbc.Row([
            dbc.Col([
                html.H3("Location History"),
                html.P(
                    """Select a node to view history of fill levels of that particular node"""
                ),
                #DATE
                html.Div(
                    className="div-for-dropdown",
                    children=[
                        dcc.Dropdown(
                            id="node-dropdown",
                            options=[
                                {"label": i, "value": i}
                                for i in list_of_locations
                            ],
                            value = 'Node 0',
                            placeholder="Select a Node",
                        ),
                    ],
                ),
            ], width=3),
            
            dbc.Col([
                dcc.Graph(id="node-chart"),
            ], width=6),
            
            dbc.Col([
                html.H4("Waste Events"),
            dash_table.DataTable(id='table',
            columns=[{"name": i, "id": i} for i in tab.columns],
            data=tab.to_dict('records'),
            style_header={
                'fontWeight': 'bold',
                # 'border': 'thin lightgrey solid',
                'backgroundColor': 'rgb(89, 195, 106)',
                'color': 'white',
                'textAlign': 'center',
            },
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'left',
                'width': '90px',
                'minWidth': '90px',
                'maxWidth': '90px',
                 
                # 'whiteSpace': 'no-wrap',
                # 'overflow': 'hidden',
                # 'textOverflow': 'ellipsis',
                # 'backgroundColor': 'Rgb(255,255,255)'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
                {
                    'if': {'column_id': 'country'},
                    'backgroundColor': 'rgb(255, 255, 255)',
                    'color': 'black',
                    'fontWeight': 'bold',
                    'textAlign': 'center'
                }
            ],
            fixed_rows={'headers': True, 'data': 0}
            
            )
            ], width=3),
        ], justify='center'),

        


    ], fluid = True, id="header2")

], 

fluid = True)

@app.callback(
    Output("node-chart", "figure"),
    [
        Input("interval-component", "n_intervals"),
    ],
)
def node_graph(n_intervals):
    global fill_db, node_data
    container_depth = 450  # in cm

    # print("POLLING ------->", n_intervals, fill_db)
    if n_intervals <=1:
        try:
            node_0 = node_data.copy()
            print(node_0.columns)
            node_0['Date/Time'] = pd.to_datetime(node_0['Date/Time'])
            node_0.set_index(node_0['Date/Time'], inplace=True)
        except Exception as e:
            print("EXCEPTION HERE: ", e)



        return go.Figure(
            data=[

                Scatter(
                    x = node_0.index,
                    y = node_0['fill_value'],
                    line = dict(
                        color = "#7BEC97",
                        width = 2
                    ),
                ),
                # Plot of important locations on the map
            ],

            layout=Layout(
                height = 450,
                # width = 1075,
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='#ffffff',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='#ffffff',
                    ),
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    linecolor='#ffffff',
                    showticklabels=True,
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='#ffffff',
                    ),
                ),
                autosize=True,
                margin=dict(
                    autoexpand=False,
                    l=50,
                    r=50,
                    t=50,
                    # b=150
                ),
                showlegend=False,
                plot_bgcolor='#343332',
                paper_bgcolor = "#343332"
            )

        )

    if fill_db["updated"] == True:
        print("IN DF UPDATE")
        val = fill_db["value"]
        # fill_percent = (val/container_depth) * 100
        fill_percent = ((container_depth - val) / container_depth) * 100
        
        # if fill_percent != 100:
        #     fill_percent = 100 - fill_percent
        print(">> Fill %:", fill_percent)
        
        old_date = pd.to_datetime(node_data[-1:]["Date/Time"].values)
        new_date = old_date + datetime.timedelta(seconds=10)
        node_data = node_data.append(pd.DataFrame({'Date/Time': new_date, 'fill_value': fill_percent}), ignore_index=True)

        print("New Node Data Shape: ", node_data.shape)

        fill_db["updated"] = False

    node_0 = node_data.copy()
    node_0['Date/Time'] = pd.to_datetime(node_0['Date/Time'])
    node_0.set_index(node_0['Date/Time'], inplace=True)

    fig = go.Figure(
        data=[
            Scatter(
                x = node_0.index,
                y = node_0['fill_value'],
                line = dict(
                    color = "#7BEC97",
                    width = 2
                ),
            ),
            # Plot of important locations on the map
        ],

        layout=Layout(
            height = 400,
            # width = 1075,
            title=dict(text ='University Road Sensor 2   |   Depth: 4.5 meter',
                            font =dict(family='Sherif',
                               size=18,
                               color = 'white')
            ),
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='#ffffff',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='#ffffff',
                ),
            ),
            yaxis=dict(
            	title=dict(text ='Fill %',
                            font =dict(family='Sherif',
                               size=14,
                               color = 'white')
            	),
                showgrid=False,
                zeroline=False,
                showline=False,
                linecolor='#ffffff',
                showticklabels=True,
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='#ffffff',
                ),
            ),
            autosize=True,
            margin=dict(
                autoexpand=False,
                l=50,
                r=50,
                t=50,
                # b=150
            ),
            showlegend=False,
            plot_bgcolor='#343332',
            paper_bgcolor = "#343332"
        )

    )
    fig.add_trace(Scatter(x=node_0.index, y=[95.0]*len(node_0.index), name='ALERT',
    	line=dict(color='firebrick', width=2, dash='dash')
    	))
    return fig



@app.callback(
    Output("pie-chart", "figure"),
    [
        Input("date-picker", "date"),
    ],
)

def update_pie(datePicked):
    labels = ["Empty", "Full", "Normal", "Overflow"]
    waste_data = [59,312,136,131]
    colors = ['#E6F69D', '#FEAE65', '#64C2A6','#F66D44']

    ann1 = dict(font=dict(size=15),
                showarrow=False,
                text='Waste',
                # Specify text position (place text in a hole of pie)
                )

    return go.Figure(
        data=[
            # Plot of important locations on the map
            Pie(
                labels=labels,
                values=waste_data,
                hoverinfo='percent',
                textinfo='label+value',
                textfont=dict(size=16),
                name = 'Waste',
                hole = 0.4,
                marker=dict(
                    colors=colors,
                    # line=dict(color='#1E1E1E', width=1)
                ),
            ),
        ],

        layout=Layout(
            height = 350,
            width = 350,
            autosize=True,
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
            # annotations = [ann1],
            legend = dict(

                traceorder="normal",
                font=dict(
                family="sans-serif",
                size=10,
                color="white"
                ),
                # bgcolor="LightSteelBlue",
                # bordercolor="Black",
                # borderwidth=2
            ),
            showlegend=True,
            plot_bgcolor = "#1B1B1B",
            paper_bgcolor = "#1B1B1B",
            # title="Fill Levels"
        ),
    )



@app.callback(
    Output("map-graph", "figure"),
    [
        Input("date-picker", "date"),
    ],
)
def update_graph(datePicked):
    zoom =14

    latInitial = 34.007430
    lonInitial = 71.553375
    bearing = 0

    date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    monthPicked = date_picked.month - 4
    dayPicked = date_picked.day - 1

    return go.Figure(
        data=[
            # Plot of important locations on the map
            Scattermapbox(
                lat=[list_of_locations['Node {}'.format(i)]['lat'] for i in range(0, 11)],
                lon=[list_of_locations['Node {}'.format(i)]['lon'] for i in range(0, 11)],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=['Node {}'.format(i) for i in range(0,11)],

                marker=dict(size=12, color="#F66D44"),
            ),

            Scattermapbox(
                lat=[list_of_locations['Node {}'.format(i)]['lat'] for i in range(11, 35)],
                lon=[list_of_locations['Node {}'.format(i)]['lon'] for i in range(11, 35)],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=['Node {}'.format(i) for i in range(11,35)],

                marker=dict(size=12, color="#59C36A"),
            ),

            Scattermapbox(
                lat=[list_of_locations['Node {}'.format(i)]['lat'] for i in range(35, 45)],
                lon=[list_of_locations['Node {}'.format(i)]['lon'] for i in range(35, 45)],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=['Node {}'.format(i) for i in range(35,45)],

                marker=dict(size=12, color="#FEAE65"),
            ),

            Scattermapbox(
                lat=[list_of_locations['Node {}'.format(i)]['lat'] for i in range(45, 51)],
                lon=[list_of_locations['Node {}'.format(i)]['lon'] for i in range(45, 51)],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=['Node {}'.format(i) for i in range(45,51)],

                marker=dict(size=12, color="#E6F69D"),
            ),
        ],
        layout=Layout(
            height = 500,
            # width = 1075,
            autosize=True,
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
                style="dark", #"satellite-streets", #"""'light', 'basic', 'outdoors', 'satellite', or 'satellite-streets' """
                bearing=bearing,
                zoom=zoom,
            ),
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

@app.callback(
    Output('alert-popup', 'is_open'),
    [
        Input('interval-component', 'n_intervals'),
    ]
)
def theft_alert(n_intervals):
    global theft_dict
    
    if theft_dict['alert'] == True:
        print(theft_dict)
        print("ALERT IS TRUE")
        theft_dict['alert'] = False

        return True
    else:
        return False

theft_dict = {
    "alert": False
}

fill_db = {
    "value": None,
    "updated": False
}

@server.route('/waste_node/<num>/theft', methods=['GET'])
def theft_alert(num):
    global theft_dict
    print("THEFT API")
    if request.method == "GET":
        theft_dict['alert'] = True
        print("  ****    THEFT !!  *****")
        return """THEFT ALERT API HIT"""
    return """Please use GET Method"""

@server.route("/waste/<node>/data/", methods=['POST'])
def waste_collection(node):
    global fill_db
    print("POST from Node:", node)
    if request.method == "POST":
        data = flask.request.get_json()
        print(data)
        fill_db["value"] = data["fill_level"]
        fill_db["updated"] = True

        print(fill_db)
    return """SUCCESS"""


latitude, longitude = 0.00, 0.00
# latitude, longitude = 34.003395, 71.518186
@server.route('/waste_node/<num>', methods=['POST'])
def waste_data(num):
    if request.method == "POST":
        global fill_db
        global latitude; global longitude
        
        node_ip = request.remote_addr
        print("Got New POST from Node: {} -->> IP: {}".format(num, node_ip))
        data = request.get_json(force=True)
        print("DATA:", data)
        temp_latitude = data.get('latitude', None)
        
        if (temp_latitude != 0.00) & (temp_latitude is not None):
            latitude, longitude = data['latitude'], data['longitude']
        latitude, longitude = 34.003395, 71.518186  ## WSSP Location
        
        fill_db["value"] = data["fill_level"]
        fill_db["updated"] = True
        
        print("*******************       GOT New HIT      *******************")
        print(data)
        print("[INFO] Node: {}   |   Location: University Road Container 1".format(num))
        print("[1] Fill-Level: ", data['fill_level'])
        print("[2] Latitude: ", latitude)
        print("[3] Longitude: ", longitude)
    return """SUCCESS"""




if __name__ == '__main__':
	# app.run_server(debug=True)
    app.run_server(host = "0.0.0.0" , debug=True, port=5555, threaded=False)