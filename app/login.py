import streamlit as st
from auth import init_auth_state, is_authenticated, login_user, logout_user

def login():
    init_auth_state()
    
    # 🔹 Empêche les erreurs si 'username' n'existe pas encore
    if "username" not in st.session_state:
        st.session_state["username"] = ""

    st.title("🔐 Connexion à Speech Coach")

    # Si l'utilisateur est déjà connecté
    if is_authenticated():
        st.success(f"✅ Bienvenue, {st.session_state['username']} 👋")
        if st.button("🔓 Se déconnecter"):
            logout_user()
            st.experimental_rerun()
        return True

    # Formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if login_user(username, password):
            st.session_state["username"] = username  # 🔹 on garde l'utilisateur en session
            st.success("Connexion réussie, chargement de l'application...")
            st.experimental_rerun()
        else:
            st.error("❌ Nom d'utilisateur ou mot de passe incorrect")

    return False
