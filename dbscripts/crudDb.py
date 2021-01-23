import sqlite3

"""
permet de recuperer le prochain id a utiliser pour le donner a une image a enregitrer
le projet n'utilse pas de sequence
"""
def getNextId():
    # connect db
    conn = sqlite3.connect("thumbnails.db")
    curseur = conn.cursor()
    nombre = 1

    #requete de recuperation du maximum
    try:
        createTableString = "SELECT MAX(id) FROM thumbnails;"
        resulSet = curseur.execute(createTableString)
    except sqlite3.OperationalError as exeption:
        #erreur technique
        return str(exeption) + "Bdd non crée"
    try:
        for resultat in resulSet:
            nombre = int(resultat[0])
            nombre += 1
    except TypeError as exception:
        #s'il n'y a aucune ligne en bdd
        print(str(exception) + " : pas de resultat dans la base")
        nombre = 1

    conn.close()
    return nombre

"""
methode d'insertion d'une ligne d'information sur une miniature
"""
def saveImage(id, state, meta):
    conn = sqlite3.connect("thumbnails.db")
    curseur = conn.cursor()
    #le lien pour acceder a l'image via l'api
    link = "http://127.0.0.1:5000/thumbnails/" + str(id) + ".jpg"
    insertString = (
        """insert into thumbnails (id,state,metadata,link) values (?,?,?,?)"""
    )
    params = (id, str(state), str(meta), str(link))
    curseur.execute(insertString, params)
    conn.commit()
    conn.close()

"""
methode de recuperation des informations en base de la miniature dont l'id est @id
"""
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

"""
methode de recuperation de l'ensemble des images presentes en base
"""
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


"""
Methode de suppression d'une ligne correspondant a une miniature @id
"""
def deleteImage(id):
    conn = sqlite3.connect("thumbnails.db")
    curseur = conn.cursor()
    selectString = """delete from thumbnails where id=?"""
    params = (id,)
    curseur.execute(selectString, params)
    conn.commit()
    conn.close()