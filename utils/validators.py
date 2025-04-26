import re
import croniter

def validate_cron_expression(expression):
    """
    Valide une expression cron
    
    Args:
        expression (str): L'expression cron à valider
        
    Returns:
        tuple: (is_valid, error_message)
            - is_valid (bool): True si l'expression est valide, False sinon
            - error_message (str): Message d'erreur si invalide, chaîne vide sinon
    """
    # Vérifier le format de base
    if not expression or not isinstance(expression, str):
        return False, "L'expression cron ne peut pas être vide"
    
    # Vérifier le nombre de parties
    parts = expression.strip().split()
    if len(parts) != 5:
        return False, "L'expression cron doit avoir 5 parties séparées par des espaces"
    
    try:
        # Utiliser croniter pour vérifier si l'expression est valide
        croniter.croniter(expression)
        return True, ""
    except (ValueError, KeyError) as e:
        return False, f"Expression cron invalide: {str(e)}"

def validate_minute(minute):
    """Valide la partie minute d'une expression cron"""
    return validate_cron_part(minute, 0, 59)

def validate_hour(hour):
    """Valide la partie heure d'une expression cron"""
    return validate_cron_part(hour, 0, 23)

def validate_day_of_month(day):
    """Valide la partie jour du mois d'une expression cron"""
    return validate_cron_part(day, 1, 31)

def validate_month(month):
    """Valide la partie mois d'une expression cron"""
    return validate_cron_part(month, 1, 12)

def validate_day_of_week(day):
    """Valide la partie jour de la semaine d'une expression cron"""
    return validate_cron_part(day, 0, 7)

def validate_cron_part(part, min_val, max_val):
    """
    Valide une partie individuelle d'une expression cron
    
    Args:
        part (str): La partie de l'expression à valider
        min_val (int): Valeur minimale acceptable
        max_val (int): Valeur maximale acceptable
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Astérisque est toujours valide
    if part == "*":
        return True, ""
    
    # Vérifier les listes (séparées par des virgules)
    if "," in part:
        for item in part.split(","):
            is_valid, msg = validate_cron_part(item, min_val, max_val)
            if not is_valid:
                return False, msg
        return True, ""
    
    # Vérifier les plages (a-b)
    if "-" in part:
        try:
            start, end = map(int, part.split("-"))
            if start < min_val or end > max_val or start > end:
                return False, f"Plage invalide {part}, doit être entre {min_val}-{max_val}"
            return True, ""
        except ValueError:
            return False, f"Format de plage invalide: {part}"
    
    # Vérifier les pas (*/n ou a/b)
    if "/" in part:
        base, step = part.split("/")
        
        # Valider la base
        if base != "*":
            is_valid, msg = validate_cron_part(base, min_val, max_val)
            if not is_valid:
                return False, msg
        
        # Valider le pas
        try:
            step_val = int(step)
            if step_val < 1:
                return False, "Le pas doit être un entier positif"
            return True, ""
        except ValueError:
            return False, f"Format de pas invalide: {step}"
    
    # Vérifier la valeur simple
    try:
        val = int(part)
        if val < min_val or val > max_val:
            return False, f"Valeur {val} hors limites ({min_val}-{max_val})"
        return True, ""
    except ValueError:
        return False, f"Format invalide: {part}"