#################### LIBRARIES #######################
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_trich_components as dtc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

#################### START OF "app" ########################
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Content MINI-boxes style
mini_container = {
  'border-radius': '5px',
  'background-color': '#f9f9f9',
  'margin': '10px',
  'padding': '5px',
  'position': 'relative',
  'box-shadow': '2px 2px 2px lightgrey',
}


######################### DATA ##########################
df_tiendas_mapa = pd.read_csv("Tiendas_mapa.csv")
# It's necessary to convert "cluster" column to categorical variable
df_tiendas_mapa['cluster'] = df_tiendas_mapa['cluster'].astype('str')

recomendacion = pd.read_excel('Recomendacion.xlsx')
print(recomendacion)

# dropdown_dict = [{"label": str(i)+' - '+str(df_tiendas_mapa[df_tiendas_mapa['Tienda'] == i]['Nombre Tienda'].\
#     iloc[0]).upper(),"value":str(i)} for i in df_tiendas_mapa['Tienda'].unique()]

dropdown_dict = [{"label":str(i), "value":str(i)} for i in recomendacion['usuario'].unique()]

######################### SIDEBAR LAYOUT ############################
sidebar = html.Div(
    [
    #html.H2("Sidebar", className="Sidebar-Logo"),
    html.Img(className="logo_mintic", src="https://colombiatic.mintic.gov.co/679/channels-581_logo_footer_mintic.png",
        style={'height':'12%','align':'center'}),
    html.Hr(),
    dbc.Nav(
        [
        dbc.NavLink("Recomendación", href="/page-1", id="page-1-link"),
        dbc.NavLink("Estadísticas", href="/page-2", id="page-2-link"),
        dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
        ],
        vertical=True,
        pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    )

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

########################### FIRST PAGE LAYOUT ######################
# Here we have all the content of the homepage

homepage_layout = html.Div(
    children=[
    html.Div(className='jumbotron',
        children=[html.Div(id="error-message"),
        dbc.Row([
            # dbc.Col(
            #     html.H6(className="h2-title", children="Tea-té Recomienda")
            #     ),
            dbc.Col(
               html.Img(className="Imagen_logo_1",
                   src="https://static.wixstatic.com/media/c6e056_02725f5e9e344faa9360e00d78eff6de~mv2.png",
                   style={'height':'70%','align':'left'})
               ),
            ], align='left'),
        ]),
    dbc.Container([
        html.H4('Subcategorias más populares'),
        dtc.Carousel([
            html.Div('slide 1',style=mini_container),
            dbc.Card([
                dbc.CardHeader([html.H6("Aseo", className="card-title")]),
                dbc.CardBody([
                    html.P("Fabricante: JGB", className="card-text"),
                    ])],style={"width": "10"}, color='info', outline=True),
            html.Div('slide 2',style=mini_container),
            html.Div('slide 3',style=mini_container),
            html.Div('slide 4',style=mini_container),
            html.Div('slide 5',style=mini_container),
            html.Div('slide 6',style=mini_container)
        ],
            slides_to_scroll=1,
            swipe_to_slide=True,
            autoplay=True,
            speed=500,
            variable_width=True,
            center_mode=True,
            responsive=[
            {
            'breakpoint': 991,
            'settings': {'arrows': False}
            }]
        ),
        dbc.Row([
            dbc.Col([
                html.H5('Seleccione Región:'),
                dcc.RadioItems(
                    options=[
                    {'label': 'REGIÓN CALI', 'value': 'REGION CALI'},
                    {'label': 'REGIÓN MEDELLÍN', 'value': 'REGION MEDELLIN'},
                    ],value='REGION CALI', labelStyle={'display': 'block'}
                    ),
                html.Br(),
                html.H5('Seleccione Tienda:'),
                dcc.Dropdown(
                    id='dropdown_tienda',
                    options=dropdown_dict,
                    #value='20000541',
                    placeholder="Seleccione Tienda"
                    ),
                ],style=mini_container,width=4),
            dbc.Col([
                html.Div(id='Tabla_recomendaciones', children=[])
                ],style=mini_container),
            ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                dbc.CardHeader([html.H6("Aseo", className="card-title")]),
                dbc.CardBody([
                    html.P("Fabricante: JGB", className="card-text"),
                    ])],style={"width": "10"}, color='info', outline=True),
                ],style=mini_container,width=3),
            dbc.Col([
                html.Center(children=[  
                    dcc.Graph(id='mapa_tiendas', figure={}),
                    ]),
                ],style=mini_container),
            ]),
        ]),
    ])
######################### CALLBACKS ###########################

################## CALLBACKS SIDEBAR #####################
# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
    )

def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return homepage_layout
    elif pathname == "/page-2":
        return html.P("This is the content of page 2. Yay!")
    elif pathname == "/page-3":
        return html.P("Oh cool, this is page 3!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

################## CALLBACKS HOMEPAGE ###################

### Callback tabla recomendación

@app.callback(
    Output(component_id="Tabla_recomendaciones",component_property="children"),
    [
    Input(component_id="dropdown_tienda", component_property="value")
    ]
)

def actualizar_tabla_recomendaciones(input_tienda):
    recomendacion_1 = recomendacion.copy()
    recomendacion_1 = recomendacion_1[recomendacion_1['usuario'] == int(input_tienda)][['Tipo R',0,1,2,3,4,5,6,7,8,9]]
    recomendacion_1 = recomendacion_1.set_index('Tipo R').T

    return dbc.Table.from_dataframe(recomendacion_1,
     striped=True, 
     bordered=True, 
     size='0.5sm', 
     hover=True)

### Callback mapa
@app.callback(
    Output(component_id="mapa_tiendas",component_property="figure"),
    [
    Input(component_id="dropdown_tienda", component_property="value")
    ]
)

def grafico_mapa(input_tienda):
    tiendas_df = df_tiendas_mapa.groupby('Tienda', as_index=False).max()
    center_lat = tiendas_df[tiendas_df['Tienda'] == int(input_tienda)]['latitude'].mean()
    center_lon = tiendas_df[tiendas_df['Tienda'] == int(input_tienda)]['longitude'].mean()

    map_box_access_token = "pk.eyJ1IjoiaHVtYmVydG9jcnYiLCJhIjoiY2tnbG5xZWpyMTJhdzJycGVyamZma2FjYyJ9.juzkmatkYaLTmiprDJCD0w"
    px.set_mapbox_access_token(map_box_access_token)
    fig_map = px.scatter_mapbox(tiendas_df, center=go.layout.mapbox.Center(lat=center_lat, lon=center_lon),
        lat='latitude', 
        lon='longitude',
        color="cluster",
        color_continuous_scale=px.colors.cyclical.IceFire,
        hover_name="Nombre Tienda",
        size_max=100,
        zoom=18
        )
           
    return fig_map

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8050', debug=True)