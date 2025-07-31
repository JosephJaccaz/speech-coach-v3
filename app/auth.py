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

def login_user(username: str, password: str) -> bool:
    """
    Vérifie les identifiants fournis et met à jour la session si valides.
    Retourne True si la connexion réussit, sinon False.
    """
    init_auth_state()  # ✅ Sécurité pour éviter les KeyErrors

    if username in VALID_USERS and VALID_USERS[username] == password:
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
        st.session_state["login_attempts"] = 0  # Reset après succès
        return True
    
    # En cas d'échec
    st.session_state["login_attempts"] += 1
    return False

def logout_user():
    """Déconnecte l'utilisateur et réinitialise les variables de session."""
    init_auth_state()
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
