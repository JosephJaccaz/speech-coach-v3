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
    """
    Envoie un email au coach responsable de l'ONG + langue, dans la langue de l'interface.
    """
    t = textes.get(langue_interface, textes["fr"])
    mapping = charger_mapping_coachs()
    coach_email = get_email_coach(ong, langue, mapping)

    if not coach_email:
        st.warning(t["coach_notification_failed"])
        return False

    # 📨 Sujet par langue
    sujets = {
        "fr": f"[Speech Coach IA] Nouveau pitch - {nom_dialogueur}",
        "de": f"[Speech Coach IA] Neuer Pitch von {nom_dialogueur}",
        "it": f"[Speech Coach IA] Nuovo pitch - {nom_dialogueur}"
    }
    sujet = sujets.get(langue_interface, sujets["fr"])

    # 💬 Corps de mail localisé
    corps = {
        "fr": f"""
        <p>Bonjour,</p>
        <p>Un·e dialogueur·euse a soumis un nouveau pitch pour l'ONG <b>{ong}</b> en langue <b>{langue.upper()}</b>.</p>
        <p><b>Email du dialogueur :</b> {nom_dialogueur}</p>
        <p><b>🧠 Feedback IA :</b></p>
        <pre>{feedback_ia}</pre>
        <p>Merci pour ton suivi ✨<br>– Speech Coach IA</p>
        """,
        "de": f"""
        <p>Hallo,</p>
        <p>Ein*e Fundraiser*in hat einen neuen Pitch f&uuml;r die NGO <b>{ong}</b> auf <b>{langue.upper()}</b> eingereicht.</p>
        <p><b>Email der Person:</b> {nom_dialogueur}</p>
        <p><b>🧠 Feedback der KI:</b></p>
        <pre>{feedback_ia}</pre>
        <p>Danke f&uuml;r dein Coaching ✨<br>– Speech Coach IA</p>
        """,
        "it": f"""
        <p>Ciao,</p>
        <p>Un* dialogator* ha inviato un nuovo pitch per l'ONG <b>{ong}</b> in lingua <b>{langue.upper()}</b>.</p>
        <p><b>Email del dialogatore:</b> {nom_dialogueur}</p>
        <p><b>🧠 Feedback IA:</b></p>
        <pre>{feedback_ia}</pre>
        <p>Grazie per il tuo coaching ✨<br>– Speech Coach IA</p>
        """
    }
    html_content = corps.get(langue_interface, corps["fr"])

    msg = MIMEText(html_content, "html", "utf-8")
    msg["Subject"] = sujet
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
