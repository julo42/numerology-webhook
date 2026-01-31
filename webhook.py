from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage
from openai import OpenAI

from prompt import SYSTEM_PROMPT_PREMIUM

app = Flask(__name__)

# Gmail
GMAIL_USER = os.environ.get("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# OpenAI
client = OpenAI(timeout=60)  # Timeout global

def generate_guidance_stream(prenom1, date1, prenom2, date2):
    """
    Génère la guidance complète en streaming depuis GPT-5-mini
    """
    prompt = SYSTEM_PROMPT_PREMIUM.format(
        prenom1=prenom1,
        date1=date1,
        prenom2=prenom2,
        date2=date2
    )

    guidance_text = ""
    try:
        with client.responses.stream(
            model="gpt-5-mini",
            input=prompt,
            reasoning={"effort": "medium"},  # qualité correcte + rapide
        ) as stream:
            for event in stream:
                # Chaque delta de texte généré
                if event.type == "output_text.delta":
                    guidance_text += event.delta
        return guidance_text

    except Exception as e:
        # Renvoie une erreur lisible
        return f"Erreur génération guidance: {str(e)}"

@app.route("/send_report", methods=["POST"])
def send_report():
    payload = request.json
    contact = payload.get("data", {}).get("contact", {})

    # Mapping des champs système.io → notre format
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

    # Vérification des champs requis
    for field in ["nom_a", "date_a", "nom_b", "date_b", "email"]:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Génération guidance via streaming
    guidance_text = generate_guidance_stream(
        data["nom_a"], data["date_a"],
        data["nom_b"], data["date_b"]
    )

    # Préparation de l'email
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = data["email"]
    msg["Subject"] = f"Votre guidance de couple – LUNEA-NOVA"

    # Texte brut fallback
    msg.set_content(guidance_text[:4000])

    # HTML simple
    html_content = guidance_text.replace("\n", "<br>")
    msg.add_alternative(f"""
        <html>
            <body style="font-family:Arial; line-height:1.6;">
                {html_content}
            </body>
        </html>
    """, subtype="html")

    # Envoi sécurisé via SMTP SSL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": f"Erreur SMTP: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
