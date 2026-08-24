def generer_page_accueil():
    return """
    <h1>GED - Extraction de documents</h1>
    <form action="/analyser" method="post" enctype="multipart/form-data">
        <label>Sélectionner un fichier (image ou PDF) : </label>
        <input type="file" name="document" accept=".png,.jpg,.jpeg,.pdf">
        <button type="submit">Analyser</button>
    </form>
    """


def generer_page_resultat(donnees, texte):
    mots_cles_html = ""
    for mot in donnees["mots_cles_recherche"]:
        mots_cles_html += f"<li>{mot}</li>"
    html = f"""
    <h1>Résultat de l'extraction</h1>
    <p><strong>Date :</strong> {donnees.get("date", "Non trouvée")}</p>
    <p><strong>Expéditeur :</strong> {donnees["expediteur"]}</p>
    <p><strong>Destinataire :</strong> {donnees["destinataire"]}</p>
    <p><strong>Objet :</strong> {donnees["objet"]}</p>
    <p><strong>Type de courrier :</strong> {donnees["type_courrier"]}</p>
    <p><strong>Résumé :</strong> {donnees["resume"]}</p>
    <p><strong>Mots-clés :</strong></p>
    <ul>{mots_cles_html}</ul>
    <hr>
    <h3>Texte brut extrait</h3>
    <pre>{texte}</pre>
    <a href="/">Analyser un autre document</a>
    """
    return html
