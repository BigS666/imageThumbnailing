from flask import Flask
import json
from flask import jsonify
from flask import request
import imageWorking

app = Flask(__name__)

@app.route('/images', methods=['POST'])
def soumissionImage():
    """ upload a new image, responds an image ID

    >> Windows
    >>> curl -F ‘mydata=testFile.txt’ http://127.0.0.1:5000/images \n
    >> Unix / mac
    >>> curl -F ‘mydata=@path/to/local/file’ http://127.0.0.1:5000/images \n
    >{id:42}
    """
    retour =''

    #testing existance of 'mydata' as attached file to upload
    if 'mydata' not in request.files:
        return "No selected 'mydata' File to upload"
    
    file = request.files['mydata']

    #testing filname not empty
    if file.filename == '':
        return 'No file selected (name empty)'

    thubnailedImg = imageWorking.thumbnailing(file)


    return retour

@app.route('/images', methods=['GET'])
def listImages():
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
    {{id:42,state:success,metadatas:{},thumbadress:'http://127.0.0.1:5000/thumbnails/42.jpg'}}
    """
    params=request.args

    retour = params
    print(retour)

    return jsonify(retour)

@app.route('/thumbnails/<int:thumbnail_id>.jpg', methods=['GET'])
def getThumbnail(thumbnail_id):
    """ read the requested generated thumbnail

    >>> curl UPLOAD_ADDRESS/thumbnails/42.jpg
    <img  src="static/42.jpg">
    """
    lienversimage = '<img src="../static/'+str(thumbnail_id)+'.jpg">'

    return lienversimage