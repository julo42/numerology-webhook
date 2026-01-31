from openai import OpenAI


if __name__ == '__main__':
    prenom1 = 'Julien'
    date1 = '30/11/1980'
    prenom2 = 'Esther'
    date2 = '12/04/1978'

    with open('prompt', 'r', encoding='utf-8') as fd:
        buf = fd.read()

    prompt = buf.format(
        prenom1=prenom1,
        date1=date1,
        prenom2=prenom2,
        date2=date2
    )

    client = OpenAI()

    guidance_text = ""
    with client.responses.stream(model="gpt-5-mini", input=prompt) as stream:
        for event in stream:
            if event.type == "output_text.delta":
                guidance_text += event.delta
                print(event.delta, end="", flush=True)


    print("[GPT] Début génération…")

    last_logged = 0
    guidance_text = ""

    try:
        # Streaming
        with client.responses.stream(
            model="gpt-5-mini",
            input=prompt,
            reasoning={"effort": "medium"}
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    guidance_text += event.delta
                    # Log progress tous les 100 caractères
                    if len(guidance_text) // 100 > last_logged:
                        last_logged = len(guidance_text) // 100
                        print(f"[GPT] {len(guidance_text)} caractères générés…")

        print("\n[GPT] Génération terminée.")
        print("\n=== CONTENU FINAL ===")
        print(guidance_text)

    except Exception as e:
        print(f"[ERROR] Génération échouée: {str(e)}")
