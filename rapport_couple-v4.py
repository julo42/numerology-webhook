from datetime import datetime
import webbrowser

# ------------------------
# Constantes
# ------------------------

MASTER_NUMBERS = {11, 22, 33}
SCORE_MIN = 40
SCORE_MAX = 90

# ------------------------
# Matrice de compatibilité
# ------------------------

COMPATIBILITE_MATRIX = {
    (1, 1): {"score": 65, "forces": "Leadership partagé", "tensions": "Conflit d’ego", "leviers": "Clarifier les rôles"},
    (1, 2): {"score": 60, "forces": "Complémentarité action/écoute", "tensions": "Dominance du 1", "leviers": "Valoriser la sensibilité"},
    (2, 2): {"score": 75, "forces": "Harmonie et écoute mutuelle", "tensions": "Dépendance affective", "leviers": "Affirmation personnelle"},
    (3, 3): {"score": 78, "forces": "Joie et créativité", "tensions": "Superficialité", "leviers": "Approfondir le lien"},
    (4, 4): {"score": 76, "forces": "Stabilité et fiabilité", "tensions": "Rigidité", "leviers": "Introduire de la souplesse"},
    (5, 5): {"score": 74, "forces": "Liberté et mouvement", "tensions": "Instabilité", "leviers": "Cadre minimal"},
    (6, 6): {"score": 82, "forces": "Amour durable et protection", "tensions": "Fusion excessive", "leviers": "Autonomie émotionnelle"},
    (7, 7): {"score": 70, "forces": "Compréhension profonde", "tensions": "Isolement", "leviers": "Ouverture émotionnelle"},
    (8, 8): {"score": 62, "forces": "Puissance et ambition", "tensions": "Rapport de force", "leviers": "Leadership partagé"},
    (9, 9): {"score": 78, "forces": "Compassion et transmission", "tensions": "Nostalgie", "leviers": "Renouveau"},
    (11, 11): {"score": 76, "forces": "Connexion spirituelle élevée", "tensions": "Hypersensibilité", "leviers": "Ancrage émotionnel"}
}

DEFAULT_COMPAT = {
    "score": 60,
    "forces": "Différences enrichissantes",
    "tensions": "Ajustements nécessaires",
    "leviers": "Communication consciente"
}

# ------------------------
# Outils dates & numérologie
# ------------------------

def parse_date(date_str):
    if "-" in date_str:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    elif "/" in date_str:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
    else:
        raise ValueError("Format de date invalide")
    return dt.strftime("%Y-%m-%d")


def reduction_numerologique(n):
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(c) for c in str(n))
    return n


def chemin_de_vie(date_str):
    date_norm = parse_date(date_str)
    total = sum(int(c) for c in date_norm if c.isdigit())
    return reduction_numerologique(total)

# ------------------------
# Compatibilité
# ------------------------

def compatibilite_couple(cv1, cv2):
    key = tuple(sorted((cv1, cv2)))
    return COMPATIBILITE_MATRIX.get(key, DEFAULT_COMPAT)


def calcul_ponderations(cv1, cv2):
    bonus = 0

    # Écart vibratoire
    diff = abs(cv1 - cv2)
    if diff <= 2:
        bonus += 10
    elif diff >= 6:
        bonus -= 10

    # Présence de maître-nombre
    if cv1 in MASTER_NUMBERS:
        bonus += 5
    if cv2 in MASTER_NUMBERS:
        bonus += 5

    return bonus


def score_final(cv1, cv2):
    base = compatibilite_couple(cv1, cv2)["score"]
    bonus = calcul_ponderations(cv1, cv2)
    score = base + bonus
    return max(SCORE_MIN, min(SCORE_MAX, score))


def interpretation(score):
    if score >= 85:
        return "Synergie exceptionnelle et alignement naturel"
    if score >= 70:
        return "Compatibilité harmonieuse avec potentiel durable"
    if score >= 55:
        return "Compatibilité évolutive nécessitant ajustements conscients"
    return "Relation karmique à forts enjeux d’apprentissage"


def recommandations(cv1, cv2):
    recs = [
        "Instaurer une communication consciente et régulière.",
        "Respecter les besoins et rythmes individuels."
    ]
    if 4 in (cv1, cv2):
        recs.append("Introduire plus de souplesse dans l’organisation.")
    if 5 in (cv1, cv2):
        recs.append("Préserver l’espace personnel et la liberté.")
    if 7 in (cv1, cv2):
        recs.append("Partager des temps de réflexion ou de profondeur.")
    if cv1 in MASTER_NUMBERS or cv2 in MASTER_NUMBERS:
        recs.append("Ancrer la relation dans des projets concrets.")
    return recs[:5]

# ------------------------
# Rapport
# ------------------------

def rapport_couple(nom_a, date_a, nom_b, date_b):
    cv1 = chemin_de_vie(date_a)
    cv2 = chemin_de_vie(date_b)

    compat = compatibilite_couple(cv1, cv2)
    score = score_final(cv1, cv2)

    synthese = (
        f"{nom_a} et {nom_b} présentent une compatibilité globale de {score}/100. "
        f"Cette relation repose sur {compat['forces'].lower()} et "
        f"demande une vigilance particulière concernant {compat['tensions'].lower()}."
    )

    return {
        "noms": f"{nom_a} & {nom_b}",
        "chemin_de_vie": {nom_a: cv1, nom_b: cv2},
        "score_compatibilite": score,
        "interpretation": interpretation(score),
        "axes_relationnels": compat,
        "recommandations": recommandations(cv1, cv2),
        "synthese": synthese
    }

# ------------------------
# HTML
# ------------------------

def render_rapport_html(rapport):
    chemins = "".join(
        f"<li><strong>{nom}</strong> : {cv}</li>"
        for nom, cv in rapport["chemin_de_vie"].items()
    )

    recommandations = "".join(
        f"<li>{rec}</li>" for rec in rapport["recommandations"]
    )

    return f"""
<html>
<body style="font-family:Arial;background:#f6f6f6;padding:20px;">
<div style="max-width:600px;margin:auto;background:#fff;padding:20px;border-radius:8px;">
<h1 style="text-align:center;">Rapport Numérologique de Couple</h1>

<p style="text-align:center;font-size:18px;"><strong>{rapport['noms']}</strong></p>

<h2>🔢 Chemins de vie</h2>
<ul>{chemins}</ul>

<h2>❤️ Compatibilité</h2>
<p style="font-size:22px;color:#2c7;"><strong>{rapport['score_compatibilite']} / 100</strong></p>
<p>{rapport['interpretation']}</p>

<h2>⚖️ Axes relationnels</h2>
<ul>
<li><strong>Forces</strong> : {rapport['axes_relationnels']['forces']}</li>
<li><strong>Tensions</strong> : {rapport['axes_relationnels']['tensions']}</li>
<li><strong>Leviers</strong> : {rapport['axes_relationnels']['leviers']}</li>
</ul>

<h2>🧠 Synthèse</h2>
<p>{rapport['synthese']}</p>

<h2>✅ Recommandations</h2>
<ul>{recommandations}</ul>

<hr>
<p style="font-size:12px;color:#777;text-align:center;">Rapport généré automatiquement – Numérologie</p>
</div>
</body>
</html>
"""

# ------------------------
# Exécution
# ------------------------

if __name__ == "__main__":
    nom_a = "Alice"
    date_a = "01/01/2000"
    nom_b = "Bob"
    date_b = "04/02/1998"

    rapport = rapport_couple(nom_a, date_a, nom_b, date_b)
    html = render_rapport_html(rapport)

    path = "/tmp/rapport.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open(f"file://{path}")
