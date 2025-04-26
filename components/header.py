import streamlit as st

def render_header():
    """Affiche l'en-tête de l'application"""
    st.markdown("""
    <div class="header">
        <h1>📆 Générateur d'expressions Cron</h1>
        <p>Un outil simple pour créer et tester des expressions cron</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction et explication
    st.markdown("""
    <div class="intro-box">
        <p>Les expressions <b>cron</b> sont utilisées pour planifier des tâches automatiques à des moments précis.
        Elles sont composées de 5 champs (minute, heure, jour du mois, mois, jour de la semaine) qui définissent quand une tâche doit s'exécuter.</p>
        <p>Utilisez cet outil pour créer facilement des expressions cron et visualiser leurs prochaines exécutions.</p>
    </div>
    """, unsafe_allow_html=True)