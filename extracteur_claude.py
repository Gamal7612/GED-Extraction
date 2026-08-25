# extracteur_claude.py
# Extraction structurée avec function calling - Claude choisit le type de document

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SCHEMA_LETTRE = {
    "name": "extraire_lettre",
    "description": "À utiliser pour une correspondance personnelle ou administrative classique, avec un expéditeur et un destinataire identifiables (courrier, réclamation, correspondance).",
    "input_schema": {
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Format AAAA-MM-JJ, null si non trouvée"},
            "expediteur": {"type": "string"},
            "destinataire": {"type": "string"},
            "objet": {"type": "string"},
            "resume": {"type": "string"},
            "mots_cles_recherche": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["expediteur", "destinataire", "objet", "resume", "mots_cles_recherche"]
    }
}

SCHEMA_FACTURE = {
    "name": "extraire_facture",
    "description": "À utiliser pour un document commercial de type facture, avec des montants, une TVA, des références de paiement ou un numéro de facture.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Format AAAA-MM-JJ"},
            "numero_facture": {"type": "string"},
            "emetteur": {"type": "string"},
            "destinataire": {"type": "string"},
            "montant_total": {"type": "string", "description": "Montant TTC avec devise"},
            "montant_tva": {"type": "string"},
            "resume": {"type": "string"},
            "mots_cles_recherche": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["numero_facture", "emetteur", "destinataire", "montant_total", "resume", "mots_cles_recherche"]
    }
}

SCHEMA_CONTRAT = {
    "name": "extraire_contrat",
    "description": "À utiliser pour un contrat, avec des parties prenantes identifiées, une durée ou des clauses.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Format AAAA-MM-JJ"},
            "parties": {"type": "array", "items": {"type": "string"}},
            "objet_contrat": {"type": "string"},
            "duree": {"type": "string"},
            "resume": {"type": "string"},
            "mots_cles_recherche": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["parties", "objet_contrat", "resume", "mots_cles_recherche"]
    }
}

SCHEMA_GENERIQUE = {
    "name": "extraire_document_generique",
    "description": "À utiliser UNIQUEMENT si le document ne correspond à aucun autre type connu (ni lettre, ni facture, ni contrat).",
    "input_schema": {
        "type": "object",
        "properties": {
            "titre": {"type": "string"},
            "resume": {"type": "string"},
            "mots_cles_recherche": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["titre", "resume", "mots_cles_recherche"]
    }
}

OUTILS_DISPONIBLES = [SCHEMA_LETTRE, SCHEMA_FACTURE, SCHEMA_CONTRAT, SCHEMA_GENERIQUE]


def extraire_donnees(texte_document):
    """Analyse un document et extrait ses données selon le type détecté par Claude."""
    reponse = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=OUTILS_DISPONIBLES,
        tool_choice={"type": "any"},
        messages=[
            {"role": "user", "content": f"Analyse ce document et extrais les informations avec l'outil le plus adapté :\n\n{texte_document}"}
        ]
    )

    bloc = reponse.content[0]
    type_document = bloc.name
    donnees = bloc.input

    return type_document, donnees