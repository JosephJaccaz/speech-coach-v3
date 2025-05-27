# Speech Coach IA — Version modulaire

**Speech Coach IA** est un outil de feedback intelligent pour les pitchs vocaux des dialogueurs·euses d’ONG. Il permet d’analyser un enregistrement audio, de l’évaluer selon une grille pédagogique claire, et de proposer un retour structuré en 7 étapes.

Cette version repose sur une **architecture modulaire**, plus propre, plus maintenable et prête pour la collaboration.

---

## 🧠 Fonctionnalités
- 📤 Upload d’un fichier audio (MP3 ou WAV)
- 🎧 Transcription automatique avec Whisper (OpenAI)
- 🧠 Analyse rhétorique personnalisée avec GPT-4
- 📝 Feedback structuré (7 étapes + baromètre)
- 🇫🇷 🇩🇪 🇮🇹 Multilingue
- ✉️ Envoi automatique du feedback par mail

---

## 🗂️ Structure du projet
```
speech-coach-v2/
├── app/
│   ├── main.py                 ← interface Streamlit principale
│   ├── feedback.py             ← fonction GPT pour générer le retour
│   ├── transcription.py        ← traitement de l’audio avec Whisper
│   ├── ong_context.py          ← chargement des données ONG
│   ├── utils.py                ← fonctions génériques : gauge, note, etc.
│   └── interface_texts.py      ← textes d’interface multilingues
│
├── prompts/
│   ├── prompt_fr.txt
│   ├── prompt_de.txt
│   └── prompt_it.txt
│
├── data/
│   └── organisations/*.json    ← infos ONG (slogan, redflags, pitch modèle...)
│
├── assets/                     ← images, logo (si besoin)
├── streamlit_app.py            ← point d’entrée de l’app (à la racine)
├── requirements.txt
├── .gitignore
└── README.md                   ← ce fichier
```

---

## 🚀 Lancer l’application en local
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## ☁️ Déploiement sur Streamlit Cloud
1. Crée un nouveau dépôt GitHub avec ce code
2. Sur [streamlit.io/cloud](https://streamlit.io/cloud), connecte ton dépôt
3. Indique `streamlit_app.py` comme **main file**
4. Ajoute tes clés dans `.streamlit/secrets.toml` :
```toml
openai_key = "sk-..."
email_user = "..."
email_password = "..."
```
5. Clique sur "Deploy" 🎉

---

## 📌 Notes importantes
- Aucun fichier audio n’est stocké : tout reste local à la session
- L’outil est pensé pour un usage pédagogique, bienveillant, et respectueux de la vie privée
- GPT-4 n’invente pas de chiffres, et les feedbacks sont toujours cadrés par les prompts


