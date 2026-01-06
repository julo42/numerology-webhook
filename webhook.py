from flask import Flask, request, jsonify
import os
import tempfile
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from rapport_couple import rapport_couple, generate_pdf
import base64

app = Flask(__name__)

# Variables d'environnement à configurer sur Render
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")

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

    # Lire et encoder le PDF
    with open(pdf_file, "rb") as f:
        encoded_file = base64.b64encode(f.read()).decode()

    # Créer l'email SendGrid
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=recipient,
        subject=f"Rapport Numérologique: {nom_a} & {nom_b}",
        html_content=f"Bonjour,<br><br>Veuillez trouver en pièce jointe le rapport numérologique pour {nom_a} et {nom_b}.<br><br>Cordialement."
    )

    attachment = Attachment(
        FileContent(encoded_file),
        FileName("rapport_couple.pdf"),
        FileType("application/pdf"),
        Disposition("attachment")
    )
    message.attachment = attachment

    # Envoyer via SendGrid
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return jsonify({"status": "success", "sendgrid_status": response.status_code}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
