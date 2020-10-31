import base64
import io
import pathlib

import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
import numpy as np
from scipy import stats

import seaborn as sns
import json
import os


df_orig = pd.read_csv("datos_con_coordenadas_v1 (1).csv", compression='gzip', low_memory=False)
df = df_orig.copy() 

def set_mes_number(x):
    mes_dic = {'Enero 2019':1, 'Abril 2019':4, 'Mayo 2019':5, 'Noviembre 2019':11,
       'Diciembre 2019':12, 'Junio 2020':18, 'Agosto 2020':20, 'Enero 2020':13,
       'Febrero 2020':14, 'Febrero 2019':2, 'Julio 2019':7, 'Septiembre 2019':9,
       'Marzo 2020':15, 'Marzo 2019':3, 'Mayo 2020':17, 'Abril 2020':16,
       'Octubre 2019':10, 'Julio 2020':19, 'Junio 2019':6, 'Agosto 2019':8}
    
    return mes_dic[x]
    
df['mes_number'] = df['MES'].apply(set_mes_number)

# Se agregó una columna mes_number que indica el número exacto del mes entre 1 y 20 para los 20 meses usados

df_top_ventas = df[df['Region']=='region cali'][['Cantidad de pedido','Pedido','Valor Unitario Pedido', 'UM', 'Nombre Fabricante', 'NOMBRE SUB','Valor TotalFactura','Nombre Material']].groupby('Nombre Material', as_index=False).agg({
        'Cantidad de pedido':'sum', 
        'Valor Unitario Pedido':'sum', 
        'UM':'max',
        'Pedido':'count',
        'Nombre Fabricante':'max',
        'NOMBRE SUB':'max',
        'Valor TotalFactura':'sum'})

df_top_ventas_cantidad = df_top_ventas.sort_values(by='Cantidad de pedido', ascending=False).reset_index()
df_top_ventas_valortotal = df_top_ventas.sort_values(by='Valor TotalFactura', ascending=False).reset_index()
df_top_ventas_registros = df_top_ventas.sort_values(by='Pedido', ascending=False).reset_index()

input_tienda = 20000541
dfsbar = df[df['Tienda']==input_tienda]

dropdown_dict = [{"label":str(df[df['Tienda'] == i]['Region'].iloc[0]).upper()+' - '+str(i)+' - '+str(df[df['Tienda'] == i]['Nombre Tienda'].iloc[0]).upper(),
                  "value":str(i)} for i in df['Tienda'].unique()]

Nombre_Tienda = df[df['Tienda']==int(input_tienda)]['Nombre Tienda'].max()
dfsbar = df[df['Tienda']==input_tienda]
dfsbar =pd.crosstab(dfsbar['mes_number'], dfsbar['NOMBRE SUB']).reset_index()
fig = px.bar(dfsbar, x="mes_number", y=dfsbar.columns, title="Evolución tienda: "+ Nombre_Tienda)

dfsbar = df[df['Tienda']==20000541]
dfsbar =pd.crosstab(dfsbar['mes_number'], dfsbar['NOMBRE SUB']).reset_index()
figx = px.bar(dfsbar, x="mes_number", y=dfsbar.columns, title="Evolución mensual de productos ordenados por categoria para una tienda")

mini_container = {
  'border-radius': '5px',
  'background-color': '#f9f9f9',
  'margin': '10px',
  'padding': '5px',
  'position': 'relative',
  'box-shadow': '2px 2px 2px lightgrey',
}

df_temp = df_top_ventas_cantidad.copy()

## --------------- Esta es la configuración de los Cuadros de recomendación de productos populares

lista_cards2 = []
list_of_outputs_pop_prod = []

