from datetime import datetime
import webbrowser

# ============================================================
# CONSTANTES
# ============================================================

MASTER_NUMBERS = {11, 22, 33}
COMPATIBILITE_DISTANCE = {
    0: 100,
    1: 90,
    2: 80,
    3: 65,
    4: 50,
}

# ============================================================
# OUTILS NUMÉROLOGIQUES
# ============================================================

def reduction(n):
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(c) for c in str(n))
    return n

def parse_date(date_str):
    d = datetime.strptime(date_str, "%d/%m/%Y")
    return d.day, d.month, d.year

def profil_numerologique(date_str):
    j, m, a = parse_date(date_str)
    return {
        "jour": reduction(j),
        "mois": reduction(m),
        "annee": reduction(a),
        "chemin": reduction(j + m + a),
        "emotion": reduction(j + m),
        "mental": reduction(m + a),
    }

def distance_vibratoire(a, b):
    return min(abs(a - b), 9 - abs(a - b))

# ============================================================
# CATÉGORISATIONS NUMÉROLOGIQUES STANDARD
# ============================================================

def dominante(p):
    if p["chemin"] in {4, 6, 8}:
        return "stable"
    if p["chemin"] in {3, 5}:
        return "mobile"
    if p["chemin"] in {2, 7, 9, 11}:
        return "introspective"
    return "equilibree"

def dynamique_couple(p1, p2):
    d = distance_vibratoire(p1["chemin"], p2["chemin"])
    if d == 0:
        return "fusion"
    if d <= 2:
        return "harmonie"
    if d <= 4:
        return "complementarite"
    return "tension"

# ============================================================
# PHRASES COMPLÈTES (INDEXÉES PAR ÉTAT CALCULÉ)
# ============================================================

PROFIL_PHRASES = {
    "stable": (
        "Énergie ancrée et structurée. Besoin de sécurité, de constance et de repères affectifs. "
        "Personnalité fiable et rassurante."
    ),
    "mobile": (
        "Énergie dynamique et changeante. Besoin de liberté, de mouvement et de stimulation. "
        "Personnalité vive et adaptable."
    ),
    "introspective": (
        "Énergie intérieure et réfléchie. Besoin de sens, de profondeur et de compréhension émotionnelle. "
        "Personnalité sensible et lucide."
    ),
    "equilibree": (
        "Énergie équilibrée et neutre. Besoin de stabilité et de relations harmonieuses. "
        "Personnalité standard."
    ),
}

DYNAMIQUE_PHRASES = {
    "fusion": (
        "une résonance vibratoire naturelle favorisant une compréhension instinctive et profonde"
    ),
    "harmonie": (
        "une harmonie fluide fondée sur l’écoute, la compréhension mutuelle et la stabilité émotionnelle"
    ),
    "complementarite": (
        "une complémentarité évolutive permettant à chacun de grandir au contact de l’autre"
    ),
    "tension": (
        "une dynamique intense et transformatrice demandant une conscience relationnelle accrue"
    ),
}

INTIMITE_PHRASES = {
    ("stable", "mobile"): (
        "Dans l’intimité, {A} apporte profondeur et stabilité.\n"
        "{B} apporte mouvement, légèreté et créativité."
    ),
    ("mobile", "stable"): (
        "Dans l’intimité, {A} apporte mouvement, légèreté et créativité.\n"
        "{B} apporte profondeur et stabilité."
    ),
    ("equilibree", "equilibree"): (
        "Dans l’intimité, les deux partenaires partagent une approche équilibrée, "
        "alliant présence émotionnelle et respect des rythmes personnels."
    ),
}

COMMUNICATION_PHRASES = {
    "fluide": (
        "La communication repose sur une écoute naturelle et une expression sincère, "
        "favorisant des échanges apaisés et constructifs."
    ),
    "ajustement": (
        "La communication demande une attention consciente afin d’éviter les malentendus "
        "et de respecter la sensibilité de chacun."
    ),
}

INFLUENCE_DOMINANTE_PHRASES = {
    "stable": "apaisement, structure et stabilité émotionnelle",
    "mobile": "ouverture, dynamisme et créativité",
    "introspective": "profondeur, écoute et compréhension intérieure",
    "equilibree": "équilibre, modération et adaptabilité relationnelle",
}

HARMONISATION_PHRASES = {
    "tension": (
        "Instaurer une communication consciente afin de transformer les tensions en leviers d’évolution"
    ),
    "dispersion": (
        "Mettre en place un cadre souple permettant de canaliser l’énergie du couple"
    ),
    "rigidite": (
        "Introduire davantage de souplesse et d’adaptabilité dans le quotidien"
    ),
    "surcharge": (
        "Ancrer la relation dans des projets concrets et structurants"
    ),
    "equilibre": (
        "Préserver l’harmonie existante par une attention mutuelle régulière"
    ),
}

# ============================================================
# CALCULS DÉRIVÉS
# ============================================================

