import dash_bootstrap_components as dbc
import plotly.express as px

from dash import html, dcc, Input, Output, Dash
from dslib.plots import plot

prefix = '/dash/example/'

app = Dash(
    __name__,
    requests_pathname_prefix=prefix
)

data = px.data.iris()


def layout():
    return dbc.Container([
        html.H1('Interactive Histogram!!'),
        html.H5('Select Column:'),
        dbc.Select(
            id='demo-dropdown',
            options=list(map(lambda v: {'label': v}, data.columns)),
            value=data.columns[0]
        ),
        html.Br(),
        html.H5('Altair:'),
        html.Iframe(
            id='plot-iframe',
            style={'width': '100%', 'height': '500px'}
        ),
        html.H5('Plotly:'),
        dcc.Graph(id='plot-area'),
        html.Div(id='dd-output-container')
    ])


app.layout = layout


@app.callback(
    Output('plot-area', 'figure'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return px.histogram(data, x=value, text_auto=True, nbins=30)


@app.callback(
    Output('plot-iframe', 'srcDoc'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return plot().histogram(data, value).to_html()
    # return f'You have selected {value}'

# def shutdown():
#   func = request.environ.get('werkzeug.server.shutdown')
#   if func is None:
#     raise RuntimeError('Not running with the Werkzeug Server')
#   func()


# shutdown()
# app.run_server(port=9009, debug=True)
