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
    st.warning(f"🌍 Langue reçue dans notifier_coach : {langue_interface}")
    t = textes.get(langue_interface, textes["fr"])
    email_texts = t["email_coach"]

    mapping = charger_mapping_coachs()
    coach_email = get_email_coach(ong, langue, mapping)

    if not coach_email:
        st.warning(t["coach_notification_failed"])
        return False

    subject = t["email_subject_coach"].format(ong=ong)

    html_content = f"""
    <html>
      <body style="font-family:Arial, sans-serif; line-height:1.6; font-size:15px; color:#222;">
        <p>{email_texts['salutation']}</p>
        <p>{email_texts['intro'].format(ong=ong, langue=langue.upper())}</p>
        <ul>
            <li><b>{email_texts['nom_dialogueur']}</b> {nom_dialogueur}</li>
        </ul>
        <p><b>{email_texts['feedback']}</b></p>
        <div style="
          border-left: 4px solid #ccc;
          padding: 16px;
          margin: 24px 0;
          background-color: #f9f9f9;
          font-size: 15px;
          line-height: 1.8;
        ">
          {feedback_ia.replace('\\n', '<br><br>')}
        </div>

        <p>{email_texts['merci']}</p>
        <p>{email_texts['signature']}</p>
      </body>
    </html>
    """

    msg = MIMEText(html_content, "html", "utf-8")
    msg["Subject"] = subject
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
