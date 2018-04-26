from flask import render_template, request, flash, redirect, send_file

import xml.etree.ElementTree as ET

from ..app import app, login
from ..modeles.donnees import Mot
from ..modeles.donnees import Commentaire
from ..modeles.utilisateurs import User
from ..constantes import MOTS_PAR_PAGE
from flask_login import login_user, current_user, logout_user


@app.route("/", methods=["GET", "POST"])
def accueil():
    """ Route permettant l'affichage d'une page accueil
    """
    # On a bien sûr aussi modifié le template pour refléter le changement
    mots = Mot.query.all()
    return render_template("pages/accueil.html", nom="Sortiaria", mots=mots)


@app.route("/mot/<int:mot_id>")
def mot(mot_id):
    """ Route permettant l'affichage des données d'un mot
    :param mot_id: Identifiant numérique du mot
    """
    # Ce qui suit permet d'afficher le mot, les commentaires et les auteurs des commentaires
    unique_mot = Mot.query.get(mot_id)
    coms = unique_mot.commentaires
    #auteurs = coms.authorships
    return render_template("pages/mot.html", nom="Sortiaria", mot=unique_mot, coms=coms) #auteurs=auteurs

@app.route("/mot/<int:mot_id>/modif_mot", methods=["GET", "POST"])
def modif_mot(mot_id):
    """ Route permettant des modifier les données d'un mot
    :param mot_id: Identifiant numérique du mot
    """
    # On a bien sûr aussi modifié le template pour refléter le changement
    unique_mot = Mot.query.get(mot_id)
    if request.method == "POST":
        status, donnees = Mot.modif_mot(
            id=mot_id,
            terme=request.form.get("mot", None),
            prononciation=request.form.get("prononciation", None),
            grammaire=request.form.get("grammaire", None),
            genre=request.form.get("genre", None),
            definition=request.form.get("definition", None),
        )

        if status is True :
            flash("Merci pour votre contribution !", "success")
            unique_mot = Mot.query.get(mot_id)
            return redirect("/browse")

        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            unique_mot = Mot.query.get(mot_id)
    return render_template("pages/modif_mot.html", nom="Sortiaria", mot=unique_mot)    

