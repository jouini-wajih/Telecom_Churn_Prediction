import pathlib
import Prepare_Data as prd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State 
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from dash import Dash, Input, Output, html, dcc, callback,ctx


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Telecom Churn Dashboard"
server = app.server
app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df = prd.Df()




def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Telecom Churn Dashboard",style={"fontSize":30}),
                    html.H6("Predict Control Report"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.A(
                        html.Button(children="Tunisie Telecom"),
                         href="https://www.tunisietelecom.tn",
                    ),
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    html.A(
                        html.Img(id="logo", src=app.get_asset_url("tt.png"),style={'width': 80, 'height': 80}),
                        href="https://www.tunisietelecom.tn",
                    ),
                ],
            ),
        ],
    )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                        dcc.Tab(
                        id="Control-chart-tab",
                        label="Dashboard",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Specs-tab",
                        label="Predict Potential Churn customers",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                
               
                ],
            )
        ],
    )

    
    




def build_tab_1():
    return [
        html.Div(
            id="settings-menu",
            children=[
                     
                html.Div(
                    id="m",
                    # className='five columns',
                    children=[
                      
                        html.Label(id="metric-select-title", children="Upload customers csv file to predect potential churn customers , using machine learning classification model ",style=
                                   {'color':'white','position':'relative'}),                       
                          html.Label(id="metric-select", children="this will give you table containing table of the uploaded file and the probability of the churn predected",
                                   style={'color':'white','position':'relative'}),
                            html.Br(),
                        dcc.Upload(id="upi",children=html.Button('Upload File'),style={"width":"10px","position":"relative","left":"50px","width":"70px"}),
                        html.Button(id='ini',children='Inspect File',n_clicks=0,style={"position":"relative","left":"310px","top":"-39px",}),
                        html.Button(id="pr",children='Predict churn',n_clicks=0,style={"position":"relative","left":"413px",
                                                                                                   "top":"-41px",
                                                                                                   }),
                        html.Label(id="output-file-info",style={"position":"relative","top":"-30px","left":'50px'}),
                        dcc.Store(id='cached-data',storage_type='memory'),
                         dcc.Loading(
            id="loading-1",
            type="default",
            children= html.Div(id='output-data',style={'position': 'relative',"right":"50px","width":"70%"}),
            style={'position':'relative','left':'-300px','width':'500px',"height":"500px","top":"100px"}
            
        ),
                      
                    ],
                    style={'position':'relative','left':'180px','width':'100%','display': 'inline-block'}
                ),
                
                
            ],
            style={'position':'relative','width':'100%','display': 'inline-block'}
        )
    ]




def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    html.P("Telecom Churn",
                   style={'fontFamily': 'Arial',
                  'fontSize': '30px',
                  'fontWeight': 'bold',})
                ,
                  html.Img(id="logo", src=app.get_asset_url("tt.png"),style={'width': 350, 'height': 350,'position': 'relative', 'top': '-50px',}),

              

                    html.P("churn , refers to the rate at which customers discontinue using their services or terminate their subscriptions within a specific period, usually measured on a monthly or annual basis. It is a crucial metric for telecom companies as it directly impacts their customer base and revenue. High churn rates can be a sign of customer dissatisfaction, intense competition, or ineffective retention strategies, while low churn rates indicate that customers are loyal and satisfied with the services.",
                    style={'fontFamily': 'Arial',
                  'fontSize': '15px',
                  'fontWeight': 'bold',
                          'position': 'relative', 'top': '-150px'}),
                   
        
                 

    
                ],style={"position":"relative","top":"-50px"}
            ),  html.P("In this section we can control the features values and see how can this"+
                                 " affect the pie charts of churn percentage and churn predicted proba avg ."+
                                 " so we can easily detect    the most affective feature and the combination"+
                                 " of inputs values that leads to the lowest churn percentage",
                    style={'fontFamily': 'Arial',
                  'fontSize': '15px',
                  'fontWeight': 'bold',
                          'position': 'relative',"top":"-180px","left":"10px"}),
                          html.P("In this section we can see the relationship between our features values and "+
                                 "the churn proba as shown in the scatter plot and the bar plot ,we can also control the features values by the slider below.",
                    style={'fontFamily': 'Arial',
                  'fontSize': '15px',
                  'fontWeight': 'bold',
                          'position': 'relative',"left":"10px"}),html.Br(),html.Br(),
                   html.Div(id="dropd",children=[
                       dcc.Dropdown(['nb_reclamation', 'nb_jours_abonne', 'nb_appel_nuit','nb_appel_soiree','nb_appel_jour',"nb_appel_inter"
                                     ,'nb_msg_vocaux','cout_appel_jour','cout_appel_nuit','cout_appel_soiree'],
                                     'nb_reclamation', id='dropdown',disabled=False),html.Br(),
                                     html.Div(id="aa",children=[
                html.Label(id="a",children="nombre des jours abonne",style={"position":"relative","left":"40px"}),
                dcc.RangeSlider(min=0,max=100,step=1,value=[0,100],id="s10",marks=None,tooltip={"placement": "bottom", "always_visible": False})]),],style={
                    'z-index': "5","position":"relative","width":"100%"
                }),
          
        ],
    )


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)

