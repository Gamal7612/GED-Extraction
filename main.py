import os
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from extracteur_image import extraire_texte_image
from extracteur_pdf import extraire_texte_pdf
from extracteur_claude import extraire_donnees

DOSSIER_UPLOADS = "uploads"
os.makedirs(DOSSIER_UPLOADS, exist_ok=True)

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

def extraire_texte_selon_type(chemin_fichier):
    """Extrait le texte d'un fichier selon son type."""
    extension = os.path.splitext(chemin_fichier)[1].lower()
    if extension in [".png", ".jpg", ".jpeg"]:
        return extraire_texte_image(chemin_fichier)
    elif extension == ".pdf":
        return extraire_texte_pdf(chemin_fichier)
    else:
        raise ValueError("Type de fichier non supporté.")

@app.get("/", response_class=HTMLResponse)
def accueil(request:Request):
    """Page d'accueil avec le formulaire de téléchargement."""
    return templates.TemplateResponse(
        request,
        "accueil.html",
        {}
        )

@app.post("/analyser", response_class=HTMLResponse)
async def analyser(request: Request, document: UploadFile = File(...)):
    """Analyse le document téléchargé et retourne les résultats."""
    chemin_sauvegarde = os.path.join(DOSSIER_UPLOADS, document.filename)

    contenu = await document.read()
    # Sauvegarde du fichier téléchargé
    with open(chemin_sauvegarde, "wb") as f:
        f.write(contenu)
    
    try:
        texte = extraire_texte_selon_type(chemin_sauvegarde)
        donnees = extraire_donnees(texte)
        return templates.TemplateResponse(
            request,
            "resultat.html", 
            {"donnees": donnees, "texte": texte}
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


    