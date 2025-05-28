# 🎤 Speech Coach IA — Version modulaire

**Speech Coach IA** est un outil pédagogique d’analyse vocale conçu pour les dialogueurs·euses d’ONG. Il permet de recevoir un retour intelligent, structuré et multilingue à partir d’un simple fichier audio.

Cette version repose sur une **architecture modulaire**, claire, évolutive et adaptée à une collaboration d’équipe.

---

## 🧠 Fonctionnalités principales

- 📤 Upload d’un fichier audio (MP3 ou WAV)
- 🎧 Transcription automatique avec Whisper (OpenAI)
- 🧠 Analyse personnalisée avec GPT-4, adaptée à l’ONG choisie
- 📝 Feedback structuré selon les **7 étapes de formation**
- 📊 Baromètre visuel de performance
- 🇫🇷 🇩🇪 🇮🇹 Interface et prompts entièrement multilingues
- ✉️ Envoi automatique du feedback :
  - au dialogueur (par mail)
  - au coach associé à l’ONG/langue (via `coachs.json`)

---

## 📬 Système de notification e-mail

- **Dialogueur** : reçoit un feedback richement formaté (HTML) avec indicateurs, sections claires, suggestions…
- **Coach** : reçoit le **même feedback**, avec un objet personnalisé :
  ```
  Nouveau pitch à analyser (nom_ong) – email_du_dialogueur
  ```
- Le mapping coachs est défini dans `data/coachs.json` sous forme :
  ```json
  {
    "amnesty_international": {
      "fr": "coach_fr@corris.com",
      "de": "coach_de@corris.com",
      "it": "coach_it@corris.com"
    },
    ...
  }
  ```

---

## 🗂️ Structure du projet

```
speech-coach-v3/
├── app/
│   ├── main.py                 ← Interface Streamlit (appelée via streamlit_app.py)
│   ├── feedback.py             ← Génération de feedback avec GPT
│   ├── transcription.py        ← Transcription audio via Whisper
│   ├── ong_context.py          ← Chargement du contexte ONG pour le prompt
│   ├── utils.py                ← Fonctions utilitaires (gauge, note, format HTML...)
│   ├── email_sender.py         ← Fonction d’envoi du feedback par mail
│   ├── coach_notifier.py       ← Mapping ONG/langue → e-mail coach
│   └── interface_texts.py      ← Textes multilingues de l’interface + baromètre
│
├── prompts/
│   ├── prompt_fr.txt
│   ├── prompt_de.txt
│   └── prompt_it.txt
│
├── data/
│   ├── coachs.json             ← Mapping ONG/langue vers e-mails des coachs
│   └── organisations/          ← Données JSON pour chaque ONG (modèle, slogan, redflags…)
│
├── streamlit_app.py            ← Point d’entrée de l’application
├── requirements.txt            ← Dépendances Python
└── README.md                   ← Ce fichier
```

---

## 📌 Notes importantes

- 🔒 Aucun fichier audio n’est stocké ni partagé : tout reste local à la session.
- 💡 L’outil respecte une logique **bienveillante**, **formative**, et **confidentielle**.
- 🤖 Le prompt GPT est cadré pour éviter toute invention ou hallucination.