for i in range(10):
  lista_cards2.append(dbc.Card([
    dbc.CardHeader(f"Recomendación # {i+1}"),
    dbc.CardBody([
      html.H5(children="Subcategoria: "+ str(df_temp.loc[i,'NOMBRE SUB']).capitalize() , className="card-title", id=f'rec{i+1}-subcategoria{i+1}'),
      html.H6(children=str(df_temp.loc[i,'Nombre Material']).capitalize(), className="card-subtitle", id=f'rec{i+1}-producto{i+1}'),
      html.P(children="Fabricante: " + str(df_temp.loc[i,'Nombre Fabricante']).capitalize() , className="card-text", id=f'rec{i+1}-fabricante{i+1}'),
      ])],
    style={"width": "15rem"}, color='info', outline=True))

  list_of_outputs_pop_prod.append(Output(component_id=f'rec{i+1}-subcategoria{i+1}',component_property="children"))
  list_of_outputs_pop_prod.append(Output(component_id=f'rec{i+1}-producto{i+1}',component_property="children"))
  list_of_outputs_pop_prod.append(Output(component_id=f'rec{i+1}-fabricante{i+1}',component_property="children"))

list_of_outputs_pop_prod.append(Output(component_id='Tabla_top', component_property="children"))

# card=   dbc.Card([
#             dbc.CardHeader("Recomendación # 1"),
#             dbc.CardBody([
#                     html.H4("Subcategoria: Aseo", className="card-title"),
#                     html.H6("Blanqueador Limpido", className="card-subtitle"),
#                     html.P("Fabricante: JGB", className="card-text"),
#             ])],
#         style={"width": "14rem"}, color='info', outline=True)

lista1=  dbc.Row(
  [
  dbc.Col(lista_cards2[0]),
  dbc.Col(lista_cards2[1]),
  dbc.Col(lista_cards2[2]),
  dbc.Col(lista_cards2[3]),
  ],
  className="mb-2",)

lista2=  dbc.Row(
  [
  dbc.Col(lista_cards2[4]),
  dbc.Col(lista_cards2[5]),
  dbc.Col(lista_cards2[6]),
  dbc.Col(lista_cards2[7]),
  ],
  className="mb-2_1",)

lista3=  dbc.Row(
  [
  dbc.Col(lista_cards2[8]),
  dbc.Col(lista_cards2[9]),
  ],
  className="mb-2_1",)

br = html.Br()

# ----------------------------------------------------------------------------
#                          Inicio de la web applicatión
#-----------------------------------------------------------------------------
group_colors = {"control": "light blue", "reference": "red"}
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY], 
  meta_tags=[{"name": "viewport", "content": "width=device-width"}])

# ----------------------------------------------------------------------------
#                                   Layout HTML
#-----------------------------------------------------------------------------

# Apertura de layout y Div principal

