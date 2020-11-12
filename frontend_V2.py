#################### LIBRARIES #######################
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_trich_components as dtc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import random
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

# Tabla principal Completa
df_orig = pd.read_csv('datos_con_coordenadas_v1 (1).csv', compression='gzip')
df = df_orig.copy() # Copia de la tabla original

# 
df_tiendas_mapa = pd.read_csv("Tiendas_mapa.csv")
# It's necessary to convert "cluster" column to categorical variable
df_tiendas_mapa['cluster'] = df_tiendas_mapa['cluster'].astype('str')

recomendacion = pd.read_excel('Recomendacion.xlsx')

for col in recomendacion.columns[2:]:
    recomendacion[col]=recomendacion[col].apply(lambda x: df[df['Material']==x]['Nombre Material'].max())

# dropdown_dict = [{"label": str(i)+' - '+str(df_tiendas_mapa[df_tiendas_mapa['Tienda'] == i]['Nombre Tienda'].\
#     iloc[0]).upper(),"value":str(i)} for i in df_tiendas_mapa['Tienda'].unique()]

#dropdown_dict = [{"label":str(i)+' - '+str(df[df['Tienda'] == i]['Nombre Tienda'].iloc[0]),"value":str(i)} for i in recomendacion['usuario'].unique()]

#Saltos de linea
br = html.Br()

#Función creación carrusel
def crear_carousel(product_list):
    list_colores = ['primary','secondary','info','success','warning','danger','dark']
    carrusel = dtc.Carousel([
        dbc.Container([dbc.Card([dbc.CardBody([html.H6('#1'),html.P(product_list[0].upper(),style={'fontSize':11}, className="card-title"),])],
            style={"size": "8rem"}, color=random.choice(list_colores), inverse=True)]),
        dbc.Container([dbc.Card([dbc.CardBody([html.H6('#2'),html.P(product_list[1].upper(),style={'fontSize':11}, className="card-title"),])],
            style={"size": "8rem"}, color=random.choice(list_colores), inverse=True)]),
        dbc.Container([dbc.Card([dbc.CardBody([html.H6('#3'),html.P(product_list[2].upper(),style={'fontSize':11}, className="card-title"),])],
            style={"size": "8rem"}, color=random.choice(list_colores), inverse=True)]),
        dbc.Container([dbc.Card([dbc.CardBody([html.H6('#4'),html.P(product_list[3].upper(),style={'fontSize':11}, className="card-title"),])],
            style={"size": "8rem"}, color=random.choice(list_colores), inverse=True)]),
        dbc.Container([dbc.Card([dbc.CardBody([html.H6('#5'),html.P(product_list[4].upper(),style={'fontSize':11}, className="card-title"),])],
            style={"size": "8rem"}, color=random.choice(list_colores), inverse=True)]),
        dbc.Container([dbc.Card([dbc.CardBody([html.H6('#6'),html.P(product_list[5].upper(),style={'fontSize':11}, className="card-title"),])],
            style={"size": "8rem"}, color=random.choice(list_colores), inverse=True)]),
        dbc.Container([dbc.Card([dbc.CardBody([html.H6('#7'),html.P(product_list[6].upper(),style={'fontSize':11}, className="card-title"),])],
            style={"size": "8rem"}, color=random.choice(list_colores), inverse=True)]),
        dbc.Container([dbc.Card([dbc.CardBody([html.H6('#8'),html.P(product_list[7].upper(),style={'fontSize':11}, className="card-title"),])],
            style={"size": "8rem"}, color=random.choice(list_colores), inverse=True)]),
        dbc.Container([dbc.Card([dbc.CardBody([html.H6('#9'),html.P(product_list[8].upper(),style={'fontSize':11}, className="card-title"),])], 
            style={"size": "8rem"}, color=random.choice(list_colores), inverse=True)]),
        dbc.Container([dbc.Card([dbc.CardBody([html.H6('#10'),html.P(product_list[9].upper(),style={'fontSize':11}, className="card-title"),])],
            style={"size": "8rem"}, color=random.choice(list_colores), inverse=True)]),                                                               
        ],
        slides_to_scroll=1,
        swipe_to_slide=True,
        autoplay=True,
        speed=500,
        variable_width=False,
        center_mode=False,
        responsive=[
        {
        'breakpoint': 991,
        'settings': {
        'arrows': True
        }
        }])
    return carrusel

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

