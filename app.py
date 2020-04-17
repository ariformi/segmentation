import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output 
import plotly.graph_objects as go
import pandas as pd
import base64
import dash_auth
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import numpy as np

path = '/Users/ariannaformignani/Desktop/Mi Scusi/DB_miscusi/segmentation_dataframe.csv'
df= pd.read_csv(path)

df.head()


def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read()) 
    return 'data:image/png;base64,{}'.format(encoded.decode())

path_img = '/Users/ariannaformignani/Desktop/Mi Scusi/logo.png'

colors = {'background': '#F5F1EC',
          'text': '#AC1C26',
          'cluster': ['rgb(171, 33, 43)',  # Red
                     'rgb(41, 128, 110)',  # green
                     'rgb(247, 183, 47)',  # yellow
                     'rgb(51, 170, 191)'  # lightblue
                     ]}

USERNAME_PASSWORD_PAIRS = [['miscusi', 'ariformi'],['miscusi_1', 'giacomo']]



mt_Occasional_hang_out = '''**100% Italians**

**Quite high frequency** of around 2/3 time

**Low revenue** with an average of **13€**

Table of **4/5 people**

Number of different **stores visited: 1**

Number of different **type of services: 1**

Preferred service type: **Fine Dining**
''' 
mt_turist = '''**100% Foreigners** from 21 different countries

**Low frequency** of around 1 time

**High revenue** with an average of **25€**

Table of **3/4 people**

Number of different **stores visited: 1**

Number of different **type of services: 1**

Preferred service type: **Fine Dining**
''' 
mt_Addicted = '''**100% Italians**

**High frequency** of around 6/7 time

**High revenue** with an average of **18€**

Table of **3/4 people**

Number of different **stores visited: 2**

Number of different **type of services: 2**

Preferred service type: **Fast Casual**

''' 
mt_Well_off = '''**100% Italians**

** frequency** of around 1 time

**High revenue** with an average of **33€**

Table of **3/4 people**

Number of different **stores visited: 1**

Number of different **type of services: 1**

Preferred service type: **Fine Dining**
''' 

markdown_text = [mt_Occasional_hang_out,mt_turist,mt_Addicted,mt_Well_off]

color_gradient = [['rgb(171, 33, 43)','rgb(194, 90, 82)','rgb(212, 135, 122)','rgb(171, 33, 160)'],
                ['rgb(41, 128, 110)','rgb(89, 151, 137)','rgb(137, 179, 170)','rgb(41, 128, 230)',],
                 ['rgb(247, 183, 47)','rgb(252, 203, 131)','rgb(225, 228, 192)','rgb(247, 183, 167)'],
                 ['rgb(51, 170, 191)','rgb(124, 191, 209)','rgb(177, 216, 226)','rgb(51, 170, 130)',]]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server

app.layout = html.Div([
                    dbc.Row([
                        dbc.Col(html.H1(children='MISCUSI FAMILY SEGMENTATION',
                                style={'font-size': 20})),
                        
                        dbc.Col(html.Img(src= encode_image(path_img),
                                 style = {'width': '20%',
                                         'float': 'right'}))
                            ]),
    
                    dbc.Row([
                        dbc.Col(html.Label('SEGMENT SELECTION', style= {'font-size': 10}), width= 'auto'),
                        dbc.Col(dcc.Dropdown(id='segment',
                                    options=[{'label': 'Occasional hang-out', 'value': 0},
                                             {'label': 'Tourist', 'value': 1},
                                             {'label': 'Addicted', 'value': 2},
                                             {'label': 'Well-off', 'value': 3}],
                                    value= 3,
                                    style= {'font-size': 12}), width=4)
                            ]),
    
                    dbc.Row([
                        dbc.Col(html.Div([
                            dcc.Graph(id='scatterplot')]), width=4),
                        dbc.Col(html.Div([
                            dcc.Graph(id = 'portion')],style={'margin-left':0}), width=5),
                        dbc.Col(
                            html.Div([html.Label('SUMMARY', style = {'padding-left':103,
                                                                     'padding-top': 10,
                                                                    'padding-bottom': -20}),
                                      html.Div(dcc.Markdown(id = 'description',
                                                            style={'font-family': 'Arial',
                                                                    'margin-bottom': 0, 'margin-left':30})) 
                            ], style= {'font-size': 12,'margin-top':28, 'margin-right':30,
                                       'border': 'thin lightgrey dashed'}))
                         
                            ],no_gutters=True ),
                    
                    dbc.Row([
                        dbc.Col(html.Div([
                            dcc.Graph(id='frequency_revenue')]), width=4),
                        dbc.Col(html.Div([
                            dcc.Graph(id='age')]), width=1),
                        dbc.Col(html.Div([
                            dcc.Graph(id='num_service-service_type')]), width=4),
                        dbc.Col(html.Div([
                            dcc.Graph(id='country'),
                            dcc.Graph(id='guests')]), width=3)
                    ],style={'margin-top': -45},no_gutters=True)
  
                ],style={'color': colors['text'],'margin': 20,
                                    'font-family': 'Arial black'})
    

    
    
