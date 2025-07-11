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
    fecha_formateada = fecha_houston.strftime('%A %d de %B de %Y').capitalize()
    mensaje = (
        f"🌞 ¡Muy buenos días, familia P.1🦁!\n\n"
        f"🗓️ Hoy es *{fecha_formateada}*.\n\n"
        "Iniciamos un nuevo día con la energía y el compromiso de seguir creciendo juntos 💫.\n"
        "Recuerda que aquí estamos para *apoyarnos y crecer juntos* 💪🚀.\n\n"
        "📣 ¡Invita a más personas a unirse! ¡Más grande, más fuerte! 🔥🙌"
    )
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  data={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})
    print(f"[{datetime.now()}] Mensaje diario enviado")

schedule.every().day.at("12:00").do(enviar_mensaje_buenos_dias)

ULTIMO_UPDATE_ID = None

def enviar_mensaje_bienvenida(nombre):
    mensaje = f"👋 ¡Bienvenido/a, {nombre}, a la comunidad P.1🦁!\n\nRevisa los mensajes anclados para ver reglas y recursos."
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  data={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})

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
                enviar_mensaje_bienvenida(m.get("first_name", "Nuevo miembro"))
    except Exception as e:
        print("Error revisar miembros:", e)

app = Flask(__name__)
@app.route('/')
def home(): return "Bot P.1🦁 activo"

Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()

while True:
    schedule.run_pending()
    revisar_nuevos_miembros()
    time.sleep(5)
