from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage
from openai import OpenAI

from prompt import  SYSTEM_PROMPT_PREMIUM

app = Flask(__name__)

# Gmail
GMAIL_USER = os.environ.get("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# OpenAI
client = OpenAI()

def generate_guidance(prenom1, date1, prenom2, date2):
    prompt = SYSTEM_PROMPT_PREMIUM.format(
        prenom1=prenom1,
        date1=date1,
        prenom2=prenom2,
        date2=date2
    )

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        reasoning={"effort": "low"},
        max_output_tokens=3500
    )

    # Extraction robuste
    parts = []
    for item in response.output:
        for content in item.content:
            if content["type"] == "output_text":
                parts.append(content["text"])

    return "\n".join(parts)


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
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Génération IA
    guidance_text = generate_guidance(
        data["nom_a"],
        data["date_a"],
        data["nom_b"],
        data["date_b"]
    )

    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = data["email"]
    msg["Subject"] = f"Votre guidance de couple – LUNEA-NOVA"

    # Texte brut fallback
    msg.set_content(guidance_text[:4000])

    # HTML simple (tu peux enrichir CSS)
    html_content = guidance_text.replace("\n", "<br>")
    msg.add_alternative(f"""
        <html>
            <body style="font-family:Arial; line-height:1.6;">
                {html_content}
            </body>
        </html>
    """, subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
