# Installation de l'application

### Mac OS

**Pré-requis : il est nécessaire d'avoir installé Python3 et MySQL.**

Nous vous conseillons de mettre en place un environnement l'environnement virtuel afin de ne pas modifier l'environnement général de votre ordinateur:
* créer un dossier
* dans ce dossier, créer un environnement virtuel. Pour cela, installer tout d'abord la distribution Anaconda. Vous pouvez la télécharger depuis http://continuum.io/downloads.  Des détails pour l'installation peuvent être trouvés ici : http://docs.continuum.io/anaconda/install.html Utilisez bien la version 3.6 proposée :

  * Installer l'environnement virtuel avec la commande`conda create -n dictionnaire`
  * Puis taper `source activate dictionnaire`
Cette commande sera nécessaire à chaque fois afin d'activer l'environnement virtuel pour pouvoir utiliser Sortiaria.
* Cloner le dossier Dictionnaire en tapant `git clone`+url du code
* Exécuter le fichier datamodel.sql en tapant dans le terminal `mysql -u root -p < datamodel.sql`
* Se déplacer dans le dossier dictionnaire
* Pour lancer Sortiaria taper `python run.py`

A taper dans le terminal pour lancer Sortiaria les fois suivantes :
* `source activate dictionnaire`
* `python run.py`


### Linux (Ubuntu/Debian)

**Pré-requis : il est nécessaire d'avoir installé Python3 et MySQL.**

Nous vous conseillons de mettre en place un environnement l'environnement virtuel afin de ne pas modifier l'environnement général de votre ordinateur:
* créer un dossier
* dans ce dossier, créer un environnement virtuel. Pour cela :

  * Installer l'environnement virtuel avec la commande `sudo apt-get install python3 libfreetype6-dev python3-pip python3-virtualenv`

  * Puis taper `virtualenv ~/.dictionnaire -p python3`
  * Ensuite, taper `source ~/.dictionnaire/bin/activate`
Cette commande sera nécessaire à chaque fois afin d'activer l'environnement virtuel pour pouvoir utiliser Sortiaria.
* Cloner le dossier Dictionnaire en tapant `git clone`+url du code
* Exécuter le fichier datamodel.sql en tapant dans le terminal `mysql -u root -p < datamodel.sql`
* Installer les packages nécessaires au fonctionnement de Sortiaria avec `pip install -r requirements.txt`
* Se déplacer dans le dossier dictionnaire
* Pour lancer Sortiaria taper `python3 run.py`

A taper dans le terminal pour lancer Sortiaria les fois suivantes :
* `source ~/.dictionnaire/bin/activate`
* `python3 run.py`




# Consignes pour le dictionnaire

On créera un système de dictionnaire avec un système de comptes utilisateurs à valider où
- une entrée = un mot
- Une fois un mot enregistré, on pourra ajouter des commentaires signés (par l'auteur) sur le mot
- Chaque commentaire peut être accompagné de plusieurs exemples (qui peuvent avoir une source en lien, un titre de source, un auteur de source)
- On supportera le markdown comme méthode d'entrée des textes libres et on le convertira en HTML à la sortie pour l'affichage
- On pourra faire une recherche dans les commentaires et les entrées du dictionnaire
- On proposera une sortie TEI simple à afficher sur une URL précise ( /entree/motdudictionnaire/xml-tei par exemple )

(Tiré du [wiki du cours de Python](https://github.com/PonteIneptique/cours-python/wiki/2017-2018---Devoirs))

### CONSIGNES GLOBALES :

1. Les rendus se feront via git et github en particulier sur des dépôts de [Chartes-TNAH](https://github.com/Chartes-TNAH).
2. La notation peut différer d'un membre à l'autre du groupe.
3. Une documentation pour la mise en place du projet (installation) sera mise à disposition. Le README de ce dépôt peut être utilisé comme référence.
4. Des données de tests seront fournies afin d'utiliser l'application.
5. (Optionnel) Des tests unitaires seront fournis *Note: cet encart dépendra de l'évolution du cours*.
6. **Le design final ne sera pas évalué** bien qu'il soit recommandé que l'ensemble reste lisible et utilisable.


### la documentation :
- expliciter la mise en place du projet
- documenter le code (variables lisibles)
