import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title('Grupo 1 - PUCP Python')

def reset_1():
    st.session_state['ubigeo'] = None

df = pd.read_csv(r"/mount/src/dashboaard/Data/TB_CENTRO_VACUNACION.csv",
                 sep = ";")

df_1 = pd.read_csv(r"/mount/src/dashboaard/Data/TB_UBIGEOS.csv",
                 sep = ";")
# df = pd.read_csv(r"Data/TB_CENTRO_VACUNACION.csv",
#                  sep = ";")

# df_1 = pd.read_csv(r"Data/TB_UBIGEOS.csv",
#                  sep = ";")

df.rename(columns={"latitud": "lat", "longitud": "lon"}, inplace=True)
df['lat'] = df['lat'].astype(float)
df['lon'] = df['lon'].astype(float)


df = df[(df['lat'].between(-90, 90)) & (df['lon'].between(-180, -45))]
df = df[~((df['lat'] == 0) & (df['lon'] == 0))]

df_2 = pd.merge(df, df_1, on='id_ubigeo', how='inner')


# Función para mostrar solo la etiqueta en el selectbox
# def format_option(option):
#     # Buscar la etiqueta correspondiente al ID seleccionado
#     etiqueta = df_2[df_2['id_ubigeo'] == option]['ubigeo_inei'].astype(str).iloc[0]
#     # Asumiendo que las etiquetas son numéricas o que deseas tratarlas como tal para formatear
#     etiqueta_formateada = etiqueta.zfill(6)
#     return etiqueta_formateada

def format_option(option):
    # Buscar la etiqueta y la información adicional correspondiente al ID seleccionado
    row = df_2[df_2['id_ubigeo'] == option]
    etiqueta = row['ubigeo_inei'].astype(str).iloc[0]
    etiq_depa = row['departamento'].iloc[0]
    etiqueta_formateada = etiqueta.zfill(6)
    # Concatenar la etiqueta con la información adicional
    etiqueta_concatenada = f"{etiqueta_formateada} - {etiq_depa}"
    return etiqueta_concatenada



col1, col2 = st.columns(2)

with col1:

    st.title("Centros de Vacunación COVID-19")
    ubigeo  = st.selectbox(
        "Buscar por Ubigeo",
    options = df_2["id_ubigeo"].unique(),
    index = None,
    format_func = format_option,
    key='ubigeo',
    placeholder = "Seleccione Ubigeo",
    )

    # Filtramos el DataFrame basado en el ubigeo seleccionado
    df_2 = df_2[df_2["id_ubigeo"] == ubigeo]

    departamento  = st.selectbox(
        "Buscar por Departamento",
    df_2["departamento"].unique(),
    index = None,
    placeholder = "Seleccione Departamento",
    #    on_change = reset_1
    )

    # Filtramos el DataFrame basado en el ubigeo seleccionado
    df_2 = df_2[df_2["departamento"] == departamento]

    provincia  = st.selectbox(
        "Buscar por provincia",
    df_2["provincia"].unique(),
    index = None,
    placeholder = "Seleccione provincia",
    #   on_change = reset_1
    )
    # Filtramos el DataFrame basado en el ubigeo seleccionado
    df_2= df_2[df_2["provincia"] == provincia]
    distrito  = st.selectbox(
        "Buscar por distrito",
    df_2["distrito"].unique(),
    index = None,
    placeholder = "Seleccione distrito",
    # on_change = reset_1
    )

# if departamento != None:
#     df_2 = df_2[((df_2['departamento'] == departamento))]

# if provincia != None:
#     df_2 = df_2[((df_2['provincia'] == provincia))]

# if distrito != None:
#     df_2 = df_2[((df_2['distrito'] == distrito))]

# if ubigeo != None:
#     df_2 = df_2[((df_2['id_ubigeo'] == ubigeo))]

st.set_page_config(layout="wide")
st.write(df_2[["id_centro_vacunacion", "ubigeo_inei", "nombre","departamento", "provincia", "distrito"]])

with col2:
    if not df.empty:
        st.map(df_2[["lat", "lon"]])
    else:
        st.write("No hay datos válidos para mostrar en el mapa.")
