import streamlit as st

# --- Exemple d'identifiants ---
VALID_USERS = {
    "joseph": "motdepasse123",
    "admin": "admin123"
}

def login():
    # Initialiser l'état si absent
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    st.title("🔑 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if VALID_USERS.get(username) == password:
            st.session_state["authenticated"] = True
            st.success("✅ Connexion réussie, chargement de l'application...")
            st.rerun()
        else:
            st.error("❌ Identifiants invalides")

    return st.session_state["authenticated"]