########################### FIRST PAGE LAYOUT ########################
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
                   style={'height':'100%','align':'left'})
               ),
            ], align='left'),
        ]),
    dbc.Container([
        html.H4('Subcategorias populares'),
        # ESTE ES EL SLIDER SUPERIOR, CADA ELEMENTO DEL SLIDER ES LA IMAGEN
        dtc.Carousel([
            html.Img(className="Imagen_slider1",
                   src="https://static.wixstatic.com/media/e9606e_52e15af7d9b54c4ca1b51a67e4abb8f3~mv2.png"),
            html.Img(className="Imagen_slider2",
                   src="https://static.wixstatic.com/media/e9606e_3057be61ba094ba684ac33e852ff4702~mv2.png"),
            html.Img(className="Imagen_slider3",
                   src="https://static.wixstatic.com/media/e9606e_a01463d424f8451b93e125b093aa2a71~mv2.png"),
            html.Img(className="Imagen_slider4",
                   src="https://static.wixstatic.com/media/e9606e_0c228475e917406f9367b43a79ffdf6d~mv2.png"),
            html.Img(className="Imagen_slider5",
                   src="https://static.wixstatic.com/media/e9606e_7f2dde5a4cc541859bdf5599d4b2562d~mv2.png"),
            html.Img(className="Imagen_slider6",
                   src="https://static.wixstatic.com/media/e9606e_adf6f666ace4425f9aca6cdf6dd0c732~mv2.png"),
            html.Img(className="Imagen_slider7",
                   src="https://static.wixstatic.com/media/e9606e_a01463d424f8451b93e125b093aa2a71~mv2.png"),
            html.Img(className="Imagen_slider8",
                   src="https://static.wixstatic.com/media/e9606e_a01463d424f8451b93e125b093aa2a71~mv2.png"),            
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
        ), # AQUI TERMINA EL SLIDER LA CONFIGURACIÓN SE DEJA TAL CUAL
        dbc.Row([
            # COLUMNA DONDE ESTÁ LA SELECCIÓN DE REGIÓN Y TIENDA
            dbc.Col([
                html.H5('Seleccione Región:'),
                dcc.RadioItems(
                    id='selector_region',
                    options=[
                    {'label': 'REGIÓN CALI', 'value': 'REGION CALI'},
                    {'label': 'REGIÓN MEDELLÍN', 'value': 'REGION MEDELLIN'},
                    ],value='REGION CALI', labelStyle={'display': 'block'}
                    ),
                br,
                html.H5('Seleccione Tienda:'),
                dcc.Dropdown(
                    id='dropdown_tienda',
                    options=[],
                    placeholder="Seleccione Tienda"
                    ),
                br,
                html.Center(children=[  
                    dcc.Graph(id='mapa_tiendas', figure={}),
                    ]),
                ],style=mini_container,width=4),
            # COLUMNA DONDE APARECEN LAS RECOMENDACIONES
            dbc.Col([
                html.Div(id='area_recomendaciones', children=[])
                ],style=mini_container),
            ]),
        # NUEVA FILA DONDE ESTÁ EL BOX VACÍO Y EL MAPA
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
                    dcc.Graph(id='mapa_tiendas_', figure={}),
                    ]),
                ],style=mini_container),
            ]),
        ]), # AQUI TERMINA LA SEGUNDA FILA DONDE ESTÁ EL MAPA
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
    [
    Output(component_id="dropdown_tienda",component_property="options"),
    Output(component_id="dropdown_tienda",component_property="value")
    ],
    [
    Input(component_id="selector_region",component_property="value")
    ]
)

def actualizar_selec_region(region_s):
    if str(region_s) == "REGION CALI":
        df_temp = df.copy()
        lista_cali = list(df_temp[df_temp['Region'] == 'region cali']['Tienda'].unique())
        dropdown_dict = [{"label":str(i)+' - '+str(df[df['Tienda'] == i]['Nombre Tienda'].\
            iloc[0]),"value":str(i)} for i in recomendacion[recomendacion['usuario'].isin(lista_cali)]['usuario'].unique()]
        valor_default_tiendas = recomendacion[recomendacion['usuario'].isin(lista_cali)]['usuario'].unique()[0]
        return dropdown_dict, valor_default_tiendas
    elif str(region_s) == "REGION MEDELLIN":
        df_temp = df.copy()
        lista_medellin = list(df_temp[df_temp['Region'] == 'region medellin']['Tienda'].unique())
        dropdown_dict = [{"label":str(i)+' - '+str(df[df['Tienda'] == i]['Nombre Tienda'].\
            iloc[0]),"value":str(i)} for i in recomendacion[recomendacion['usuario'].isin(lista_medellin)]['usuario'].unique()]
        valor_default_tiendas = recomendacion[recomendacion['usuario'].isin(lista_medellin)]['usuario'].unique()[0]
        return dropdown_dict, valor_default_tiendas


@app.callback(
    Output(component_id='area_recomendaciones', component_property="children"),
    [
    Input(component_id="dropdown_tienda", component_property="value"),
    ],
)

def update_radio_rec_system(input_tienda):
    #calculo de top productos mas pedidos por la tienda seleccionada
    top_productos = df[df['Tienda']==int(input_tienda)][['Nombre Material','Pedido']].groupby(['Nombre Material'], as_index=False).count()
    top_productos = top_productos.sort_values(by='Pedido', ascending=False).reset_index().head(10)
    top_productos = top_productos['Nombre Material'].tolist()

    list_custom = recomendacion[(recomendacion['usuario']==int(input_tienda)) & (recomendacion['Tipo R']=='Custom')]
    list_custom = list_custom.iloc[0,2:].tolist()
    list_custom = [x.capitalize() for x in list_custom]
    
    list_region = recomendacion[(recomendacion['usuario']==int(input_tienda)) & (recomendacion['Tipo R']=='Region')]
    list_region = list_region.iloc[0,2:].tolist()
    list_region = [x.capitalize() for x in list_region]
    
    list_cluster = recomendacion[(recomendacion['usuario']==int(input_tienda)) & (recomendacion['Tipo R']=='Cluster')]
    list_cluster = list_cluster.iloc[0,2:].tolist()
    list_cluster = [x.capitalize() for x in list_cluster]

    
    tablas_rec = html.Div(children=[
        html.H4(className="h4-title", children="Productos más comprados por ti", style={'font-weight':'bold'}),
        #dbc.Table.from_dataframe(top_productos, striped=True, bordered=True, size='sm', hover=True, dark=True),
        crear_carousel(top_productos), br,

        html.H4(className="h4-title", children="Recomendados especiales para ti", style={'font-weight':'bold'}),
        crear_carousel(list_custom), br,

        html.H4(className="h4-title", children="Productos comprados por usuarios parecidos a tí", style={'font-weight':'bold'}),
        crear_carousel(list_cluster), br,

        html.H4(className="h4-title", children="Productos más populares en tu región", style={'font-weight':'bold'}),
        crear_carousel(list_region), br,
        ])

    return tablas_rec

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