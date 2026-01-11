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

def reduction_numerologique(n):
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(c) for c in str(n))
    return n

def chemin_de_vie(date_str):
    total = sum(int(c) for c in date_str if c.isdigit())
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
    leviers_phrase = LEVIERS_PHRASES.get(compat["leviers"], "maintenir une communication consciente")

    synthese = (
        f"{nom_a} et {nom_b} présentent une compatibilité globale de {score}/100. "
        f"Cette relation repose sur {forces_phrase} et "
        f"demande une vigilance particulière concernant {tension_phrase}. "
        f"Pour progresser, il est conseillé de {leviers_phrase}."
    )

    return {
        "noms": f"{nom_a} & {nom_b}",
        "chemin_de_vie": {nom_a: date_a, nom_b: date_b},
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
    noms = rapport['noms']
    cv_dict = rapport['chemin_de_vie']
    score = rapport['score_compatibilite']
    synthese = rapport['synthese']

    nom_a, nom_b = list(cv_dict.keys())
    date_a, date_b = cv_dict[nom_a], cv_dict[nom_b]

    # Profils individuels (texte narratif)
    def profil_html(nom, cv):
        if cv in [1, 3, 5]:
            energie = "Énergie créative, communicative, adaptable."
            besoins = "Besoin de liberté, de mouvement, de variété, et de stimulation intellectuelle."
            traits = "Esprit vif, expressif, ouvert."
        elif cv in [2, 4, 6]:
            energie = "Énergie intuitive, profonde, sensible."
            besoins = "Besoin d’authenticité, de stabilité affective, de compréhension émotionnelle et d’ancrage."
            traits = "Personnalité tournée vers la sagesse intérieure."
        elif cv in [7, 8, 9, 11, 22, 33]:
            energie = "Énergie analytique et structurante, réfléchie et stratégique."
            besoins = "Besoin de clarté, d’organisation et d’épanouissement personnel."
            traits = "Esprit réfléchi, autonome, parfois intense."
        else:
            energie = "Énergie équilibrée et neutre."
            besoins = "Besoin de stabilité et de relations harmonieuses."
            traits = "Personnalité standard."
        return f"<p>{energie} {besoins} {traits}</p>"

    profil_a_html = profil_html(nom_a, date_a)
    profil_b_html = profil_html(nom_b, date_b)

    # Axes relationnels
    compat = rapport['axes_relationnels']
    forces_phrase = FORCES_PHRASES.get(compat["forces"], compat["forces"])
    tension_phrase = TENSION_PHRASES.get(compat["tension_key"], "ajustements nécessaires")
    leviers_phrase = LEVIERS_PHRASES.get(compat["leviers"], "communication consciente")

    html = f"""
<html>
<head><meta charset="utf-8"><title>Rapport Numérologique de Couple</title></head>
<body style="font-family:Arial,sans-serif;background:#f6f6f6;padding:20px;">
<div style="max-width:700px;margin:auto;background:#fff;padding:20px;border-radius:8px;">
<h1 style="text-align:center;">NUMÉROLOGIE DE COUPLE</h1>
<p style="text-align:center;font-size:18px;"><strong>{noms}</strong></p>

<p>Cette étude complète explore la dynamique profonde du couple grâce à une analyse numérologique fondée sur les dates de naissance :</p>
<ul>
<li>{nom_a} : {date_a}</li>
<li>{nom_b} : {date_b}</li>
</ul>
<p>Elle couvre : les profils individuels, l’énergie commune, la communication, l’intimité, l’influence mutuelle, les forces, les défis et les chemins d’harmonisation.</p>

<h2>Profils Individuels</h2>
<h3>{nom_a} ({date_a})</h3>{profil_a_html}
<h3>{nom_b} ({date_b})</h3>{profil_b_html}

<h2>Énergie Fondamentale du Couple</h2>
<p>Ensemble, leurs vibrations créent une dynamique fondée sur :</p>
<ul>
<li>la complémentarité entre {nom_a} et {nom_b} ;</li>
<li>une capacité à équilibrer réflexion intérieure et expression spontanée ;</li>
<li>une alchimie émotionnelle forte ;</li>
<li>un potentiel évolutif élevé basé sur la compréhension et l’ouverture.</li>
</ul>
<p>Leur essence commune est marquée par {forces_phrase}, {tension_phrase} et {leviers_phrase}.</p>

<h2>Intimité et Vie Privée</h2>
<p>Dans l’intimité, {nom_a} apporte profondeur et stabilité.<br>{nom_b} apporte mouvement, légèreté et créativité.</p>
<p>Ils trouvent un équilibre naturel lorsque :</p>
<ul>
<li>{nom_a} s’ouvre à plus de spontanéité ;</li>
<li>{nom_b} ralentit pour accueillir l’émotion et la profondeur.</li>
</ul>
<p>Résultat : une intimité vivante, chaleureuse, authentique.</p>

<h2>Communication & Interaction</h2>
<p>Forces :</p>
<ul>
<li>{nom_a} : écoute, intuition, calme.</li>
<li>{nom_b} : expression, créativité, dynamisme.</li>
</ul>
<p>Défis :</p>
<ul>
<li>éviter que la sensibilité de {nom_a} ne se sente submergée ;</li>
<li>éviter que l’énergie verbale de {nom_b} ne devienne impulsive.</li>
</ul>
<p>Clés d’harmonisation :</p>
<ul>
<li>parler avec douceur ;</li>
<li>exprimer les besoins simplement ;</li>
<li>ne pas interpréter trop vite les émotions de l’autre.</li>
</ul>

<h2>Influence Mutuelle</h2>
<p>Ce que {nom_a} apporte à {nom_b} :</p>
<ul>
<li>apaisement</li>
<li>profondeur</li>
<li>stabilité émotionnelle</li>
</ul>
<p>Ce que {nom_b} apporte à {nom_a} :</p>
<ul>
<li>ouverture</li>
<li>dynamisme</li>
<li>créativité</li>
</ul>
<p>Ils se complètent naturellement : ensemble, ils créent un équilibre rare.</p>

<h2>Chemin d’Harmonisation</h2>
<ul>
<li>valoriser leurs différences plutôt que les craindre ;</li>
<li>instaurer un rythme alternant calme ({nom_a}) et mouvement ({nom_b}) ;</li>
<li>cultiver la gratitude mutuelle ;</li>
<li>maintenir un dialogue clair et apaisé ;</li>
<li>nourrir des projets communs stimulant l’un et rassurant l’autre.</li>
</ul>

<p style="font-weight:bold;">Score de compatibilité : {score}/100</p>

<hr>
<p style="font-size:12px;color:#777;text-align:center;">Rapport généré automatiquement – Numérologie</p>
</div>
</body>
</html>
"""
    return html


# ------------------------
# Exécution
# ------------------------
if __name__ == "__main__":
    exemples = [
        ("Danielle Combelles", "24/11/1966", "Frédéric Néron", "23/05/1975"),
        ("Alice", "01/01/2000", "Bob", "04/02/1998"),
        ("Julien", "30/11/1980", "Esther", "12/04/1978")
    ]

    for i, (nom_a, date_a, nom_b, date_b) in enumerate(exemples, 1):
        rapport = rapport_couple(nom_a, date_a, nom_b, date_b)
        html = render_rapport_html(rapport)
        path = f"/tmp/rapport_couple_{i}.html"
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"Rapport Numérologique : {rapport['noms']}")
        print(
            f"Bonjour,\n\n"
            f"Voici votre rapport numérologique de couple.\n\n"
            f"Score : {rapport['score_compatibilite']}/100\n\n"
            f"{rapport['synthese']}"
        )

        webbrowser.open(f"file://{path}")
