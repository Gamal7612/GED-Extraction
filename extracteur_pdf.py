# extracteur_pdf.py
# Extraction de texte depuis un PDF

from pypdf import PdfReader

def extraire_texte_pdf(chemin_fichier):
    reader = PdfReader(chemin_fichier)
    texte = ""
    for page in reader.pages:
        texte += page.extract_text()
    return texte