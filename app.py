import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

st.set_page_config(page_title="PowerTech Motor", layout="centered")

st.markdown("<h1 style='text-align: center; color: gold;'>PowerTech Motor</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gold;'>Control de Mantenimiento</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Ing. Ronny Calva</p>", unsafe_allow_html=True)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Conexión con Google Sheets por KEY
sheet = client.open_by_key("1Fmwe1G9mM6WQlRb4QIHq4FIoZYl2Jm3-")
worksheet = sheet.sheet1

menu = st.selectbox("Selecciona una opción", ["Buscar Vehículo", "Agregar Vehículo"])

if menu == "Buscar Vehículo":
    placa = st.text_input("Ingrese la placa del vehículo:").upper()
    if placa:
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        resultado = df[df["Placa"] == placa]
        if not resultado.empty:
            st.dataframe(resultado)
            if st.button("Eliminar registro"):
                idx = resultado.index[0]
                worksheet.delete_row(idx + 2)
                st.success("Registro eliminado")
            else:
                for i, row in resultado.iterrows():
                    for col in df.columns:
                        new_val = st.text_input(f"{col}", row[col], key=f"{col}-{i}")
                        df.at[i, col] = new_val
                if st.button("Guardar cambios"):
                    idx = resultado.index[0]
                    for col_idx, col in enumerate(df.columns):
                        worksheet.update_cell(idx + 2, col_idx + 1, df.at[idx, col])
                    st.success("Cambios guardados")
        else:
            st.warning("🚫 No se encontró esa placa en la base de datos.")

elif menu == "Agregar Vehículo":
    with st.form("registro_form"):
        placa = st.text_input("Placa").upper()
        marca = st.text_input("Marca")
        modelo = st.text_input("Modelo")
        km = st.text_input("Kilometraje")
        fecha = st.date_input("Fecha de ingreso")
        tipo = st.text_input("Tipo de servicio")
        obs = st.text_area("Observaciones")
        tecnico = st.text_input("Técnico responsable")
        cliente = st.text_input("Nombre de cliente")
        cedula = st.text_input("Número de cédula")
        telefono = st.text_input("Teléfono")
        submitted = st.form_submit_button("Guardar")

        if submitted:
            values = [placa, marca, modelo, km, str(fecha), tipo, obs, tecnico, cliente, cedula, telefono]
            worksheet.append_row(values)
            st.success("Registro guardado exitosamente")
