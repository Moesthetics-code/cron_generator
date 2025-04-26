import streamlit as st

def render_footer():
    """Affiche le pied de page de l'application"""
    st.markdown("---")
    
    # Pied de page
    st.markdown("""
    <style>
    .github-icon {
        width: 20px;
        height: 20px;
        vertical-align: middle;
    }            
    </style>
    <div class="footer">
        <p>Générateur d'expressions Cron | Développé avec ❤️ par Mohamed NDIAYE</p>
        <p class="small">Cet outil est à titre informatif uniquement. Testez toujours vos expressions cron dans votre environnement spécifique.</p>
        <a href="https://github.com/Moesthetics-code/cron_generator" target="_blank">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" class="github-icon" />
    </a>
    </div>
    """, unsafe_allow_html=True)