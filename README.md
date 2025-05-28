# Speech Coach AI — Modular Version

**Speech Coach AI** is an intelligent feedback tool for NGO fundraisers. It analyzes a vocal pitch recording, evaluates it using a structured educational framework, and delivers clear, constructive feedback in 7 steps.

This version uses a **modular architecture** — cleaner, more maintainable, and designed for team collaboration.

---

## 🧠 Features
- 📤 Upload an audio file (MP3 or WAV)
- 🎧 Automatic transcription using Whisper (OpenAI)
- 🧠 Custom rhetorical analysis using GPT-4
- 📝 Structured feedback (7 steps + performance gauge)
- 🌍 Multilingual: 🇫🇷 French, 🇩🇪 German, 🇮🇹 Italian
- ✉️ Automatic email delivery of feedback to the user and the coach

---

## 🗂️ Project Structure

```
speech-coach-v3/
├── app/
│   ├── main.py                 ← main Streamlit interface
│   ├── feedback.py             ← GPT logic to generate feedback
│   ├── transcription.py        ← audio processing via Whisper
│   ├── ong_context.py          ← load context from NGO files
│   ├── utils.py                ← utilities: gauge, note parsing, etc.
│   ├── interface_texts.py      ← multilingual UI and email text definitions
│   ├── coach_notifier.py       ← coach email mapping & lookup
│   └── email_sender.py         ← generic email sending logic
│
├── prompts/
│   ├── prompt_fr.txt
│   ├── prompt_de.txt
│   └── prompt_it.txt
│
├── data/
│   ├── coachs.json             ← NGO-language → coach email mapping
│   └── organisations/*.json    ← NGO information (slogan, redflags, model speech...)
│
├── streamlit_app.py            ← entry point to launch the app
├── requirements.txt
└── README.md                   ← this file
```

---

## 📌 Important Notes

- Audio files are **not stored**: they remain local to the session
- The app is intended for **educational**, supportive, and privacy-respecting use
- GPT-4 is guided by clear prompts and does **not invent facts or statistics**

---
