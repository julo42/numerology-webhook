from datetime import datetime


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


def axes_relationnels(cv1, cv2):
    axes = {}
    # Forces
    if cv1 == cv2:
        axes["forces"] = "Grande harmonie, valeurs partagées."
    elif abs(cv1 - cv2) in (1, 2):
        axes["forces"] = "Complémentarité naturelle."
    else:
        axes["forces"] = "Diversité de points de vue stimulante."

    # Tensions
    if cv1 == 4 or cv2 == 4:
        axes["tensions"] = "Rigidité et besoin de contrôle."
    elif cv1 == 5 or cv2 == 5:
        axes["tensions"] = "Besoin d'indépendance et d'espace."
    else:
        axes["tensions"] = "Petites frictions liées aux différences de tempérament."

    # Leviers
    axes["leviers"] = "Écoute active, patience et projets communs."
    return axes


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
          <p style="font-size:20px;">
            <strong>{rapport["score_compatibilite"]} / 100</strong>
          </p>

          <h2>⚖️ Axes relationnels</h2>
          <ul>
            {axes}
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
    score = score_couple(cv1, cv2)
    axes = axes_relationnels(cv1, cv2)
    recs = recommandations(cv1, cv2)
    synthese = f"{nom_a} et {nom_b} ont un score de compatibilité de {score}/100. " \
               f"Axes clés : forces ({axes['forces']}), tensions ({axes['tensions']})."
    rapport = {
        "noms": f"{nom_a} & {nom_b}",
        "chemin_de_vie": {nom_a: cv1, nom_b: cv2},
        "score_compatibilite": score,
        "axes_relationnels": axes,
        "recommandations": recs,
        "synthese": synthese
    }
    return rapport


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
