from PIL import Image
from PIL.ExifTags import TAGS

def thumbnailing(image):
    #thnail = image
    im = Image.open(image)
    #print(im)
    #print(im.format)
    #print(im.size)
    im.thumbnail((50, 50))
    r, g, b, *args = im.split()
    im = Image.merge("RGB", (r, g, b))
    #im.save("pillow-logo-thumbnail.jpg", "JPEG")
    return im

def open(chemin):
    return Image.open(chemin)

def getTags(image):
    im = Image.open(image)
    im.verify()
    exif_data = im._getexif()
    labeled = {}
    for (key, val) in exif_data.items():
        labeled[TAGS.get(key)] = val

    return labeled

def getAllInfo(image):
    im = Image.open(image)
    return im.__dict__

def getInfo(image):
    im = Image.open(image)
    return im.info