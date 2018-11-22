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

#----------------------------------------------------------------------------------------------------
def create_eafDiv():

   style = {'border': '1px solid green',
            'border-radius': '5px',
            'padding': '10px'}

   kid = html.H4("label in div")

   divTop = html.Div([html.H4('eafDdiv'), kid])
   divBottom = html.Div(html.H4('eaf upload?'))
   children = [divTop, divBottom]

   div = html.Div(children=children, id='eaf-div', className="six columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_soundDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   children = [html.Label('soundDiv'),
               html.Label('sound upload?'),
               html.Label('sound bottom')]

   div = html.Div(children=children, id='sound-div', className="six columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
app.layout = html.Div(
    children=[
        create_eafDiv(),
        create_soundDiv()
    ],
    className="row",
    id='outerDiv',
    style={'margin':  '20px',
           'padding': '30px',
           'border': '1px blue solid',
           'border-radius': "5px",
           'height':  '300px',
        })


