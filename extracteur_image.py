# extracteur_image.py
# Extraction de texte depuis une image via OCR (Tesseract)

import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extraire_texte_image(chemin_fichier):
    image = Image.open(chemin_fichier)
    texte = pytesseract.image_to_string(image, lang="fra")
    return texte