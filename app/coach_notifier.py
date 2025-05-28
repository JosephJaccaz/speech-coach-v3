import json
import os

def charger_mapping_coachs(json_path="data/coachs.json"):
    """
    Charge le fichier JSON contenant la correspondance ONG/langue → email du coach.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Fichier introuvable : {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_email_coach(ong, langue, mapping):
    """
    Retourne l'email du coach pour une ONG et une langue données.
    """
    ong_entry = mapping.get(ong)
    if ong_entry:
        return ong_entry.get(langue)
    return None
