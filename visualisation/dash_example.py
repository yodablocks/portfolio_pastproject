# !pip install dash
import dash
from dash import dcc
from dash import html
import numpy as np

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Random Scatter Plot'),

    dcc.Graph(
        id='scatter-plot',
        figure={
            'data': [
                {
                    'x': np.random.rand(100),
                    'y': np.random.rand(100),
                    'mode': 'markers',
                    'marker': {
                        'size': 10,
                        'color': 'rgb(0, 128, 0)',
                        'opacity': 0.7
                    },
                    'type': 'scatter'
                }
            ],
            'layout': {
                'title': 'Random Scatter Plot'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(mode='inline', port=8050, debug=False)
