import datetime
import base64
import pdb

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = True

app.layout = html.Div([
   html.Div([html.Label("eaf file"), html.Div(html.Label("upload?"), style={'border': "1px solid red"})],
            id='eaf-div',
            style={'margin': '20px;',
                   'padding': '20px',
                   'border': "1px solid blue"}),
   html.Div([html.Label("sound file")],
            id="sound-div",
            style={'margin': '20px;',
                   'padding': '20px',
                   'border': "1px solid green"}),
   html.Div([html.Label("tier guide file")],
            id="tierGuie-div",
            style={'margin': '20px;',
                   'padding': '20px',
                   'border': "1px solid green"}),

   html.Div([html.Label("grammatical terms file")],
            id="grammaticalTerms-div",
            style={'margin': '20px;',
                   'padding': '20px',
                   'border': "1px solid green"}),
    ],
   style={'columnCount': 4,
          'rowCount': 2,
          'height': "800px"}
)


