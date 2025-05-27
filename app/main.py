import streamlit as st
from app.transcription import transcribe_audio
from app.feedback import generate_feedback
from app.ong_context import load_ong_context
from app.utils import draw_gauge, interpret_note, format_feedback_as_html
from app.interface_texts import textes, barometre_legendes
from pathlib import Path
from app.email_sender import send_feedback_email


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
    ong_names = [f.stem.replace("_", " ").title() for f in ong_files]
    ong_map = dict(zip(ong_names, ong_files))
    ong_choisie = st.selectbox(t["ong_label"], ong_names)

    audio_file = st.file_uploader(t["upload_label"], type=["mp3", "wav"])
    audio_bytes = audio_file.read() if audio_file else None

    st.markdown(t["info_format"])

    if user_email and audio_bytes and ong_choisie:
        st.success(t["messages"]["speech_ready"])

        with st.spinner(t["messages"]["transcription_spinner"]):
            transcript, detected_lang = transcribe_audio(audio_bytes)

        st.success(t["messages"]["transcription_done"])
        st.info(f"{t['messages']['langue_detectee']} {detected_lang.upper()}")

        prompt = load_ong_context(ong_map[ong_choisie], langue_choisie, transcript)

        with st.spinner(t["messages"]["generation_feedback"]):
            feedback, note = generate_feedback(prompt)

            if note:
                st.markdown({
                    "fr": "### 🎯 Baromètre de performance",
                    "de": "### 🎯 Leistungsbarometer",
                    "it": "### 🎯 Barometro di performance"
                }[langue_choisie])
                draw_gauge(note)
                st.markdown(f"**{interpret_note(note, langue_choisie)}**")

                with st.expander({
                    "fr": "ℹ️ Que signifie le baromètre ?",
                    "de": "ℹ️ Was bedeutet das Barometer?",
                    "it": "ℹ️ Cosa indica il barometro?"
                }[langue_choisie]):
                    st.markdown(barometre_legendes[langue_choisie])

            html_feedback = format_feedback_as_html(feedback, detected_lang)
            st.markdown(html_feedback, unsafe_allow_html=True)

send_feedback_email(to=email_user, html_content=html_feedback)


