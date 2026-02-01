from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage
import threading
import json
import uuid
import time
from openai import OpenAI

app = Flask(__name__)

# Gmail
GMAIL_USER = os.environ.get("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# OpenAI client
client = OpenAI()

# -----------------------------
# Configuration job queue
# -----------------------------
BASE_DIR = "/var/data/jobs"  # disque persistant Render
PENDING_DIR = os.path.join(BASE_DIR, "pending")
PROCESSING_DIR = os.path.join(BASE_DIR, "processing")


os.makedirs(PENDING_DIR, exist_ok=True)
os.makedirs(PROCESSING_DIR, exist_ok=True)

# Reprise automatique au démarrage : déplacer tous les jobs processing-* vers pending
for f in os.listdir(PROCESSING_DIR):
    src = os.path.join(PROCESSING_DIR, f)
    dst = os.path.join(PENDING_DIR, f)
    try:
        os.rename(src, dst)  # move atomique
    except FileExistsError:
        os.remove(src)

print(f"[STARTUP] Worker prêt. Pending jobs : {len(os.listdir(PENDING_DIR))}")

NUM_THREADS = 2  # nombre de threads worker
for _ in range(NUM_THREADS):
    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()


# -----------------------------
# Fonction de traitement d'un job
# -----------------------------
def generate_and_send_email_from_file(job_file_path):
    try:
        with open(job_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        nom1 = data["nom1"]
        date1 = data["date1"]
        nom2 = data["nom2"]
        date2 = data["date2"]
        recipient = data["recipient"]

        print(f"[GPT] Début génération pour {nom1} + {nom2}…")

        buf = ''
        with open('rules', 'r', encoding='utf-8') as fd:
            buf += fd.read()
        buf += '\n\n'
        with open('prompt', 'r', encoding='utf-8') as fd:
            buf += fd.read()

        prompt = buf.format(
            nom1=nom1,
            date1=date1,
            nom2=nom2,
            date2=date2
        )

        last_logged = 0
        guidance_text = ""
        try:
            with client.responses.stream(
                model="gpt-5-mini",
                input=prompt,
                reasoning={"effort": "medium"},
            ) as stream:
                for event in stream:
                    if event.type == "response.output_text.delta":
                        guidance_text += event.delta
                        if len(guidance_text) // 100 > last_logged:
                            last_logged = len(guidance_text) // 100
                            print(f"[GPT] {len(guidance_text)} caractères générés…")
            print(f"[GPT] Génération terminée ({len(guidance_text)} caractères).")

        except Exception as e:
            guidance_text = f"Erreur génération guidance: {str(e)}"
            print(f"[GPT] {guidance_text}")

        # Préparer l'email
        msg = EmailMessage()
        msg["From"] = GMAIL_USER
        msg["To"] = recipient
        msg["Subject"] = f"Votre guidance de couple – LUNEA-NOVA"
        msg.set_content(guidance_text[:4000])
        html_content = guidance_text.replace("\n", "<br>")
        msg.add_alternative(f"""
            <html>
                <body style="font-family:Arial; line-height:1.6;">
                    {html_content}
                </body>
            </html>
        """, subtype="html")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as server:
                server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
                server.send_message(msg)
            print(f"[MAIL] Envoyé à {recipient}")

        except Exception as e:
            print(f"[MAIL] Erreur SMTP pour {recipient}: {str(e)}")

    finally:
        if os.path.exists(job_file_path):
            os.remove(job_file_path)

# -----------------------------
# Worker loop
# -----------------------------
def worker_loop():
    while True:
        pending_files = os.listdir(PENDING_DIR)
        if not pending_files:
            time.sleep(1)
            continue

        for fname in pending_files:
            src_path = os.path.join(PENDING_DIR, fname)
            dst_path = os.path.join(PROCESSING_DIR, fname)
            try:
                os.rename(src_path, dst_path)  # move atomique
            except FileNotFoundError:
                continue
            except FileExistsError:
                continue
            generate_and_send_email_from_file(dst_path)

# -----------------------------
# Flask API
# -----------------------------
@app.route("/send_report", methods=["POST"])
def send_report():
    payload = request.json
    contact = payload.get("data", {}).get("contact", {})

    fields_map = {
        "nom_a": "first_name",
        "date_a": "date_de_naissance",
        "nom_b": "prnom_conjoint",
        "date_b": "date_de_naissance_conjoint"
    }

    data = {}
    data["email"] = contact.get("email")

    for k1, k2 in fields_map.items():
        if k2 in contact.get("fields", {}):
            data[k1] = contact["fields"][k2]

    for field in ["nom_a", "date_a", "nom_b", "date_b", "email"]:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Créer le job JSON dans pending/
    job_id = str(uuid.uuid4())
    job_file = os.path.join(PENDING_DIR, f"{job_id}.json")
    with open(job_file, "w", encoding="utf-8") as f:
        json.dump({
            "nom1": data["nom_a"],
            "date1": data["date_a"],
            "nom2": data["nom_b"],
            "date2": data["date_b"],
            "recipient": data["email"]
        }, f)

    print(f"[API] Requête reçue pour {data['email']}, job créé {job_id}")
    return jsonify({"status": "accepted", "message": "Le rapport sera envoyé par email."}), 202

# -----------------------------
# Main : démarrage threads + Flask
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