app.layout = html.Div(children=[
    # Configuración de espacio para mensaje de error -------------------------
    html.Div(id="error-message"),
    # Banner superior del dashboard ------------------------------------------
    html.Div(
       #className="study-browser-nammer row",
       className='jumbotron',
       children=[
           # Elementos del banner superior -----------------------------------
           dbc.Row([
               dbc.Col(    
               html.Div(className=" ", children=html.Img(className=" ", 
                    src="https://teate.co/wp-content/themes/teatetheme/images/logo.png")),
                        # Cierro la imagen y el div de la imagen         
           
            width={"size": 'auto', "order": "last", "offset": 1}), # Fin de la columna 2 del banner: Logo 
                        
               
           dbc.Col(
           
               #Titulo
               html.H2(className="h2-title", children="DS4A: Teate Project. Team 45 Dashboard Web App"),
               
           width={"sm": '12', "order": "first"}), # Fin de la columna 1 del banner : Texto
               

           ], justify='around', align='center'), # Fin del row del banner superior    
               
               
       ]), #Cierro el div banner superior      
    
      
    
       # Inicio cuerpo principal ----------
    
       dbc.Container([

       # Inicio fila row1 ---  input frame ----------
           
      dbc.Row([       
           
          dbc.Col([
              html.Br(),    
              html.B(children=[
                  html.H3(className="h3-title", children="Ingrese Tienda: ", style={'font-weight':'bold'}),
                  ])
          ]),
          
        
          dbc.Col([  
          
          html.Br(),   
          dcc.Dropdown(
                id='dropdown_tienda',
                options=dropdown_dict,
                value='20000541',
                #placeholder="Seleccione cód tienda"
           ),
                            
              
           ]),
            
       ], style=mini_container), # fin fila row1 ---  input frame ----------
           
           
       html.Hr(),
           
       # Inicio fila row2 ---  cuerpo principal ----------
    
       dbc.Row([
       
           dbc.Col([
               
               #Titulo en Fila 2 - Col 1
               html.H2(className="h2-title", children="Gráfica No. 1"),
               html.H4(className="h4-title", children="Evolución de Compras", style={'font-weight':'bold'}),
               dcc.Graph(id='grafico_1', figure={}),
                
               
           ], md=6, width="auto", align='center'), # Fin de fila 2 Col 1
           
           
           dbc.Col([
            
               #Titulo en Fila 2 - Col 2

               html.H2(className="h2-title", children="Gráfica No. 2"),
               html.H4(className="h4-title", children="Evolución de Compras Cluster", style={'font-weight':'bold'}),
               dcc.Graph(id='grafico_2', figure={}),
                       
           ], md=6, width="auto"), # Fin de fila 2 Col 2
           
           html.Div(className='dropdown-menu show', children=[
                   
                   dbc.RadioItems(
                       className="example-radios-row",
                       id='menu_grafico_1',
                       options=[
                            {'label': 'Materiales ', 'value': 'Nombre Material'},
                            {'label': 'Subcategorias ', 'value': 'NOMBRE SUB'},
                            {'label': 'Categorias ', 'value': 'NOMBRE CAT'}
                        ],
                        value='NOMBRE SUB',      
                    ),
                      
               ], style=mini_container),
           
       ], align='center', justify='center'), # fin de row2 --- Cuerpo principal --------------
    
        #-------------------------------------------------------------------------------------
        #                                    inicio fila 3 Mapa
        #-------------------------------------------------------------------------------------

                    
            #html.Br(),
            html.Hr(),
            html.H2(className="h2-title", children="Gráfica No. 3"),
            html.H4(className="h4-title", children="Mapa de distribución tiendas", style={'font-weight':'bold'}),
            html.Center(children=[  
                dcc.Graph(id='grafico_3', figure={}, style={'width': '1200px', 'height': '600px'}),
                
                html.H4(className="h4-title", children="Productos más populares", style={'font-weight':'bold'}),
                br,
                dbc.RadioItems(
                   className="example-radios-row",
                   id='radio_tipo_top_products',
                   options=[
                        {'label': 'Por cantidad vendida', 'value': '1'},
                        {'label': 'Por valor ventas', 'value': '2'},
                        {'label': 'Por Pedidos donde aparece ', 'value': '3'}
                    ],
                    value='1',
                    inline=True
                ), 

            
                
                br, lista1, br, lista2, br, lista3
                      
            ]),
           
           
            
       
        #-------------------------------------------------------------------------------------
        #                                    inicio fila 4 tablas
        #-------------------------------------------------------------------------------------
           
        html.Br(),
        html.Br(), 
        html.Hr(),
        html.H2(className="h2-title", children="Tabla No. 1"),
        html.H4(className="h4-title", children="Resumen tiendas", style={'font-weight':'bold'}),

        dbc.Row([
        html.Div(children=[
             
          #  dash_table.DataTable(id='tabla_tienda',
          #                      columns=[{'name':i, 'id':i} for i in lista_cols_tabla],
          #                      data= df_tiendas_table.head(5).to_dict('records'),
          #                      ),
        
            html.Br(),
            html.Div(id='Tabla_top')
            
           
        ])     
       ], align='center', justify='center', style=mini_container), # fin de row3 --- Cuerpo principal --------------
    
       
         #-------------------------------------------------------------------------------------
        #                                    inicio fila 5 Recomendaciones
        #-------------------------------------------------------------------------------------
           

        html.Br(),
        html.Br(), 
        html.Hr(),
        html.H2(className="h2-title", children="Recomendaciones Filtrado colaborativo"),
        html.H4(className="h4-title", children="Sistema version 1: _______", style={'font-weight':'bold'}),
        html.Br(),
        html.Br(), 
        html.Br(),
        html.Br(), 
        
                   
           
           
       ], ) # Fin del container del body -------------------------------------------------------

    ]) # Cierro el div principal



