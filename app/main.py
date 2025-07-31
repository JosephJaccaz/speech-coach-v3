import streamlit as st
from app.transcription import transcribe_audio
from app.feedback import generate_feedback
from app.ong_context import load_ong_context
from app.utils import draw_gauge, interpret_note, detect_troll_content
from app.interface_texts import textes, barometre_legendes
from app.email_sender import send_feedback_email
from pathlib import Path
from app.auth import login
import json

# Vérification de l'authentification
if not st.session_state.get("authenticated", False):
    logged_in = login()
    if not logged_in:
        st.stop()  # Empêche le reste du code de s'exécuter

def run_app():
    st.set_page_config(page_title="Speech Coach IA", page_icon="🎤")

    # Logo + titre centré
    st.markdown("""
        <div style="width: 100%; display: flex; flex-direction: column; align-items: center; margin-bottom: 40px;">
            <img src="https://www.thejob.ch/wp-content/themes/corris2014/images/corris_logo.svg" width="200" style="margin-bottom: 10px;" />
            <h1 style="font-family: 'Zen Kaku Gothic Antique', sans-serif; font-weight: 500; font-size: 32px; text-align: center; margin: 0;">
                &emsp;Speech Coach IA
            </h1>
        </div>
    """, unsafe_allow_html=True)

    # Langue
    langue_choisie = st.selectbox(
        "Choisis ta langue / Wähle deine Sprache / Scegli la tua lingua",
        options=["fr", "de", "it"],
        format_func=lambda x: {"fr": "Français 🇫🇷", "de": "Deutsch 🇩🇪", "it": "Italiano 🇮🇹"}[x]
    )
    t = textes[langue_choisie]

    st.write(t["intro"])
    user_email = st.text_input(t["email_label"], key="email")

    # Sélection ONG
    ong_dir = Path("data/organisations")
    ong_files = list(ong_dir.glob("*.json"))

    ong_map_list = []
    for f in ong_files:
        with open(f, encoding="utf-8") as fp:
            data = json.load(fp)
            name = data["meta"]["nom_par_langue"][langue_choisie]
            ong_map_list.append((name, f))

    ong_map_list.sort(key=lambda x: x[0].lower())
    ong_display_names = [name for name, _ in ong_map_list]
    ong_display_map = {name: path for name, path in ong_map_list}

    ong_choisie = st.selectbox(t["ong_label"], ong_display_names)
    audio_file = st.file_uploader(t["upload_label"], type=["mp3", "wav"])
    audio_bytes = audio_file.read() if audio_file is not None else None

    st.markdown(t["info_format"])

    if user_email and audio_bytes and ong_choisie:
        st.success(t["messages"]["speech_ready"])

        with st.spinner(t["messages"]["transcription_spinner"]):
            transcript, detected_lang = transcribe_audio(audio_bytes)

        st.success(t["messages"]["transcription_done"])

        # Détection contenu inapproprié
        if detect_troll_content(transcript):
            send_feedback_email(
                to="joseph.jaccaz@corris.com",
                html_content=f"""
                <p><b>⚠️ Alerte contenu inapproprié détecté</b></p>
                <p><b>Utilisateur :</b> {user_email}</p>
                <p><b>Transcription suspecte :</b></p>
                <pre>{transcript}</pre>
                """
            )

        # Génération feedback
        ong_path = ong_display_map[ong_choisie]
        prompt = load_ong_context(ong_path, langue_choisie, transcript)

        with st.spinner(t["messages"]["generation_feedback"]):
            feedback, note = generate_feedback(prompt)

            if note is not None:
                st.markdown({
                    "fr": "### 🌟 Baromètre de performance",
                    "de": "### 🌟 Leistungsbarometer",
                    "it": "### 🌟 Barometro di performance"
                }[langue_choisie])
                draw_gauge(note)
                st.markdown(f"**{interpret_note(note, langue_choisie)}**")

                with st.expander({
                    "fr": "ℹ️ Que signifie le baromètre ?",
                    "de": "ℹ️ Was bedeutet das Barometer?",
                    "it": "ℹ️ Cosa significa il barometro?"
                }[langue_choisie]):
                    st.markdown(barometre_legendes[langue_choisie])
            else:
                st.warning("⚠️ Aucune note n'a pu être générée pour ce pitch.")

if __name__ == "__main__":
    run_app()
