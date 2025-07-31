import streamlit as st
from pathlib import Path
import json
from login import login

# --- CONFIG APP ---
st.set_page_config(page_title="Speech Coach IA", page_icon="🎤", layout="centered")

# --- PARAMÈTRES GLOBAUX ---
DATA_DIR = Path("data")
ONG_DIR = DATA_DIR / "organisations"


# --- CHARGEMENT DES TRADUCTIONS ---
def load_translations(lang="fr"):
    translations_path = DATA_DIR / "translations.json"
    if translations_path.exists():
        with open(translations_path, "r", encoding="utf-8") as f:
            translations = json.load(f)
        return translations.get(lang, translations.get("fr", {}))
    else:
        return {}


# --- HEADER DE L'APP ---
def display_header():
    st.title("🎤 Speech Coach IA")
    st.markdown("**Votre outil d'analyse de pitchs optimisé pour les dialogueurs**")
    st.divider()


# --- CHARGEMENT DES ONG DISPONIBLES ---
def get_ong_files():
    ong_files = list(ONG_DIR.glob("*.json"))
    ong_display_names = [file.stem for file in ong_files]
    return ong_files, ong_display_names


# --- LOGIQUE PRINCIPALE ---
def run_app():
    # Authentification
    if not st.session_state.get("authenticated", False):
        if not login():
            return

    # Traductions
    lang = st.session_state.get("lang", "fr")
    t = load_translations(lang)

    # Affichage du header
    display_header()

    # Liste des fichiers ONG
    ong_files, ong_display_names = get_ong_files()

    if not ong_files:
        st.error("⚠️ Aucune ONG trouvée dans le dossier `data/organisations`.")
        st.stop()

    # Sélecteur d'ONG
    ong_choisie = st.selectbox(t.get("ong_label", "Sélectionnez une ONG"), ong_display_names)

    st.success(f"✅ Vous avez choisi : **{ong_choisie}**")
    st.write("L'application est prête à analyser les pitchs pour cette ONG.")


# --- POINT D'ENTRÉE ---
if __name__ == "__main__":
    run_app()
