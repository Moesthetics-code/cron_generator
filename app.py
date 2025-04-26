import streamlit as st
from datetime import datetime
import pytz
import sys
import os

# Ajouter le répertoire parent au chemin d'importation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer les modules locaux
from utils.cron_utils import generate_cron_expression, get_next_executions
from utils.validators import validate_cron_expression
from components.sidebar import render_sidebar
from components.header import render_header
from components.cron_builder import render_cron_builder
from components.cron_preview import render_cron_preview
from components.custom_expression import render_custom_expression
from components.footer import render_footer

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Générateur d'expressions Cron",
    page_icon="📆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chargement du CSS personnalisé
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Initialisation des états de session si nécessaire
    if "cron_expression" not in st.session_state:
        st.session_state.cron_expression = "* * * * *"
    if "timezone" not in st.session_state:
        st.session_state.timezone = "UTC"
    if "is_valid" not in st.session_state:
        st.session_state.is_valid = True
    if "error_message" not in st.session_state:
        st.session_state.error_message = ""
    
    # Rendu de la barre latérale
    render_sidebar()
    
    # Contenu principal
    render_header()
    
    # Création de deux colonnes pour le builder et l'aperçu
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Rendu du générateur d'expressions cron
        render_cron_builder()
    
        render_custom_expression()
    
    with col2:
        # Rendu de l'aperçu des exécutions
        render_cron_preview()
    
    # Pied de page
    render_footer()

if __name__ == "__main__":
    main()