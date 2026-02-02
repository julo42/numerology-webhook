from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage
import threading
import json
import uuid
import time
from openai import OpenAI

# -----------------------------
# App & config
# -----------------------------
app = Flask(__name__)

GMAIL_USER = os.environ.get("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme123")

NUM_THREADS = 5

BASE_DIR = "/var/data/jobs"
PENDING_DIR = os.path.join(BASE_DIR, "pending")
PROCESSING_DIR = os.path.join(BASE_DIR, "processing")

SUBJECT_FILE = "/var/data/subject"
PROMPT_FILE = "/var/data/prompt"

client = OpenAI()

os.makedirs(PENDING_DIR, exist_ok=True)
os.makedirs(PROCESSING_DIR, exist_ok=True)

# Reprise jobs en cours
for f in os.listdir(PROCESSING_DIR):
    try:
        os.rename(
            os.path.join(PROCESSING_DIR, f),
            os.path.join(PENDING_DIR, f)
        )
    except Exception:
        pass

print(f"Pending jobs: {len(os.listdir(PENDING_DIR))}")


# Permet de renvoyer un propmt avec des valeurs non interprétées
class SilentDict(dict):
    def __missing__(self, k):
        return '{' + k + '}'


# -----------------------------
# Auth helper
# -----------------------------
def check_admin_auth(req):
    return req.headers.get("X-Admin-Password") == ADMIN_PASSWORD


# -----------------------------
# Job processing
# -----------------------------
def generate_and_send_email_from_file(job_file_path):
    try:
        with open(job_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        email = data["email"]
        fields = SilentDict(data["fields"])

        print(f"Generating report for: {data}")

        with open(SUBJECT_FILE, "r", encoding="utf-8") as f:
            subject = f.read().format_map(fields)

        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            prompt = f.read().format_map(fields)

        guidance_text = ""

        with client.responses.stream(
            model="gpt-5-mini",
            input=prompt,
            reasoning={"effort": "medium"},
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    guidance_text += event.delta

        msg = EmailMessage()
        msg["From"] = GMAIL_USER
        msg["To"] = email
        msg["Subject"] = subject
        msg.set_content(guidance_text[:4000])

        msg.add_alternative(
            "<html><body style='font-family:Arial'>"
            + guidance_text.replace("\n", "<br>")
            + "</body></html>",
            subtype="html",
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        print(f"Report sent to {email}")

    finally:
        if os.path.exists(job_file_path):
            os.remove(job_file_path)

# -----------------------------
# Worker loop
# -----------------------------
def worker_loop():
    print('Worker thread started')
    while True:
        for fname in os.listdir(PENDING_DIR):
            src = os.path.join(PENDING_DIR, fname)
            dst = os.path.join(PROCESSING_DIR, fname)
            try:
                os.rename(src, dst)
            except Exception:
                continue
            generate_and_send_email_from_file(dst)
        time.sleep(1)

for _ in range(NUM_THREADS):
    threading.Thread(target=worker_loop, daemon=True).start()

# -----------------------------
# API – envoi rapport
# -----------------------------
@app.route("/send_report", methods=["POST"])
def send_report():
    payload = request.json or {}
    data = payload.get("data", {}).get("contact", {})

    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400

    job_id = str(uuid.uuid4())
    job_file = os.path.join(PENDING_DIR, f"{job_id}.json")

    with open(job_file, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f'File generated: {job_file}')

    return jsonify({"status": "accepted"}), 202

# -----------------------------
# Admin API – templates
# -----------------------------
@app.route("/admin/templates", methods=["GET"])
def admin_get_templates():
    if not check_admin_auth(request):
        return jsonify({"error": "unauthorized"}), 401

    def read(path):
        return open(path, "r", encoding="utf-8").read() if os.path.exists(path) else ""

    return jsonify({
        "subject": read(SUBJECT_FILE),
        "prompt": read(PROMPT_FILE),
    })

@app.route("/admin/templates", methods=["POST"])
def admin_update_templates():
    if not check_admin_auth(request):
        return jsonify({"error": "unauthorized"}), 401

    payload = request.json or {}

    if "subject" in payload:
        open(SUBJECT_FILE, "w", encoding="utf-8").write(payload["subject"])

    if "prompt" in payload:
        open(PROMPT_FILE, "w", encoding="utf-8").write(payload["prompt"])

    return jsonify({"status": "ok"})

# -----------------------------
# Admin page
# -----------------------------
@app.route("/admin")
def admin_page():
    return """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Admin – Templates</title>
<style>
body { font-family: Arial; max-width: 900px; margin: auto; padding: 20px; }
input, textarea { width: 100%; margin-bottom: 12px; }
textarea { height: 320px; font-family: monospace; }
.hidden { display: none; }
button { padding: 8px 16px; }
</style>
</head>
<body>

<h2>Administration</h2>

<div id="login">
    <p>Mot de passe :</p>
    <input type="password" id="pwd">
    <button onclick="login()">Connexion</button>
</div>

<div id="editor" class="hidden">
    <p><strong>Sujet</strong></p>
    <input id="subject">

    <p><strong>Prompt</strong></p>
    <textarea id="prompt"></textarea>

    <button onclick="save()">💾 Sauvegarder</button>
</div>

<script>
let adminPassword = "";

async function login() {
    const pwd = document.getElementById("pwd").value;
    const res = await fetch("/admin/templates", {
        headers: { "X-Admin-Password": pwd }
    });

    if (!res.ok) {
        alert("Mot de passe incorrect");
        return;
    }

    adminPassword = pwd;

    const data = await res.json();
    document.getElementById("subject").value = data.subject;
    document.getElementById("prompt").value = data.prompt;

    document.getElementById("login").classList.add("hidden");
    document.getElementById("editor").classList.remove("hidden");
}

async function save() {
    const res = await fetch("/admin/templates", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-Admin-Password": adminPassword
        },
        body: JSON.stringify({
            subject: document.getElementById("subject").value,
            prompt: document.getElementById("prompt").value
        })
    });

    alert(res.ok ? "✔ Sauvegardé" : "❌ Erreur");
}
</script>

</body>
</html>
"""
