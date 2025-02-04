
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

# Carga del modelo entrenado
def cargar_modelo():
    with open('modelo.pkl', 'rb') as file:
        return pickle.load(file)

logmodel = cargar_modelo()

def predecir_cancelacion(data):
    return logmodel.predict_proba(data)[:, 1]

def enviar_correo(destinatario):
    asunto = "Oferta especial para Palladium: Activa tu descuento"
    mensaje_html = '''
    <html>
        <head></head>
        <body>
            <h1>Oferta Exclusiva para Palladium</h1>
            <p>Queremos evitar la cancelación y, para ello, te ofrecemos un <strong>descuento especial</strong> en tu próxima reserva.</p>
            <p><a href="https://palladiumhotels.com/activar-descuento">Activar Descuento</a></p>
            <p>¡No dejes pasar esta oportunidad!</p>
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
        server.sendmail(GMAIL_USER, destinatario, msg.as_string())
        server.quit()
        return "Correo enviado correctamente."
    except Exception as e:
        return f"Error al enviar el correo: {e}"

# Inputs manuales en Google Colab
hotel_grande_dummy = int(input("¿Es un hotel grande? (1=Sí, 0=No): "))
lead_time = int(input("Lead Time (número de días desde la reserva hasta el check-in): "))
noches = int(input("Número de noches reservadas: "))
familia_dummy = int(input("¿Es una familia? (1=Sí, 0=No): "))
valor_reserva = float(input("Valor de la reserva (€): "))
cunas_dummy = int(input("¿Se ha solicitado una cuna? (1=Sí, 0=No): "))
adultos = int(input("Número de adultos: "))
fidelidad_dummy = int(input("¿Es un cliente fidelizado? (1=Sí, 0=No): "))
aux_tipo_valor = int(input("Tipo de habitación (Número entre 0 y 6): "))

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

probabilidad = predecir_cancelacion(data)[0] * 100
print(f"La probabilidad de cancelación es del {probabilidad:.2f}%")

if probabilidad > 50:
    recipient_email = input("Ingrese el correo del destinatario: ")
    if recipient_email:
        resultado = enviar_correo(recipient_email)
        print(resultado)
    else:
        print("⚠️ No se ingresó un destinatario.")
