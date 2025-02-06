import pandas as pd
import streamlit as st
import io

st.title("Generar formato IUF1")

# Cargar archivos desde el usuario
archivo1 = st.file_uploader("Cargar archivo de la Mora", type=['csv'])
archivo2 = st.file_uploader("Cargar archivo a actualizar", type=['csv'])

# Botón para realizar el cruce de los archivos
if archivo1 and archivo2:
    if st.button("Realizar Cruce"):
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
        
        # Obtener el nombre del archivo original y modificarlo
        archivo2_nombre = "IUF1_" + archivo2.name
        
        # Botón para descargar el archivo actualizado
        st.download_button(label="Descargar archivo actualizado", data=output, file_name=archivo2_nombre, mime="text/csv")
        
        st.success("Actualización completada.")
