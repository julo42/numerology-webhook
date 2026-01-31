from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage
from threading import Thread
from openai import OpenAI
import time

from prompt import SYSTEM_PROMPT_PREMIUM

app = Flask(__name__)

# Gmail
GMAIL_USER = os.environ.get("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# OpenAI client
client = OpenAI(timeout=180)  # Timeout global

def generate_guidance_stream(prenom1, date1, prenom2, date2):
    prompt = SYSTEM_PROMPT_PREMIUM.format(
        prenom1=prenom1,
        date1=date1,
        prenom2=prenom2,
        date2=date2
    )

    guidance_text = ""
    print(f"[GPT] Début génération pour {prenom1} + {prenom2}…", flush=True)

    try:
        # Streaming GPT complet
        with client.responses.stream(
            model="gpt-5-mini",
            input=prompt,
            reasoning={"effort": "high"}
        ) as stream:
            for event in stream:
                if hasattr(event, "type") and event.type in ("output_text.delta", "output_text"):
                    delta = getattr(event, "delta", None) or getattr(event, "text", "")
                    guidance_text += delta
                    print(delta, end="", flush=True)
        print(f"\n[GPT] Génération terminée ({len(guidance_text)} caractères).", flush=True)
        return guidance_text.strip()
    except Exception as e:
        err_msg = f"[GPT] Erreur génération: {str(e)}"
        print(err_msg, flush=True)
        return err_msg

def send_email(recipient, subject, text):
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(text[:4000])
    html_content = text.replace("\n", "<br>")
    msg.add_alternative(
        f"<html><body style='font-family:Arial; line-height:1.6;'>{html_content}</body></html>",
        subtype="html"
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"[MAIL] Envoyé à {recipient}", flush=True)
    except Exception as e:
        print(f"[MAIL] Erreur SMTP: {e}", flush=True)

def process_report_background(data):
    """Tâche en arrière-plan : génération GPT + envoi email"""
    try:
        guidance_text = generate_guidance_stream(
            data["nom_a"], data["date_a"],
            data["nom_b"], data["date_b"]
        )
        send_email(data["email"], "Votre guidance de couple – LUNEA-NOVA", guidance_text)
    except Exception as e:
        print(f"[BACKGROUND] Erreur: {e}", flush=True)

@app.route("/send_report", methods=["POST"])
def send_report():
    payload = request.json
    contact = payload.get("data", {}).get("contact", {})

    # Mapping champs système.io → interne
    fields_map = {
        "nom_a": "first_name",
        "date_a": "date_de_naissance",
        "nom_b": "prnom_conjoint",
        "date_b": "date_de_naissance_conjoint"
    }

    data = {"email": contact.get("email")}
    for k1, k2 in fields_map.items():
        if k2 in contact.get("fields", {}):
            data[k1] = contact["fields"][k2]

    # Vérification des champs requis
    for field in ["nom_a", "date_a", "nom_b", "date_b", "email"]:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Lancer le traitement **en arrière-plan**
    Thread(target=process_report_background, args=(data,), daemon=True).start()

    # Réponse HTTP immédiate
    print(f"[API] Requête reçue pour {data['email']}, traitement en arrière-plan.", flush=True)
    return jsonify({
        "status": "processing",
        "message": "Le rapport est en cours de génération et sera envoyé par email."
    }), 202

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