def scatter(_x,_y,_color,_title,_height=400,c=px.colors.qualitative.Pastel,data=df):
    data['churn']=data['churn'].astype(str)
    fig= px.scatter(data, x=_x, y=_y, color=_color,
                                 color_discrete_sequence=c,
                                                 title=_title)
    fig.update_traces(marker=dict(size=3),),
    fig.update_layout(plot_bgcolor="#161a28",paper_bgcolor="#161a28",height=_height,
                      font_color="white",
                      title_font_color="white",
                      legend_title_font_color="white",
                          margin=dict(l=20, r=20, t=55, b=5),)
    fig.update_xaxes( zeroline=False,gridwidth=0.5,linecolor="#1e2130", gridcolor='#1e2130'),
    fig.update_yaxes( zeroline=False,gridwidth=0.5,linecolor='#1e2130', gridcolor='#1e2130')
    return fig

def scatter2(_x,_y,_color,_title,_height=400,c=px.colors.sequential.GnBu):
    df['churn']=df['churn'].astype(str)
    fig= px.scatter(df, x=_x, y=_y, color=_color,color_continuous_scale=c,
                                                 title=_title)
    fig.update_traces(marker=dict(size=3),),
    fig.update_layout(plot_bgcolor="#161a28",paper_bgcolor="#161a28",height=_height,
                      font_color="white",
                      title_font_color="white",
                      legend_title_font_color="white",
                          margin=dict(l=20, r=20, t=55, b=5),)
    fig.update_xaxes( zeroline=False,gridwidth=0.5,linecolor="#1e2130", gridcolor='#1e2130'),
    fig.update_yaxes( zeroline=False,gridwidth=0.5,linecolor='#1e2130', gridcolor='#1e2130')
    return fig
    
    
def build_top_panel():
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            # Metrics summary
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("This plot shows the corrolation between churn proba and calls count per day evening and night"),
                    html.Div(
                        id="metric-div",
                        children=[
                           
         html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabss",
                value="tab3",
                className="custom-tabs",
                children=[
                        dcc.Tab(
                        id="Control-chart-tab",
                        label="Jour",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Specs-tab",
                        label="Nuit",
                        value="tab4",
                        selected_className="custom-tab--selected",
                        className="custom-tab",
                    ),
                       dcc.Tab(
                        id="Specs-tab",
                        label="Soiree",
                        value="tab5",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                 ],
      )
      
        ],
    ),         
               
      
        html.Div(id="d",children=[                   
       dcc.Graph(
        id='scatter',
        figure=scatter(_x="nb_appel_jour",_y="churn_proba",_color='churn',_title="churn porba per day calls count "),
       )
            
        
      ])
                        ],
                        
         
                    ),
                ],

            ),
            # Piechart
       
        ],
                     style={'height': 500,}

    )

def sliders1():
    min1=df['nb_jours_abonne'].min()
    max1=df['nb_jours_abonne'].max()
    min2=df['nb_appel_jour'].min()
    max2=df['nb_appel_jour'].max()
    min3=df['nb_appel_nuit'].min()
    max3=df['nb_appel_nuit'].max()
  
    return html.Div(id="sliders",children=[
         html.Br(),
    html.Label("nombre des jours abonne",style={"position":"relative","left":"50px"}),
    dcc.RangeSlider(min=min1,max=max1,step=1,value=[min1,max1],id="s1",marks=None,tooltip={"placement": "bottom", "always_visible": False}),
 html.Label("nombre d appel par jour",style={"position":"relative","left":"50px"}),
 dcc.RangeSlider(min=min2,max=max2,step=1,value=[min2,max2],id="s2",marks=None,tooltip={"placement": "bottom", "always_visible": False}),
 html.Label("nombre d appel par nuit",style={"position":"relative","left":"50px"}),
 dcc.RangeSlider(min=min3,max=max3,step=1,value=[min3,max3],id="s3",marks=None,tooltip={"placement": "top", "always_visible": False}),

    ], style={"left":"30px","position":"relative",'width': '45%', 'display': 'inline-block',"height":"60px"})
    
