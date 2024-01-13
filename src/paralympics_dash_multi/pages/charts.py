# Line and bar charts page
from dash import html, register_page, get_asset_url
import dash_bootstrap_components as dbc

# register the page in the app
register_page(__name__, name="Charts", title="Charts")

# Variables that define the three rows and their contents
dropdown = dbc.Select(
    id="type-dropdown",  # id uniquely identifies the element, will be needed later
    options=[
        {"label": "Events", "value": "events"},
        # The value is in the format of the column heading in the data
        {"label": "Sports", "value": "sports"},
        {"label": "Countries", "value": "countries"},
        {"label": "Athletes", "value": "participants"},
    ],
    value="events"  # The default selection
)

checklist = dbc.Checklist(
    options=[
        {"label": "Summer", "value": "summer"},
        {"label": "Winter", "value": "winter"},
    ],
    value=["summer"],  # Values is a list as you can select both winter and summer
    id="checklist-input",
)

row_one = html.Div(
    dbc.Row([
        dbc.Col([html.H1("Charts"), html.P(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent congue luctus elit nec gravida. Fusce "
            "efficitur posuere metus posuere malesuada. ")
                 ], width=12),
    ]),
)

row_two = html.Div(
    dbc.Row([
        dbc.Col(children=[
            dropdown
        ], width=2),
        dbc.Col(children=[
            html.Img(src=get_asset_url('line-chart-placeholder.png'), className="img-fluid"),
        ], width=4),
        dbc.Col(children=[
            # see checklist variable defined earlier
            checklist,
        ], width=2),
        dbc.Col(children=[
            html.Img(src=get_asset_url('bar-chart-placeholder.png'), className="img-fluid"),
        ], width=4),
    ], align="start")
)

# Add an HTML layout to the Dash app.
# The layout is wrapped in a DBC Container()
layout = dbc.Container([
    row_one,
    row_two,
])
