                            Documentation

Le fichier Maso contient 3 fichiers, un fichier data, un fichier documentation, un fichier texte (READ ME) et fichier source (SRC) 

Fichier Data

Le dossier Data contient les fichiers données (T,V) et données calibration qui regroupent les sauvegardes des données des mesures effectuées 

Fichier source (SRC)

Le fichier source contient les fichiers code permettant de faire fonctionner le programme. 
On y trouve 5 fichiers, un fichier “Consigne”,  un fichier “calibration”, un 
fichier “Mesures”, un fichier “pycache”(cache), et un fichier “arduino_redox.ino”

2.1)   Fichier Consignes

Le fichier consigne contient le code du menu. Grâce à l’importation des informations du fichier calibration et Mesures, on peut choisir les consignes que doit suivre le boîtier de commande.

6 propositions sont faites à l’utilisateur, en fonction du choix fait par ce dernier, des mesures peuvent être effectuées, ou, pour les choix plus précis, un 2ème menu peut s’afficher afin de préciser la demande. 
L’utilisateur peut choisir entre plusieurs options :

1. Calibration d’usine - permettant de mesurer sans coefficient correctif 
2. Solution Calibration à 1 étalon - permettant de mesurer le coefficient correctif que l’on appliquera aux mesures
3. Mesure simple - permettant de choisir le nombre de mesures souhaitée
4. Mesure en continu - permettant de suivre en temps réel l’évolution des mesures
5. Réinitialiser la calibration - permettant d’enregistrer une nouvelle valeur de calibration 
6. Quitter le programme

Lors de la calibration à 1 étalon, l’enregistrement se fait automatiquement après la calibration complète

Lors de la réalisation des mesures (options 3 et 4), l’utilisateur choisit, avant l’enregistrement, le format de sortie : représentation graphique ou données brutes. La procédure d’enregistrement diffère ensuite selon l’option sélectionnée : 

option 3. Mesure simple : Les résultats s'enregistrent automatiquement dans un dossier data.
option 4. Mesure en continue : après avoir pressé q choisir l’option enregistrer les données (ou quitter)

2.2) Fichier calibration:

Ce fichier regroupe les fonctions permettant de:

Définir le coefficient correctif (nul dans le cas de la calibration d’usine)
réajuster la valeur de potentiel mesuré en fonction du coefficient correctif défini au dessus

2.3) Fichier Mesure :

Ce fichier regroupe les fonctions permettant de:

lister la température et le voltage
tracer les graphiques de températures et de voltage

2.4) fichier pycache : 

Ce fichier contient le cache du code

2.5) Fichier arduino_redox.ino : 

Ce fichier contient le code téléversé dans le boîtier arduino permettant de faire l’acquisition des données

Remarques à l’utilisateur : 

- L’arrêt du programme en cours se fait lorsque la touche ‘q’ est pressée. Cependant il est nécessaire parfois que la touche soit pressée plusieurs fois afin que le programme cesse complètement.

- Le calibrage utilisé si celui-ci n'est pas réalisé en amont des mesures effectuées, est basé sur le dernier enregistrement de la sonde. Veillez donc à calibrer correctement la machine avant la réalisation des mesures. Réinitialiser le calibrage renvoie un terme correctif nul.

- Pour changer la fréquence de mesure :
Changer la fonction time.sleep de la mesure souhaitée (graphe_live, data_live etc)

- A la fin de l’utilisation du programme, choisir impérativement l’option 6. Quitter le programme afin d’éviter les bugs