def sliders2():
    min4=df['nb_appel_soiree'].min()
    max4=df['nb_appel_soiree'].max()
    min5=df['nb_appel_inter'].min()
    max5=df['nb_appel_inter'].max()
    min6=df['nb_reclamation'].min()
    max6=df['nb_reclamation'].max()
    return html.Div(id="sliders",children=[
         html.Br(),
    html.Label("nombre d appel par soiree",style={"position":"relative","left":"50px"}),
    dcc.RangeSlider(min=min4,max=max4,step=1,value=[min4,max4],id="s4",marks=None,tooltip={"placement": "bottom", "always_visible": False}),
 html.Label("nombre d appel international",style={"position":"relative","left":"50px"}),
 dcc.RangeSlider(min=min5,max=max5,step=1,value=[min5,max5],id="s5",marks=None,tooltip={"placement": "bottom", "always_visible": False}),
 html.Label("nombre de reclamation",style={"position":"relative","left":"50px"}),
 dcc.RangeSlider(min=min6,max=max6,step=1,value=[min6,max6],id="s6",marks=None,tooltip={"placement": "top", "always_visible": False}),
  

    ], style={"left":"30px","position":"relative",'width': '45%', 'display': 'inline-block',"height":'60px'})
                    
     
     
def pie_chart1(d):
    fig=px.pie(
            data_frame=d,
            names='churn',
            hole=.7,color_discrete_sequence=["#1e2130","#eac56d"],
        
            
            )
    fig.update_layout(plot_bgcolor="#161a28",paper_bgcolor="#161a28",
                      font_color="white",
                      title_font_color="white",
                      legend_title_font_color="white",
                      showlegend=False,
                       margin=dict(l=20, r=20, t=0, b=150),
                       annotations=[dict(text='% CHURN', x=0.5, y=0.5, font_size=20, showarrow=False)]
                        )
    return fig

def pie_chart2(d):
    a=d['churn_proba'].mean()*100    
    
    data = {
    'category': ['avg_churn', 'not'],
    'values': [a,100-a]
    }
    dd = pd.DataFrame(data)
    
    fig=px.pie(
        
            dd, values='values', names='category',
            hole=.7,color_discrete_sequence=["#1e2130","#65c2ca"],
        
            
            )
    fig.update_layout(plot_bgcolor="#161a28",paper_bgcolor="#161a28",
                      font_color="white",
                      title_font_color="white",
                      legend_title_font_color="white",
                      showlegend=False,
                       margin=dict(l=20, r=20, t=0, b=150),
                       annotations=[dict(text='CHURN Proba Avg', x=0.5, y=0.5, font_size=20, showarrow=False)]
                        )
    return fig

def pie_chart3(d):
    mdf=d['churn_proba']>0.5
    vc=mdf.value_counts()
    a=(vc[1]/(vc[0]+vc[1]))*100
    
    dataa = {
    'Category': ['% proba > 0.5', '% proba < 0.5'],
    'Values': [a,100-a]
    }
    ddf = pd.DataFrame(dataa)
    
    fig=px.pie(
        
            ddf, values='Values', names='Category',
            hole=.7,color_discrete_sequence=["#1e2130","#de2a28"],
        
            
            )
    fig.update_layout(plot_bgcolor="#161a28",paper_bgcolor="#161a28",
                      font_color="white",
                      title_font_color="white",
                      legend_title_font_color="white",
                      showlegend=False,
                       margin=dict(l=20, r=20, t=0, b=150),
                       annotations=[dict(text='% TRUE CHURN PRED', x=0.5, y=0.5, font_size=20, showarrow=False)]
                        )
    return fig
  
def generate_piechart(p):
    return html.Div(id="pie",children=[
                                       dcc.Graph(
        id="piechart",
        figure=p,
    )],
                     style={"left":"50px","position":"relative","top":"20px","showlegend":"False","autoscale":"True","width":"30%","height":"30%",'display': 'inline-block'}
        
    )        
    
def build_charts(d):
    ret =generate_piechart(pie_chart1(d)),generate_piechart(pie_chart3(d)),generate_piechart(pie_chart2(d))
    return ret
    



def build_chart_panel():
    return html.Div(
        id="control-chart-container",
       
        children=[
            generate_section_banner("This graph shows how can features affect chern and predicted churn %"),
                 html.Div(
                id="Churn_per",
                children=[sliders1(),sliders2(),
                html.Div(id="chartcb",children=[build_charts(df)[0],build_charts(df)[1],build_charts(df)[2]]),
                    
                ],
        
        
            ),
        ],style={"height":"530px",'display': 'inline-block'}
    )