# ----------------------------------------------------------------------------
#                             Callbacks e interactividad
#-----------------------------------------------------------------------------



@app.callback(
    
        Output(component_id="grafico_1",component_property="figure"),
    [
        Input(component_id="dropdown_tienda", component_property="value"),
        Input(component_id="menu_grafico_1", component_property="value"),
    ],
)
def grafico_categorias_tienda(input_tienda,filtro):
    
    Nombre_Tienda = df[df['Tienda']==int(input_tienda)]['Nombre Tienda'].max()
    
    dfsbar = df[df['Tienda']==int(input_tienda)]
    dfsbar =pd.crosstab(dfsbar['mes_number'], dfsbar[filtro]).reset_index()
    fig_cat_tienda = px.bar(dfsbar, x="mes_number", y=dfsbar.columns, title=("Evolución compras "+ Nombre_Tienda))
    fig_cat_tienda.update_layout(
        title=Nombre_Tienda,
    )
    
    #fig_cat_tienda.show()
    
    
    return fig_cat_tienda



@app.callback(
    
        Output(component_id="grafico_2",component_property="figure"),
    
    [
        Input(component_id="dropdown_tienda", component_property="value"),
        Input(component_id="menu_grafico_1", component_property="value"),
    ],
)
def grafico_categorias_tienda_cluster(input_tienda,filtro):
    
    Nombre_Tienda = df[df['Tienda']==int(input_tienda)]['Nombre Tienda'].max()
    
    dfsbar2 = df[df['Tienda']==int(input_tienda)]
    dfsbar2 =pd.crosstab(dfsbar2['mes_number'], dfsbar2[filtro]).reset_index()
    fig_cat_tienda_cluster = px.bar(dfsbar2, x="mes_number", y=dfsbar2.columns, title=("Evolución compras "+ Nombre_Tienda))
    fig_cat_tienda_cluster.update_layout(
        title=Nombre_Tienda,
    )
    
    #fig_cat_tienda.show()
    
    
    return fig_cat_tienda_cluster



@app.callback(
    
        Output(component_id="grafico_3",component_property="figure"),

    
    [
        Input(component_id="dropdown_tienda", component_property="value"),
    ],
)
def grafico_mapa(input_tienda):
    
    #tiendas_df = df[df['Region']=='region cali'][['longitude','latitude','lealtad','Nombre Tienda']].groupby('Nombre Tienda', as_index=False).max()
    #center_lat = tiendas_df.latitude.mean()
    #center_lon = tiendas_df.longitude.mean()
    
    tiendas_df = df[['longitude','latitude','lealtad','Tienda','Nombre Tienda']].groupby('Nombre Tienda', as_index=False).max()
    print(input_tienda)
    center_lat = tiendas_df[tiendas_df['Tienda'] == int(input_tienda)]['latitude'].mean()
    center_lon = tiendas_df[tiendas_df['Tienda'] == int(input_tienda)]['longitude'].mean()

    print(center_lat, ',', center_lon)
    
    map_box_access_token = "pk.eyJ1IjoiaHVtYmVydG9jcnYiLCJhIjoiY2tnbG5xZWpyMTJhdzJycGVyamZma2FjYyJ9.juzkmatkYaLTmiprDJCD0w"
    px.set_mapbox_access_token(map_box_access_token)
    fig_map = px.scatter_mapbox(tiendas_df, center=go.layout.mapbox.Center(lat=center_lat, lon=center_lon), 
      lat='latitude', 
      lon='longitude',   
      color="lealtad", 
      color_continuous_scale=px.colors.cyclical.IceFire, 
      hover_name="Nombre Tienda", 
      size_max=100, zoom=18
      )
           
    return fig_map





#-------------------------------------------------------------------------------------------!!!!!!!!!!!!!!!!!!!!
#html.H5(id='rec1-subcategoria1'),
#html.H6(id='rec1-producto1'),
#html.P(id='rec1-fabricante1'),

