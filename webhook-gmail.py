from flask import Flask, request, jsonify
import os
import tempfile
import base64
import smtplib
from email.message import EmailMessage

from rapport_couple import rapport_couple, generate_pdf

app = Flask(__name__)

# Variables d'environnement Gmail
GMAIL_USER = os.environ.get("GMAIL_USER")
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

    # Générer PDF temporaire
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmpfile:
        pdf_file = tmpfile.name

    rapport = rapport_couple(nom_a, date_a, nom_b, date_b)
    generate_pdf(rapport, pdf_file)

    # Lire le PDF
    with open(pdf_file, "rb") as f:
        pdf_data = f.read()

    # Construire l'email
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = recipient
    msg["Subject"] = f"Rapport Numérologique : {nom_a} & {nom_b}"

    msg.set_content(
        f"""
Bonjour,

Veuillez trouver en pièce jointe le rapport numérologique
pour {nom_a} et {nom_b}.

Cordialement.
"""
    )

    msg.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename="rapport_couple.pdf"
    )

    # Envoi via Gmail SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        return jsonify({"status": "success", "provider": "gmail"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
