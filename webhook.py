import os
import sys
import smtplib
from flask import Flask, request, jsonify
from email.message import EmailMessage
from openai import OpenAI

from prompt import SYSTEM_PROMPT_PREMIUM

app = Flask(__name__)

# --- Gmail ---
GMAIL_USER = os.environ.get("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# --- OpenAI client avec timeout long ---
client = OpenAI(timeout=180)  # 3 min max pour chaque requête

# --- Fonction robuste pour générer la guidance ---
def generate_guidance(prenom1, date1, prenom2, date2):
    """
    Génération complète via GPT-5-mini en streaming,
    logs directs dans Render et fichier temporaire pour debug.
    """
    prompt = SYSTEM_PROMPT_PREMIUM.format(
        prenom1=prenom1,
        date1=date1,
        prenom2=prenom2,
        date2=date2
    )

    guidance_text = ""
    log_file = f"/tmp/guidance_{prenom1}_{prenom2}.log"

    try:
        print(f"[GPT] Début génération pour {prenom1} / {prenom2}…", flush=True)
        with client.responses.stream(
            model="gpt-5-mini",
            input=prompt,
            reasoning={"effort": "high"},  # meilleure qualité possible
        ) as stream:
            for event in stream:
                # On prend tous les textes générés
                if getattr(event, "type", None) in ("output_text.delta", "output_text"):
                    delta = getattr(event, "delta", "") or getattr(event, "text", "")
                    guidance_text += delta

                    # Logs pour Render
                    print(delta, end="", flush=True)

                    # Sauvegarde fichier temporaire pour debug
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(delta)
                        f.flush()

        print(f"\n[GPT] Génération terminée, longueur: {len(guidance_text)} caractères", flush=True)
        return guidance_text.strip()

    except Exception as e:
        err_msg = f"Erreur génération guidance: {str(e)}"
        print(err_msg, flush=True)
        return err_msg

# --- Endpoint webhook ---
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

    # Vérification des champs requis
    for field in ["nom_a", "date_a", "nom_b", "date_b", "email"]:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Génération GPT
    guidance_text = generate_guidance(
        data["nom_a"], data["date_a"], data["nom_b"], data["date_b"]
    )

    # Préparation de l'email
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = data["email"]
    msg["Subject"] = f"Votre guidance de couple – LUNEA-NOVA"

    msg.set_content(guidance_text)  # texte complet sans limite

    # HTML simple pour lecture confortable
    html_content = guidance_text.replace("\n", "<br>")
    msg.add_alternative(f"<html><body style='font-family:Arial; line-height:1.6;'>{html_content}</body></html>", subtype="html")

    # Envoi
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=120) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"[SMTP] Email envoyé à {data['email']}", flush=True)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        err = f"Erreur SMTP: {str(e)}"
        print(err, flush=True)
        return jsonify({"error": err}), 500

# --- Run local (port depuis Render) ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
