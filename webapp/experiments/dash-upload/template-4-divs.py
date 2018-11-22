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

buttonStyle = {'width': '60%',
               'height': '60px',
               'lineHeight': '60px',
               'borderWidth': '1px',
               'borderStyle': 'dashed',
               'borderRadius': '5px',
               'textAlign': 'center',
               'margin': '5px'
               }
#----------------------------------------------------------------------------------------------------
def create_eafUploader():

    uploader = dcc.Upload(id='upload-image',
                          children=html.Div([html.A('Select File')]),
                          style=buttonStyle,
                          multiple=False)

    return uploader

#----------------------------------------------------------------------------------------------------
def create_eafDiv():

   style = {'border': '1px solid green',
            'border-radius': '5px',
            'padding': '10px'}

   title = html.H4("Upload EAF file")
   uploader = create_eafUploader()
   assessmentTextBox = html.Textarea()
   button = html.Button("Validate", style=buttonStyle)

   children = [title, uploader, button, assessmentTextBox]

   div = html.Div(children=children, id='eaf-div', className="three columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_soundDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   children = [html.Label('soundDiv'),
               html.Label('sound upload?'),
               html.Label('sound bottom')]

   div = html.Div(children=children, id='sound-div', className="three columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_tierMapDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   children = [html.Label('tierMapDiv'),
               html.Label('tierMap upload'),
               html.Label('tierMap display')]

   div = html.Div(children=children, id='tierMap-div', className="three columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_grammaticalTermsDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   children = [html.Label('grammaticalTermsDiv'),
               html.Label('grammaticalTerms upload'),
               html.Label('grammaticalTerms display')]

   div = html.Div(children=children, id='grammaticalTerms-div', className="three columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
app.layout = html.Div(
    children=[
        create_eafDiv(),
        create_soundDiv(),
        create_tierMapDiv(),
        create_grammaticalTermsDiv()
    ],
    className="row",
    id='outerDiv',
    style={'margin':  '20px',
           'padding': '30px',
           'border': '1px blue solid',
           'border-radius': "5px",
           'height':  '300px',
        })


