# main.py
import os
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from extracteur_image import extraire_texte_image
from extracteur_pdf import extraire_texte_pdf
from extracteur_claude import extraire_donnees

DOSSIER_UPLOADS = "uploads"
os.makedirs(DOSSIER_UPLOADS, exist_ok=True)

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Correspondance entre le nom d'outil choisi par Claude et le template à utiliser
TEMPLATES_PAR_TYPE = {
    "extraire_lettre": "resultat_lettre.html",
    "extraire_facture": "resultat_facture.html",
    "extraire_contrat": "resultat_contrat.html",
    "extraire_document_generique": "resultat_generique.html"
}


def extraire_texte_selon_type(chemin_fichier):
    """Détecte l'extension et appelle le bon extracteur."""
    extension = os.path.splitext(chemin_fichier)[1].lower()
    if extension in [".png", ".jpg", ".jpeg"]:
        return extraire_texte_image(chemin_fichier)
    elif extension == ".pdf":
        return extraire_texte_pdf(chemin_fichier)
    else:
        raise ValueError(f"Type de fichier non supporté : {extension}")


@app.get("/", response_class=HTMLResponse)
def accueil(request: Request):
    return templates.TemplateResponse(request, "accueil.html", {})


@app.post("/analyser", response_class=HTMLResponse)
async def analyser_document(request: Request, document: UploadFile = File(...)):
    chemin_sauvegarde = os.path.join(DOSSIER_UPLOADS, document.filename)

    contenu = await document.read()
    with open(chemin_sauvegarde, "wb") as f:
        f.write(contenu)

    try:
        texte = extraire_texte_selon_type(chemin_sauvegarde)
        type_document, donnees = extraire_donnees(texte)

        nom_template = TEMPLATES_PAR_TYPE.get(type_document, "resultat_generique.html")

        return templates.TemplateResponse(
            request,
            nom_template,
            {"donnees": donnees, "texte": texte}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))