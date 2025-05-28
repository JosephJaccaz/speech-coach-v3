import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageChops
import io

import re

def extract_note(feedback_text: str) -> float | None:
    """
    Extrait une note sur 10 (par ex. '7.5/10' ou '8/10') depuis un bloc de texte.
    Gère les formats avec virgule ou point.
    """
    match = re.search(r"(\d+(?:[.,]\d+)?)/10", feedback_text)
    if match:
        note_str = match.group(1).replace(",", ".")
        try:
            return float(note_str)
        except ValueError:
            return None
    return None


def draw_gauge(score):
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(5, 1.8), dpi=160, subplot_kw={'projection': 'polar'})

    # Mettre 0 à gauche (horizontal) et rotation antihoraire
    ax.set_theta_zero_location('W')  # 0° : Bas
    ax.set_theta_direction(-1)

    # Définition des zones
    zones = [
        (0, 2, '#8B0000'),     # Rouge foncé
        (2, 4, '#FF4500'),     # Orange vif
        (4, 6, '#FFA500'),     # Orange clair
        (6, 8, '#ADFF2F'),     # Vert clair
        (8, 10, '#228B22')     # Vert foncé
    ]

    for start, end, color in zones:
        theta1 = np.interp(start, [0, 10], [0, np.pi])
        theta2 = np.interp(end, [0, 10], [0, np.pi])
        ax.barh(
            y=1,
            width=theta2 - theta1,
            left=theta1,
            height=0.35,
            color=color,
            edgecolor='white',
            linewidth=1.5
        )

    # Aiguille
    angle = np.interp(score, [0, 10], [0, np.pi])
    ax.plot([angle, angle], [0, 1], color='black', lw=3)
    ax.plot(angle, 1, 'o', color='black', markersize=6)

    # Nettoyage du style
    ax.set_ylim(0, 1.1)
    ax.axis('off')
    plt.subplots_adjust(left=0.05, right=0.95, top=1.05, bottom=-10)
    fig.patch.set_alpha(0)  # Fond transparent (utile si tu veux l'intégrer avec d'autres éléments visuels)


    from PIL import Image, ImageChops

    # 1. Sauvegarde le graphique dans un buffer mémoire
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0, transparent=True)
    plt.close(fig)  # nettoyage mémoire
    buf.seek(0)
    img = Image.open(buf)

    # 2. Crop automatique du fond blanc transparent
    bg = Image.new(img.mode, img.size, (255, 255, 255, 0))  # fond transparent
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()

    if bbox:
        img_cropped = img.crop(bbox)
    else:
        img_cropped = img  # fallback : pas de différence détectée

    # 3. Affichage sans le moindre bord inutile
    st.image(img_cropped)

def interpret_note(score, langue):
    labels = {
        "fr": [
            (9, "🟢 Excellent – alignement parfait avec la méthode d’adhésion"),
            (7, "🟢 Bon – encore perfectible sur quelques points"),
            (5, "🟠 Moyen – équilibre émotionnel fragile"),
            (3, "🔴 Faible – attention à la tonalité et au discours"),
            (0, "⛔ Problématique – discours à retravailler profondément")
        ],
        "de": [
            (9, "🟢 Exzellent – vollständig im Einklang mit dem Dialogkonzept"),
            (7, "🟢 Gut – kleinere Verbesserungen möglich"),
            (5, "🟠 Mittel – emotionale Balance fragil"),
            (3, "🔴 Schwach – auf Ton und Inhalt achten"),
            (0, "⛔ Problematisch – muss grundlegend überarbeitet werden")
        ],
        "it": [
            (9, "🟢 Eccellente – perfettamente in linea con il metodo di adesione"),
            (7, "🟢 Buono – migliorabile in alcuni punti"),
            (5, "🟠 Medio – equilibrio emotivo fragile"),
            (3, "🔴 Debole – attenzione al tono e al messaggio"),
            (0, "⛔ Problema – discorso da rivedere profondamente")
        ]
    }
    for threshold, label in labels.get(langue, labels["fr"]):
        if score >= threshold:
            return label
    return "❓ Note non interprétable"


import re

