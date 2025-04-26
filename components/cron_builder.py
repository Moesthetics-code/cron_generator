import streamlit as st
from utils.cron_utils import generate_cron_expression

def render_cron_builder():
    """Affiche l'interface de construction d'une expression cron"""
    st.markdown("## 🔧 Constructeur d'expression Cron")
    
    with st.container():
        st.markdown("""
        <div class="instruction-box">
            Sélectionnez les valeurs pour chaque partie de l'expression cron. 
            L'expression sera générée automatiquement ci-dessous.
        </div>
        """, unsafe_allow_html=True)

        # Créer les options pour chaque partie de l'expression cron
        col1, col2 = st.columns(2)
        
        with col1:
            # Minutes
            minute_options = {
                "*": "Chaque minute",
                "0": "Minute 0 (début de l'heure)",
                "15": "Minute 15 (quart d'heure)",
                "30": "Minute 30 (demi-heure)",
                "45": "Minute 45 (trois-quart d'heure)",
                "*/5": "Toutes les 5 minutes",
                "*/10": "Toutes les 10 minutes",
                "*/15": "Toutes les 15 minutes",
                "*/30": "Toutes les 30 minutes",
                "0,30": "Minutes 0 et 30"
            }
            minute = st.selectbox(
                "Minute",
                options=list(minute_options.keys()),
                format_func=lambda x: f"{x} - {minute_options[x]}",
                index=0,
                key="minute_select"
            )
            
            # Heures
            hour_options = {
                "*": "Chaque heure",
                "0": "Minuit (0h)",
                "6": "6h du matin",
                "12": "Midi (12h)",
                "18": "18h (6h du soir)",
                "*/2": "Toutes les 2 heures",
                "*/4": "Toutes les 4 heures",
                "*/6": "Toutes les 6 heures",
                "*/12": "Toutes les 12 heures",
                "9-17": "Heures de bureau (9h-17h)"
            }
            hour = st.selectbox(
                "Heure",
                options=list(hour_options.keys()),
                format_func=lambda x: f"{x} - {hour_options[x]}",
                index=0,
                key="hour_select"
            )
            
            # Jours du mois
            day_options = {
                "*": "Chaque jour du mois",
                "1": "1er du mois",
                "15": "15 du mois",
                "L": "Dernier jour du mois",
                "1,15": "1er et 15 du mois",
                "*/2": "Tous les 2 jours",
                "*/5": "Tous les 5 jours",
                "*/10": "Tous les 10 jours",
                "1-5": "Du 1er au 5 du mois",
                "1-7": "Première semaine du mois"
            }
            day_of_month = st.selectbox(
                "Jour du mois",
                options=list(day_options.keys()),
                format_func=lambda x: f"{x} - {day_options[x]}",
                index=0,
                key="day_select"
            )
        
        with col2:
            # Mois
            month_options = {
                "*": "Chaque mois",
                "1": "Janvier",
                "2": "Février",
                "3": "Mars",
                "4": "Avril",
                "5": "Mai",
                "6": "Juin",
                "7": "Juillet",
                "8": "Août",
                "9": "Septembre",
                "10": "Octobre",
                "11": "Novembre",
                "12": "Décembre",
                "*/3": "Tous les 3 mois",
                "*/6": "Tous les 6 mois",
                "1,7": "Janvier et Juillet",
                "3-5": "Printemps (Mars-Mai)",
                "6-8": "Été (Juin-Août)",
                "9-11": "Automne (Sept-Nov)",
                "1,2,12": "Hiver (Déc-Fév)"
            }
            month = st.selectbox(
                "Mois",
                options=list(month_options.keys()),
                format_func=lambda x: f"{x} - {month_options[x]}",
                index=0,
                key="month_select"
            )
            
            # Jours de la semaine
            dow_options = {
                "*": "Chaque jour de la semaine",
                "1": "Lundi",
                "2": "Mardi",
                "3": "Mercredi",
                "4": "Jeudi",
                "5": "Vendredi",
                "6": "Samedi",
                "0": "Dimanche",
                "1-5": "Jours ouvrables (Lun-Ven)",
                "0,6": "Week-end (Sam-Dim)",
                "1,3,5": "Lundi, Mercredi, Vendredi"
            }
            day_of_week = st.selectbox(
                "Jour de la semaine",
                options=list(dow_options.keys()),
                format_func=lambda x: f"{x} - {dow_options[x]}",
                index=0,
                key="dow_select"
            )
        
        # Générer l'expression cron
        cron_expression = generate_cron_expression(minute, hour, day_of_month, month, day_of_week)
        
        # Mettre à jour la session state
        st.session_state.cron_expression = cron_expression
        
        # Affichage joli de l'expression générée
        st.markdown("""
        <div class="cron-result">
            <div class="cron-label">Expression Cron générée :</div>
            <div class="cron-expression">{}</div>
        </div>
        """.format(cron_expression), unsafe_allow_html=True)
        
        # Explication des parties
        st.markdown("""
        <div class="cron-explanation">
            <div class="explanation-title">Syntaxe :</div>
            <div class="explanation-parts">
                <span class="part">minute</span>
                <span class="part">heure</span>
                <span class="part">jour_du_mois</span>
                <span class="part">mois</span>
                <span class="part">jour_de_semaine</span>
            </div>
        </div>
        """, unsafe_allow_html=True)