@app.callback(Output(component_id='scatterplot',component_property='figure'),
              [Input(component_id='segment',component_property='value')])

def update_scatterplot(segment_value):
    traces = []
    for i in range(0,4):
        if i != segment_value:
            traces.append(go.Scatter(x = df[df['Segment K-means PCA']== i]['Component 2'],
                                    y = df[df['Segment K-means PCA']== i]['Component 1'],
                                    mode = 'markers',
                                    opacity = 0.3,
                                    marker={'size': 5,
                                            'color': colors['cluster'][i],
                                            'line': {'width':0.1,
                                                      'color':'white'} },
                                    name= df[df['Segment K-means PCA']== i]['Legend'].unique()[0]
                                    ))
        else: traces.append(go.Scatter(x = df[df['Segment K-means PCA']== i]['Component 2'],
                                    y = df[df['Segment K-means PCA']== i]['Component 1'],
                                    mode = 'markers',
                                    marker={'size': 5,
                                            'color': colors['cluster'][i],
                                            'line': {'width':0.1,
                                                      'color':'white'} },
                                    name= df[df['Segment K-means PCA']== i]['Legend'].unique()[0]
                                    ))
    return {'data' : traces,
           'layout': go.Layout(title = 'CLUSTERS',
                                height=350,
                                hovermode='closest',
                                titlefont = {'family':'Arial black',
                                             'size':12,
                                             'color' : colors['text']},
                                xaxis = {'showgrid':False,
                                        'showticklabels':False},
                                yaxis = {'showgrid':False,
                                        'showticklabels':False},
                                showlegend=False )}    


@app.callback(Output(component_id='portion',component_property='figure'),
              [Input(component_id='segment',component_property='value')])

def update_portion(segment_value):
    pull=[0, 0, 0, 0]
    for i in range(0,4):
        if i == segment_value:
            pull[i] = 0.2
    
    return {'data': [go.Pie(
             labels= ['Occasional hang-out','Tourist','Addicted','Well-off'],
             values= df['Segment K-means PCA'].value_counts().sort_index().values,
             pull=pull,
             marker = {'colors': colors['cluster']})],


        'layout': go.Layout(
            title = 'SIZE',
            height=350,
            titlefont = {'family':'Arial black',
                         'size':12,
                         'color' : colors['text']},
            legend = {'orientation':'v'})
             }


@app.callback(Output(component_id='description',component_property='children'),
              [Input(component_id='segment',component_property='value')])

def update_description(segment_value):
    return markdown_text[segment_value]


@app.callback(Output(component_id='age',component_property='figure'),
              [Input(component_id='segment',component_property='value')])

def update_age(segment_value):
    dff = df[df['Segment K-means PCA']==segment_value]
    return {'data' : [go.Box(y= dff['age'],
                             name= dff.Legend.unique()[0],
                            boxpoints = 'outliers',
                            marker = dict(
                                color = colors['cluster'][segment_value]),
                            line = dict(
                                color = colors['cluster'][segment_value])
                            )],
           'layout': go.Layout(title = "AGE",
                               height=400,
                               margin=dict(l=20, r=0, b=2),
                              titlefont = {'family':'Arial black',
                                             'size':12,
                                             'color' : colors['text']})}


@app.callback(Output(component_id='frequency_revenue',component_property='figure'),
              [Input(component_id='segment',component_property='value')])

