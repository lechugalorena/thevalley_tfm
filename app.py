import streamlit as st
import pandas as pd
import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración del servidor SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = "thevalleypalladium@gmail.com"
GMAIL_PASSWORD = "poiu vjjs upgl brme"  # Usa una contraseña de aplicación

@st.cache_resource
def cargar_modelo():
    with open('modelo.pkl', 'rb') as file:
        return pickle.load(file)

logmodel = cargar_modelo()

def enviar_correo_callback():
    recipient_email = st.session_state.get("recipient_email", "")
    if recipient_email and "@" in recipient_email:
        result = enviar_correo(recipient_email)
        if result == True:
            st.success("¡El correo de oferta se ha enviado exitosamente!")
        else:
            st.error(result)
    else:
        st.warning("Por favor, ingrese un correo electrónico válido.")
        

def predecir_cancelacion(data):
    return logmodel.predict_proba(data)[:, 1]

def enviar_correo(destinatario):
    asunto = "Oferta especial de Palladium: Activa tu beneficio en tu próxima reserva"
    mensaje_html = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>¡Oferta Exclusiva para Ti! 🎉</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #e9f5ff;
                margin: 0;
                padding: 0;
            }
            .container {
                background-color: #ffffff;
                max-width: 600px;
                margin: 40px auto;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }
            .header-image {
                display: block;
                margin: 0 auto 20px;
                max-width: 200px;
            }
            .hotel-image {
                display: block;
                margin: 20px auto;
                max-width: 100%;
                border-radius: 10px;
            }
            h1 {
                color: #333333;
                text-align: center;
            }
            p {
                color: #555555;
                line-height: 1.6;
            }
            .button {
                display: inline-block;
                background-color: #28a745;
                color: #ffffff;
                padding: 12px 24px;
                margin: 20px 0;
                text-decoration: none;
                border-radius: 6px;
                text-align: center;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img class="header-image" src="https://intripertravelmedia.com/wp-content/uploads/2019/10/logo.png" alt="Enterprise Icon">
            <h1>¡Hola! 😄 Descubre tu oferta exclusiva</h1>
            <p>Nos alegra tenerte con nosotros. Por eso, te ofrecemos un <strong>descuento especial</strong> para que disfrutes de tu próxima experiencia. 🚀</p>
            <img class="hotel-image" src="https://www.palladiumhotelgroup.com/content/dam/palladium/images/hoteles/mexico/costa-mujeres/hotel/piscinas/grand-palladium-costa-mujeres-resort-spa/Grand-Palladium-Costa-Mujeres-Resort-Spa_Vista-general-de-la-piscina-principal.jpg.transform/rendition-md/image.jpg" alt="Hotel Imagen">
            <p style="text-align: center;">
                <a class="button" href="https://palladiumhotels.com/activar-descuento">¡Activa tu descuento ahora! 👉</a>
            </p>
            <p style="text-align: center;">¡No esperes, estamos aquí para ayudarte a disfrutar lo mejor! 🤝</p>
        </div>
    </body>
    </html>
    '''
    
    msg = MIMEMultipart("alternative")
    msg["From"] = GMAIL_USER
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje_html, "html"))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return f"Error al enviar el correo: {e}"

# Interfaz de Streamlit
st.title("Prototipo para la predicción de cancelación y envío de oferta especial")
st.write("Complete la siguiente información:")

lead_time = st.number_input("Lead Time (días desde la reserva hasta el check-in):", min_value=0, step=1, value=30)
noches = st.number_input("Número de noches reservadas:", min_value=1, step=1, value=7)
familia_dummy = st.selectbox("¿Es una familia?", options=[0, 1], format_func=lambda x: "Sí" if x == 1 else "No")
valor_reserva = st.number_input("Valor de la reserva (€):", min_value=0.0, step=1.0, value=1500.0)
adultos = st.number_input("Número de adultos:", min_value=1, step=1, value=2)
fidelidad_dummy = st.selectbox("¿Es un cliente fidelizado?", options=[0, 1], format_func=lambda x: "Sí" if x == 1 else "No")
aux_tipo_valor = st.slider("Tipo de habitación (0 a 6):", min_value=0, max_value=6, value=3)

if st.button("Predecir Cancelación"):
    data = pd.DataFrame({
        'LEAD_TIME': [lead_time],
        'NOCHES': [noches],
        'FAMILIA': [familia_dummy],
        'VALOR_RESERVA': [valor_reserva],
        'ADULTOS': [adultos],
        'FIDELIDAD_DUMMY': [fidelidad_dummy],
        'AUX_TIPO': [aux_tipo_valor]
    })
    
    probabilidad = predecir_cancelacion(data)[0] * 100
    st.success(f"La probabilidad de cancelación es del {probabilidad:.2f}%")
    
    if probabilidad > 50:
        st.info("La probabilidad de cancelación supera el 50%. Se recomienda enviar una oferta especial.")
        
        recipient_email = st.text_input(
            "Ingrese el correo del destinatario:",
            key="recipient_email",
            on_change=enviar_correo_callback
        )
