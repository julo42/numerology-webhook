from datetime import datetime

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


# ------------------------
# Fonctions Numérologie
# ------------------------
def chemin_de_vie(date_str):
    """Calcule le chemin de vie à partir de la date YYYY-MM-DD"""
    total = sum(int(c) for c in date_str if c.isdigit())
    while total > 9 and total not in (11, 22, 33):
        total = sum(int(c) for c in str(total))
    return total


def score_couple(cv1, cv2):
    diff = abs(cv1 - cv2)
    base_score = 100 - diff * 10
    return max(0, min(base_score, 100))


def compatibilite_couple(cv1, cv2):
    key = tuple(sorted((cv1, cv2)))
    data = COMPATIBILITE_MATRIX.get(
        key,
        {
            "score": 60,
            "forces": "Différences enrichissantes",
            "tensions": "Ajustements nécessaires",
            "leviers": "Communication consciente"
        }
    )
    return data


def recommandations(cv1, cv2):
    recs = []
    recs.append("Planifier des moments de qualité ensemble.")
    recs.append("Communiquer ouvertement sur les besoins et limites.")
    if 4 in (cv1, cv2):
        recs.append("Travailler sur la flexibilité et la tolérance.")
    if 5 in (cv1, cv2):
        recs.append("Respecter l'espace personnel et l'indépendance.")
    if 7 in (cv1, cv2):
        recs.append("Partager des activités intellectuelles ou spirituelles.")
    return recs[:5]


def render_rapport_html(rapport):
    chemins = "".join(
        f"<li><strong>{nom}</strong> : {cv}</li>"
        for nom, cv in rapport["chemin_de_vie"].items()
    )

    axes = "".join(
        f"<li><strong>{k.capitalize()}</strong> : {v}</li>"
        for k, v in rapport["axes_relationnels"].items()
    )

    recommandations = "".join(
        f"<li>{rec}</li>"
        for rec in rapport["recommandations"]
    )

    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; background:#f6f6f6; padding:20px;">
        <div style="max-width:600px; background:#ffffff; margin:auto; padding:20px; border-radius:8px;">

          <h1 style="text-align:center;">Rapport Numérologique de Couple</h1>
          <p style="text-align:center; font-size:18px;">
            <strong>{rapport["noms"]}</strong>
          </p>

          <hr>

          <h2>🔢 Chemins de vie</h2>
          <ul>
            {chemins}
          </ul>

          <h2>❤️ Score de compatibilité</h2>
          <p style="font-size:22px; font-weight:bold; color:#2c7;">
          {rapport["score_compatibilite"]} / 100
          </p>

          <h2>⚖️ Axes relationnels</h2>
          <ul>
          <li><strong>Forces</strong> : {rapport["axes_relationnels"]["forces"]}</li>
          <li><strong>Tensions</strong> : {rapport["axes_relationnels"]["tensions"]}</li>
          <li><strong>Leviers d’harmonie</strong> : {rapport["axes_relationnels"]["leviers"]}</li>
          </ul>

          <h2>🧠 Synthèse</h2>
          <p>{rapport["synthese"]}</p>

          <h2>✅ Recommandations pratiques</h2>
          <ul>
            {recommandations}
          </ul>

          <hr>

          <p style="font-size:12px; color:#777; text-align:center;">
            Rapport généré automatiquement – Numérologie
          </p>

        </div>
      </body>
    </html>
    """


# ------------------------
# Rapport complet
# ------------------------
def rapport_couple(nom_a, date_a, nom_b, date_b):
    cv1 = chemin_de_vie(date_a)
    cv2 = chemin_de_vie(date_b)

    compat = compatibilite_couple(cv1, cv2)

    synthese = (
        f"{nom_a} et {nom_b} présentent une compatibilité de "
        f"{compat['score']}/100. "
        f"Cette relation repose sur {compat['forces'].lower()}, "
        f"tout en demandant une vigilance particulière sur {compat['tensions'].lower()}."
    )

    return {
        "noms": f"{nom_a} & {nom_b}",
        "chemin_de_vie": {nom_a: cv1, nom_b: cv2},
        "score_compatibilite": compat["score"],
        "axes_relationnels": {
            "forces": compat["forces"],
            "tensions": compat["tensions"],
            "leviers": compat["leviers"]
        },
        "recommandations": recommandations(cv1, cv2),
        "synthese": synthese
    }


if __name__ == '__main__':
    import webbrowser

    nom_a = 'Alice'
    date_a = '01/01/2000'
    nom_b = 'Bob'
    date_b = '04/02/1998'

    rapport = rapport_couple(nom_a, date_a, nom_b, date_b)
    html_content = render_rapport_html(rapport)
    path = '/tmp/rapport.html'
    with open(path, 'w', encoding='utf-8') as fd:
        fd.write(html_content)
    webbrowser.open(f'file://{path}')
