from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage

from rapport_couple import rapport_couple, render_rapport_html

app = Flask(__name__)

GMAIL_USER = os.environ.get("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

@app.route("/send_report", methods=["POST"])
def send_report():
    data = request.json
    for field in ["nom_a", "date_a", "nom_b", "date_b", "email"]:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    nom_a, date_a = data["nom_a"], data["date_a"]
    nom_b, date_b = data["nom_b"], data["date_b"]
    recipient = data["email"]

    # Génération du rapport
    rapport = rapport_couple(nom_a, date_a, nom_b, date_b)
    html_content = render_rapport_html(rapport)

    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = recipient
    msg["Subject"] = f"Rapport Numérologique : {rapport['noms']}"

    # Fallback texte
    msg.set_content(
        f"Bonjour,\n\n"
        f"Voici votre rapport numérologique de couple.\n\n"
        f"Score : {rapport['score_compatibilite']}/100\n\n"
        f"{rapport['synthese']}"
    )

    # Version HTML
    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        return jsonify({"status": "success", "delivery": "gmail_html"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
