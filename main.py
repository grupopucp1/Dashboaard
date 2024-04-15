import streamlit as st
import pandas as pd
import numpy as np

st.title('Grupo 1 - PUCP Python')
st.write('¡Hola!')

def reset_1():
    st.session_state['ubigeo'] = None

df = pd.read_csv(r"Data\TB_CENTRO_VACUNACION.csv",
                 sep = ";")

df_1 = pd.read_csv(r"Data\TB_UBIGEOS.csv",
                 sep = ";")


df.rename(columns={"latitud": "lat", "longitud": "lon"}, inplace=True)
df['lat'] = df['lat'].astype(float)
df['lon'] = df['lon'].astype(float)


df = df[(df['lat'].between(-90, 90)) & (df['lon'].between(-180, -45))]
df = df[~((df['lat'] == 0) & (df['lon'] == 0))]

df_2 = pd.merge(df, df_1, on='id_ubigeo', how='inner')

st.title("Centros de Vacunación COVID-19")
ubigeo  = st.selectbox(
    "Buscar por Ubigeo",
   df_2["id_ubigeo"].unique(),
   index = None,
   key='ubigeo',
   placeholder = "Seleccione Ubigeo",
)

departamento  = st.selectbox(
    "Buscar por Departamento",
   df_2["departamento"].unique(),
   index = None,
   placeholder = "Seleccione Departamento",
   on_change = reset_1
)

provincia  = st.selectbox(
    "Buscar por provincia",
   df_2["provincia"].unique(),
   index = None,
   placeholder = "Seleccione provincia",
   on_change = reset_1
)

distrito  = st.selectbox(
    "Buscar por distrito",
   df_2["distrito"].unique(),
   index = None,
   placeholder = "Seleccione distrito",
   on_change = reset_1
)

if departamento != None:
    df_2 = df_2[((df_2['departamento'] == departamento))]

if provincia != None:
    df_2 = df_2[((df_2['provincia'] == provincia))]

if distrito != None:
    df_2 = df_2[((df_2['distrito'] == distrito))]

if ubigeo != None:
    df_2 = df_2[((df_2['id_ubigeo'] == ubigeo))]

col1, col2 = st.columns(2)

with col1:
    st.write(df_2.head())

with col2:
    if not df.empty:
        st.map(df_2[["lat", "lon"]])
    else:
        st.write("No hay datos válidos para mostrar en el mapa.")