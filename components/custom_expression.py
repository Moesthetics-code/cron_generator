import streamlit as st
from utils.validators import validate_cron_expression

def render_custom_expression():
    """Permet à l'utilisateur de saisir une expression cron personnalisée"""
    st.markdown("## ✏️ Expression personnalisée")

    # Premier expander : saisie de l'expression
    with st.expander("Saisir une expression cron personnalisée", expanded=False):
        st.markdown("""
        <div class="instruction-box">
            Vous pouvez saisir directement une expression cron personnalisée ci-dessous.
            L'aperçu des exécutions sera mis à jour automatiquement.
        </div>
        """, unsafe_allow_html=True)

        # Champ de saisie pour l'expression personnalisée
        custom_expression = st.text_input(
            "Expression cron",
            value=st.session_state.cron_expression,
            placeholder="* * * * *",
            help="Format: minute heure jour_du_mois mois jour_de_la_semaine"
        )

        # Valider l'expression saisie
        if custom_expression:
            is_valid, error_message = validate_cron_expression(custom_expression)

            if is_valid:
                st.session_state.cron_expression = custom_expression
                st.success("Expression cron valide !")
            else:
                st.error(f"Expression cron invalide: {error_message}")

    # Deuxième expander : aide, en dehors du premier
    with st.expander("Aide sur la syntaxe cron", expanded=False):
        st.markdown("""
        ### Syntaxe des expressions cron

        Une expression cron se compose de 5 champs séparés par des espaces:

        ```
        ┌───────────── minute (0 - 59)
        │ ┌───────────── heure (0 - 23)
        │ │ ┌───────────── jour du mois (1 - 31)
        │ │ │ ┌───────────── mois (1 - 12)
        │ │ │ │ ┌───────────── jour de la semaine (0 - 6) (Dimanche = 0)
        │ │ │ │ │
        │ │ │ │ │
        * * * * *
        ```

        ### Caractères spéciaux

        - `*` : correspond à toutes les valeurs possibles
        - `,` : permet de spécifier plusieurs valeurs (ex: `1,3,5`)
        - `-` : définit une plage de valeurs (ex: `1-5`)
        - `/` : définit un pas (ex: `*/5` = toutes les 5 unités)

        ### Exemples courants

        | Expression         | Description                                   |
        |--------------------|-----------------------------------------------|
        | `* * * * *`        | Toutes les minutes                            |
        | `0 * * * *`        | Toutes les heures (à la minute 0)             |
        | `0 0 * * *`        | Tous les jours à minuit                       |
        | `0 0 * * 0`        | Tous les dimanches à minuit                   |
        | `0 0 1 * *`        | Le premier jour de chaque mois à minuit      |
        | `0 9-17 * * 1-5`   | 9h à 17h, du lundi au vendredi                |
        | `*/15 * * * *`     | Toutes les 15 minutes                         |
        """)
