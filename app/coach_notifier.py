import json
import os
import smtplib
from email.mime.text import MIMEText
import streamlit as st
from app.interface_texts import textes

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

def notifier_coach(ong, langue, nom_dialogueur, feedback_ia, langue_interface="fr"):
    t = textes.get(langue_interface, textes["fr"])
    email_texts = t["email_coach"]

    html_content = f"""
    <p>{email_texts['salutation']}</p>
    <p>{email_texts['intro'].format(ong=ong, langue=langue.upper())}</p>
    <ul>
        <li><b>{email_texts['nom_dialogueur']}</b> {nom_dialogueur}</li>
    </ul>
    <p><b>{email_texts['feedback']}</b></p>
    <pre>{feedback_ia}</pre>
    <p>{email_texts['merci']}</p>
    <p>{email_texts['signature']}</p>
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