def influence_phrase(nom_source, nom_cible, p_source):
    dom = dominante(p_source)
    return (
        f"Ce que {nom_source} apporte à {nom_cible} : "
        f"{INFLUENCE_DOMINANTE_PHRASES[dom]}."
    )

def chemin_harmonisation(p1, p2):
    points = []

    if distance_vibratoire(p1["chemin"], p2["chemin"]) >= 5:
        points.append("tension")

    d1, d2 = dominante(p1), dominante(p2)
    if d1 == d2 == "mobile":
        points.append("dispersion")
    elif d1 == d2 == "stable":
        points.append("rigidite")

    if p1["chemin"] in MASTER_NUMBERS or p2["chemin"] in MASTER_NUMBERS:
        points.append("surcharge")

    if not points:
        points.append("equilibre")

    return [HARMONISATION_PHRASES[p] for p in dict.fromkeys(points)]

def score_compatibilite(p1, p2):
    def comp(a, b):
        d = distance_vibratoire(a, b)
        return COMPATIBILITE_DISTANCE.get(d, 50)

    score_chemin = comp(p1["chemin"], p2["chemin"])
    score_emotion = comp(p1["emotion"], p2["emotion"])
    score_mental = comp(p1["mental"], p2["mental"])
    score_jour = comp(p1["jour"], p2["jour"])

    score = (
        score_chemin * 0.40 +
        score_emotion * 0.25 +
        score_mental * 0.20 +
        score_jour * 0.15
    )

    # Bonus nombres maîtres (conditionné)
    if (
        (p1["chemin"] in MASTER_NUMBERS or p2["chemin"] in MASTER_NUMBERS)
        and score >= 70
    ):
        score += 5

    return round(min(100, score))

# ============================================================
# API PUBLIQUE — INCHANGÉE
# ============================================================

def rapport_couple(nom_a, date_a, nom_b, date_b):
    p1 = profil_numerologique(date_a)
    p2 = profil_numerologique(date_b)

    dom1, dom2 = dominante(p1), dominante(p2)
    dyn = dynamique_couple(p1, p2)
    score = score_compatibilite(p1, p2)

    synthese = (
        f"{nom_a} et {nom_b} présentent une compatibilité globale de {score}/100. "
        f"Cette relation repose sur {DYNAMIQUE_PHRASES[dyn]}."
    )

    return {
        "noms": f"{nom_a} & {nom_b}",
        "dates": {nom_a: date_a, nom_b: date_b},
        "profils": {
            nom_a: PROFIL_PHRASES[dom1],
            nom_b: PROFIL_PHRASES[dom2],
        },
        "dynamique": DYNAMIQUE_PHRASES[dyn],
        "intimite": INTIMITE_PHRASES.get(
            (dom1, dom2), INTIMITE_PHRASES.get(("equilibree", "equilibree"))
        ),
        "communication": COMMUNICATION_PHRASES[
            "ajustement" if dyn == "tension" else "fluide"
        ],
        "influence": {
            "A": influence_phrase(nom_a, nom_b, p1),
            "B": influence_phrase(nom_b, nom_a, p2),
        },
        "chemin": chemin_harmonisation(p1, p2),
        "score_compatibilite": score,
        "synthese": synthese,
    }

def render_rapport_html(rapport):
    nom_a, nom_b = rapport["dates"].keys()
    date_a, date_b = rapport["dates"].values()

    html = f"""
<html>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;">
<h1>NUMÉROLOGIE DE COUPLE</h1>
<h2>{rapport['noms']}</h2>

<p>Cette étude complète explore la dynamique profonde du couple grâce à une analyse numérologique fondée sur les dates de naissance :</p>
<ul>
<li>{nom_a} : {date_a}</li>
<li>{nom_b} : {date_b}</li>
</ul>

<h3>Profils Individuels</h3>
<p><strong>{nom_a}</strong><br>{rapport['profils'][nom_a]}</p>
<p><strong>{nom_b}</strong><br>{rapport['profils'][nom_b]}</p>

<h3>Énergie Fondamentale du Couple</h3>
<p>Leur essence commune est marquée par {rapport['dynamique']}.</p>

<h3>Intimité et Vie Privée</h3>
<p>{rapport['intimite'].format(A=nom_a, B=nom_b)}</p>

<h3>Communication & Interaction</h3>
<p>{rapport['communication']}</p>

<h3>Influence Mutuelle</h3>
<p>{rapport['influence']['A']}</p>
<p>{rapport['influence']['B']}</p>

<h3>Chemin d’Harmonisation</h3>
<ul>{"".join(f"<li>{c}.</li>" for c in rapport["chemin"])}</ul>

<p><strong>Score de compatibilité : {rapport['score_compatibilite']}/100</strong></p>
</body>
</html>
"""
    return html

# ============================================================
# EXÉCUTION — STRICTEMENT INCHANGÉE
# ============================================================

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
        webbrowser.open(f"file://{path}")