def bar(x,data=df):
   
    fig=px.histogram(data, x="churn", y=x,color_discrete_sequence=px.colors.qualitative.Pastel,
             color='churn',
             histfunc='avg',
             )
    fig.update_layout(plot_bgcolor="#161a28",paper_bgcolor="#161a28",height=400,width=400,
                      font_color="white",
                      title_font_color="white",
                      legend_title_font_color="white",
                          margin=dict(l=20, r=20, t=55, b=5),)
    fig.update_xaxes( zeroline=False,gridwidth=2,linecolor="#1e2130", gridcolor='#1e2130'),
    fig.update_yaxes( zeroline=False,gridwidth=2,linecolor='#1e2130', gridcolor='#1e2130')
    return fig


def build_chart_panel2():
    return html.Div(
        id="control-chart-container",
       
        children=[html.Div(id="ban",children=generate_section_banner("how some features affect churn predicted proba"),style={"width":"100%","position":"relative",})
            ,  html.Div(
                id="Churn_per2",
                children=[html.Div(id="e1",children=dcc.Graph(
                figure=scatter(_x='nb_reclamation',_y='churn_proba',_color='churn',_title='nb reclamation / churn proba'),
                ),style={'position':'relative','width':'30%',"left":"350px"}),
                          html.Div(id="e2",children=dcc.Graph(figure=bar("nb_reclamation")),style={"width":"15%",'position':'relative','top':'-400px',
                                                                                   "left":"850px"}),

 
            
          
                
        ],style={"width":"170%","position":"relative","right":"350px","height":"400px",'display': 'inline-block'}
    )])









app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
    
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
     
    ]
)




@app.callback(
    [Output("Churn_per2", 'children',allow_duplicate=True),Output('aa','children')],
    [Input('dropdown', 'value')],prevent_initial_call=True,
)
def update_(selected_value):
    return ([html.Div(id="e1",children=dcc.Graph(
                figure=scatter(_x=selected_value,_y='churn_proba',_color='churn',_title=selected_value+'/ churn proba',data=df),
                ),style={'position':'relative','width':'30%',"left":"350px"}),
                          html.Div(id="e2",children=dcc.Graph(figure=bar(selected_value,data=df)),style={"width":"15%",'position':'relative','top':'-400px',
                                                                                   "left":"850px"}),],
                            [html.Label(children=selected_value,style={"position":"relative","left":"40px"}),
                dcc.RangeSlider(min=df[selected_value].min(),max=df[selected_value].max(),step=1,
                                value=[df[selected_value].min(),df[selected_value].max()],id="s10",marks=None,
                                tooltip={"placement": "bottom", "always_visible": False})],
                                                                                   
                                                                                   )

@app.callback(
    [Output("Churn_per2", 'children')],
    [Input('dropdown', 'value'),Input('s10', 'value')],
)
def update_(selected_value,s):
    d=df[df[selected_value].between(s[0],s[1])]
    return ([html.Div(id="e1",children=dcc.Graph(
                figure=scatter(_x=selected_value,_y='churn_proba',_color='churn',_title=selected_value+'/ churn proba',data=d),
                ),style={'position':'relative','width':'30%',"left":"350px"}),
                          html.Div(id="e2",children=dcc.Graph(figure=bar(selected_value,data=d)),style={"width":"15%",'position':'relative','top':'-400px',
                                                                                   "left":"850px"}),],
                         
                                                                                   
                                                                                   )



    


import base64
import io



@app.callback(
    [Output('output-file-info', 'children'),Output('cached-data', 'data')],
    [Input('upi', 'contents')],
    [State('upi', 'filename'),]
)
def update_output(contents, filename ):
  if contents is not None:
    try:
        content_string = contents.split(',')[1]
        decoded = base64.b64decode(content_string)
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
    
    return filename,df.to_dict(orient='records'),
  else:
        return "No file selected.",df.to_dict(orient='records'),



@app.callback(
    Output('output-data', 'children'),
    Input('ini','n_clicks'),
    Input('pr', 'n_clicks'),
    State('cached-data', 'data'),
    prevent_initial_call=True
)
def update_graph(b1, b2,stored_data):
    ddf=pd.DataFrame(stored_data)
    triggered_id = ctx.triggered_id
    if triggered_id == 'ini':
         return up1(b1,ddf)
    elif triggered_id == 'pr':
         return up2(b2,ddf)

