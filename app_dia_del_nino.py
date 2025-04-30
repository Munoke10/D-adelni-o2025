
import streamlit as st
from PIL import Image
import pandas as pd
import openpyxl
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Registro Día del Niño", page_icon="🎈", layout="centered")

# Cargar logo
if os.path.exists("LOGO DE BATESVILLE 2024.png"):
    st.image("LOGO DE BATESVILLE 2024.png", width=200)

st.title("🎉 Registro de Empleados e Invitados - Día del Niño 2.0")

# Archivos
archivo_excel = "BaseDatos_DiaDelNino_{}.xlsx".format(datetime.now().strftime("%Y%m%d"))
archivo_empleados = "empleados.xlsx"

# Crear archivo Excel si no existe
if not os.path.exists(archivo_excel):
    df_base = pd.DataFrame(columns=["Número de Empleado", "Nombre", "Área", "Turno", "Fecha", "Hora"] + [f"Invitado {i}" for i in range(1, 11)])
    df_base.to_excel(archivo_excel, index=False)

# Leer archivo de empleados
df_empleados = pd.DataFrame()
if os.path.exists(archivo_empleados):
    df_empleados = pd.read_excel(archivo_empleados)

# Formulario
with st.form("registro_formulario"):
    num_empleado = st.text_input("Número de Empleado:", max_chars=10)
    nombre = ""
    area = ""
    turno = ""

    if num_empleado and df_empleados.shape[0] > 0:
        empleado = df_empleados[df_empleados["Número de Empleado"].astype(str) == num_empleado]
        if not empleado.empty:
            nombre = empleado.iloc[0]["Nombre Completo"]
            area = empleado.iloc[0]["Área"]
            turno = empleado.iloc[0]["Turno"]
        else:
            st.warning("Empleado no encontrado.")

    st.text_input("Nombre:", value=nombre, disabled=True)
    st.text_input("Área:", value=area, disabled=True)
    st.text_input("Turno:", value=turno, disabled=True)

    invitados = []
    st.markdown("### Invitados")
    for i in range(10):
        invitado = st.text_input(f"Invitado {i+1}:", key=f"invitado_{i}")
        if invitado:
            invitados.append(invitado)

    submitted = st.form_submit_button("Registrar")

    if submitted:
        if not nombre or not area or not turno:
            st.error("Primero busca un número de empleado válido.")
        else:
            df = pd.read_excel(archivo_excel)
            if num_empleado in df["Número de Empleado"].astype(str).values:
                st.error("Este número de empleado ya está registrado.")
            else:
                fecha = datetime.now().strftime("%d/%m/%Y")
                hora = datetime.now().strftime("%H:%M:%S")
                fila = [num_empleado, nombre, area, turno, fecha, hora] + invitados + [""] * (10 - len(invitados))
                df.loc[len(df)] = fila
                df.to_excel(archivo_excel, index=False)
                st.success("Registro exitoso.")

