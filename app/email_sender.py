import smtplib
from email.mime.text import MIMEText
import streamlit as st

def send_feedback_email(to: str, html_content: str, custom_subject: str = None) -> None:
    """
    Envoie le feedback par email au destinataire, avec sujet personnalisable.

    Args:
        to: adresse e-mail du destinataire
        html_content: contenu HTML du message
        custom_subject: sujet de l’e-mail (facultatif)
    """
    subject = custom_subject or "💬 Speech Coach IA : Feedback de ton speech"

    msg = MIMEText(html_content, "html", "utf-8")
    msg["Subject"] = subject
    msg["From"] = st.secrets["email_user"]
    msg["To"] = to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(st.secrets["email_user"], st.secrets["email_password"])
            server.send_message(msg)
        st.success(f"✅ Feedback envoyé automatiquement à {to} !")
    except Exception as e:
        st.error(f"❌ Erreur lors de l'envoi de l'e-mail : {e}")
