from imageThumbnailingApp import app
import re
import dbscripts.crudDb
from PIL import Image
import io


def testPost():
    """
    Ce test vérifie que l'api de miniaturisation d'image fonctionne
    on verifie que le retour de l'api est un id
    """
    with app.test_client() as c:

        #image de test presente dans le repertoire
        image = "Capture.PNG"
        data = {"mydata": (open(image, "rb"), image)}
        #on post l'image
        rv = c.post("/images", data=data)
        body = rv.data
        #atterne de verification du retour de l'api
        pattern = re.compile('{"id":.*}')
        #le retour respecte bien la pattern d'une reponse attendue
        assert pattern.match(body.decode("utf-8"))

def testSupprLastIamge():
    """
    Ce test vérifie que l'appel a la suppression d'une image fonctionne
    il supprime la derniere image ajoutée
    """
    with app.test_client() as c:
        #recuperation de l'id de la derniere image ajoutee
        _id = dbscripts.crudDb.getNextId() - 1
        rv = c.delete("/images/" + str(_id))
        body = rv.data
        #on verifie que le retour est succes
        assert body.decode("utf-8") == '{ {"state":"success"} }'


def testImageList():
    """
    Ce test vérifie que l'appel a l'api de listing des images fonctionne.
    Le retour de l'api contient un element "state"
    """
    with app.test_client() as c:
        #appel de l'api de listing
        rv = c.get("/images")
        json_data = rv.data
        #patterne d'une reponse simple correctement formee
        pattern = re.compile('.*"state":.*')
        assert pattern.match(json_data.decode("utf-8"))

def testGetThumnail():
    """
    Ce test vérifie que l'appel a l'api de récupération de miniature fonctionne
    Le retour de l'api est une image 
    """
    with app.test_client() as c:
        #appel de l'api de recuperation de miniature
        rv = c.get("/thumnails/3.jpg")
        body = rv.data
        #on construit l'image a partir des bytes retournes
        im = Image.open(io.BytesIO(body))
        #on construit l'image depuis le repertoir
        image2 = Image.open("static/3.jpg")
        #on compare que l'image du repertoire est celle retournée par l'api
        assert im == image2