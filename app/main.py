import streamlit as st
from pathlib import Path
import json

st.set_page_config(page_title="Speech Coach IA", page_icon="🎤")

from app.transcription import transcribe_audio
from app.feedback import generate_feedback
from app.ong_context import load_ong_context
from app.utils import draw_gauge, format_feedback_as_html, extract_note, detect_troll_content
from app.interface_texts import textes
from app.email_sender import send_feedback_email
from app.coach_notifier import get_email_coach
from app.auth import login_user as login, logout_user as logout

# --- Authentification ---
if not st.session_state.get("authenticated", False):
    if not login():
        st.stop()
else:
    if st.button("Se déconnecter"):
        logout()
        st.stop()

# --- App principale ---
def run_app():
    st.set_page_config(page_title="Speech Coach IA", page_icon="🎤")

    # Logo + titre
    st.markdown("""
        <div style="text-align:center; margin-bottom:30px;">
            <img src="https://www.thejob.ch/wp-content/themes/corris2014/images/corris_logo.svg" width="200"/>
            <h1>Speech Coach IA</h1>
        </div>
    """, unsafe_allow_html=True)

    # Sélection de la langue
    langue_choisie = st.selectbox(
        "Choisis ta langue / Wähle deine Sprache / Scegli la tua lingua",
        ["fr", "de", "it"],
        format_func=lambda x: {"fr": "Français 🇫🇷", "de": "Deutsch 🇩🇪", "it": "Italiano 🇮🇹"}[x]
    )
    t = textes[langue_choisie]

    # Email utilisateur
    user_email = st.text_input(t["email_label"])

    # Sélection ONG
    ong_dir = Path("data/organisations")
    ong_files = list(ong_dir.glob("*.json"))
    ong_map = {}

    for f in ong_files:
        with open(f, encoding="utf-8") as fp:
            data = json.load(fp)
            name = data["meta"]["nom_par_langue"].get(langue_choisie, f.stem)
            ong_map[name] = f

    ong_choisie = st.selectbox(t["ong_label"], sorted(ong_map.keys()))

    # Upload audio
    audio_file = st.file_uploader(t["upload_label"], type=["mp3", "wav"])

    if st.button(t["analyse_button"]) and user_email and audio_file:
        st.success(t["messages"]["speech_ready"])

        # Transcription
        with st.spinner(t["messages"]["transcription_spinner"]):
            transcript, detected_lang = transcribe_audio(audio_file.read())
        st.success(t["messages"]["transcription_done"])

        # Détection contenu suspect
        if detect_troll_content(transcript):
            send_feedback_email(
                to="joseph.jaccaz@corris.com",
                html_content=f"<p>⚠️ Contenu suspect envoyé par {user_email}</p><pre>{transcript}</pre>"
            )

        # Charger contexte ONG
        prompt = load_ong_context(ong_map[ong_choisie], langue_choisie, transcript)

        # Génération feedback
        with st.spinner(t["messages"]["generation_feedback"]):
            feedback = generate_feedback(prompt)
        note = extract_note(feedback)

        # --- Baromètre ---
        if note is not None:
            draw_gauge(note, langue_choisie)
        else:
            st.warning("⚠️ Note non détectée dans le feedback.")

        # --- Feedback ---
        st.markdown(format_feedback_as_html(feedback), unsafe_allow_html=True)

        # --- Notification coach ---
        email_coach = get_email_coach(ong_choisie)
        if email_coach:
            send_feedback_email(
                to=email_coach,
                html_content=f"<p>Analyse terminée pour <b>{user_email}</b> (ONG : {ong_choisie})</p>"
            )

if __name__ == "__main__":
    run_app()
