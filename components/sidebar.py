import streamlit as st

def render_sidebar():
    """Affiche la barre latérale avec des informations et des options"""
    with st.sidebar:
        st.markdown("# 📆 Générateur Cron")
        
        st.markdown("""
        Cet outil vous permet de :
        
        - Créer des expressions cron facilement
        - Visualiser les prochaines exécutions
        - Comprendre la syntaxe cron
        
        Idéal pour les développeurs, DevOps, et administrateurs système.
        """)
        
        # Séparateur
        st.markdown("---")
        
        # Cas d'utilisation courants
        st.markdown("### 🚀 Cas d'utilisation courants")
        
        common_cases = {
            "Tous les jours à minuit": "0 0 * * *",
            "Toutes les heures": "0 * * * *",
            "Tous les lundis à 9h": "0 9 * * 1",
            "Chaque 15 minutes": "*/15 * * * *",
            "1er du mois à midi": "0 12 1 * *",
            "Week-end à 10h": "0 10 * * 0,6",
            "Heures de bureau (9h-17h Lu-Ve)": "0 9-17 * * 1-5"
        }
        selected_case = st.selectbox("Cas prédéfini :", options=[""] + list(common_cases.keys()))
        if selected_case:
            st.session_state.cron_expression = common_cases[selected_case]
        
        # Séparateur
        st.markdown("---")
        
        # Mode sombre/clair
        theme_mode = st.radio("Thème", ["Clair", "Sombre"])
        
        if theme_mode == "Sombre":
            # Injecter du CSS pour le mode sombre
            st.markdown("""
            <style>
                body {
                    background-color: #121212;
                    color: #f0f0f0;
                }
                .stApp {
                    background-color: #121212;
                }
                .css-1d391kg, .css-1lcbmhc {
                    background-color: #1e1e1e;
                }
                .sidebar .sidebar-content {
                    background-color: #1e1e1e;
                }
            </style>
            """, unsafe_allow_html=True)
        
        # Séparateur
        st.markdown("---")
        
        # À propos
        with st.expander("À propos"):
            st.markdown("""
            #### Générateur d'expressions Cron
            
            Cet outil a été créé pour simplifier la création et le test d'expressions cron.
            
            Les expressions cron sont utilisées pour planifier des tâches récurrentes dans les systèmes Unix/Linux, ainsi que dans de nombreux frameworks et outils de planification.
            
            **Technologies utilisées:**
            - Streamlit
            - Python
            - croniter
            
            **Librairies requises:**
            - streamlit
            - croniter
            - pytz
            """)