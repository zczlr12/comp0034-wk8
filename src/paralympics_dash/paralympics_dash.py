""" Code as at the end of week 7 activities """
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from figures import line_chart, bar_gender

external_stylesheets = [dbc.themes.BOOTSTRAP]
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Create the Plotly Express line chart object, e.g. to show number of sports
line = line_chart("sports")

# Create the Plotly Express stacked bar chart object to show gender split of participants for the type of event
bar = bar_gender("winter")

# Layout variables
card = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('logos/2022_Beijing.jpg'), top=True, style={
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

dropdown = dbc.Select(
    id="type-dropdown",
    options=[
        {"label": "Events", "value": "events"},
        {"label": "Sports", "value": "sports"},
        {"label": "Countries", "value": "countries"},
        {"label": "Athletes", "value": "participants"},
    ],
    value="events"
)

checklist = dbc.Checklist(
    options=[
        {"label": "Summer", "value": "summer"},
        {"label": "Winter", "value": "winter"},
    ],
    value=["summer"],
    id="checklist-input",
    inline=True,
)

row_one = html.Div(
    dbc.Row([
        dbc.Col([html.H1("Paralympics Dashboard"), html.P(
            "Use the charts to help you answer the questions.")
                 ], width=12),
    ]),
)

row_two = dbc.Row([
        dbc.Col(children=[
            dropdown
        ], width=2),
        dbc.Col(children=[
            checklist,
        ], width={"size": 2, "offset": 4}),
    ], align="start")

row_three = dbc.Row([
        dbc.Col(children=[
            dcc.Graph(id="line", figure=line),
        ], width=6),
        dbc.Col(children=[
            dcc.Graph(id="bar", figure=bar),
            # html.Img(src=app.get_asset_url('bar-chart-placeholder.png'), className="img-fluid"),
        ], width=6),
    ], align="start")

row_four = dbc.Row([
        dbc.Col(children=[
            html.Img(src=app.get_asset_url('map-placeholder.png'), className="img-fluid"),
        ], width=8),
        dbc.Col(children=[
            card,
        ], width=4),
    ], align="start")

app.layout = dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four,
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)
    # Runs on port 8050 by default, this just shows the parameter to use to change to another port if needed