def format_feedback_as_html(feedback_text, langue):
    # ✅ Convertir les **gras** en <strong>...</strong>
    html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", feedback_text)

    # ✅ Coloration et mots-clés
    html = html.replace("✓", "<span style='color:green; font-weight:bold;'>✓</span>")
    html = html.replace("⚠️", "<span style='color:red; font-weight:bold;'>⚠️</span>")
    html = html.replace("Suggestion d'amélioration", "<span style='color:#007BFF; font-weight:bold;'>Suggestion d'amélioration</span>")
    html = html.replace("Verbesserungsvorschlag", "<span style='color:#007BFF; font-weight:bold;'>Verbesserungsvorschlag</span>")
    html = html.replace("Suggerimento di miglioramento", "<span style='color:#007BFF; font-weight:bold;'>Suggerimento di miglioramento</span>")

    # ✅ Aération du texte
    paragraphs = html.split("\n")
    html_body = ""
    for line in paragraphs:
        line = line.strip()
        if not line:
            continue
        if line.startswith(("🟢", "📊", "🔍", "🎯", "🤝", "💢", "🌱", "🚀", "➡️", "📝")):
            html_body += f"<p style='margin:20px 0 6px 0; font-weight:bold;'>{line}</p>"
        elif any(key in line for key in ["Conclusion", "Conclusione", "Fazit"]):
            html_body += "<hr style='margin:24px 0; border:none; border-top:2px solid #eee;'>"
            html_body += f"<p style='margin:20px 0 6px 0; font-weight:bold;'>{line}</p>"
        else:
            html_body += f"<p style='margin:4px 0;'>{line}</p>"

    # ✅ Introduction et signature localisées
    intro, signature = {
        "fr": (
            "<p>Bonjour 👋<br>Voici ton feedback personnalisé suite à l’analyse de ton pitch vocal :</p><br>",
            "<p style='color:gray;'>--<br>Speech Coach IA 🧠<br>Un outil conçu avec soin pour les dialogueurs et leurs formateurs.</p>"
        ),
        "de": (
            "<p>Hallo 👋<br>Hier ist dein persönliches Feedback zur Analyse deines Sprach-Pitchs :</p><br>",
            "<p style='color:gray;'>--<br>Speech Coach IA 🧠<br>Ein Werkzeug mit Herz – für Fundraiser und Trainer:innen.</p>"
        ),
        "it": (
            "<p>Ciao 👋<br>Ecco il tuo feedback personalizzato sull’analisi del tuo pitch vocale :</p><br>",
            "<p style='color:gray;'>--<br>Speech Coach IA 🧠<br>Uno strumento creato con cura per dialogatori e formatori.</p>"
        )
    }.get(langue, ("<p>Hello 👋</p>", "<p style='color:gray;'>-- Speech Coach IA</p>"))

    if langue == "fr":
        signature += "<p style='font-size:12px; color:#aaa;'>PS : Ce feedback a été généré avec amour, café ☕ et un soupçon de GPT par Joseph 💻</p>"

    return f"""
        <div class='zen-feedback'>
            {intro}
            {html_body}
            {signature}
        </div>
    """

def detect_troll_content(transcript: str) -> bool:
    """
    Retourne True si le texte contient des termes problématiques (insultes, provocations, troll) en français, allemand ou italien.
    """
    import re
    text = transcript.lower()

    mots_suspects = [
        # 🇫🇷 Français
        r"\b(connard|enculé|nique|merde|putain|ta gueule|bordel|bite|nègre|bougnoule|connasse|salope|batard|pute|enfoiré)\b",
        r"\b(c’est une blague|je me fous|aucun sens|parle pour rien dire)\b",
        r"\b(gpt|openai|chatgpt|robot)\b.*(test|bidon|n’importe quoi)",

        # 🇩🇪 Allemand
        r"\b(scheisse|arschloch|idiot|dummkopf|blödmann|spasti|verpiss dich|halt die fresse|leck mich)\b",
        r"\b(ist doch ein witz|interessiert mich nicht|machst du nur test|völliger unsinn)\b",
        r"\b(chatgpt|gpt|openai|ki|künstliche intelligenz)\b.*(test|fake|blödsinn|verarsche)",

        # 🇮🇹 Italien
        r"\b(cazzo|merda|stronzo|vaffanculo|cretino|idiota|testa di cazzo|imbecille)\b",
        r"\b(non me ne frega niente|è una stronzata|che cazzata)\b",
        r"\b(chatgpt|gpt|intelligenza artificiale)\b.*(prova|finta|scherzo|assurdo)"
    ]

    return any(re.search(p, text) for p in mots_suspects)
