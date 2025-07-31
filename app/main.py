import streamlit as st
from pathlib import Path
import json

# --- Configuration initiale ---
st.set_page_config(page_title="Speech Coach IA", page_icon="🎤")

from app.transcription import transcribe_audio
from app.feedback import generate_feedback
from app.ong_context import load_ong_context
from app.utils import draw_gauge, format_feedback_as_html, extract_note, detect_troll_content
from app.interface_texts import textes
from app.email_sender import send_feedback_email
from app.coach_notifier import get_email_coach
from app.auth import login_user as login, logout_user as logout

from app.auth import login  # ← vérifie que le chemin est bon

try:
    if not callable(login):
        st.error("⚠️ Erreur : la fonction login() n'est pas définie correctement.")
        st.stop()
    if not login():  # login doit retourner True si connecté
        st.stop()
except Exception as e:
    st.error(f"Erreur dans login() : {e}")
    st.stop()

# --- Authentification ---
if not st.session_state.get("authenticated", False):
    if not login():
        st.stop()
else:
    if st.button("Se déconnecter"):
        logout()
        st.experimental_rerun()

# --- App principale ---
def run_app():
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

    # Sélection ONG (mise en cache pour accélérer)
    @st.cache_data
    def load_ong_files():
        ong_dir = Path("data/organisations")
        ong_files = list(ong_dir.glob("*.json"))
        ong_map = {}
        for f in ong_files:
            try:
                with open(f, encoding="utf-8") as fp:
                    data = json.load(fp)
                    name = data["meta"]["nom_par_langue"].get(langue_choisie, f.stem)
                    ong_map[name] = f
            except Exception as e:
                st.error(f"Erreur de lecture du fichier {f.name}: {e}")
        return ong_map

    ong_map = load_ong_files()
    if not ong_map:
        st.error("Aucune ONG trouvée dans le dossier `data/organisations`.")
        st.stop()

    ong_choisie = st.selectbox(t["ong_label"], sorted(ong_map.keys()))

    # Upload audio
    audio_file = st.file_uploader(t["upload_label"], type=["mp3", "wav"])

    # Lancement analyse
    if st.button(t["analyse_button"]):
        if not user_email:
            st.warning("⚠️ Merci d'entrer ton adresse email.")
            st.stop()
        if not audio_file:
            st.warning("⚠️ Merci d'uploader un fichier audio.")
            st.stop()

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
        else:
            st.info("ℹ️ Aucun coach défini pour cette ONG.")

# --- Lancement ---
if __name__ == "__main__":
    run_app()
