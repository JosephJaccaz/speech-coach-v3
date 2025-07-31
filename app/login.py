import streamlit as st

# ---- Données d'authentification (à remplacer plus tard par une vraie BDD)
USER_CREDENTIALS = {
    "coach": "password123",
    "dialogueur": "test1234",
    "admin": "1234"
}

# ---- Fonction de connexion
def login():
    st.title("🔐 Connexion à Speech Coach")

    # Initialisation de session_state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    # ✅ Si déjà connecté, afficher un message et bouton déconnexion
    if st.session_state.logged_in:
        st.success(f"✅ Bienvenue, {st.session_state.username} 👋")
        if st.button("Se déconnecter"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()
        return True

    # ---- Formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("❌ Nom d'utilisateur ou mot de passe incorrect")

    return False

# ---- Exécution directe (utile si tu lances login.py seul)
if __name__ == "__main__":
    login()
