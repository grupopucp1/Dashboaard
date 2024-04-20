import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title   = "Centros de Vacunación", 
                   page_icon    = ":syringe:",
                   layout       = "wide")

st.title('Grupo 1 - PUCP Python')

df = pd.read_csv(r"/mount/src/dashboaard/Data/TB_CENTRO_VACUNACION.csv",
                 sep = ";")

df_1 = pd.read_csv(r"/mount/src/dashboaard/Data/TB_UBIGEOS.csv",
                 sep = ";")


# Convertir cadenas vacías y otros posibles valores vacíos a NaN
df.replace(['', None, 'NA'], np.nan, inplace=True)
df_1.replace(['', None, 'NA'], np.nan, inplace=True)


df.rename(columns={"latitud": "lat", "longitud": "lon"}, inplace=True)
df['lat'] = df['lat'].astype(float)
df['lon'] = df['lon'].astype(float)

df = df[(df['lat'].between(-90, 90)) & (df['lon'].between(-180, -45))]
df = df[~((df['lat'] == 0) & (df['lon'] == 0))]

df_2 = pd.merge(df, df_1, on='id_ubigeo', how='inner')

# Aplicar filtro para eliminar las coordenadas específicas
df_2 = df_2[~((df_2['lat'] == -11.69362300) & (df_2['lon'] == -78.60168760))]
df_2 = df_2[~((df_2['lat'] == -14.14865833) & (df_2['lon'] == -76.26907333))]
df_2 = df_2[~((df_2['lat'] == -8.98800646) & (df_2['lon'] == -78.96392121))]

# Verificación: Imprime las filas que deberían haber sido eliminadas para confirmar que ya no están
print("Verificación de la eliminación de las coordenadas específicas:")
print(df_2[(df_2['lat'] == -11.69362300) & (df_2['lon'] == -78.60168760)])
print(df_2[(df_2['lat'] == -14.14865833) & (df_2['lon'] == -76.26907333)])
print(df_2[(df_2['lat'] == -8.98800646) & (df_2['lon'] == -78.96392121)])




df_2['ubigeo_inei'] = df_2['ubigeo_inei'].astype(str).apply(lambda x: x.zfill(6))

df_2["concat"] = df_2["ubigeo_inei"] + " - "+  df_2["departamento"] + " - " +df_2["provincia"] + " - " + df_2["distrito"]

#def format_option(option):
    # Buscar la etiqueta y la información adicional correspondiente al ID seleccionado
#    row = df_2[df_2['id_ubigeo'] == option]
#    etiqueta = row['ubigeo_inei'].astype(str).iloc[0]
#    etiq_depa = row['departamento'].iloc[0]
#    etiq_prov = row['provincia'].iloc[0]
#    etiq_dist = row['distrito'].iloc[0]
#    etiqueta_formateada = etiqueta.zfill(6)
    # Concatenar la etiqueta con la información adicional
#    etiqueta_concatenada = f"{etiqueta_formateada} - {etiq_depa} - {etiq_prov} - {etiq_dist}"
#    return etiqueta_concatenada

def reset_ubi():
    st.session_state['ubigeo'] = None

def reset_dep():
    st.session_state['departamento'] = None
    st.session_state['provincia'] = None
    st.session_state['distrito'] = None

if 'departamento' not in st.session_state:
    st.session_state['departamento'] = None
if 'provincia' not in st.session_state:
    st.session_state['provincia'] = None

def act_dep_fr_prov():
    st.session_state['ubigeo'] = None
    if 'provincia' in st.session_state and st.session_state['provincia']:
        selected_provincia = st.session_state['provincia']
        departamento = df_2[df_2['provincia'] == selected_provincia]['departamento']
        if not departamento.empty:
            st.session_state['departamento'] = departamento.unique()[0]
        else:
            st.session_state['departamento'] = None
        st.session_state['provincia'] = selected_provincia

def act_dep_prov_fr_dis():
    st.session_state['ubigeo'] = None
    if 'distrito' in st.session_state and st.session_state['distrito']:
        selected_distrito = st.session_state['distrito']
        departamento = df_2[df_2['distrito'] == selected_distrito]['departamento']
        provincia = df_2[df_2['distrito'] == selected_distrito]['provincia']

        if not departamento.empty:
            st.session_state['departamento'] = departamento.unique()[0]
        else:
            st.session_state['departamento'] = None
        if not provincia.empty:
            st.session_state['provincia'] = provincia.unique()[0]
        else:
            st.session_state['provincia'] = None

        st.session_state['distrito'] = selected_distrito


departamento_options = df_2['departamento'].unique()

st.header("Centros de Vacunación COVID-19")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Busqueda por Ubigeo")
    ubigeo  = st.selectbox(
        "Seleccione Ubigeo",
        label_visibility = "collapsed",
        options = df_2["concat"].unique(),
        index = None,
        #format_func = format_option,
        key = 'ubigeo',
        placeholder = "Seleccione Ubigeo",
        on_change = reset_dep
    )
    
    st.divider()
    st.subheader("Busqueda por Ubicación")

    departamento  = st.selectbox(
        "Buscar por Departamento",
        label_visibility = "collapsed",
        options = df_2["departamento"].unique(),
        index = None,
        key = "departamento",
        placeholder = "Seleccione Departamento",
        on_change = reset_ubi
    )

    if departamento != None:
        df_2 = df_2[((df_2['departamento'] == departamento))]

    provincia  = st.selectbox(
            "Buscar por provincia",
            label_visibility = "collapsed",
            options = df_2["provincia"].unique(),
            index = None,
            key = "provincia",
            placeholder = "Seleccione provincia",
            on_change = act_dep_fr_prov
    )

    if provincia != None:
        df_2 = df_2[((df_2['provincia'] == provincia))]

    distrito  = st.selectbox(
            "Buscar por distrito",
            label_visibility = "collapsed",
            options = df_2["distrito"].unique(),
            index = None,
            key = "distrito",
            placeholder = "Seleccione distrito",
            on_change = act_dep_prov_fr_dis
    )

    if distrito != None:
        df_2 = df_2[((df_2['distrito'] == distrito))]

if ubigeo != None:
    df_2 = df_2[((df_2['concat'] == ubigeo))]

with col2:
    if not df.empty:
        if len(df_2)>1:
            st.write(":round_pushpin: Se encontraron {} Centros de Vacunación".format(int(len(df_2))))    
        elif len(df_2) ==1:
            st.write(":round_pushpin: Se encontró 1 Centros de Vacunación")
        else:
            st.write("No se encontraron Centros de Vacunación")

        mapa = st.map(df_2,
               latitude = "lat",
               longitude = "lon",
               color='#ff0000')
    else:
        st.write("No hay datos válidos para mostrar en el mapa.")

df_3 = df_2[["id_centro_vacunacion", "ubigeo_inei", "nombre", "departamento", "provincia", "distrito"]].copy()

df_3.rename(columns = {
    "id_centro_vacunacion": "ID Centro", 
    "ubigeo_inei": "Ubigeo",
    "nombre": "Centro de Vacunación",
    "departamento": "Departamento",
    "provincia":"Provincia",
    "distrito":"Distrito"
    }, inplace=True)



st.subheader("Detalle de resultado de búsqueda (Centros de Vacunación)")


st.dataframe(df_3.reset_index(drop=True), use_container_width=True)

