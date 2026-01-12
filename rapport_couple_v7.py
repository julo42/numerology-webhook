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
    """
    Détecte automatiquement les formats les plus courants :
    - "JJ/MM/AAAA"
    - "YYYY-MM-JJ"
    - "YYYY/MM/DD"
    - "DD-MM-YYYY"
    Retourne (jour, mois, année) sous forme d'entiers.
    """
    formats = ["%d/%m/%Y", "%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"]
    for fmt in formats:
        try:
            d = datetime.strptime(date_str, fmt)
            return d.day, d.month, d.year
        except ValueError:
            continue
    raise ValueError(f"Format de date inconnu : {date_str}")

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
    if a in MASTER_NUMBERS or b in MASTER_NUMBERS:
        return min(abs(a - b), 11)
    return min(abs(a - b), 9 - abs(a - b))

# ============================================================
# CATÉGORISATIONS NUMÉROLOGIQUES
# ============================================================

def dominante(p):
    chemin = p["chemin"]
    if chemin in {4, 6, 8}:
        return "stable"
    if chemin in {3, 5}:
        return "mobile"
    if chemin in {2, 7, 9, 11}:
        return "introspective"
    if chemin in {22, 33}:
        return "maitre"
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
# PHRASES VARIÉES
# ============================================================

# Phrases pour intimité
INTIMITE_PHRASES = {
    ("stable", "stable"): "Dans l’intimité, {A} et {B} partagent sécurité et constance, créant un environnement rassurant et harmonieux.",
    ("stable", "mobile"): "Dans l’intimité, {A} apporte stabilité et profondeur, {B} apporte énergie et créativité.",
    ("stable", "introspective"): "Dans l’intimité, {A} apporte sécurité, {B} apporte clairvoyance et profondeur.",
    ("stable", "maitre"): "Dans l’intimité, {A} apporte stabilité, {B} inspire et guide.",

    ("mobile", "stable"): "Dans l’intimité, {A} insuffle mouvement et créativité, {B} apporte constance et sécurité.",
    ("mobile", "mobile"): "Dans l’intimité, {A} et {B} partagent dynamisme et spontanéité, favorisant amusement et innovation, mais doivent parfois coordonner leurs rythmes.",
    ("mobile", "introspective"): "Dans l’intimité, {A} apporte spontanéité et dynamisme, {B} offre réflexion et profondeur.",
    ("mobile", "maitre"): "Dans l’intimité, {A} apporte mouvement et créativité, {B} inspire et guide.",

    ("introspective", "stable"): "Dans l’intimité, {A} offre clairvoyance, {B} apporte stabilité et soutien.",
    ("introspective", "mobile"): "Dans l’intimité, {A} offre réflexion et sens, {B} apporte spontanéité et dynamisme.",
    ("introspective", "introspective"): "Dans l’intimité, {A} et {B} partagent profondeur et analyse, favorisant conversations riches et compréhension mutuelle.",
    ("introspective", "maitre"): "Dans l’intimité, {A} apporte profondeur et analyse, {B} inspire et guide.",

    ("maitre", "stable"): "Dans l’intimité, {A} inspire et guide, {B} apporte équilibre et sécurité.",
    ("maitre", "mobile"): "Dans l’intimité, {A} inspire et guide, {B} apporte mouvement et légèreté.",
    ("maitre", "introspective"): "Dans l’intimité, {A} inspire et élève, {B} apporte profondeur et analyse.",
    ("maitre", "maitre"): "Dans l’intimité, {A} et {B} partagent vision et inspiration mutuelle, guidant leur relation avec clarté et intuition."
}
INTIMITE_PHRASES_DEFAULT = "Dans l’intimité, {A} et {B} harmonisent leurs différences et s’épanouissent ensemble."

# Communication selon dynamique
COMMUNICATION_PHRASES = {
    "fusion": "La communication est naturelle et spontanée, favorisant compréhension et complicité.",
    "harmonie": "Les échanges sont équilibrés, basés sur écoute et respect mutuel.",
    "complementarite": "La communication permet à chacun d’apporter ses forces et de combler les faiblesses de l’autre.",
    "tension": "La communication demande vigilance et ajustement afin d’éviter malentendus et conflits."
}