def up1(c,ddf ):  
  PAGE_SIZE=15
  d=ddf[['nb_jours_abonne','nb_appel_jour','nb_appel_nuit','nb_appel_soiree','nb_reclamation','churn']]
  if c>0:
        return dash_table.DataTable(d.to_dict('records'), [{"name": i, "id": i} for i in d.columns],
    page_size=PAGE_SIZE,
                                        style_header={
            'backgroundColor': "#1e2130",
            'fontWeight': 'bold'
        },                                 style_cell={
            'backgroundColor': "#1e2130",
            'fontWeight': 'bold'
        }),
    

def up2(c,ddf):
  PAGE_SIZE=15
  d=prd.d_clean(ddf)
  d["churn_proba"]=prd.pred(d)


  d=d[['nb_jours_abonne','nb_appel_jour','nb_appel_nuit','nb_appel_soiree','nb_reclamation','churn_proba']]
  print(d)
  if c>0:  
        return dash_table.DataTable(d.to_dict('records'), [{"name": i, "id": i} for i in d.columns], 
                                     style_data_conditional=[
        {
            'if': {'column_id': 'churn_proba', 'filter_query': '{churn_proba}<0.25 && {churn_proba}>=0'},
            'backgroundColor': '#107dac',  
             
            
        },
        {
            'if': {'column_id': 'churn_proba', 'filter_query': '{churn_proba}<0.5 && {churn_proba} >= 0.25'},
            'backgroundColor': '#1ebbd7',
            
        },   {
            'if': {'column_id': 'churn_proba', 'filter_query': '{churn_proba}<0.75 && {churn_proba} >= 0.5'},
              'backgroundColor': '#ff7b7b', 
        },   {
            'if': {'column_id': 'churn_proba', 'filter_query': '{churn_proba} >= 0.75'},
            'backgroundColor': '#ff5252', 
        },
    ],
                                    page_size=PAGE_SIZE,   
                                        style_header={
            'backgroundColor': "#1e2130",
            'fontWeight': 'bold'
        },                                 style_cell={
            'backgroundColor': "#1e2130",
            'fontWeight': 'bold'
        }),
    


@app.callback(
    [Output("app-content", "children")],
    [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return build_tab_1(), 
    else:
        return (
        html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel(),
                html.Div(
                    id="graphs-container",
                    children=[build_top_panel(), build_chart_panel(),
                              build_chart_panel2()],
                ),
            ],
        ),
     
    )
        
        
@app.callback(
    [Output("d", "children")],
    [Input("app-tabss", "value")],
)
def render_tab_conten(tab_switch):
    if tab_switch=="tab3":
        fig=scatter(_x="nb_appel_jour",_y="churn_proba",_color='churn',_title="churn porba per day calls count ")

    elif tab_switch=="tab4":
        fig=scatter(_x="nb_appel_nuit",_y="churn_proba",_color='churn',_title="churn porba per night calls count")

    else  :
        fig=scatter(_x="nb_appel_soiree",_y="churn_proba",_color='churn',_title="churn porba per evening calls count")


    return (dcc.Graph(figure=fig),)



    fig= px.scatter(df, x='nb_appel_jour', y='duree_appel_jour(minutes)', color='churn_proba',
                                 color_continuous_scale='Viridis'),

    return (dcc.Graph(id="scatter",figure=fig),)

    
@app.callback(
    [Output("chartcb", "children")],
    [Input("s1", "value"),Input("s2", "value"),Input("s3", "value"),
     Input("s4", "value"),Input("s5", "value"),Input("s6", "value"),],
)
def test(s1,s2,s3,s4,s5,s6):
    d=df[df['nb_jours_abonne'].between(s1[0],s1[1])]
    d=d[df['nb_appel_jour'].between(s2[0],s2[1])]
    d=d[df['nb_appel_nuit'].between(s3[0],s3[1])]
    d=d[df['nb_appel_soiree'].between(s4[0],s4[1])]
    d=d[df['nb_appel_inter'].between(s5[0],s5[1])]
    d=d[df['nb_reclamation'].between(s6[0],s6[1])]
    return build_charts(d),
    
    
    


# Update interval
@app.callback(
    Output("n-interval-stage", "data"),
    [Input("app-tabs", "value")],
 
)
def update_interval_state(tab_switch, cur_interval, disabled, cur_stage):
    if disabled:
        return cur_interval

    if tab_switch == "tab1":
        return cur_interval
    if tab_switch == "tab2" :
        return cur_stage
    else :
        return cur_stage












# Running the server
if __name__ == "__main__":
    app.run_server(debug=False, port=8050)

