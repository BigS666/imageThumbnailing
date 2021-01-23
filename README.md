# imageThumbnailing
Projet python de miniaturisation d'images

# projet github
https://github.com/BigS666/imageThumbnailing

# Description de l'API
curl http://127.0.0.1:5000/thumnails/9
-> renvoie la miniature de l'image 9

curl -F mydata=@Capture.PNG http://127.0.0.1:5000/images
-> upluaod l'image Capture.PNG

curl http://127.0.0.1:5000/images
-> liste l'ensemble des images de l'api

curl http://127.0.0.1:5000/images/5
-> donne le détail de l'image 5 

curl -X DELETE http://127.0.0.1:5000/images/1
-> supprime l'image 1

# Démarrage de du l'api avec Flask
## dans linux dans le dossier conetant imageThumbnailingApp.py
python3 FLASK_APP=imageThumbnailingApp.py flask run
