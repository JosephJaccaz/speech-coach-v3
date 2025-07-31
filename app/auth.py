# app/auth.py

import streamlit as st

def login():
    """Fonction de login temporaire"""
    st.sidebar.title("Connexion")
    username = st.sidebar.text_input("Nom d'utilisateur")
    password = st.sidebar.text_input("Mot de passe", type="password")
    
    if st.sidebar.button("Se connecter"):
        if username and password:
            st.session_state["logged_in"] = True
            st.success("Connexion réussie")
        else:
            st.error("Veuillez entrer un nom d'utilisateur et un mot de passe")