HARMONISATION_PHRASES = {
    "tension": "Transformer les tensions en leviers d’évolution par communication consciente.",
    "dispersion": "Canaliser l’énergie du couple par un cadre souple.",
    "rigidite": "Introduire plus de souplesse et d’adaptabilité dans le quotidien.",
    "surcharge": "Ancrer la relation dans des projets concrets et structurants.",
    "equilibre": "Préserver l’harmonie existante par attention mutuelle régulière."
}

CHEMIN_DOMINANTES = {
    1: "affirmation", 2: "écoute", 3: "expression", 4: "stabilité", 5: "mouvement",
    6: "harmonie", 7: "intériorité", 8: "structure", 9: "compassion",
    11: "intuition", 22: "construction", 33: "transmission"
}

DYNAMIQUE_PHRASES = {
    "fusion": (
        "Leur essence commune reflète une fusion profonde : ils partagent naturellement "
        "leurs émotions, idées et projets, créant une connexion instinctive et harmonieuse."
    ),
    "harmonie": (
        "Leur essence commune est marquée par l’harmonie : leurs différences se complètent "
        "facilement, permettant des échanges équilibrés et une stabilité affective."
    ),
    "complementarite": (
        "Leur essence commune est caractérisée par la complémentarité : chacun apporte "
        "ses forces là où l’autre a des besoins, favorisant croissance et équilibre mutuel."
    ),
    "tension": (
        "Leur essence commune connaît une certaine tension : des différences de rythme, "
        "de besoins ou de priorités peuvent créer des frictions, mais aussi des opportunités "
        "d’évolution et de conscientisation dans la relation."
    ),
}

# ============================================================
# PROFILS INDIVIDUELS DETAILLES
# ============================================================

def get_profil_phrase_full(p):
    """
    Génère un profil individuel détaillé selon plusieurs critères :
    - Chemin de vie (dominante)
    - Jour (personnalité profonde)
    - Mois (émotion)
    - Année (mental)
    """
    chemin_dom = CHEMIN_DOMINANTES.get(p["chemin"], "équilibre")
    chemin_phrases = {
        1: "indépendant et assertif",
        2: "réceptif et diplomate",
        3: "créatif et expressif",
        4: "organisé et fiable",
        5: "adaptable et curieux",
        6: "protecteur et harmonieux",
        7: "réfléchi et introspectif",
        8: "ambitieux et structuré",
        9: "altruiste et compatissant",
        11: "visionnaire et intuitif",
        22: "constructif et stratégique",
        33: "enseignant et inspirant"
    }
    chemin_phrase = chemin_phrases.get(p["chemin"], "équilibré et modéré")
    return (
        f"Chemin de vie : {chemin_phrase}. "
        f"Nuances personnelles : personnalité centrée sur le jour {p['jour']}, "
        f"émotions influencées par le mois {p['mois']}, mental et réflexion guidés par l'année {p['annee']}."
    )

# ============================================================
# CALCULS DÉRIVÉS
# ============================================================

