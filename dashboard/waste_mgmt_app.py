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

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


data = pd.read_csv("waste.csv")
data['Date/Time'] = pd.to_datetime(data['Date/Time'], format = "%Y-%m-%d")
data.sort_values(by=['Date/Time'], inplace=True)

table_header = [
    html.Thead(html.Tr([html.Th(data.columns[0]), html.Th(data.columns[1]), html.Th(data.columns[2]), html.Th(data.columns[3]), html.Th(data.columns[4])]))
]

tbody = []
for i in range(0,5):
    new = data.iloc[i]
    tbody.append(html.Tr([html.Td(new[0]), html.Td(new[1]), html.Td(round(new[2],4)), html.Td(round(new[3],4)), html.Td(new[4])]))


# table_header = [
#     html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
# ]

table_body = [html.Tbody(tbody)]
# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoiemVlcmFrd3luZSIsImEiOiJjazdyenBsbzAwaW9wM2ZudjFnbmZlNDBhIn0.yVq3jzmrcnc5QeUPCkKnLQ"

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
                                html.Br(),html.Br(),
                                dcc.Dropdown(
                                    id="node-dropdown",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in list_of_locations
                                    ],
                                    placeholder="Select a Node",
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
                        html.Div(
                            className="row",
                            children= [
                                html.H4("Latest Activity"),
                                dbc.Table(
                                    table_header + table_body,
                                    bordered=True,
                                    dark = True,
                                    hover= True,
                                    striped=True,
                                    size = 'sm',
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
    zoom = 11

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
        ],
        layout=Layout(
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
#
# @app.callback(
#     Output("pie-chart2", "figure"),
#     [
#         Input("date-picker", "date"),
#     ],
# )
#
# def update_pie(datePicked):
#     labels = ["Empty", "Full", "Normal", "Overflow"]
#     waste_data = [59,312,136,131]
#     colors = ['#E6F69D', '#FEAE65', '#64C2A6','#F66D44']
#
#     ann1 = dict(font=dict(size=20),
#                 showarrow=False,
#                 text='Waste',
#                 # Specify text position (place text in a hole of pie)
#                 )
#
#     return go.Figure(
#         data=[
#             # Plot of important locations on the map
#             Pie(
#                 labels=labels,
#                 values=waste_data,
#                 hoverinfo='label+percent',
#                 textinfo='value',
#                 textfont=dict(size=16),
#                 name = 'Waste',
#                 marker=dict(
#                     colors=colors,
#                     # line=dict(color='#1E1E1E', width=1)
#                     ),
#             ),
#         ],
#
#         layout=Layout(
#             height = 320,
#             width = 320,
#             autosize=True,
#             margin=go.layout.Margin(l=50, r=50, t=0, b=0),
#             # annotations = [ann1],
#             legend = dict(
#                 # x=0,
#                 # y=1,
#                 traceorder="normal",
#                 font=dict(
#                 family="sans-serif",
#                 size=12,
#                 color="white"
#                 ),
#                 # bgcolor="LightSteelBlue",
#                 # bordercolor="Black",
#                 # borderwidth=2
#             ),
#             showlegend=False,
#             plot_bgcolor = "#1E1E1E",
#             paper_bgcolor = "#1E1E1E",
#             # title="Fill Levels"
#         ),
#     )

if __name__ == "__main__":
    app.run_server(debug=True, port = 5000)
