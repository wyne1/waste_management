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
import datetime
import random
import flask
from list_locations import list_of_locations

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


data = pd.read_csv("waste.csv")
data['Date/Time'] = pd.to_datetime(data['Date/Time'], format = "%Y-%m-%d")
data.sort_values(by=['Date/Time'], inplace=True)

# table_header = [
#     html.Thead(html.Tr([html.Th(data.columns[0]), html.Th(data.columns[1]), html.Th(data.columns[2]), html.Th(data.columns[3]), html.Th(data.columns[4])]))
# ]
#
# tbody = []
# for i in range(0,4):
#     new = data.iloc[i]
#     tbody.append(html.Tr([html.Td(new[0]), html.Td(new[1]), html.Td(round(new[2],4)), html.Td(round(new[3],4)), html.Td(new[4])]))
#
# table_body = [html.Tbody(tbody)]

# node_dict = {}
# node_data = pd.read_csv("node_data.csv")
# for node in node_data.groupby(node_data['node']):
#     node_dict[node[0]] = node[1].sort_values(by=['Date/Time'])
#     break
#
# # node_dict["Node 0"] = node_dict["Node 0"][:10]
#
# print(node_dict["Node 0"].head())

date = dt.now()

node_data = pd.DataFrame(columns=["Date/Time", "fill_value"])
for i in range(6):
    if i != 0:
        date1 = date + datetime.timedelta(seconds=i*10)
    else:
        date1 = date
    node_data.loc[i] = [str(date1)[:19], round(23/6.7 + i*2.5, 3)]


table_header = [
    html.Thead(html.Tr([html.Th(node_data.columns[0]), html.Th(data.columns[1])]))
]

tbody = []
for i in range(0,5):
    new = node_data.iloc[i]
    tbody.append(html.Tr([html.Td(new[0]), html.Td(new[1])]))

table_body = [html.Tbody(tbody)]


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoiemVlcmFrd3luZSIsImEiOiJjazdyenBsbzAwaW9wM2ZudjFnbmZlNDBhIn0.yVq3jzmrcnc5QeUPCkKnLQ"

app.layout = html.Div(
    children = [
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
        # TOP ROW
        html.Div(
            [
                html.Div(
                    className="one-third column",
                    children = [
                        html.Img(
                            src=app.get_asset_url("logo.png"),
                            id="plotly-image",
                            style={
                                "height": "80px",
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

        # Map Row
        html.Div(
            className = "row flex-display",
            children = [
                # Column for user controls
                html.Div(
                    className = "three columns div-user-controls",
                    children = [
                        html.H2("Waste Management Demo"),
                        html.P(
                            """Select different days using the date picker or by selecting
                            different time frames on the histogram."""
                        ),
                        #DATE
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
                        ),
                    ],
                ),
                # Column for Map controls
                html.Div(
                    className="seven columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                    ],
                ),
                # Column for Overall and History
                html.Div(
                    className = "three columns div-pie-chart",
                    id = "pie",
                    children = [
                        html.Div(
                            className="row",
                            children= [
                                html.H4("Containers Fill Level"),
                                dcc.Graph(id="pie-chart")
                            ],
                        ),
                    ],
                ),
            ]
        ),
        # Node Row
        html.Div(
            className = "row flex-display",
            children = [
                # Column for user controls
                html.Div(
                    className = "three columns div-user-controls",
                    children = [
                        html.H2("Node History"),
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
                    ],
                ),
                # Column for Map controls
                html.Div(
                    className= "seven columns div-node-charts bg-grey",
                    children = [
                        dcc.Graph(id="node-chart")
                    ],
                ),
                # Column for Overall and History
                html.Div(
                    className = "three columns div-pie-chart",
                    children = [
                        html.Div(
                            children= [
                                html.H4("Latest Activity"),
                                dbc.Table(
                                    table_header + table_body,
                                    bordered=True,
                                    dark = True,
                                    hover= True,
                                    striped=True,
                                    size = 'md',
                                    responsive = True,
                                    id = "table"
                                ),
                            ],
                        ),
                    ],
                ),
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
    zoom =12

    latInitial = 31.485849
    lonInitial = 74.327748
    bearing = 0

    date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    monthPicked = date_picked.month - 4
    dayPicked = date_picked.day - 1

    return go.Figure(
        data=[
            # Plot of important locations on the map
            Scattermapbox(
                lat=[list_of_locations[i]["lat"] for i in list_of_locations],
                lon=[list_of_locations[i]["lon"] for i in list_of_locations],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=[i for i in list_of_locations],

                marker=dict(size=12, color="#7BEC97"),
            ),
            Scattermapbox(
                lat=[list_of_locations['Node 0']["lat"]],
                lon=[list_of_locations['Node 0']["lon"]],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=["Node 0"],

                marker=dict(size=12, color="#FF7981"),
            ),
        ],
        layout=Layout(
            # height = 350,
            # width = 1075,
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
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
    Output("pie-chart", "figure"),
    [
        Input("date-picker", "date"),
    ],
)

def update_pie(datePicked):
    labels = ["Empty", "Full", "Normal", "Overflow"]
    waste_data = [59,312,136,131]
    colors = ['#E6F69D', '#FEAE65', '#64C2A6','#F66D44']

    ann1 = dict(font=dict(size=20),
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
                hoverinfo='label+percent',
                textinfo='value',
                textfont=dict(size=16),
                name = 'Waste',
                marker=dict(
                    colors=colors,
                    # line=dict(color='#1E1E1E', width=1)
                ),
            ),
        ],

        layout=Layout(
            height = 320,
            width = 320,
            autosize=True,
            margin=go.layout.Margin(l=30, r=30, t=0, b=0),
            # annotations = [ann1],
            legend = dict(
                # x=0,
                # y=1,
                traceorder="normal",
                font=dict(
                family="sans-serif",
                size=12,
                color="white"
                ),
                # bgcolor="LightSteelBlue",
                # bordercolor="Black",
                # borderwidth=2
            ),
            showlegend=True,
            plot_bgcolor = "#1E1E1E",
            paper_bgcolor = "#1E1E1E",
            # title="Fill Levels"
        ),
    )



@app.callback(
    Output("node-chart", "figure"),
    [
        Input("interval-component", "n_intervals"),
    ],
)
def node_graph(n_intervals):
    global fill_db, node_data

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
                height = 350,
                width = 1075,
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
        old_date = pd.to_datetime(node_data[-1:]["Date/Time"].values)
        new_date = old_date + datetime.timedelta(seconds=10)
        node_data = node_data.append(pd.DataFrame({'Date/Time': new_date, 'fill_value': val}), ignore_index=True)

        print(node_data)

        fill_db["updated"] = False

    node_0 = node_data.copy()
    node_0['Date/Time'] = pd.to_datetime(node_0['Date/Time'])
    node_0.set_index(node_0['Date/Time'], inplace=True)

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
            height = 350,
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




fill_db = {
    "value": None,
    "updated": False
}

@server.route("/waste/<node>/data", methods=['POST'])
def waste_collection(node):
    global fill_db
    print("POST from Node:", node)
    if flask.request.method == "POST":
        data = flask.request.get_json()
        print(data)
        fill_db["value"] = data["fill_level"]
        fill_db["updated"] = True

        print(fill_db)
    return """SUCCESS"""

if __name__ == "__main__":
    app.run_server(host = "0.0.0.0" ,debug=True, port = 5000, threaded=False)
