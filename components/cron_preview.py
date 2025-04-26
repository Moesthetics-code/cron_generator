import streamlit as st
import pytz
from datetime import datetime
import streamlit.components.v1 as components
from utils.cron_utils import get_next_executions, get_human_readable_description
from utils.validators import validate_cron_expression
import pandas as pd
from io import BytesIO


def render_cron_preview():
    """Affiche l'aperçu des prochaines exécutions et des informations sur l'expression cron"""
    st.markdown("## 📅 Aperçu des exécutions")
    
    with st.container():
        # Obtenir l'expression cron actuelle
        cron_expression = st.session_state.cron_expression
        
        # Valider l'expression
        is_valid, error_message = validate_cron_expression(cron_expression)
        st.session_state.is_valid = is_valid
        st.session_state.error_message = error_message
        
        # Si l'expression est invalide, afficher une erreur
        if not is_valid:
            st.error(f"Expression cron invalide: {error_message}")
            return
        
        # Sélection du fuseau horaire
        all_timezones = pytz.all_timezones
        common_timezones = ["UTC", "Europe/Paris", "America/New_York", "Asia/Tokyo"]
        
        # Option pour afficher tous les fuseaux horaires
        show_all_timezones = st.checkbox("Afficher tous les fuseaux horaires", False)
        
        # Liste des fuseaux horaires à afficher
        timezone_list = all_timezones if show_all_timezones else common_timezones
        
        # Sélecteur de fuseau horaire
        timezone = st.selectbox(
            "Fuseau horaire",
            options=timezone_list,
            index=timezone_list.index(st.session_state.timezone) if st.session_state.timezone in timezone_list else 0,
            key="tz_select"
        )
        
        # Mettre à jour le fuseau horaire dans la session
        st.session_state.timezone = timezone
        
        # Nombre d'exécutions à afficher
        num_executions = st.slider(
            "Nombre d'exécutions à afficher",
            min_value=5,
            max_value=30,
            value=5,
            step=5
        )
        
        # Description en langage naturel
        human_readable = get_human_readable_description(cron_expression)
        st.markdown(f"""
        <div class="human-description">
            <div class="description-title">Description :</div>
            <div class="description-text">{human_readable}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Obtenir les prochaines exécutions
        next_executions = get_next_executions(cron_expression, count=num_executions, timezone=timezone)
        
        # Afficher les prochaines exécutions
        if next_executions:
            st.markdown("<div class='executions-title'>Prochaines exécutions :</div>", unsafe_allow_html=True)
            
            df = pd.DataFrame([{
                "N°": i + 1,
                "Date et heure d'exécution": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "Délai restant": (
                    lambda td: (
                        f"{td.days}j {td.seconds//3600}h {(td.seconds//60)%60}m {td.seconds%60}s"
                        if td.total_seconds() > 0 else "Déjà passé"
                    )
                )(dt - datetime.now(pytz.timezone(timezone)))
            } for i, dt in enumerate(next_executions)])

            buffer = BytesIO()
            df.to_excel(buffer, index=False, sheet_name="Exécutions")
            buffer.seek(0)

            st.download_button(
                label="📄 Télécharger en Excel",
                data=buffer,
                file_name="cron_executions.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # Format de date localisé
            with st.container():
                for i, execution_time in enumerate(next_executions):
                    # Formater la date pour l'affichage
                    formatted_date = execution_time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Calculer le délai jusqu'à l'exécution
                    now = datetime.now(pytz.timezone(timezone))
                    time_delta = execution_time - now
                    days = time_delta.days
                    hours, remainder = divmod(time_delta.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    
                    # Construire la chaîne de délai
                    if days > 0:
                        delta_str = f"dans {days} jours, {hours}h {minutes}m {seconds}s"
                    elif hours > 0:
                        delta_str = f"dans {hours}h {minutes}m {seconds}s"
                    elif minutes > 0:
                        delta_str = f"dans {minutes}m {seconds}s"
                    else:
                        delta_str = f"dans {seconds}s"
                    
                    # Afficher l'exécution avec son délai
                    st.markdown(f"""
                    <div class="execution-item">
                        <div class="execution-number">{i+1}.</div>
                        <div class="execution-time">{formatted_date}</div>
                        <div class="execution-delta">{delta_str}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Impossible de calculer les prochaines exécutions. Vérifiez la syntaxe de l'expression cron.")
        
        # Exportation et partage
        st.markdown("### 📤 Exportation")
        
        export_col1, export_col2 = st.columns(2)
        
        # Copier l'expression dans le presse-papiers
        with export_col1:
            components.html(f"""
            <button onclick="navigator.clipboard.writeText('{cron_expression}'); 
                            let btn = this; 
                            btn.innerText='✅ Copié !'; 
                            setTimeout(() => btn.innerText='📋 Copier', 2000);">
                📋 Copier le cron
            </button>
            """, height=35)

        # Générer le lien à partager
        with export_col2:
            base_url = "https://cron-generator.streamlit.app/?expression="
            share_url = base_url + cron_expression.replace(" ", "%20")
            
            components.html(f"""
            <button onclick="navigator.clipboard.writeText('{share_url}');
                            let btn = this; 
                            btn.innerText='✅ Lien copié !'; 
                            setTimeout(() => btn.innerText='🔗 Partager', 2000);">
                🔗 Partager
            </button>
            """, height=35)