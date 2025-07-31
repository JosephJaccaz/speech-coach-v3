import streamlit as st

# ---- Données d'authentification (à remplacer plus tard par une vraie BDD)
USER_CREDENTIALS = {
    "coach": "password123",
    "dialogueur": "test1234"
}

# ---- Gestion de l'authentification
def login():
    st.title("🔐 Connexion à Speech Coach")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Connexion réussie ✅")
            st.experimental_rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect ❌")

# ---- Protection de page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()
else:
    st.success(f"Bienvenue, {st.session_state['username']} 👋")
    if st.button("Se déconnecter"):
        st.session_state.clear()
        st.experimental_rerun()
