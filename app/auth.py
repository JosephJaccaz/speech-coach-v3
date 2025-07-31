import streamlit as st

# --- Base d'utilisateurs autorisés ---
VALID_USERS = {
    "joseph": "motdepasse123",
    "coach": "password123",
    "dialogueur": "test1234",
    "admin": "1234"
}

def init_auth_state():
    """Initialise toutes les variables de session liées à l'authentification."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    if "login_attempts" not in st.session_state:
        st.session_state["login_attempts"] = 0

def is_authenticated() -> bool:
    """Retourne True si l'utilisateur est connecté."""
    return st.session_state.get("authenticated", False)

def login_user():
    # Exemple de login basique
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        user = st.text_input("Utilisateur")
        pwd = st.text_input("Mot de passe", type="password")
        if st.button("Connexion"):
            if user == "admin" and pwd == "1234":
                st.session_state.authenticated = True
                st.success("✅ Connecté")
                return True
            else:
                st.error("❌ Identifiants invalides")
                return False
        return False
    return True

def logout_user():
    st.session_state.authenticated = False
