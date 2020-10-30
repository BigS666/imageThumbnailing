from flask import Flask
import json
from flask import jsonify
from flask import request

app = Flask(__name__)

@app.route('/images', methods=['POST'])
def soumissionImage():
    """ upload a new image, responds an image ID

    >>> curl -F ‘data=@path/to/local/file’ UPLOAD_ADDRESS/images
    42
    """
    params=request.form['']

    retour = params
    print(retour)

    return retour

@app.route('/images', methods=['GET'])
def litesImages():
    """ Lists all the stockedimages

    >>> curl http://127.0.0.1:5000/images
    {{id:42,thumbadress:'UPLOAD_ADDRESS/thumbnails/42.jpg'}}
    """
    params=request.args

    retour = params
    print(retour)

    return jsonify(retour)

@app.route('/images/<int:image_id>', methods=['GET'])
def infoImage(image_id):
    """ describe image processing state (pending, success, failure) metadata and links to thumbnail

    >>> curl UPLOAD_ADDRESS/images/42
    {{id:42,state:success,thumbadress:'UPLOAD_ADDRESS/thumbnails/42.jpg'}}
    """
    params=request.args

    retour = params
    print(retour)

    return jsonify(retour)

@app.route('/thumbnails/<int:thumbnail_id>.jpg', methods=['GET'])
def getThumbnail(thumbnail_id):
    """ read the requested generated thumbnail

    >>> curl UPLOAD_ADDRESS/thumbnails/42.jpg
    <img  src="thumbnails/42.jpg">
    """
    lienversimage = '<img src="../thumbnails/'+str(thumbnail_id)+'.jpg">'

    return lienversimage