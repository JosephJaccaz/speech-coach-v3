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

    # Vérifier si déjà connecté
    if st.session_state.get("logged_in", False):
        st.success(f"✅ Bienvenue, {st.session_state['username']} 👋")
        if st.button("Se déconnecter"):
            st.session_state.clear()
            st.experimental_rerun()
        return True

    # Formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Connexion réussie ✅")
            st.experimental_rerun()
        else:
            st.error("❌ Nom d'utilisateur ou mot de passe incorrect")

    return False

# ---- Appel de la fonction (utile si le fichier est exécuté directement)
if __name__ == "__main__":
    login()
