from datetime import datetime
import webbrowser

# ------------------------
# Constantes
# ------------------------

MASTER_NUMBERS = {11, 22, 33}
SCORE_MIN = 40
SCORE_MAX = 90

# ------------------------
# Phrases complètes pour la synthèse
# ------------------------

FORCES_PHRASES = {
    "Leadership partagé": "un leadership équilibré et coopératif",
    "Complémentarité action/écoute": "une complémentarité entre action et écoute",
    "Harmonie et écoute mutuelle": "une harmonie basée sur l’écoute réciproque",
    "Joie et créativité": "une relation joyeuse et créative",
    "Stabilité et fiabilité": "une stabilité et fiabilité constantes",
    "Liberté et mouvement": "un couple basé sur la liberté et le mouvement",
    "Amour durable et protection": "un amour protecteur et durable",
    "Compréhension profonde": "une compréhension profonde entre partenaires",
    "Puissance et ambition": "une dynamique de puissance et d’ambition",
    "Compassion et transmission": "une relation empreinte de compassion et de transmission",
    "Connexion spirituelle élevée": "une connexion spirituelle élevée",
    "Différences enrichissantes": "une relation enrichissante grâce à la diversité des personnalités"
}

TENSION_PHRASES = {
    "ego": "la gestion des ego et des rapports de pouvoir",
    "dominance": "une tendance à la dominance dans la relation",
    "dependance": "une possible dépendance affective",
    "superficialite": "un manque de profondeur émotionnelle",
    "rigidite": "une rigidité dans les habitudes ou attentes",
    "instabilite": "une tendance à l’instabilité ou à la dispersion",
    "fusion": "un risque de fusion excessive",
    "isolement": "une tendance au repli ou à la distance émotionnelle",
    "rapport": "la gestion de rapports de force",
    "nostalgie": "une propension à se projeter dans le passé",
    "hypersensibilite": "une hypersensibilité émotionnelle",
    "ajustements": "la nécessité d’ajustements mutuels conscients"
}

LEVIERS_PHRASES = {
    "Clarifier les rôles": "clarifier les rôles et responsabilités",
    "Valoriser la sensibilité": "valoriser la sensibilité et l’écoute",
    "Affirmation personnelle": "favoriser l’affirmation personnelle",
    "Approfondir le lien": "approfondir le lien émotionnel",
    "Introduire de la souplesse": "introduire de la souplesse dans le quotidien",
    "Cadre minimal": "mettre en place un cadre minimal pour structurer la liberté",
    "Autonomie émotionnelle": "préserver l’autonomie émotionnelle",
    "Ouverture émotionnelle": "encourager l’ouverture émotionnelle",
    "Leadership partagé": "pratiquer un leadership partagé",
    "Renouveau": "favoriser le renouveau et l’adaptation",
    "Ancrage émotionnel": "ancrer la relation dans le concret",
    "Communication consciente": "maintenir une communication consciente et régulière"
}

# ------------------------
# Termes courts pour tableau
# ------------------------

TENSION_SHORT = {
    "ego": "Conflit d’ego",
    "dominance": "Dominance du 1",
    "dependance": "Dépendance affective",
    "superficialite": "Superficialité",
    "rigidite": "Rigidité",
    "instabilite": "Instabilité",
    "fusion": "Fusion excessive",
    "isolement": "Isolement",
    "rapport": "Rapport de force",
    "nostalgie": "Nostalgie",
    "hypersensibilite": "Hypersensibilité",
    "ajustements": "Ajustements nécessaires"
}

# ------------------------
# Matrice de compatibilité
# ------------------------