def update_frequency_revenue(segment_value):
    traces = []
    dff = df.groupby('Segment K-means PCA').mean()
    for i in range(0,4):
        if i != segment_value:
            traces.append(go.Scatter(x = [dff['amount_mean'][i]],
                                    y = [dff['frequency'][i]],
                                    mode = 'markers',
                                    opacity = 0.3,
                                    name= df[df['Segment K-means PCA']== i]['Legend'].unique()[0],
                                    marker={'size': 20,
                                            'color': colors['cluster'][i],
                                            'line': {'width':0.1,
                                                      'color':'white'} }
                                    ))
        else: traces.append(go.Scatter(x = [dff['amount_mean'][i]],
                                    y = [dff['frequency'][i]],
                                    mode = 'markers',
                                    name= df[df['Segment K-means PCA']== i]['Legend'].unique()[0],
                                    marker={'size': 20,
                                            'color': colors['cluster'][i],
                                            'line': {'width':0.1,
                                                      'color':'white'} }
                                    ))
    return {'data' : traces,
           'layout': go.Layout(title = 'REVENUE - FREQUENCY',
                               height=420,
                                hovermode='closest',
                                titlefont = {'family':'Arial black',
                                             'size':12,
                                             'color' : colors['text']},
                                xaxis = {'title':'revenue'},
                                yaxis = {'title':'frequency'},
                               font=dict(family="Arial",
                                            size=11,
                                            color="black"),
                                showlegend=False )}    


@app.callback(Output(component_id='country',component_property='figure'),
              [Input(component_id='segment',component_property='value')])

def update_country(segment_value):
    value = df[df['Segment K-means PCA']== segment_value]['country'].value_counts()
    option_labels = [['Foreigners'],['Italians']]
    label_index = df[df['Segment K-means PCA']== segment_value]['country'].unique()[0]
    
    return {'data':[go.Pie(labels=option_labels[label_index],
                           values=value.values,
                           hole=0.3,
                           textinfo='label+percent',
                           marker={'colors': [colors['cluster'][segment_value]]})],
           'layout':go.Layout(title = 'COUNTRY',
                               height=200,
                              margin=dict(t = 80, b = 5, pad=0, l =0,r=0),
                                titlefont = {'family':'Arial black',
                                             'size':12,
                                             'color' : colors['text']},
                                showlegend=False ) }


@app.callback(Output(component_id='guests',component_property='figure'),
              [Input(component_id='segment',component_property='value')])

def update_guests(segment_value):
    value = df[df['Segment K-means PCA']== segment_value]['services_type'].value_counts().sort_index().values
    option_labels = ['Fast Casual','Fine Dining','Delivery','Takeaway']
    
    return {'data':[go.Pie(labels=option_labels,
                           values=value,
                           hole=0.3,
                           textinfo='label+percent',
                           textposition='inside',
                           marker={'colors': color_gradient[segment_value]})],
           'layout':go.Layout(title = 'SERVICE TYPE',
                              margin=dict(t = 80,b = 5, pad=0,l=0,r=0),
                               height=200,
                                titlefont = {'family':'Arial black',
                                             'size':12,
                                             'color' : colors['text']},
                              
                              uniformtext_minsize=10, 
                              uniformtext_mode='hide',
                                showlegend=False ) }


@app.callback(Output(component_id='num_service-service_type',component_property='figure'),
              [Input(component_id='segment',component_property='value')])

def update_num_service_service_type(segment_value):
    dff = df[df['Segment K-means PCA']== segment_value]
    traces = []
    traces.append(go.Bar(y = [np.round(dff['guests_mean'].mean())],
                                    name= 'Guests',
                                    marker={'color': color_gradient[segment_value][0]}
                                    ))
    traces.append(go.Bar(y = [np.round(dff['num_stores'].mean())],
                                    name= 'stores number',
                                    marker={'color': color_gradient[segment_value][1]}
                                    ))
    traces.append(go.Bar(y = [np.round(dff['different_services'].mean())],
                                    name= 'number services',
                                    marker={'color': color_gradient[segment_value][2]}
                                    ))
    return {'data' : traces,
           'layout': go.Layout(title = 'GUESTS - STORES NUM - SERVICES NUM',
                               height=450,
                               margin=dict(r=0),
                                titlefont = {'family':'Arial black',
                                             'size':12,
                                             'color' : colors['text']},
                                legend={'x':0.55},
                               xaxis = {'showgrid':False,
                                        'showticklabels':False})} 



if __name__ == '__main__':
        app.run_server()
