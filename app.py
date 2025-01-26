
import streamlit as st
import pandas as pd
import pickle

# Carga del modelo entrenado
with open('modelo.pkl', 'rb') as file:
    logmodel = pickle.load(file)

# Título de la aplicación
st.title("Predicción de Cancelaciones - Regresión Logística")

# Descripción de la app
st.write("""
Introduce los valores de las variables y obten la probabilidad de que se produzca una cancelación.
""")

# Inputs para cada variable
hotel_grande = st.selectbox("¿Es un hotel grande?", options=["No", "Sí"])
hotel_grande_dummy = 1 if hotel_grande == "Sí" else 0

lead_time = st.number_input("Lead Time (días de antelación)", min_value=0, value=800)
noches = st.number_input("Número de noches", min_value=1, value=4)
familia = st.selectbox("¿Es una familia?", options=["No", "Sí"])
familia_dummy = 1 if familia == "Sí" else 0
valor_reserva = st.number_input("Valor de la reserva (€)", min_value=0, value=3000)
cunas = st.number_input("Número de cunas", min_value=0, value=1)
adultos = st.number_input("Número de adultos", min_value=1, value=4)
fidelidad = st.selectbox("¿Es un cliente fidelizado?", options=["No", "Sí"])
fidelidad_dummy = 1 if fidelidad == "Sí" else 0
aux_tipo = st.number_input("Tipo auxiliar", min_value=0, value=6)

# Botón para predecir
if st.button("Predecir"):
    data = pd.DataFrame({
        'HOTEL_GRANDE_DUMMY': [hotel_grande_dummy],
        'LEAD_TIME': [lead_time],
        'NOCHES': [noches],
        'FAMILIA': [familia_dummy],
        'VALOR_RESERVA': [valor_reserva],
        'CUNAS': [cunas],
        'ADULTOS': [adultos],
        'FIDELIDAD_DUMMY': [fidelidad_dummy],
        'AUX_TIPO': [aux_tipo]
    })
    probabilidad = logmodel.predict_proba(data)[:, 1]
    st.success(f"La probabilidad de cancelación es del {probabilidad[0] * 100:.2f}%")
