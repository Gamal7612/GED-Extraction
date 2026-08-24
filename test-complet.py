# test_complet.py
from extracteur_image import extraire_texte_image
from extracteur_claude import extraire_donnees

texte = extraire_texte_image("images/resiliation.png")
print("--- Texte extrait ---")
print(texte)
print("\n--- Extraction structurée ---")

resultat = extraire_donnees(texte)
print(resultat)