from imageThumbnailingApp import app
import re
import dbscripts.crudDb


def testPost():
    """
    Ce test vérifie que l'api de miniaturisation d'image fonctionne
    on verifie que le retour de l'api est un id
    """
    with app.test_client() as c:

        image = "Capture.PNG"
        data = {"mydata": (open(image, "rb"), image)}
        rv = c.post("/images", data=data)
        body = rv.data
        pattern = re.compile('{"id":.*}')
        print(body.decode("utf-8"))
        result = False
        if pattern.match(body.decode("utf-8")):
            result = True
        assert result


def getThumnails():
    with app.test_client() as c:
        rv = c.get("/thumbnails/3")
        body = rv.data
        open(body, "rb")
        assert body == '<img src="thumbnails/42.jpg">'


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
    Le retour contient un element "state"
    """
    with app.test_client() as c:
        rv = c.get("/images")
        json_data = rv.data
        pattern = re.compile('.*"state":.*')
        result = False
        if pattern.match(json_data.decode("utf-8")):
            result = True
        assert result
