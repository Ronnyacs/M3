import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

st.set_page_config(page_title="PowerTech Motor", layout="centered")

st.markdown("""
<h1 style='color:gold;text-align:center;'>PowerTech Motor</h1>
<h3 style='color:white;text-align:center;'>Control de Mantenimiento</h3>
<h5 style='color:gray;text-align:center;'>Ing. Ronny Calva</h5>
""", unsafe_allow_html=True)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Fmwe1G9mM6WQlRb4QIHq4FIoZYl2Jm3-/edit")
worksheet = sheet.get_worksheet(0)

def get_data():
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def update_sheet(df):
    worksheet.clear()
    worksheet.append_row(df.columns.tolist())
    for row in df.values.tolist():
        worksheet.append_row(row)

df = get_data()

menu = st.radio("Opciones", ["Buscar / Editar / Eliminar", "Agregar nuevo registro"], horizontal=True)

if menu == "Buscar / Editar / Eliminar":
    placa = st.text_input("Buscar por placa:", "").upper()
    if placa:
        result = df[df["Placa"] == placa]
        if not result.empty:
            edited = {}
            st.subheader("Datos del vehículo")
            for column in df.columns:
                new_value = st.text_input(f"{column}:", result.iloc[0][column])
                edited[column] = new_value
            if st.button("Guardar cambios"):
                idx = df[df["Placa"] == placa].index[0]
                for key in edited:
                    df.at[idx, key] = edited[key]
                update_sheet(df)
                st.success("Registro actualizado correctamente.")
            if st.button("Eliminar registro"):
                df = df[df["Placa"] != placa]
                update_sheet(df)
                st.warning("Registro eliminado.")
        else:
            st.error("Placa no encontrada.")

if menu == "Agregar nuevo registro":
    st.subheader("Datos del vehículo y cliente")
    new_data = {}
    for field in df.columns:
        new_data[field] = st.text_input(field)
    if st.button("Agregar"):
        df = df.append(new_data, ignore_index=True)
        update_sheet(df)
        st.success("Registro agregado correctamente.")
