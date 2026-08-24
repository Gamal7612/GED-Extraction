# extracteur_claude.py
# Extraction structurée des informations d'une lettre via Claude

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()  # Charger les variables d'environnement depuis le fichier .env
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SCHEMA_EXTRACTION = {
    "name": "extraire_donnees_lettre",
    "description": "Extrait les informations structurées d'une lettre pour une GED",
    "input_schema": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "Date d'envoi de la lettre, format AAAA-MM-JJ. Si non trouvée, mettre null."
            },
            "expediteur": {
                "type": "string",
                "description": "Nom de la personne ou de l'entité qui envoie la lettre"
            },
            "destinataire": {
                "type": "string",
                "description": "Nom de la personne ou de l'entité destinataire"
            },
            "objet": {
                "type": "string",
                "description": "Objet/sujet principal de la lettre"
            },
            "type_courrier": {
                "type": "string",
                "enum": ["facture", "reclamation", "contrat", "courrier_administratif", "correspondance_personnelle", "autre"],
                "description": "Catégorie du courrier"
            },
            "resume": {
                "type": "string",
                "description": "Résumé du contenu en 2-3 phrases maximum"
            },
            "mots_cles_recherche": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Mots-clés utiles pour retrouver ce document dans une recherche future, incluant synonymes et thématiques associées, même s'ils n'apparaissent pas littéralement dans le texte"
            }
        },
        "required": ["expediteur", "destinataire", "objet", "type_courrier", "resume", "mots_cles_recherche"]
    }
}

def extraire_donnees(texte_lettre):
    reponse = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools =[SCHEMA_EXTRACTION],
        tool_choice={"type": "tool", "name": "extraire_donnees_lettre"},
        messages=[
            {"role": "user", "content": f"Analyse cette lettre et extrait les informations structurées : \n\n{texte_lettre}"}
        ]
    )
    return reponse.content[0].input