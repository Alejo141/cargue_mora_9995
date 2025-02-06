import pandas as pd
import streamlit as st
import io

st.title("Actualización de VALOR_MORA en CSV")

# Cargar archivos desde el usuario
archivo1 = st.file_uploader("Cargar archivo con 'Saldo de Factura'", type=['csv'])
archivo2 = st.file_uploader("Cargar archivo a actualizar", type=['csv'])

# Inicializar estado de sesión para los archivos
if 'archivo1' not in st.session_state:
    st.session_state.archivo1 = None
if 'archivo2' not in st.session_state:
    st.session_state.archivo2 = None
if 'output' not in st.session_state:
    st.session_state.output = None

if archivo1 and archivo2:
    st.session_state.archivo1 = archivo1
    st.session_state.archivo2 = archivo2
    
    # Leer los archivos CSV
    df1 = pd.read_csv(archivo1)
    df2 = pd.read_csv(archivo2)
    
    # Crear un diccionario para acceder rápidamente a los valores de 'Saldo de Factura'
    saldo_factura_dict = df1.set_index('NIU')['Saldo_Factura'].to_dict()
    
    # Asegurarse de que las columnas sean numéricas
    df2['VALOR_MORA'] = pd.to_numeric(df2['VALOR_MORA'], errors='coerce').fillna(0)
    
    # Actualizar el campo 'VALOR_MORA' en df2 con los valores del diccionario
    df2['VALOR_MORA'] = df2['NIU'].map(saldo_factura_dict).fillna(df2['VALOR_MORA'])
    
    # Manejar los valores vacíos o 'NA' en el campo ID_FACTURA
    df2['ID_FACTURA'] = df2['ID_FACTURA'].replace('', 'NA')
    df2['ID_FACTURA'] = df2['ID_FACTURA'].fillna('NA')
    
    # Guardar el resultado en un buffer
    output = io.BytesIO()
    df2.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)
    
    # Guardar el buffer en el estado de sesión
    st.session_state.output = output
    
    # Obtener el nombre del archivo original y modificarlo
    archivo2_nombre = "IUF1_" + archivo2.name
    
    # Botón para descargar el archivo actualizado
    st.download_button(label="Descargar archivo actualizado", data=st.session_state.output, file_name=archivo2_nombre, mime="text/csv")
    
    st.success("Actualización completada.")

# Botón para borrar los archivos cargados y el archivo a descargar
if st.button("Borrar archivos"):
    st.session_state.archivo1 = None
    st.session_state.archivo2 = None
    st.session_state.output = None
    st.rerun()