@app.route("/contribuer", methods=["GET", "POST"])
def ajout_mot():
    # Route permettant d'ajouter des entrées 
    
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = Mot.creer_mot(
            terme=request.form.get("mot", None),
            prononciation=request.form.get("prononciation", None),
            grammaire=request.form.get("grammaire", None),
            genre=request.form.get("genre", None),
            definition=request.form.get("definition", None),
        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect("/browse")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/ajout_mot.html")
    return render_template("pages/ajout_mot.html")

@app.route("/mot/<int:mot_id>/supprimer_mot", methods=["GET", "POST"])
def delete(mot_id):
    """ Route permettant la suppression d'un mot
    :param mot_id: Identifiant numérique du mot
    """

    if request.method == "GET":
        unique_mot = Mot.query.get(mot_id)
        return render_template("pages/supprimer_mot.html", nom="Sortiaria" , mot=unique_mot)
    else:
        status = Mot.supprimer_mot(id=mot_id)
        if status is True :
            flash("Mot supprimé !", "success")
            return redirect("/")
        else:
            flash("La suppression a échoué.", "danger")
            return redirect("/mot/" + str(mot_id))

@app.route("/mot/<int:mot_id>/tei")
def export_tei(mot_id):
    """ Route permettant l'affichage des données d'un mot en TEI
    :param mot_id: Identifiant numérique du mot
    """
    unique_mot = Mot.query.get(mot_id)
    coms = unique_mot.commentaires

    TEI = ET.Element('TEI')
    TEI.set('xmlns','http://www.tei-c.org/ns/1.0')
    teiHeader = ET.SubElement(TEI, 'teiHeader')
    fileDesc = ET.SubElement(teiHeader, 'fileDesc')
    titleStmt = ET.SubElement(fileDesc, 'titleStmt')
    title = ET.SubElement(titleStmt, 'title')
    title.text = unique_mot.mot_terme
    publicationStmt = ET.SubElement(teiHeader, 'publicationStmt')
    p = ET.SubElement(publicationStmt, 'p')
    p.text = 'Sortiaria est un dictionnaire en ligne développé par Marie-Laurence Bonhomme, Léa Frering, Armâne Magnier et Alyx Taounza-Jeminet en Master 2 Technologies numériques appliquées à l\'histoire à l\'École nationale des chartes'
    text = ET.SubElement(TEI, 'text')
    body = ET.SubElement(text, 'body')
    entry = ET.SubElement(body, 'entry')
    form = ET.SubElement(entry, 'form')
    orth = ET.SubElement(form, 'orth')
    orth.text = unique_mot.mot_terme
    pron = ET.SubElement(form, 'pron')
    pron.text = unique_mot.mot_phon
    gramGrp = ET.SubElement(entry, 'gramGrp')
    pos = ET.SubElement(gramGrp, 'pos')
    pos.text = unique_mot.mot_gram
    gen = ET.SubElement(gramGrp, 'gen')
    gen.text = unique_mot.mot_genre
    sense = ET.SubElement(entry, 'sense') 
    defn = ET.SubElement(sense, 'def')
    defn.text = unique_mot.mot_def 
    for com in coms:
        note = ET.SubElement(entry, 'note')  
        label = ET.SubElement(note, 'label')
        label.text = com.commentaire_titre
        p = ET.SubElement(note, 'p')
        p.text = com.commentaire_texte
        if com.commentaire_source:
            bibl = ET.SubElement(note, 'bibl')
            bibl.text = com.commentaire_source

    myTEI = ET.tostring(TEI, encoding='unicode')
    myfile = open("sortiaria/temp/export_tei.xml", "w")
    myfile.write('<?xml version=\"1.0\" encoding=\"UTF-8\"?> <?xml-model href=\"http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng\" type=\"application/xml\" schematypens=\"http://relaxng.org/ns/structure/1.0\"?> <?xml-model href=\"http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng\" type=\"application/xml\" schematypens=\"http://purl.oclc.org/dsdl/schematron\"?>' + str(myTEI))

    return send_file("temp/export_tei.xml", attachment_filename="export_tei.xml")

@app.route("/mot/<int:mot_id>/commentaire", methods=["GET", "POST"])
def ajout_commentaire(mot_id):
    """ Route permettant l'ajout d'un commentaire sur un mot
    :param mot_id: Identifiant numérique du mot
    """

    if request.method == "POST":
        statut, donnees = Commentaire.ajout_commentaire(
            titre=request.form.get("titre", None),
            texte=request.form.get("texte", None),
            source=request.form.get("source", None),
            c_mot_id=request.form.get("mot_id", None),
            auteur=request.form.get("authorship", None)
        )
        if statut is True:
            flash("Commentaire enregistré !", "success")
            return redirect("/mot/" + str(mot_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            unique_mot = Mot.query.get(mot_id)
            # ce qui suit permet de rapatrier automatiquement l'auteur du commentaire dans le formulaire d'ajout de commentaire.    
            auteurs = coms.authorships
            return render_template("pages/ajout_commentaire.html", mot=unique_mot, auteurs=auteurs)
    unique_mot = Mot.query.get(mot_id)
    auteurs = coms.authorships
    return render_template("pages/ajout_commentaire.html", nom="Sortiaria", mot=unique_mot, auteurs=auteurs)

@app.route("/recherche")
def recherche():
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats = []

    # On fait de même pour le titre de la page
    titre = "Recherche"
    if motclef:
        resultats = Mot.query.filter(
            Mot.mot_terme.like("%{}%".format(motclef))
        ).paginate(page=page, per_page=MOTS_PAR_PAGE)
        titre = "Résultat pour la recherche `" + motclef + "`"

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef
    )

@app.route("/browse")
def browse():
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = Mot.query.paginate(page=page, per_page=MOTS_PAR_PAGE)

    return render_template(
        "pages/browse.html",
        resultats=resultats
    )

@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            password=request.form.get("password", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
	if current_user.is_authenticated is True:
		logout_user()
		flash("Vous êtes déconnecté-e", "info")
	return redirect("/")
