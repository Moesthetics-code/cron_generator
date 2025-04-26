import croniter
import pytz
from datetime import datetime

def generate_cron_expression(minute, hour, day_of_month, month, day_of_week):
    """
    Génère une expression cron basée sur les paramètres donnés
    
    Args:
        minute (str): Valeur pour les minutes
        hour (str): Valeur pour les heures
        day_of_month (str): Valeur pour le jour du mois
        month (str): Valeur pour le mois
        day_of_week (str): Valeur pour le jour de la semaine
        
    Returns:
        str: Expression cron formatée
    """
    return f"{minute} {hour} {day_of_month} {month} {day_of_week}"

def get_next_executions(cron_expression, count=10, timezone="UTC"):
    """
    Obtient les prochaines exécutions pour une expression cron donnée
    
    Args:
        cron_expression (str): Expression cron valide
        count (int, optional): Nombre d'exécutions à retourner. Par défaut 10.
        timezone (str, optional): Fuseau horaire à utiliser. Par défaut "UTC".
        
    Returns:
        list: Liste des dates/heures des prochaines exécutions
    """
    try:
        # Création d'un objet timezone
        tz = pytz.timezone(timezone)
        
        # Date actuelle dans le fuseau horaire spécifié
        now = datetime.now(tz)
        
        # Création de l'itérateur cron
        cron = croniter.croniter(cron_expression, now)
        
        # Récupération des prochaines exécutions
        next_executions = []
        for _ in range(count):
            next_datetime = cron.get_next(datetime)
            next_executions.append(next_datetime)
            
        return next_executions
    except Exception as e:
        return []

def get_human_readable_description(cron_expression):
    """
    Convertit une expression cron en description lisible par un humain
    
    Args:
        cron_expression (str): Expression cron valide
        
    Returns:
        str: Description lisible de l'expression cron
    """
    parts = cron_expression.split()
    if len(parts) != 5:
        return "Expression cron invalide"
    
    minute, hour, day_of_month, month, day_of_week = parts
    
    descriptions = []
    
    # Minutes
    if minute == "*":
        descriptions.append("chaque minute")
    elif "/" in minute:
        base, interval = minute.split("/")
        descriptions.append(f"toutes les {interval} minutes")
    elif "," in minute:
        descriptions.append(f"aux minutes {minute}")
    else:
        descriptions.append(f"à la minute {minute}")
    
    # Heures
    if hour == "*":
        descriptions.append("chaque heure")
    elif "/" in hour:
        base, interval = hour.split("/")
        descriptions.append(f"toutes les {interval} heures")
    elif "," in hour:
        descriptions.append(f"aux heures {hour}")
    else:
        descriptions.append(f"à {hour}h")
    
    # Jours du mois
    if day_of_month == "*":
        descriptions.append("chaque jour du mois")
    elif "," in day_of_month:
        descriptions.append(f"les jours {day_of_month} du mois")
    else:
        descriptions.append(f"le {day_of_month} du mois")
    
    # Mois
    months_map = {
        "1": "janvier", "2": "février", "3": "mars", "4": "avril",
        "5": "mai", "6": "juin", "7": "juillet", "8": "août",
        "9": "septembre", "10": "octobre", "11": "novembre", "12": "décembre"
    }
    
    if month == "*":
        descriptions.append("chaque mois")
    elif "," in month:
        month_parts = month.split(",")
        month_names = [months_map.get(m, m) for m in month_parts]
        descriptions.append(f"pendant les mois de {', '.join(month_names)}")
    else:
        month_name = months_map.get(month, month)
        descriptions.append(f"en {month_name}")
    
    # Jours de la semaine
    days_map = {
        "0": "dimanche", "1": "lundi", "2": "mardi", "3": "mercredi",
        "4": "jeudi", "5": "vendredi", "6": "samedi", "7": "dimanche"
    }
    
    if day_of_week == "*":
        descriptions.append("chaque jour de la semaine")
    elif "," in day_of_week:
        dow_parts = day_of_week.split(",")
        day_names = [days_map.get(d, d) for d in dow_parts]
        descriptions.append(f"les {', '.join(day_names)}")
    else:
        day_name = days_map.get(day_of_week, day_of_week)
        descriptions.append(f"le {day_name}")
    
    return ", ".join(descriptions)