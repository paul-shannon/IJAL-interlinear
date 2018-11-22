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
def createUploadWidget(id, prompt):

    widget = dcc.Upload(
        id=id,
        children=html.A(prompt),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        })

    div = html.Div(widget)

    return div

#----------------------------------------------------------------------------------------------------
def create_eafDiv():

   style = {'border': '1px solid green',
            'border-radius': '5px',
            'padding': '10px'}

   children = [html.Label('eaf file'),
               html.Label('upload?')]

   div = html.Div(children=children, id='eaf-div', style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_soundDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   children = [html.Label('sound file'),
               html.Label('upload?')]

   div = html.Div(children=children, id='sound-div', style=style)

   return div

#----------------------------------------------------------------------------------------------------
app.layout = html.Div(
    children=[
        create_eafDiv(),
        create_soundDiv()
    ],
    id='outerDiv',
    style={'columnCount': 2,
           'margin':  '20px',
           'padding': '30px',
           'height':  '200px',
           'border': '1px blue solid',
           'border-radius': "5px"}
)


