#test extraction des données d'une lettre à partir d'un fichier PDF
from extracteur_claude import extraire_donnees
from extracteur_pdf import extraire_texte_pdf

# Adapte le chemin vers ton fichier test
texte = extraire_texte_pdf("images/resiliation.pdf")
print("--- Texte extrait ---")
print(texte)
print("\n--- Extraction structurée ---")

resultat = extraire_donnees(texte)
print(resultat)