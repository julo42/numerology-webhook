from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage
import threading
from openai import OpenAI
from prompt import SYSTEM_PROMPT_PREMIUM

app = Flask(__name__)

# Gmail
GMAIL_USER = os.environ.get("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# OpenAI client (pas de timeout pour ne pas couper le streaming)
client = OpenAI()

def generate_and_send_email(prenom1, date1, prenom2, date2, recipient):
    """
    Génère la guidance en streaming et envoie l'email.
    Logs détaillés dans Render.
    """
    print(f"[GPT] Début génération pour {prenom1} + {prenom2}…")

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
            reasoning={"effort": "medium"},  # qualité correcte
        ) as stream:
            for event in stream:
                if event.type == "output_text.delta":
                    guidance_text += event.delta
                    # Log progress tous les 100 caractères
                    if len(guidance_text) % 100 < len(event.delta):
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

    # Envoi de l'email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"[MAIL] Envoyé à {recipient}")

    except Exception as e:
        print(f"[MAIL] Erreur SMTP pour {recipient}: {str(e)}")


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

    # Lancer la génération en arrière-plan
    threading.Thread(
        target=generate_and_send_email,
        args=(data["nom_a"], data["date_a"], data["nom_b"], data["date_b"], data["email"]),
        daemon=True
    ).start()

    print(f"[API] Requête reçue pour {data['email']}, traitement en arrière-plan.")

    return jsonify({"status": "accepted", "message": "Le rapport sera envoyé par email."}), 202


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