COMPATIBILITE_MATRIX = {
    (1, 1): {"score": 65, "forces": "Leadership partagé", "tension_key": "ego", "leviers": "Clarifier les rôles"},
    (1, 2): {"score": 60, "forces": "Complémentarité action/écoute", "tension_key": "dominance", "leviers": "Valoriser la sensibilité"},
    (2, 2): {"score": 75, "forces": "Harmonie et écoute mutuelle", "tension_key": "dependance", "leviers": "Affirmation personnelle"},
    (3, 3): {"score": 78, "forces": "Joie et créativité", "tension_key": "superficialite", "leviers": "Approfondir le lien"},
    (4, 4): {"score": 76, "forces": "Stabilité et fiabilité", "tension_key": "rigidite", "leviers": "Introduire de la souplesse"},
    (5, 5): {"score": 74, "forces": "Liberté et mouvement", "tension_key": "instabilite", "leviers": "Cadre minimal"},
    (6, 6): {"score": 82, "forces": "Amour durable et protection", "tension_key": "fusion", "leviers": "Autonomie émotionnelle"},
    (7, 7): {"score": 70, "forces": "Compréhension profonde", "tension_key": "isolement", "leviers": "Ouverture émotionnelle"},
    (8, 8): {"score": 62, "forces": "Puissance et ambition", "tension_key": "rapport", "leviers": "Leadership partagé"},
    (9, 9): {"score": 78, "forces": "Compassion et transmission", "tension_key": "nostalgie", "leviers": "Renouveau"},
    (11, 11): {"score": 76, "forces": "Connexion spirituelle élevée", "tension_key": "hypersensibilite", "leviers": "Ancrage émotionnel"}
}

DEFAULT_COMPAT = {
    "score": 60,
    "forces": "Différences enrichissantes",
    "tension_key": "ajustements",
    "leviers": "Communication consciente"
}

# ------------------------
# Interprétation
# ------------------------

INTERPRETATION_SHORT = {
    "Synergie exceptionnelle et alignement naturel": "Compatibilité exceptionnelle",
    "Compatibilité harmonieuse avec potentiel durable": "Compatibilité forte",
    "Compatibilité évolutive nécessitant ajustements conscients": "Compatibilité évolutive",
    "Relation karmique à forts enjeux d’apprentissage": "Relation à forts enjeux"
}

def interpretation(score, short=False):
    if score >= 85:
        text = "Synergie exceptionnelle et alignement naturel"
    elif score >= 70:
        text = "Compatibilité harmonieuse avec potentiel durable"
    elif score >= 55:
        text = "Compatibilité évolutive nécessitant ajustements conscients"
    else:
        text = "Relation karmique à forts enjeux d’apprentissage"
    if short:
        return INTERPRETATION_SHORT.get(text, text)
    return text

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
    diff = abs(cv1 - cv2)
    if diff <= 2:
        bonus += 10
    elif diff >= 6:
        bonus -= 10
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

    # Synthèse phrases complètes
    forces_phrase = FORCES_PHRASES.get(compat["forces"], compat["forces"])
    tension_phrase = TENSION_PHRASES.get(compat["tension_key"], "la nécessité d’ajustements mutuels conscients")
    leviers_phrase = LEVIERS_PHRASES.get(compat["leviers"], compat["leviers"])

    synthese = (
        f"{nom_a} et {nom_b} présentent une compatibilité globale de {score}/100. "
        f"Cette relation repose sur {forces_phrase} et "
        f"demande une vigilance particulière concernant {tension_phrase}. "
        f"Pour progresser, il est conseillé de {leviers_phrase}."
    )

    return {
        "noms": f"{nom_a} & {nom_b}",
        "chemin_de_vie": {nom_a: cv1, nom_b: cv2},
        "score_compatibilite": score,
        "interpretation": interpretation(score),
        "axes_relationnels": compat,  # termes courts pour le tableau
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

    recommandations_html = "".join(
        f"<li>{rec}</li>" for rec in rapport["recommandations"]
    )

    # Tensions courtes pour le tableau
    tension_table = TENSION_SHORT.get(
        rapport['axes_relationnels'].get("tension_key","ajustements"),
        "Ajustements nécessaires"
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
<p>{interpretation(rapport['score_compatibilite'], short=True)}</p>

<h2>⚖️ Axes relationnels</h2>
<ul>
<li><strong>Forces</strong> : {rapport['axes_relationnels']['forces']}</li>
<li><strong>Tensions</strong> : {tension_table}</li>
<li><strong>Leviers</strong> : {rapport['axes_relationnels']['leviers']}</li>
</ul>

<h2>🧠 Synthèse</h2>
<p>{rapport['synthese']}</p>

<h2>✅ Recommandations</h2>
<ul>{recommandations_html}</ul>

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
