# main.py
# Point d'entrée : détecte le type de fichier, extrait le texte, structure via Claude, affiche en HTML
import cgi
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from extracteur_image import extraire_texte_image
from extracteur_pdf import extraire_texte_pdf
from extracteur_claude import extraire_donnees  

from vue_html import generer_page_resultat, generer_page_accueil

DOSSIER_UPLOADS = "uploads"
os.makedirs(DOSSIER_UPLOADS, exist_ok=True)  # Dossier où les fichiers sont stockés

def extraire_texte_selon_type(chemin_fichier):
        """Détecte l'extension et appelle le bon extracteur."""
        extension = os.path.splitext(chemin_fichier)[1].lower()

        if extension in [".png", ".jpg", ".jpeg"]:
            return extraire_texte_image(chemin_fichier)
        elif extension == ".pdf":
            return extraire_texte_pdf(chemin_fichier)
        else:
            raise ValueError(f"Type de fichier non supporté : {extension}")

class MonServeur(BaseHTTPRequestHandler):
    def do_GET(self):
        url_parsee = urlparse(self.path)
        params = parse_qs(url_parsee.query)
        fichier = params.get("fichier", [None])[0]

        if fichier is None:
            html = generer_page_accueil()
        else:
            try:
                texte = extraire_texte_selon_type(fichier)
                donnees = extraire_donnees(texte)
                html = generer_page_resultat(donnees, texte)
            except Exception as e:
                html = f"<h1>Erreur</h1><p>{e}</p><a href='/'>Retour</a>"

        self.envoyer_html(html)

    def do_POST(self):
        url_parsee = urlparse(self.path)

        if url_parsee.path == "/analyser":
            # Parse le formulaire multipart (fichier envoyé)
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": self.headers["Content-Type"]}
            )

            fichier_upload = form["document"]

            if not fichier_upload.filename:
                html = "<h1>Erreur</h1><p>Aucun fichier sélectionné.</p><a href='/'>Retour</a>"
            else:
                # Sauvegarde le fichier reçu dans le dossier uploads/
                chemin_sauvegarde = os.path.join(DOSSIER_UPLOADS, fichier_upload.filename)
                with open(chemin_sauvegarde, "wb") as f:
                    f.write(fichier_upload.file.read())

                try:
                    texte = extraire_texte_selon_type(chemin_sauvegarde)
                    donnees = extraire_donnees(texte)
                    html = generer_page_resultat(donnees, texte)
                except Exception as e:
                    html = f"<h1>Erreur</h1><p>{e}</p><a href='/'>Retour</a>"

            self.envoyer_html(html)

    def envoyer_html(self, html):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


serveur = HTTPServer(("localhost", 8000), MonServeur)
print("Serveur lancé sur http://localhost:8000")
serveur.serve_forever()