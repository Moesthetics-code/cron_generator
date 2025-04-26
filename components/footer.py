import streamlit as st

def render_footer():
    """Affiche le pied de page de l'application"""
    st.markdown("---")
    
    # Pied de page
    st.markdown("""
    <div class="footer">
        <p>Générateur d'expressions Cron | Développé avec ❤️ par Mohamed NDIAYE</p>
        <p class="small">Cet outil est à titre informatif uniquement. Testez toujours vos expressions cron dans votre environnement spécifique.</p>
    </div>
    """, unsafe_allow_html=True)