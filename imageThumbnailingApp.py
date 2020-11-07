import os
import io
from flask import Flask
import json
from flask import jsonify
from flask import request
from flask import Response
from flask import send_file
from flask import send_from_directory
import imageWorking
import dbscripts.crudDb

app = Flask(__name__)

@app.route('/images', methods=['POST'])
def soumissionImage():
    """ upload a new image, responds an image ID

    >>> curl -F mydata=@Capture.PNG http://127.0.0.1:5000/images \n
    >{"id":42}
    """
    retour =''

    #testing existance of 'mydata' as attached file to upload
    if 'mydata' not in request.files:
        return "No selected 'mydata' File to upload"
    
    file = request.files['mydata']

    #testing filname not empty
    if file.filename == '':
        return 'No file selected (name empty)'

    #Obtention du prochain id disponnible
    id = dbscripts.crudDb.getNextId()

    if(type(id) == int):

        dbscripts.crudDb.saveImage(id,'pending',imageWorking.getAllInfo(file))

        #miniaturisation
        thubnailedImg = imageWorking.thumbnailing(file)

        #enregistrement de l'image
        thubnailedImg.save("static/"+ str(id) + ".jpg","JPEG")

        retour = '{"id":'+str(id)+'}'
    else :
        return ("erreur interne")

    return retour

@app.route('/images', methods=['GET'])
def listImages():
    """ Lists all the stockedimages

    >>> curl http://127.0.0.1:5000/images
    {{id:42,metadatas:{},thumbadress:'http://127.0.0.1:5000/thumbnails/42.jpg'}}
    """
    #TODO
    params=request.args

    retour = params
    print(retour)

    return retour

@app.route('/images/<int:image_id>', methods=['GET'])
def infoImage(image_id):
    """ describe image processing state (pending, success, failure) metadata and links to thumbnail

    >>> curl http://127.0.0.1:5000/images/42
    {{"state":success,"metadatas":{},"link":'http://127.0.0.1:5000/thumbnails/42.jpg'}}
    """
    retour = dbscripts.crudDb.getImage(image_id)

    return retour

@app.route('/thumbnails/<int:thumbnail_id>.jpg', methods=['GET'])
def getThumbnail(thumbnail_id):
    """ read the requested generated thumbnail

    >>> curl http://127.0.0.1:5000/thumbnails/42.jpg
    <img style="-webkit-user-select: none;margin: auto;" src="http://127.0.0.1:5000/thumbnails/42.jpg">
    """

    name =  str(thumbnail_id) + ".jpg"

    return send_from_directory("static/", name)