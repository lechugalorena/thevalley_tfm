
import streamlit as st
import pandas as pd
import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración del servidor y credenciales
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = "thevalleypalladium@gmail.com"
GMAIL_PASSWORD = "poiu vjjs upgl brme"

# Mensaje HTML con la acción de descuento
mensaje_html = '''
<html>
    <head></head>
    <body>
        <h1>Oferta Exclusiva para Palladium</h1>
        <p>Estimado/a cliente,</p>
        <p>Queremos evitar la cancelación y, para ello, te ofrecemos un <strong>descuento especial</strong> en tu próxima reserva.</p>
        <p>Haz clic en el siguiente enlace para activar tu descuento:</p>
        <p><a href="https://palladiumhotels.com/activar-descuento" style="padding:10px 20px; color: white; background-color: #007BFF; text-decoration: none;">Activar Descuento</a></p>
        <p>¡No dejes pasar esta oportunidad!</p>
        <p>Saludos,</p>
        <p>Equipo Palladium</p>
    </body>
</html>
'''
 

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

    if probabilidad[0] * 100 > 50:
              # Input fields
        recipient_email = st.text_input("Destinatario:", "")
        
        # Send button
        if st.button("Send Email"):
            if recipient_email:
                asunto = "Oferta especial para Palladium: Activa tu descuento"
                
                # Crear el mensaje MIME y adjuntar el contenido HTML
                msg = MIMEMultipart("alternative")
                msg["From"] = GMAIL_USER
                msg["To"] = recipient_email
                msg["Subject"] = asunto
                msg.attach(MIMEText(mensaje_html, "html"))
                
                try:
                        # Conectar al servidor SMTP de Gmail
                        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                        server.starttls()  # Iniciar conexión segura
                        server.login(GMAIL_USER, GMAIL_PASSWORD)
                        server.sendmail(GMAIL_USER, destinatario, msg.as_string())
                        server.quit()
                        print("Correo enviado correctamente.")
                except Exception as e:
                        print(f"Error al enviar el correo: {e}")
                st.success(result)
            else:
                st.warning("⚠️ Please fill in all fields before sending.")


