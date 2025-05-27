import openai
import io
from langdetect import detect

def transcribe_audio(audio_bytes: bytes) -> tuple[str, str]:
    """
    Transcrit un fichier audio avec Whisper et détecte la langue.
    
    Args:
        audio_bytes: contenu brut du fichier audio

    Returns:
        transcription (str), detected_language (str)
    """
    audio_io = io.BytesIO(audio_bytes)
    audio_io.name = "speech.wav"

    response = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_io,
        response_format="text"
    )

    transcription = response.strip()
    detected_lang = detect(transcription)

    return transcription, detected_lang

