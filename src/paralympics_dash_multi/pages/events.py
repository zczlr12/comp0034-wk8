# Page with the map and stats card
from dash import html, register_page, get_asset_url
import dash_bootstrap_components as dbc


# register the page in the app
register_page(__name__, name='Events', title='Events', path="/",)

# Variables that define the two rows and their contents
card = dbc.Card(
    [
        dbc.CardImg(src=get_asset_url('logos/2022_Beijing.jpg'), top=True, style={
            "width": "200px",
            "align": "left"
        }),
        dbc.CardBody(
            [
                html.H4("TownName 2026", className="card-title"),
                html.P(
                    "Highlights of the paralympic event will go here. This will be a sentence or two.",
                    className="card-text",
                ),
                html.P(
                    "Number of athletes: XX",
                    className="card-text",
                ),
                html.P(
                    "Number of events: XX",
                    className="card-text",
                ),
                html.P(
                    "Number of countries: XX",
                    className="card-text",
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

row_one = html.Div(
    dbc.Row([
        dbc.Col([html.H1("Event Details"), html.P(
            "Event details. Select a marker on the map to display the event highlights and summary data.")
                 ], width=12),
    ]),
)

row_two = html.Div(
    dbc.Row([
        dbc.Col(children=[
            html.Img(src=get_asset_url('map-placeholder.png'), className="img-fluid"),
        ], width=8),
        dbc.Col(children=[
            card,
        ], width=4),
    ], align="start")
)

# Add an HTML layout to the Dash app.
# The layout is wrapped in a DBC Container()
layout = dbc.Container([
    row_one,
    row_two,
])
