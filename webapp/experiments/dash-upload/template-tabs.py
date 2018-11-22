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

buttonStyle = {'width': '100px',
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
def create_eafUploaderTab():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   textArea = html.Textarea(placeholder='xml validation results go here',
                            style={'width': 1000,
                                   'height': 400})

   children = [create_eafUploader(),
               html.Label("Filename: "),
               html.Button("Validate XML"),
               textArea
               ]

   div = html.Div(children=children, id='eafUploaderDiv') #, style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_masterDiv():

   style = {'border': '1px solid green',
            'border-radius': '5px',
            'padding': '10px'}

   title = html.H4("Status")
   eafStatus = html.Label("EAF: ")
   soundStatus = html.Label("Sound: ")
   tierMapStatus = html.Label("Tier map: ")
   grammaticalTermsStatus = html.Label("Grammatical terms: ")
   lineBreak = html.Br()
   button = html.Button("Run", style=buttonStyle)

   children = [title, eafStatus, soundStatus, tierMapStatus, grammaticalTermsStatus, lineBreak, button]

   div = html.Div(children=children, id='master-div', className="three columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_uploadsDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   tabs = dcc.Tabs(id="tabs-example", value='tab-1-example',
                   children=[dcc.Tab(label='EAF', children=create_eafUploaderTab()),
                             dcc.Tab(label='Sound', value='tab-2-example'),
                             dcc.Tab(label='Tiers', value='tab-3-example'),
                             dcc.Tab(label='Grammatical Terms', value='tab-4-example')
                   ]),

   children = tabs;
   div = html.Div(children=children, id='uploads-div', className="nine columns") # , style=style)

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
        create_masterDiv(),
        create_uploadsDiv()
    ],
    className="row",
    id='outerDiv',
    style={'margin':  '10px',
           'padding': '20px',
           #'border': '1px blue solid',
           'border-radius': "5px",
           'height':  '300px',
        })


