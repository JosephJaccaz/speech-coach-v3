import json
import os
import smtplib
from email.mime.text import MIMEText
import streamlit as st
from app.interface_texts import textes  # ✅ pour accéder aux traductions

def charger_mapping_coachs(json_path="data/coachs.json"):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Fichier introuvable : {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_email_coach(ong, langue, mapping):
    ong_entry = mapping.get(ong)
    if ong_entry:
        return ong_entry.get(langue)
    return None

def notifier_coach(ong, langue, nom_dialogueur, lien_audio, feedback_ia, langue_interface="fr"):
    """
    Envoie un email au coach responsable de l'ONG + langue, avec interface dans la bonne langue.
    """
    t = textes.get(langue_interface, textes["fr"])  # fallback au français
    mapping = charger_mapping_coachs()
    coach_email = get_email_coach(ong, langue, mapping)

    if not coach_email:
        st.warning(t["coach_notification_failed"])
        return False

    html_content = f"""
    <p>Bonjour,</p>
    <p>Un·e dialogueur·euse a soumis un pitch pour l'ONG <b>{ong}</b> en <b>{langue.upper()}</b>.</p>
    <ul>
        <li><b>Nom (email) du dialogueur :</b> {nom_dialogueur}</li>
        <li><b>Audio :</b> {lien_audio}</li>
    </ul>
    <p><b>🧠 Feedback IA :</b></p>
    <pre>{feedback_ia}</pre>
    <p>Merci pour ton coaching ✨</p>
    <p>– Speech Coach IA</p>
    """

    msg = MIMEText(html_content, "html", "utf-8")
    msg["Subject"] = f"[Speech Coach IA] Nouveau pitch ({ong}, {langue})"
    msg["From"] = st.secrets["email_user"]
    msg["To"] = coach_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(st.secrets["email_user"], st.secrets["email_password"])
            server.send_message(msg)
        st.success(t["coach_notification_success"])
        return True
    except Exception as e:
        st.error(f"{t['coach_notification_error']} {e}")
        return False
