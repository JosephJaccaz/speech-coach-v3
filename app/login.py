import streamlit as st
from auth import init_auth_state, is_authenticated, login_user, logout_user

def login() -> bool:
    """
    Affiche l'interface de connexion et renvoie True si l'utilisateur est authentifié, sinon False.
    """
    init_auth_state()

    # Initialisation du nom d'utilisateur dans la session si inexistant
    if "username" not in st.session_state:
        st.session_state["username"] = ""

    st.title("🔐 Connexion à Speech Coach")

    # Si l'utilisateur est déjà authentifié
    if is_authenticated():
        st.success(f"✅ Bienvenue, {st.session_state['username']} 👋")
        if st.button("🔓 Se déconnecter"):
            logout_user()
            st.experimental_rerun()
        return True  # ✅ Retour explicite

    # Formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if login_user(username, password):
            st.session_state["username"] = username
            st.success("Connexion réussie, chargement de l'application...")
            st.experimental_rerun()
        else:
            st.error("❌ Nom d'utilisateur ou mot de passe incorrect")

    return False  # ✅ Toujours renvoyer False si non connecté
