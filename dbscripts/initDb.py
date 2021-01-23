import sqlite3

# Script d'intialisation de la DB
def initialisation():
    #création du fichier s'il n'existe pas
    with open("thumbnails.db", "w"):

        # create db
        conn = sqlite3.connect('thumbnails.db')
        curseur = conn.cursor()

        #creation de la table d'informations des miniatures
        createTableString = 'CREATE TABLE IF NOT EXISTS "thumbnails" ([id] Integer Primary key, [state] TEXT, [metadata] TEXT, [link] TEXT);'

        curseur.execute(createTableString)

        conn.close()

initialisation()