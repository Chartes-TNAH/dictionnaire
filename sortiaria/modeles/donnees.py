from flask import url_for
import datetime
from flask_login import current_user
from .. app import db

#############################################################
#            AUTHORSHIP ET METHODES ASSOCIEES               #
#############################################################

class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_mot_id = db.Column(db.Integer, db.ForeignKey('mot.mot_id'))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    commentaire_id = db.Column(db.Integer, db.ForeignKey('commentaire.commentaire_id'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.relationship("User", back_populates="authorships")
    mot = db.relationship("Mot", back_populates="authorships")
    commentaires = db.relationship("Commentaire", back_populates="authorships")

    def author_to_json(self):
        return {
            "author": self.user.to_jsonapi_dict(),
            "on": self.authorship_date
        }

    @staticmethod
    def m_authorship(authored):
        """" méthode pour associer la création ou modification d'un mot à un utilisateur """
        lien = Authorship(
            authorship_user_id=current_user.get_id(),
            authorship_mot_id=authored
            )
        try:
            db.session.add(lien)
            db.session.commit()
            return True
        except Exception as erreur:
            return False, [str(erreur)]
            db.session.rollback()

    @staticmethod
    def c_authorship(authored):
        """" méthode pour associer la création ou modification d'un commentaire à un utilisateur """
        lien = Authorship(
            authorship_user_id=current_user.get_id(),
            commentaire_id=authored
            )
        try:
            db.session.add(lien)
            db.session.commit()
            return True
        except Exception as erreur:
            return False, [str(erreur)]
            db.session.rollback()        

#############################################################
#                MOT ET METHODES ASSOCIEES                  #                 
#############################################################

# On crée notre modèle de mot
class Mot(db.Model):
    __tablename__ = "mot"
    mot_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    mot_terme = db.Column(db.Text)
    mot_phon = db.Column(db.Text)
    mot_gram = db.Column(db.Text)
    mot_genre = db.Column(db.Text)
    mot_def = db.Column(db.Text)
    authorships = db.relationship("Authorship", back_populates="mot")
    commentaires = db.relationship("Commentaire", back_populates="mot")

    def to_jsonapi_dict(self):
        return {
            "type": "mot",
            "id": self.mot_id,
            "attributes": {
                "terme": self.mot_terme,
		"phon": self.mot_phon,
		"gram": self.mot_gram,
		"genre": self.mot_genre,
                "definition": self.mot_def,
            },
            "links": {
                "self": url_for("mot", mot_id=self.mot_id, _external=True),
                "json": url_for("api_mot_single", mot_id=self.mot_id, _external=True)
            },
            "relationships": {
                 "editions": [
                     author.author_to_json()
                     for author in self.authorships
                 ]
            }
        }
                
    @staticmethod
    def creer_mot(terme, definition, grammaire, genre, prononciation):
        '''
            Fonction qui sert à ajouter un mot (par les utilisateurs).
            Permet de connaître l'auteur du mot. 
        '''    
        erreurs = []
        if not terme:
            erreurs.append("Le terme est obligatoire")
        if not definition:
            erreurs.append("Il faut donner une définition au mot")
        
        #on vérifie que le mot n'est pas déjà dans la base
        mot_cree = Mot.query.filter(db.and_(Mot.mot_terme == terme)).count()
        if mot_cree > 0:
            erreurs.append("Le terme est déjà inscrit dans la base de données")

        # S'il y a une erreur ou plus
        if len(erreurs) > 0:
            print(erreurs, terme, definition)
            return False, erreurs

        mot = Mot(
            mot_terme=terme,
            mot_def=definition,
            mot_phon=prononciation,
            mot_gram=grammaire,
            mot_genre=genre,
        )
        print(mot)
        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(mot)
            # On envoie le paquet
            db.session.commit()

            # On crée le log dans authorship pour savoir qui a créé le mot
            authoring = mot.mot_id
            authorship = Authorship.m_authorship(
                authored = authoring
            )

            # On renvoie l'utilisateur
            return True, mot

        except Exception as erreur:
            return False, [str(erreur)]
            db.session.rollback()

    @staticmethod
    def modif_mot(id, terme, definition, grammaire, genre, prononciation):
        #ce qui suit permet à l'utilisateur de modifier un mot

        mot = Mot.query.get(id)
        '''
            Fonction qui permet à l'utilisateur de modifier un mot
        '''
        erreurs = []
        if not terme:
            erreurs.append("Le terme est obligatoire")
        if not definition:
            erreurs.append("Il faut donner une définition au mot")


        # S'il y a une erreur ou plus
        if len(erreurs) > 0:
            print(erreurs, terme, definition)
            return False, erreurs

        mot.mot_terme = terme
        mot.mot_def = definition
        mot.mot_phon = prononciation
        mot.mot_gram = grammaire
        mot.mot_genre = genre

        try:

            # On l'ajoute au transport vers la base de données
            db.session.add(mot)
            # On envoie le paquet
            db.session.commit()

            # On crée le log dans authorship pour savoir qui a modifié le mot
            authoring = mot.mot_id
            authorship = Authorship.m_authorship(
                authored = authoring
            )

            # On renvoie l'utilisateur
            return True, mot

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def supprimer_mot(id):
        # Supprime un mot dans la base de données, retourne un booléen : True si la suppression a réussi, sinon False.
        # Supprime aussi les commentaires et les authorships associés.

        mot = Mot.query.get(id)
        coms = mot.commentaires
        auths = mot.authorships

        try:

            for com in coms:
                db.session.delete(com)
                db.session.commit()

            for auth in auths:
                db.session.delete(auth)  
                db.session.commit()

            db.session.delete(mot)
            db.session.commit()

            return True

        except Exception as failed:
            print(failed)
            return False
            db.session.rollback()


#############################################################
#          COMMENTAIRE ET METHODES ASSOCIEES                #
#############################################################

# On crée notre modèle de commentaire           
class Commentaire(db.Model):
    __tablename__ = "commentaire"
    commentaire_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    commentaire_titre = db.Column(db.Text)
    commentaire_source = db.Column(db.Text)
    commentaire_texte = db.Column(db.Text)
    commentaire_mot_id = db.Column(db.Integer, db.ForeignKey('mot.mot_id'))
    authorships = db.relationship("Authorship", back_populates="commentaires")
    mot = db.relationship("Mot", back_populates="commentaires")

    def to_jsonapi_dict(self):
        return {
            "type": "commentaire",
            "id": self.commentaire_id,
            "attributes": {
                "titre": self.commentaire_titre,
                "source": self.commentaire_source,
                "texte": self.commentaire_texte,
                "c_mot_id": self.commentaire_mot_id,
            },
            "links": {
                "self": url_for("mot", commentaire_id=self.commentaire_id, _external=True),
                "json": url_for("api_commentaire_single", commentaire_id=self.commentaire_id, _external=True)
            },
            "relationships": {
                 "editions": [
                     author.author_to_json()
                     for author in self.authorships
                 ]
            }
        }    
     
    
    @staticmethod
    def ajout_commentaire(titre, source, texte, c_mot_id):
        # ce qui suit sert à ajouter un commentaire

        mot=Mot.query.get(id)

        erreurs = []
        if not titre:
            erreurs.append("Le titre est obligatoire")
        if not texte:
            erreurs.append("Rédigez un commentaire")

        # S'il y a une erreur ou plus
        if len(erreurs) > 0:
            print(erreurs, titre, texte)
            return False, erreurs

        commentaire = Commentaire(
            commentaire_titre=titre,
            commentaire_source=source,
            commentaire_texte=texte,
            commentaire_mot_id=c_mot_id,
        )
        print(commentaire)
        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(commentaire)
            # On envoie le paquet
            db.session.commit()

            # On crée le log dans authorship pour savoir qui a modifié le mot
            authoring = commentaire.commentaire_id
            authorship = Authorship.c_authorship(
                authored = authoring
            )        


            # On renvoie l'utilisateur
            return True, mot

        except Exception as erreur:
            db.session.rollback()
            return False, [str(erreur)]


    @staticmethod
    def modifier_commentaire(id, titre, source, texte):
        # Fonction qui permet de modifier un commentaire en particulier

        commentaire = Commentaire.query.get(id)

        erreurs = []
        if not titre:
            erreurs.append("Le titre est obligatoire")
        if not texte:
            erreurs.append("Rédigez un commentaire")


        # S'il y a une erreur ou plus
        if len(erreurs) > 0:
            print(erreurs, titre, texte)
            return False, erreurs

        commentaire.commentaire_titre = titre
        commentaire.commentaire_texte = texte
        commentaire.commentaire_source = source
        
        try:

            # On l'ajoute au transport vers la base de données
            db.session.add(commentaire)
            # On envoie le paquet
            db.session.commit()

            # On crée le log dans authorship pour savoir qui a modifié le mot
            authoring = commentaire.commentaire_id
            authorship = Authorship.c_authorship(
                authored = authoring
            )

            # On renvoie l'utilisateur
            return True, commentaire

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def supprimer_commentaire(commentaire_id):
        # Fonction qui permet de supprimer un commentaire en particulier sur un mot et l'auteur associé

        com = Commentaire.query.get(commentaire_id)
        auths = com.authorships

        try:

            for auth in auths:
                db.session.delete(auth)  
                db.session.commit()

            db.session.delete(com)
            db.session.commit()
            return True

        except Exception as failed:
            print(failed)
            return False
            db.session.rollback() 
