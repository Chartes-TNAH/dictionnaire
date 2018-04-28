from flask import render_template, request, url_for, jsonify
from urllib.parse import urlencode

from ..app import app, db
from ..constantes import MOTS_PAR_PAGE, API_ROUTE
from ..modeles.donnees import Mot, Commentaire


def Json_404():
	response = jsonify({"erreur": "Unable to perform the query"})
	response.status_code = 404
	return response


@app.route(API_ROUTE+"/mot/<mot_id>")
def api_mots_single(mot_id):
	try:
		query = Mot.query.get(mot_id)
		return jsonify(query.to_jsonapi_dict())
	except:
		return Json_404()


@app.route(API_ROUTE+"/mot")
def api_mot_browse():
	""" Route permettant la recherche plein-texte
    
    """
	motclef = request.args.get("q", None)
	page = request.args.get("page", 1)

	if isinstance(page, str) and page.isdigit():
		page = int(page)
	else:
		page = 1

	if motclef:
		query = Mot.query.filter(db.or_(Mot.mot_terme.like("%{}%".format(motclef)),
			Mot.mot_def.like("%{}%".format(motclef)))	
		)
	else:
		query = Mot.query

	if len(resultats) == 0 :
		return Json_404()
	else :
		dict_resultats = {
				"resultats": [
				mot.person_to_json()
				for mot in resultats
		]
	}
	response = jsonify(dict_resultats)
	return response