import streamlit as st

# --- Exemple d'identifiants ---
VALID_USERS = {
    "joseph": "motdepasse123",
    "admin": "admin123"
}

def login():
    st.title("🔑 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    login_button = st.button("Se connecter")

    if login_button:
        if username in VALID_USERS and VALID_USERS[username] == password:
            st.session_state["authenticated"] = True
            st.success("✅ Connexion réussie, chargement de l'application...")
            st.rerun()
        else:
            st.error("❌ Identifiants invalides")

    return st.session_state.get("authenticated", False)


def logout():
    if st.button("🔓 Déconnexion"):
        st.session_state["authenticated"] = False
        st.rerun()
