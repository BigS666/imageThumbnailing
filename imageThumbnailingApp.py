import io
import json
import os

from flask import (Flask, Response, jsonify, request, send_file,
                   send_from_directory)

import dbscripts.crudDb
import imageWorking

app = Flask(__name__)


@app.route("/images", methods=["POST"])
def soumissionImage():
    """upload a new image, responds an image ID

    >>> curl -F mydata=@Capture.PNG http://127.0.0.1:5000/images \n
    >{"id":42}
    """
    retour = ""

    # testing existance of 'mydata' as attached file to upload
    if "mydata" not in request.files:
        return "No selected 'mydata' File to upload"

    file = request.files["mydata"]

    # testing filname not empty
    if file.filename == "":
        return "No file selected (name empty)"

    # Obtention du prochain id disponnible
    id = dbscripts.crudDb.getNextId()

    if type(id) == int:

        dbscripts.crudDb.saveImage(id, "pending", imageWorking.getAllInfo(file))

        # miniaturisation
        thubnailedImg = imageWorking.thumbnailing(file)

        # enregistrement de l'image
        thubnailedImg.save("static/" + str(id) + ".jpg", "JPEG")

        retour = '{"id":' + str(id) + "}"
    else:
        return "erreur interne"

    return retour


@app.route("/images", methods=["GET"])
def listImages():
    """Lists all the stockedimages

    >>> curl http://127.0.0.1:5000/images
    {{id:42,metadatas:{},thumbadress:'http://127.0.0.1:5000/thumbnails/42.jpg'}}
    """
    retour = dbscripts.crudDb.getAllImages()

    return retour


@app.route("/images/<int:image_id>", methods=["GET"])
def infoImage(image_id):
    """describe image processing state (pending, success, failure) metadata and links to thumbnail

    >>> curl http://127.0.0.1:5000/images/42
    {"state":success,"metadatas":{},"link":'http://127.0.0.1:5000/thumbnails/42.jpg'}
    """
    #recherche en base les donnees de l'image souhaitee
    retour = dbscripts.crudDb.getImage(image_id)

    return retour


@app.route("/thumbnails/<int:thumbnail_id>.jpg", methods=["GET"])
def getThumbnail(thumbnail_id):
    """read the requested generated thumbnail

    >>> curl http://127.0.0.1:5000/thumbnails/42.jpg
    <img style="-webkit-user-select: none;margin: auto;" src="http://127.0.0.1:5000/thumbnails/42.jpg">
    """
    #construction du nom du fichier correspondant a l'id souhaite
    name = str(thumbnail_id) + ".jpg"

    #envoi de l'image stockee dans le dossier static
    return send_from_directory("static/", name)


@app.route("/images/<int:image_id>", methods=["DELETE"])
def deleteImage(image_id):
    """delete the selected image

    >>> curl -X DELETE http://127.0.0.1:5000/images/1
    {{"state":"success"}}
    """
    retour = '{ {"state":"success"} }'

    #suppression de la ligne dans la base
    dbscripts.crudDb.deleteImage(image_id)

    #suppression du fichier image
    if os.path.exists("static/" + str(image_id) + ".jpg"):
        os.remove("static/" + str(image_id) + ".jpg")
    else:
        retour = '{ {"state":"echec de suppression du fichier"} }'

    return retour
