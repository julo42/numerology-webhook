from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage
from threading import Thread
from openai import OpenAI

from prompt import SYSTEM_PROMPT_PREMIUM

app = Flask(__name__)

# Gmail
GMAIL_USER = os.environ.get("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# OpenAI
client = OpenAI(timeout=120)  # Timeout global côté client

def generate_and_send_email_stream(data):
    prenom1, date1 = data["nom_a"], data["date_a"]
    prenom2, date2 = data["nom_b"], data["date_b"]
    recipient = data["email"]

    prompt = SYSTEM_PROMPT_PREMIUM.format(
        prenom1=prenom1, date1=date1, prenom2=prenom2, date2=date2
    )

    guidance_text = ""

    try:
        print(f"[GPT] Début génération pour {recipient}…")

        with client.responses.stream(
            model="gpt-5-mini",
            input=prompt,
            reasoning={"effort": "medium"},
        ) as stream:
            for event in stream:
                if event.type == "output_text.delta":
                    guidance_text += event.delta
                    # Log partiel dans Render
                    print(event.delta, end="", flush=True)

        print(f"\n[GPT] Génération terminée pour {recipient} ({len(guidance_text)} caractères)")

        # Préparation email
        msg = EmailMessage()
        msg["From"] = GMAIL_USER
        msg["To"] = recipient
        msg["Subject"] = f"Votre guidance de couple – LUNEA-NOVA"
        msg.set_content(guidance_text[:4000])
        html_content = guidance_text.replace("\n", "<br>")
        msg.add_alternative(
            f"<html><body style='font-family:Arial; line-height:1.6;'>{html_content}</body></html>",
            subtype="html"
        )

        # Envoi SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        print(f"[SMTP] Email envoyé à {recipient}")

    except Exception as e:
        print(f"[ERROR] {recipient} : {e}")

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

    data = {"email": contact.get("email")}
    for k1, k2 in fields_map.items():
        if k2 in contact.get("fields", {}):
            data[k1] = contact["fields"][k2]

    for field in ["nom_a", "date_a", "nom_b", "date_b", "email"]:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Lancer le thread en arrière-plan
    Thread(target=generate_and_send_email_stream, args=(data,), daemon=True).start()

    # Réponse immédiate
    return jsonify({"status": "accepted"}), 202

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
