import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageChops
import io

def draw_gauge(score):
    fig, ax = plt.subplots(figsize=(5, 1.8), dpi=160, subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('W')
    ax.set_theta_direction(-1)

    zones = [
        (0, 2, '#8B0000'),     # rouge foncé
        (2, 4, '#FF4500'),     # orange vif
        (4, 6, '#FFA500'),     # orange clair
        (6, 8, '#ADFF2F'),     # vert clair
        (8, 10, '#228B22')     # vert foncé
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

    angle = np.interp(score, [0, 10], [0, np.pi])
    ax.plot([angle, angle], [0, 1], color='black', lw=3)
    ax.plot(angle, 1, 'o', color='black', markersize=6)

    ax.set_ylim(0, 1.1)
    ax.axis('off')
    fig.patch.set_alpha(0)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0, transparent=True)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf)

    bg = Image.new(img.mode, img.size, (255, 255, 255, 0))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()

    img_cropped = img.crop(bbox) if bbox else img
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


def format_feedback_as_html(feedback_text, langue):
    html = feedback_text
    html = html.replace("✓", "<span style='color:green; font-weight:bold;'>✓</span>")
    html = html.replace("⚠️", "<span style='color:red; font-weight:bold;'>⚠️</span>")
    html = html.replace("Suggestion d'amélioration", "<span style='color:#007BFF; font-weight:bold;'>Suggestion d'amélioration</span>")
    html = html.replace("Verbesserungsvorschlag", "<span style='color:#007BFF; font-weight:bold;'>Verbesserungsvorschlag</span>")
    html = html.replace("Suggerimento di miglioramento", "<span style='color:#007BFF; font-weight:bold;'>Suggerimento di miglioramento</span>")
    html = html.replace("**", "")

    paragraphs = html.split("\n")
    html_body = ""
    for line in paragraphs:
        line = line.strip()
        if not line:
            continue
        if line.startswith(("🟢", "📊", "🔍", "🎯", "🤝", "💢", "🌱", "🚀", "➡️", "📝")):
            html_body += f"<p style='margin:20px 0 6px 0; font-weight:bold;'>{line}</p>"
        elif line.startswith("🎯 **Conclusion") or line.startswith("🎯 **Fazit") or line.startswith("🎯 **Conclusione"):
            html_body += "<hr style='margin:24px 0; border:none; border-top:2px solid #eee;'>"
            html_body += f"<p style='margin:20px 0 6px 0; font-weight:bold;'>{line}</p>"
        else:
            html_body += f"<p style='margin:4px 0;'>{line}</p>"

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
