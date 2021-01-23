from PIL import Image
from PIL.ExifTags import TAGS

"""
Ensemble de méthodes de traitement d'image
"""

def thumbnailing(image):
    im = Image.open(image)
    #miniaturisation de taille 50 pixels par 50
    im.thumbnail((50, 50))
    r, g, b, *args = im.split()
    im = Image.merge("RGB", (r, g, b))
    #on renvoie la miniature
    return im

def open(chemin):
    #ouvrir une image depuis un chemin
    return Image.open(chemin)

def getTags(image):
    im = Image.open(image)
    im.verify()
    #recuperations des meta datas exif
    #tous les types d'images n'ont pas leur exif de renseignes
    #on prefera getAllInfo
    exif_data = im._getexif()
    labeled = {}
    for (key, val) in exif_data.items():
        labeled[TAGS.get(key)] = val

    return labeled

def getAllInfo(image):
    im = Image.open(image)
    #renvoie toutes les informations relatives a l'image
    #utilise dan le projet pour stocker les meta datas
    return im.__dict__

def getInfo(image):
    im = Image.open(image)
    #autre facon de recupereer des informations
    #non utilise dans le projet finalement
    return im.info