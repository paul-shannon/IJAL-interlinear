import datetime
import base64
import pdb
import xmlschema
import os
import scipy.io.wavfile as wavfile
import dash
import pandas as pd
import dash_table
import yaml
import io

# schema = xmlschema.XMLSchema('http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
# schema.is_valid('../ijal_interlinear/testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf')
# schema.validate('../ijal_interlinear/testData/harryMosesDaylight/daylight_1_4.eaf')
#   xmlschema.validators.exceptions.XMLSchemaValidationError: failed validating <Element 'ANNOTATION_DOCUMENT' at
#        0x10e6e5688> with XsdKeyref(name='tierNameRef', refer='tierNameKey'):
#   Reason: Key 'tierNameRef' with value ('todo',) not found for identity constraint of element 'ANNOTATION_DOCUMENT'.

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

UPLOAD_DIRECTORY = "./UPLOADS"

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = True

buttonStyle = {'width': '140px',
               'height': '60px',
               'color': 'gray',
               'fontFamily': 'HelveticaNeue',
               'margin-right': 10,
               'lineHeight': '60px',
               'borderWidth': '1px',
               'borderStyle': 'solid',
               'borderRadius': '5px',
               'textAlign': 'center',
               'text-decoration': 'none',
               'display': 'inline-block'
               }
disabledButtonStyle = buttonStyle
disabledButtonStyle["disabled"] = True
#----------------------------------------------------------------------------------------------------
def create_eafUploader():

    uploader = dcc.Upload(id='upload-eaf-file',
                          children=html.Div([html.A('Select File', style=buttonStyle)]),
                          multiple=False,
                          style={'display': 'inline-block'})

    return uploader

#----------------------------------------------------------------------------------------------------
def create_eafUploaderTab():

   style = {'border': '5px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   textArea = dcc.Textarea(id="eafUploadTextArea",
                           placeholder='xml validation results go here',
                           value="",
                           style={'width': 600, 'height': 300})

   children = [html.Br(),
               html.Div([create_eafUploader()],
                        style={'display': 'inline-block'}),
               html.Br(),
               html.Br(),
               textArea
               ]

   div = html.Div(children=children, id='eafUploaderDiv') #, style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_soundFileUploader():

    uploader = dcc.Upload(id='upload-sound-file',
                          children=html.Div([html.A('Select File', style=buttonStyle)]),
                          multiple=False,
                          style={'display': 'inline-block'})

    return uploader

#----------------------------------------------------------------------------------------------------
def create_soundFileUploaderTab():

   style = {'border': '5px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   textArea = dcc.Textarea(id="soundFileUploadTextArea",
                           placeholder='sound file validation results go here',
                           value="",
                           style={'width': 600, 'height': 300})

   children = [html.Br(),
               html.Div([create_soundFileUploader()],
                        style={'display': 'inline-block'}),
               html.Br(),
               html.Br(),
               textArea
               ]

   div = html.Div(children=children, id='soundFileUploaderDiv')

   return div

#----------------------------------------------------------------------------------------------------
def create_tierMapFileUploader():

    uploader = dcc.Upload(id='upload-tierMap-file',
                          children=html.Div([html.A('Select File', style=buttonStyle)]),
                          multiple=False,
                          style={'display': 'inline-block'})

    return uploader

#----------------------------------------------------------------------------------------------------
def create_tierMapUploaderTab():

   style = {'border': '5px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   textArea = dcc.Textarea(id="tierMapUploadTextArea",
                           placeholder='tierGuide.yaml will be displayed here',
                           value="",
                           style={'width': 600, 'height': 300})

   children = [html.Br(),
               html.Div([create_tierMapFileUploader()],
                        style={'display': 'inline-block'}),
               html.Br(),
               html.Br(),
               textArea
               ]

   div = html.Div(children=children, id='tierGuideFileUploaderDiv')

   return div

