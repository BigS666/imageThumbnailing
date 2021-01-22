import sqlite3


def getNextId():

    # connect db
    conn = sqlite3.connect("thumbnails.db")
    curseur = conn.cursor()
    nombre = 1

    try:
        createTableString = "SELECT MAX(id) FROM thumbnails;"
        resulSet = curseur.execute(createTableString)
    except sqlite3.OperationalError as exeption:

        return str(exeption) + "Bdd non crée"

    try:
        for resultat in resulSet:
            print(resultat)
            nombre = int(resultat[0])
            nombre += 1
    except TypeError as exception:
        print(str(exception) + " : pas de resultat dans la base")

    conn.close()
    return nombre


def saveImage(id, state, meta):
    conn = sqlite3.connect("thumbnails.db")
    curseur = conn.cursor()
    link = "http://127.0.0.1:5000/thumbnails/" + str(id) + ".jpg"
    insertString = (
        """insert into thumbnails (id,state,metadata,link) values (?,?,?,?)"""
    )
    params = (id, str(state), str(meta), str(link))
    curseur.execute(insertString, params)
    conn.commit()
    conn.close()


def getImage(id):
    conn = sqlite3.connect("thumbnails.db")
    curseur = conn.cursor()
    selectString = """select state,metadata,link from thumbnails where id=?"""
    params = (id,)
    results = curseur.execute(selectString, params)
    retour = "Aucune image : " + str(id)
    for resultat in results:
        try:
            state = str(resultat[0])
            metadata = str(resultat[1])
            link = str(resultat[2])
            retour = (
                '{"state":'
                + state
                + ', "metadata":'
                + metadata
                + ', "link":'
                + link
                + "}"
            )
        except TypeError as identifier:
            print(str(identifier))
            retour = (
                "Erreur lors de la récupération des informations de l'image : "
                + str(id)
            )

    conn.close()
    return retour

def getAllImages():
    conn = sqlite3.connect("thumbnails.db")
    curseur = conn.cursor()
    selectString = """select state,metadata,link from thumbnails"""
    results = curseur.execute(selectString)
    retour = "{"
    for resultat in results:
        try:
            state = str(resultat[0])
            metadata = str(resultat[1])
            link = str(resultat[2])
            retour += '{"state": "' + state + '", "metadata":"' + metadata  + '", "link":"' + link  + '"},'
        except TypeError as identifier:
            print(str(identifier))
            retour = (
                "Erreur lors de la récupération des informations des images "
                + str(id)
            )
    #retrait de la derniere virgule
    retour = retour[:-1]
    retour += "}"

    conn.close()
    return retour

def deleteImage(id):
    conn = sqlite3.connect("thumbnails.db")
    curseur = conn.cursor()
    selectString = """delete from thumbnails where id=?"""
    params = (id,)
    curseur.execute(selectString, params)

    conn.commit()
    conn.close()