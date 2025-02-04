
# Código de tu aplicación en Streamlit
import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración del servidor SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = "thevalleypalladium@gmail.com"
GMAIL_PASSWORD = "poiu vjjs upgl brme"  # Usa la contraseña de aplicación

# Función para enviar email
def enviar_correo(destinatario):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = destinatario
    msg["Subject"] = "Oferta Especial en Palladium Hotels"

    # HTML del correo con imagen alojada en Google Drive
    mensaje_html = '''
    <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; color: #333; background-color: #f7f7f7; text-align: center; }
                .container { width: 80%; max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
                h1 { color: #007BFF; }
                .image-container img { width: 100%; border-radius: 10px; }
                .cta-button { 
                    display: inline-block; 
                    padding: 15px 25px; 
                    font-size: 18px; 
                    color: white; 
                    background-color: #007BFF; 
                    text-decoration: none; 
                    border-radius: 5px;
                    font-weight: bold;
                }
                .footer { font-size: 12px; color: #777; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Oferta Exclusiva para Ti</h1>
                <p>Queremos asegurarnos de que disfrutes de una experiencia increíble.</p>
                <div class="image-container">
                    <img src="https://drive.google.com/uc?id=1s5pRyV8Po48F_dM8ixgOMSQdsQhMuQI-" alt="Hotel de Lujo">
                </div>
                <p>Porque tenemos muchas ganas de verte, hemos preparado una oferta especial con un <strong>descuento exclusivo</strong> en tu próxima estadía.</p>
                <a href="https://palladiumhotels.com/activar-descuento" class="cta-button">Activar Descuento</a>
                <p>¡No dejes pasar esta oportunidad única!</p>
                <p>Saludos,</p>
                <p><strong>Equipo Palladium Hotels</strong></p>
                <div class="footer">
                    <p>Si tienes dudas, contáctanos en <a href="mailto:soporte@palladiumhotels.com">soporte@palladiumhotels.com</a></p>
                </div>
            </div>
        </body>
    </html>
    '''
    
    msg.attach(MIMEText(mensaje_html, "html"))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, destinatario, msg.as_string())
        server.quit()
        return "✅ Correo enviado correctamente."
    except Exception as e:
        return f"❌ Error al enviar el correo: {e}"

# Interfaz de usuario con Streamlit
st.title("📩 Envío de Ofertas de Palladium Hotels")
st.write("Introduce el correo del destinatario para enviar la oferta exclusiva.")

recipient_email = st.text_input("✉️ Correo del destinatario:")

if st.button("Enviar Email"):
    if recipient_email:
        resultado = enviar_correo(recipient_email)
        st.success(resultado)
    else:
        st.warning("⚠️ Ingresa un correo antes de enviar.")
