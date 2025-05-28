import json
import os
from email.message import EmailMessage
import smtplib

def charger_mapping_coachs(json_path="data/coachs.json"):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Fichier introuvable : {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_email_coach(ong, mapping):
    return mapping.get(ong)

def notifier_coach(ong, nom_dialogueur, lien_audio, feedback_ia, expediteur="noreply@corris.com", mot_de_passe="votre_mot_de_passe"):
    mapping = charger_mapping_coachs()
    coach_email = get_email_coach(ong, mapping)
    
    if not coach_email:
        print(f"⚠️ Aucun coach défini pour l’ONG : {ong}")
        return False

    message = EmailMessage()
    message["Subject"] = f"[Speech Coach IA] Nouveau pitch - {nom_dialogueur}"
    message["From"] = expediteur
    message["To"] = coach_email

    message.set_content(f"""
Bonjour,

Un·e dialogueur·euse a soumis un pitch pour l'ONG **{ong}**.

👤 Dialogueur·euse : {nom_dialogueur}
🎧 Audio : {lien_audio}

🧠 Feedback IA :
{feedback_ia}

Merci pour ton suivi personnalisé !

— Speech Coach IA
""")

    try:
        with smtplib.SMTP("smtp.corris.com", 587) as smtp:
            smtp.starttls()
            smtp.login(expediteur, mot_de_passe)
            smtp.send_message(message)
        print(f"✅ Notification envoyée à {coach_email}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l’envoi de l’email : {e}")
        return False

