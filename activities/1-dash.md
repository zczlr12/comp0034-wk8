# Plotly Dash version of the activities

## Check the Dash app runs

1. `python src/paralympics_dash/paralympics_dash.py`
2. Go to the URL that is shown in the terminal. By default, this is <http://127.0.0.1:8050>.
3. Stop the app using `CTRL+C`

## Introduction

A callback function is a Python function that is automatically called by Dash whenever an input component's property
changes. For example, when a user makes a choice from a dropdown list or ticks a checkbox.

The basic steps for the callback function are:

- Define the input(s)
- Define the output(s)
- Write the callback function using the `@callback` decorator

With a structure like this:

```python
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'
```

You may need to refer to the [Dash callback documentation](https://dash.plotly.com/basic-callbacks).

You may also define State. This is used where there is a "form"-like pattern to the input. That it, you may want to read
the value of an input component, but only when the user is finished entering all their information in the form rather
than immediately after it changes.

`@callback` decorator rules:

- The decorator tells Dash to call the function for us whenever the value of the "input" component (e.g. a text box)
  changes in order to update the children of the "output" component on the page (e.g. a HTML div).
- You can use any name for the function that is wrapped by the @app.callback decorator. The convention is that the name
  describes the callback output(s).
- You can use any name for the function arguments, but you must use the same names inside the callback function as you
  do in its definition, just like in a regular Python function. The arguments are positional: first the Input items and
  then any State items are given in the same order as in the decorator.
- You must use the same id you gave a Dash component in the app.layout when referring to it as either an input or output
  of the @app.callback decorator.
- The @app.callback decorator needs to be directly above the callback function declaration. If there is a blank line
  between the decorator and the function definition, the callback registration will not be successful.

[callback gotchas](https://dash.plotly.com/callback-gotchas):

- Callbacks require their Inputs, States, and Output to be present in the layout
- Callbacks require all Inputs and States to be rendered on the page
- All callbacks must be defined before the server starts
- Callback definitions don't need to be in lists (in earlier versions they were and some tutorials will show this)

## Implement the line chart dropdown callback

This callback will run when an option is selected in the dropdown selector. It will update the line chart with the
selected type of data.

Add code for the callback after the layout section.

The basic steps for the callback function are:

1. Define the input(s)
2. Define the output(s)
3. Write the callback function using the `@callback` decorator

### Define the Input

The input is the dropdown selector in row_two. Its id is `id="type-dropdown"`. The property of this component
that we want is the value of the selected option, so the parameter `value=`.

The Input looks like this: `Input(component_id='type-dropdown', component_property='value')`

### Output

The output is the line chart in row_three which has `id=line`. The property of this component that we want to update is
the `figure=`.

The output will look like this: `Output(component_id='line', component_property='figure')`

### Callback function

The function will create a new line chart by taking the value from the dropdown and pass this to the function to create
the line chart.

The code structure of the callback then looks like the following. Add code for the callback after the layout section.

```python
from dash import Input, Output


@app.callback(
    Output(component_id='line', component_property='figure'),
    Input(component_id='type-dropdown', component_property='value')
)
def update_line_chart(chart_type):
    figure = line_chart(chart_type)
    return figure
```

Run the app and use the dropdown to change the data type of the chart. The chart should update.

## Implement the checkbox callback for the gender bar chart

The callback should allow users to select whether to display winter or summer for the gender ratio chart.

Use the logic given for the dropdown above to try and work out the code for this yourself.

- Find the id of the checkbox component and the name of the parameter that holds the selected value. A checkbox takes
  multiple values so returns a list []
- Find the id of the bar chart component; the name of the parameter to update is the `figure`
- The function should create a bar chart figure using the `figures/bar_gender_faceted()` function. This function takes
  the checkbox list as a parameter.

The solution is in the week 9 code.

## Update the card when the map marker is hovered over or selected

This technique is called cross-filtering and is covered the Dash
tutorial in [Part 3: Interactive Graphing and Crossfiltering](https://dash.plotly.com/interactive-graphing) in the
section 'Update Graphs on Hover'.

### Input

We want to update the card when the map marker point for the event is hovered over. The input is the hoverData property.
The hoverData object for the scatter_geo points as defined in figures.py returns data that looks like this (I printed
the hover_data to find the structure as it was not clear from the Plotly documentation):

```python
{
    'points': [
        {
            'curveNumber': 0,
            'pointNumber': 14,
            'pointIndex': 14,
            'lon': -43.1729,
            'lat': -22.9068,
            'location': None,
            'hovertext': 'Rio 2016',
            'bbox': {
                'x0': 337.6886998475561,
                'x1': 343.6886998475561,
                'y0': 841.3762682640897,
                'y1': 847.3762682640897
            },
            'customdata': [15]
        }
    ]
}
```

This is a dictionary with list elements within it. The 'customdata' field is within the 'points' list, which is a list
of dictionaries.
First access points in the dictionary. Since the value associated with 'points' is a list, we access its first element
with [0]. Then, we accessed the 'customdata' field within this dictionary. Then since the customdata value is also a
list, we access its first element with [0].
To access it will look something like this: `hoverData['points'][0]['customdata'][0]`

### Output

The output is the stats card.

The card should only be displayed when an event marker is hovered so make a change to the layout to remove the 'card'
variable and replace with a 'Div' with an appropriate id e.g. `id=card`:

```python
row_four = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="map", figure=map)
    ], width=8, align="start"),
    dbc.Col(children=[
        html.Br(),
        # Remove `card` and replace with `html.Div(id='card')`
        # card,
        html.Div(id='card'),
    ], width=4, align="start"),
])
```

The output is now the div with the id of 'card'. The children property of this div will be the stats card layout that is
in the `create_card()` function.

Note: if you look in week 9 for the solution, the `create_card()` function has been moved to the `figures.py` module.

### Callback

The callback looks like this. The code checks that the values are not None to avoid errors.

```python
from dash import Output, Input
from paralympics_dash.figures import create_card


@app.callback(
    Output('card', 'children'),
    Input('map', 'hoverData'),
)
def display_card(hover_data):
    if hover_data is not None:
        event_id = hover_data['points'][0]['customdata'][0]
        if event_id is not None:
            return create_card(event_id)
```

## More on callbacks

These are just a few examples. There are more interactions and examples in the Dash tutorial documentation.

- [Basic callbacks documentation](https://dash.plotly.com/basic-callbacks).
- [Interactive graphing and cross filtering](https://dash.plotly.com/interactive-graphing)
- [Sharing data between callbacks](https://dash.plotly.com/sharing-data-between-callbacks)
- [Advanced callbacks](https://dash.plotly.com/advanced-callbacks

## Examples and other tutorials

- [Dash with sckit-learn models](https://plotly.com/blog/build-python-web-apps-for-scikit-learn-with-plotly-dash/) 2023
  Plotly Dash tutorial
- [CharmingData YouTube](https://www.youtube.com/watch?v=4gDwKYaA6ww) series (note: 3 years old so some syntax will have
  changed)
- [Tutorial to build a stock price tracker](https://www.statworx.com/en/content-hub/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/)
- [Tutorial to build an app that analyses avocado prices (RealPython)](https://realpython.com/python-dash/)
- [Example apps in Dash GitHub](https://github.com/plotly/dash-sample-apps)
- [Curated list of Dash apps and tutorials on GitHub](https://github.com/ucg8j/awesome-dash)
