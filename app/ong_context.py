import json
from pathlib import Path

def load_ong_context(ong_path: Path, langue: str, transcript: str) -> str:
    """
    Charge les données de l’ONG et construit le prompt complet à envoyer à GPT.

    Args:
        ong_path: chemin vers le fichier JSON de l’ONG sélectionnée
        langue: langue sélectionnée ("fr", "de", "it")
        transcript: texte du pitch transcrit

    Returns:
        prompt complet à envoyer à GPT
    """
    with open(ong_path, encoding="utf-8") as f:
        ong_data = json.load(f)

    ong_lang_data = ong_data.get(langue, {})
    slogan = ong_lang_data.get("slogan", "—")
    redflags = ", ".join(ong_lang_data.get("redflags", []))
    pitch_model = ong_lang_data.get("pitch_reference", "—")
    stats = ong_data.get("stats_importantes", {})

    ong_context = f"""
🔎 Informations ONG ({ong_path.stem.replace('_', ' ').title()}) :

- Slogan : {slogan}
- Redflags : {redflags}
- Pitch modèle : {pitch_model}
- Statistiques importantes : {stats}
"""

    prompt_path = Path("prompts") / f"prompt_{langue}.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"❌ Prompt manquant pour la langue : {langue}")

    with open(prompt_path, encoding="utf-8") as f:
        prompt_intro = f.read()

    # Construction finale du prompt
    return f"{prompt_intro}\n\n{ong_context}\n\n{transcript}"

