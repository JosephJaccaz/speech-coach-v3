import openai
import re

def generate_feedback(prompt: str) -> tuple[str, float | None]:
    """
    Appelle l'API OpenAI pour générer un feedback structuré à partir du prompt.

    Args:
        prompt: le texte complet à analyser (contenant consignes + transcription + contexte)

    Returns:
        feedback (str): le texte généré par l'IA
        note (float | None): la note extraite (si trouvée), sinon None
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un coach bienveillant et structuré pour des ONG."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )

    feedback = response.choices[0].message.content.strip()

    # Extraction de la note type 7/10
    match = re.search(r"(\d(?:\.\d)?)/10", feedback)
    note = float(match.group(1)) if match else None

    return feedback, note