#----------------------------------------------------------------------------------------------------
def create_masterDiv():

   style = {'border': '1px solid green',
            'border-radius': '5px',
            'padding': '10px'}

   title = html.H4("Status")
   eafStatus = html.Label("EAF: ", id="eafStatusLabel", style={"font-size": 14})
   soundStatus = html.Label("Sound: ")
   tierMapStatus = html.Label("Tier map: ")
   grammaticalTermsStatus = html.Label("Grammatical terms: ")
   run_button = html.Button("Run", style=buttonStyle)

   children = [title, eafStatus, soundStatus, tierMapStatus, grammaticalTermsStatus,
               html.Br(), run_button]

   div = html.Div(children=children, id='master-div', className="four columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_uploadsDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '1px'}

   tabsStyle = {'width': '100%',
                'fontFamily': 'Sans-Serif',
                'font-size': 12,
                'margin-left': 'auto',
                'margin-right': 'auto'
                }

   tabs = dcc.Tabs(id="tabs-example", value='tab-1-example',
                   children=[dcc.Tab(label='EAF', children=create_eafUploaderTab()),
                             dcc.Tab(label='Sound', children=create_soundFileUploaderTab()),
                             dcc.Tab(label='Tier Map', children=create_tierMapUploaderTab()),
                             dcc.Tab(label='GrammaticalTerms', value='tab-4-example')
                   ], style=tabsStyle)

   children = tabs;
   div = html.Div(children=children, id='uploads-div', className="eight columns") # , style=style)

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
def parse_eaf_upload(contents, filename, date):

   print("filename selected: %s" % filename)
   #pdb.set_trace()
   content_type, content_string = contents.split(',')
   nchar = len(content_string)
   print("%s (%s): %d characters" % (filename, content_type, nchar))
   return(nchar)

#----------------------------------------------------------------------------------------------------
app.layout = html.Div(
    children=[
        create_masterDiv(),
        create_uploadsDiv(),
        html.P(id="scratchPad", style={'display': 'hidden'}),
    ],
    className="row",
    id='outerDiv',
    style={'margin':  '10px',
           'padding': '20px',
           #'border': '1px blue solid',
           'border-radius': "5px",
           'height':  '300px',
        })

#----------------------------------------------------------------------------------------------------
@app.callback(Output('eafStatusLabel', 'children'),
              [Input('upload-eaf-file', 'contents')],
              [State('upload-eaf-file', 'filename'),
               State('upload-eaf-file', 'last_modified')])
def updateEafLabel(contents, name, date):
   if name is None:
       return "EAF: "
   if name is not None:
       print("on_eafUpload, name: %s" % name)
       return "EAF: %s" % name

#----------------------------------------------------------------------------------------------------
@app.callback(Output('eafUploadTextArea', 'value'),
              [Input('upload-eaf-file', 'contents')],
              [State('upload-eaf-file', 'filename'),
               State('upload-eaf-file', 'last_modified')])
def on_eafUpload(contents, name, date):
    if name is not None:
       print("on_eafUpload, name: %s" % name)
       data = contents.encode("utf8").split(b";base64,")[1]
       filename = os.path.join(UPLOAD_DIRECTORY, name)
       with open(filename, "wb") as fp:
         fp.write(base64.decodebytes(data))
         fileSize = os.path.getsize(filename)
         print("eaf file size: %d" % fileSize)
         schema = xmlschema.XMLSchema('http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
         validXML = schema.is_valid(filename)
         eaf_validationMessage = "%s (%d bytes), valid XML: %s" % (name, fileSize, validXML)
         if(not validXML):
            try:
               schema.validate(filename)
            except xmlschema.XMLSchemaValidationError as e:
               failureReason = e.reason
               eaf_validationMessage = "%s.  error: %s" % (validationMessage, failureReason)
         return eaf_validationMessage

#----------------------------------------------------------------------------------------------------
@app.callback(Output('soundFileUploadTextArea', 'value'),
              [Input('upload-sound-file', 'contents')],
              [State('upload-sound-file', 'filename'),
               State('upload-sound-file', 'last_modified')])
def on_soundUpload(contents, name, date):
    if name is None:
        return("")
    data = contents.encode("utf8").split(b";base64,")[1]
    filename = os.path.join(UPLOAD_DIRECTORY, name)
    with open(filename, "wb") as fp:
       fp.write(base64.decodebytes(data))
       fileSize = os.path.getsize(filename)
       errorMessage = ""
       validSound = True
       try:
          rate, mtx = wavfile.read(filename)
       except ValueError as e:
          print("exeption in wavfile: %s" % e)
          rate = -1
          validSound = False
          errorMessage = str(e)
       print("sound file size: %d, rate: %d" % (fileSize, rate))
       sound_validationMessage = "%s (%d bytes), valid sound: %s %s" % (name, fileSize, validSound, errorMessage)
       return sound_validationMessage

#----------------------------------------------------------------------------------------------------
@app.callback(Output('tierMapUploadTextArea', 'value'),
              [Input('upload-tierMap-file', 'contents')],
              [State('upload-tierMap-file', 'filename'),
               State('upload-tierMap-file', 'last_modified')])
def on_tierMapUpload(contents, name, date):
    if name is None:
        return("")
    encodedString = contents.encode("utf8").split(b";base64,")[1]
    decodedString = base64.b64decode(encodedString)
    s = decodedString.decode('utf-8')
    yaml_list = yaml.load(s)
    filename = os.path.join(UPLOAD_DIRECTORY, name)
    with open(filename, "w") as fp:
       fp.write(s)
       fp.close()
       return(s)
   
    return("foo")

#----------------------------------------------------------------------------------------------------
# app.run_server()