def influence_mutuelle(nom_A, nom_B, pA, pB):
    dominante_A = CHEMIN_DOMINANTES.get(pA["chemin"], "équilibre")
    dominante_B = CHEMIN_DOMINANTES.get(pB["chemin"], "équilibre")

    mapping_offre = {
        "affirmation": "élan et affirmation personnelle",
        "écoute": "apaisement et compréhension",
        "expression": "créativité et joie partagée",
        "stabilité": "structure et fiabilité",
        "mouvement": "dynamisme et adaptabilité",
        "harmonie": "équilibre et soutien",
        "intériorité": "réflexion et clairvoyance",
        "structure": "organisation et régularité",
        "compassion": "bienveillance et soutien",
        "intuition": "vision et inspiration",
        "construction": "projet concret et stabilité",
        "transmission": "partage et guidance"
    }

    mapping_complement = {
        "affirmation": "écoute et ouverture",
        "écoute": "initiative et courage",
        "expression": "écoute et constance",
        "stabilité": "flexibilité et créativité",
        "mouvement": "patience et structuration",
        "harmonie": "assertivité et décision",
        "intériorité": "expression et partage",
        "structure": "souplesse et imagination",
        "compassion": "affirmation et protection",
        "intuition": "pragmatisme et constance",
        "construction": "adaptabilité et créativité",
        "transmission": "écoute et équilibre"
    }

    phrase_A = mapping_offre.get(dominante_A, "équilibre et soutien mutuel")
    phrase_B = mapping_complement.get(dominante_B, "équilibre et soutien mutuel") if dominante_A == dominante_B else mapping_offre.get(dominante_B, "équilibre et soutien mutuel")

    return f"Ce que {nom_A} apporte à {nom_B} : {phrase_A}.", f"Ce que {nom_B} apporte à {nom_A} : {phrase_B}."

def chemin_harmonisation(p1, p2):
    points = []
    d1, d2 = dominante(p1), dominante(p2)
    dist = distance_vibratoire(p1["chemin"], p2["chemin"])

    if dist >= 5:
        points.append("tension")
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

    score = (
        comp(p1["chemin"], p2["chemin"]) * 0.40 +
        comp(p1["emotion"], p2["emotion"]) * 0.25 +
        comp(p1["mental"], p2["mental"]) * 0.20 +
        comp(p1["jour"], p2["jour"]) * 0.15
    )

    if (p1["chemin"] in MASTER_NUMBERS or p2["chemin"] in MASTER_NUMBERS) and score >= 70:
        score += 5

    return round(min(100, score))

# ============================================================
# RAPPORT DE COUPLE
# ============================================================

def get_intimite_phrase(dom1, dom2, nom_a, nom_b):
    phrase = INTIMITE_PHRASES.get((dom1, dom2), INTIMITE_PHRASES_DEFAULT)
    return phrase.format(A=nom_a, B=nom_b)

def rapport_couple(nom_a, date_a, nom_b, date_b):
    p1 = profil_numerologique(date_a)
    p2 = profil_numerologique(date_b)

    dom1, dom2 = dominante(p1), dominante(p2)
    dyn = dynamique_couple(p1, p2)
    score = score_compatibilite(p1, p2)

    synthese = f"{nom_a} et {nom_b} présentent une compatibilité globale de {score}/100."

    influence = influence_mutuelle(nom_a, nom_b, p1, p2)

    return {
        "noms": f"{nom_a} & {nom_b}",
        "dates": {nom_a: date_a, nom_b: date_b},
        "profils": {
            nom_a: get_profil_phrase_full(p1),
            nom_b: get_profil_phrase_full(p2)
        },
        "dynamique": dyn,
        "intimite": get_intimite_phrase(dom1, dom2, nom_a, nom_b),
        "communication": COMMUNICATION_PHRASES.get(dyn, 'Communication adaptée au couple'),
        "influence": {"A": influence[0], "B": influence[1]},
        "chemin": chemin_harmonisation(p1, p2),
        "score_compatibilite": score,
        "synthese": synthese,
    }

# ============================================================
# RENDER HTML
# ============================================================

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
<p>{DYNAMIQUE_PHRASES.get(rapport['dynamique'])}</p>

<h3>Intimité et Vie Privée</h3>
<p>{rapport['intimite']}</p>

<h3>Communication & Interaction</h3>
<p>{rapport['communication']}</p>

<h3>Influence Mutuelle</h3>
<p>{rapport['influence']['A']}</p>
<p>{rapport['influence']['B']}</p>

<h3>Chemin d’Harmonisation</h3>
<ul>{"".join(f"<li>{c}</li>" for c in rapport["chemin"])}</ul>

<p><strong>Score de compatibilité : {rapport['score_compatibilite']}/100</strong></p>
</body>
</html>
"""
    return html

# ============================================================
# EXÉCUTION
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