@app.callback(
    list_of_outputs_pop_prod,
    [
        Input(component_id="radio_tipo_top_products", component_property="value"),
    ],
)
def update_radio_top_products(input):
    
    if input == '1':
            df_temp = df_top_ventas_cantidad.copy()
    elif input =='2':
            df_temp = df_top_ventas_valortotal.copy()
    else:
            df_temp = df_top_ventas_registros.copy()      
        

    output1= "Subcategoria: "+ str(df_temp.loc[0,'NOMBRE SUB']).capitalize()
    output2= str(df_temp.loc[0,'Nombre Material']).capitalize()
    output3= "Fabricante: " + str(df_temp.loc[0,'Nombre Fabricante']).capitalize()

    output4= "Subcategoria: "+ str(df_temp.loc[1,'NOMBRE SUB']).capitalize()
    output5= str(df_temp.loc[1,'Nombre Material']).capitalize()
    output6= "Fabricante: " + str(df_temp.loc[1,'Nombre Fabricante']).capitalize()

    output7= "Subcategoria: "+ str(df_temp.loc[2,'NOMBRE SUB']).capitalize()
    output8= str(df_temp.loc[2,'Nombre Material']).capitalize()
    output9= "Fabricante: " + str(df_temp.loc[2,'Nombre Fabricante']).capitalize()

    output10= "Subcategoria: "+ str(df_temp.loc[3,'NOMBRE SUB']).capitalize()
    output11= str(df_temp.loc[3,'Nombre Material']).capitalize()
    output12= "Fabricante: " + str(df_temp.loc[3,'Nombre Fabricante']).capitalize()

    output13= "Subcategoria: "+ str(df_temp.loc[4,'NOMBRE SUB']).capitalize()
    output14= str(df_temp.loc[4,'Nombre Material']).capitalize()
    output15= "Fabricante: " + str(df_temp.loc[4,'Nombre Fabricante']).capitalize()

    output16= "Subcategoria: "+ str(df_temp.loc[5,'NOMBRE SUB']).capitalize()
    output17= str(df_temp.loc[5,'Nombre Material']).capitalize()
    output18= "Fabricante: " + str(df_temp.loc[5,'Nombre Fabricante']).capitalize()

    output19= "Subcategoria: "+ str(df_temp.loc[6,'NOMBRE SUB']).capitalize()
    output20= str(df_temp.loc[6,'Nombre Material']).capitalize()
    output21= "Fabricante: " + str(df_temp.loc[6,'Nombre Fabricante']).capitalize()

    output22= "Subcategoria: "+ str(df_temp.loc[7,'NOMBRE SUB']).capitalize()
    output23= str(df_temp.loc[7,'Nombre Material']).capitalize()
    output24= "Fabricante: " + str(df_temp.loc[7,'Nombre Fabricante']).capitalize()

    output25= "Subcategoria: "+ str(df_temp.loc[8,'NOMBRE SUB']).capitalize()
    output26= str(df_temp.loc[8,'Nombre Material']).capitalize()
    output27= "Fabricante: " + str(df_temp.loc[8,'Nombre Fabricante']).capitalize()

    output28= "Subcategoria: "+ str(df_temp.loc[9,'NOMBRE SUB']).capitalize()
    output29= str(df_temp.loc[9,'Nombre Material']).capitalize()
    output30= "Fabricante: " + str(df_temp.loc[9,'Nombre Fabricante']).capitalize()

    return output1, output2, output3, output4, output5, output6, output7, output8, output9, output10, output11, output12, output13, output14, output15, output16, output17, output18, output19, output20, output21, output22, output23, output24, output25, output26, output27, output28, output29, output30, dbc.Table.from_dataframe(df_temp.head(10), striped=True, bordered=True, size='sm', hover=True)
            


# Código de ejecución de la aplicación en el servidor --------------------------

if __name__=='__main__':
    app.run_server(host='0.0.0.0', port='8050', debug=True)