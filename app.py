
import streamlit as st
import pandas as pd
import pickle

# Carga del modelo entrenado
with open('modelo.pkl', 'rb') as file:
    logmodel = pickle.load(file)

# Título de la aplicación
st.title("Predicción de Cancelaciones - Regresión Logística")

# Descripción de la app
st.write("""Introduce los valores de las variables y obtén la probabilidad de que se produzca una cancelación.""")

# Inputs para cada variable
hotel_grande = st.selectbox("¿Es un hotel grande?", options=["No", "Sí"])
hotel_grande_dummy = 1 if hotel_grande == "Sí" else 0

lead_time = st.slider("Lead Time (número de días desde la reserva hasta el check-in)", min_value=0, max_value=1500, value=800)
noches = st.slider("Número de noches reservadas", min_value=1, max_value=365, value=4)

familia = st.selectbox("¿Es una familia?", options=["No", "Sí"])
familia_dummy = 1 if familia == "Sí" else 0

valor_reserva = st.slider("Valor de la reserva (€)", min_value=0, max_value=120000, value=3000)

cunas = st.selectbox("¿Se ha solicitado una cuna?", options=["No", "Sí"])
cunas_dummy = 1 if cunas == "Sí" else 0

adultos = st.slider("Número de adultos", min_value=1, max_value=8, value=2)

fidelidad = st.selectbox("¿Es un cliente fidelizado?", options=["No", "Sí"])
fidelidad_dummy = 1 if fidelidad == "Sí" else 0

aux_tipo = st.selectbox(
    "Tipo de habitación",
    options=[
        "Default Category (0)",
        "Deluxe (1)",
        "Junior Suite (2)",
        "Presidential (3)",
        "Standard (4)",
        "Suite (5)",
        "Superior (6)"
    ]
)
aux_tipo_valor = int(aux_tipo.split("(")[1].strip(")"))

# Botón para predecir
if st.button("Predecir"):
    # Crear el DataFrame con valores numéricos
    data = pd.DataFrame({
        'HOTEL_GRANDE_DUMMY': [hotel_grande_dummy],
        'LEAD_TIME': [lead_time],
        'NOCHES': [noches],
        'FAMILIA': [familia_dummy],
        'VALOR_RESERVA': [valor_reserva],
        'CUNAS': [cunas_dummy],
        'ADULTOS': [adultos],
        'FIDELIDAD_DUMMY': [fidelidad_dummy],
        'AUX_TIPO': [aux_tipo_valor]
    })
    
    # Realizar la predicción
    probabilidad = logmodel.predict_proba(data)[:, 1]
    
    # Mostrar el resultado
    st.success(f"La probabilidad de cancelación es del {probabilidad[0] * 100:.2f}%")
