import requests
import schedule
import time
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
import locale

try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain')
    except:
        pass

BOT_TOKEN = '8062761924:AAGcLjqxM2WL48N-pVw8tynhlCuH1D4_snY'
CHAT_ID = '-1002877323438'

def enviar_mensaje_buenos_dias():
    fecha_houston = datetime.utcnow() - timedelta(hours=5)
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    dia_semana = dias[fecha_houston.weekday()]
    dia = fecha_houston.day
    mes = meses[fecha_houston.month - 1]
    anio = fecha_houston.year
    fecha_formateada = f"{dia_semana} {dia} de {mes} de {anio}"

    mensaje = (
        f"🌞 *¡Muy buenos días, familia P.1🦁!*\n\n"
        f"🗓️ Hoy es *{fecha_formateada}*.\n\n"
        "Iniciamos un nuevo día con la energía y el compromiso de seguir creciendo juntos 💫.\n"
        "Recuerda que aquí estamos para *apoyarnos, impulsarnos y lograr cada meta que nos propongamos* 💪🚀.\n\n"
        "📣 *¡Invita a más personas a unirse!* Cuantos más seamos, más fuerte será nuestra comunidad 🔥🙌.\n\n"
        "🎯 *¿Tienes una batalla, live o evento planificado?* Compártelo con anticipación para agregarlo a los recordatorios automáticos ⏰.\n"
        "📝 Puedes usar este formulario para agendarlo fácilmente:\n"
        "👉 https://forms.gle/KFMDU69wxav9KvBb6\n\n"
        "*¡Estamos aquí para respaldarte!*\n\n"
        "💥✨ *¡A darlo todo hoy!*"
    )

    botones = {
        "inline_keyboard": [[
            {"text": "📜 Ver reglas", "url": "https://t.me/c/2877323438/73"},
            {"text": "🦁 ¿Qué es P.1?", "url": "https://t.me/c/2877323438/75"},
            {"text": "📅 Agendar batalla", "url": "https://forms.gle/KFMDU69wxav9KvBb6"}
        ]]
    }

    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  json={
                      "chat_id": CHAT_ID,
                      "text": mensaje,
                      "parse_mode": "Markdown",
                      "reply_markup": botones
                  })
    print(f"[{datetime.now()}] Mensaje diario enviado")

# 12:00 UTC = 7:00 a.m. hora Houston
schedule.every().day.at("12:00").do(enviar_mensaje_buenos_dias)

ULTIMO_UPDATE_ID = None

def enviar_mensaje_bienvenida(nombre):
    mensaje = (
        f"👋 *¡Bienvenido/a, {nombre}, a la comunidad P.1🦁!*\n\n"
        "Recuerda revisar los mensajes anclados donde encontrarás:\n"
        "- Las reglas del grupo\n"
        "- El significado de P.1🦁\n"
        "- Un mensaje prediseñado que puedes usar para invitar a otros\n\n"
        "*Unidos somos más, y más fuertes* 💪🔥"
    )

    botones = {
        "inline_keyboard": [[
            {"text": "📜 Ver reglas", "url": "https://t.me/c/2877323438/73"},
            {"text": "🦁 ¿Qué es P.1?", "url": "https://t.me/c/2877323438/75"},
            {"text": "📅 Agendar batalla", "url": "https://forms.gle/KFMDU69wxav9KvBb6"}
        ]]
    }

    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  json={
                      "chat_id": CHAT_ID,
                      "text": mensaje,
                      "parse_mode": "Markdown",
                      "reply_markup": botones
                  })

def revisar_nuevos_miembros():
    global ULTIMO_UPDATE_ID
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    if ULTIMO_UPDATE_ID:
        url += f"?offset={ULTIMO_UPDATE_ID + 1}"
    try:
        res = requests.get(url, timeout=10).json()
        for u in res.get("result", []):
            ULTIMO_UPDATE_ID = u["update_id"]
            for m in u.get("message", {}).get("new_chat_members", []):
                nombre = m.get("first_name", "Nuevo miembro")
                enviar_mensaje_bienvenida(nombre)
    except Exception as e:
        print("Error revisar miembros:", e)

# Mantener el bot vivo (Replit/Render)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot P.1🦁 activo"

Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

# Loop principal
# PRUEBA MANUAL DEL MENSAJE DE BUENOS DÍAS
enviar_mensaje_buenos_dias()

while True:
    schedule.run_pending()
    revisar_nuevos_miembros()
    time.sleep(5)
