import numpy as np
import Mesure as mes 
import matplotlib.pyplot as plt 
import datetime
import locale
import calibration as cal
import keyboard
from pathlib import Path
import serial
import time

BASE = Path(__file__).parent.parent

chemin = BASE/"Data"/"données (T,V)"
menu = """
Bienvenue dans le programme de calibration et de mesure de potentiel ORP !
====================================
Que voulez vous faire ?
====================================
1)Calibrer la sonde 
************************************
2) Mesure simple
3) Mesure en continu
************************************
4) Réinitialiser la calibration
5) Quitter
"""


menu_calibration = """
====================================
1) Calibration d'usine
2) Calibration à 1 étalon 
3) Calibration à 2 étalons
4) Retour au menu principal
"""
indication_calibration = """
====================================
Pour la calibration, nous vous conseillons de commencer les mesures 
au moin 30 secondes après l'immersion de la sonde dans la solution, afin que les mesures soient stables ainsi
que de faire au choisir 100 mesures pour réduire au maximum l'écart type et avoir une moyenne précise.
"""


menu_mesure="""
====================================
Quel résultat voulez-vous obtenir ?
====================================
1) Graphiques de Température et de Potentiel 
2) Données brut (T,V,csv) 
3) Retour au menu principal
"""

menu_live = """
====================================
Que voulez-vous faire ?
====================================
1) Sauvegarder les données
2) Retour au menu principal sans sauvegarder
"""
menu_mesure2 = """
====================================
Que souhaitez-vous faire de ce graphiques ?
====================================
1) Sauvegarder les données de Température et Potentiel
2) Sauvegarder la figure
3) Les deux
4) Retour au menu principal
"""
indication_live = """
/!\\ Attention, le dernier calibrage enregistré sera utilisé.
Si vous souhaitez sauvegarder les données veillez à noter apartir de quel nombre de mesure (U.A) le potentiel se stabilise (en entier) ')
Les mesures commencent, pour arreter appuyez sur q
"""
try :
    portIN,s = mes.connexion_port(br=115200, portIN='')
except  serial.SerialException :
        print(f"Erreur: impossible d'ouvrir le port, essayez de le trouver manuellement")

continuer = True
C0 = 0
while continuer :
   reponse = input(menu)
   if reponse == "1":
        reponse_calibration = input(menu_calibration)
        print(indication_calibration)
        if reponse_calibration == '1' :
            C0 =(cal.calibration_usine()) 
            print("Calibration d'usine appliquée (C0 = 0).")
        
        elif reponse_calibration == '2':
            nb_mesures = int(input("Combien de mesures voulez-vous faire pour la calibration à un étalon ? (en entier)"))
            _,V= mes.data(s,N=nb_mesures)
            C0 = cal.calibration_etalon(V)
            print("Voici le terme correctif (offset): %4.2f" % (C0))
        
        elif reponse_calibration == '3' :
            C0,V1_moy, V2_moy, tendance,r_squared,E1,E2 = cal.calibration_2_etalons(s, E1=None,E2=None, V1=None, V2=None)
            fig =cal.graphe_cal2(V1_moy, V2_moy, tendance, r_squared, E1, E2)
            print("Voici le terme correctif : %4.2f" % (C0))
        if reponse_calibration == '2' or reponse_calibration =='3' :
            rep = input("Souhaitez-vous sauvegarder les données de calibration ? (yes/no) : ")
            if rep == 'yes' :
                if reponse_calibration == '2' :
                    cal.enregistrement_cal(C0,nb_etalons=1)
                elif reponse_calibration == '3' :
                    cal.enregistrement_cal(C0,tendance=tendance, nb_etalons=2)
                    cal.enregistrement_cal2_png(fig)
         

   elif reponse == '2' :      
       """_summary_
               Sous-option 3-1-1/2/3 — Sauvegarde des données Potentiel et / ou température
               Génère un fichier .csv horodaté contenant  la liste V_real et/ ou T 
               Le nom du fichier suit le format : 'Mesure Voltage et/ou Température JJ Mois, HHhMM.csv' """
       print('Attention, le dernier calibrage enregistré sera utilisé et les mesures vont commencé')
       T,V = mes.data(s)
       V_real = cal.V_real_f(V,C0)
       reponse_mesure = input(menu_mesure)

       if reponse_mesure == "1" :
           fig = mes.Graphe_T_V(T,V_real)
           reponse_mesure2 = input(menu_mesure2) 

           if reponse_mesure2 == '1':
               mes.enregistrement_csv (T,V_real)

           elif reponse_mesure2 == '2':
               mes.enregistrement_png(fig)
           elif reponse_mesure2 == '3':
               mes.enregistrement_csv(T,V_real)
               mes.enregistrement_png(fig)
               

     
       elif reponse_mesure == '2':
        mes.enregistrement_csv(T,V)                    
           
   elif reponse == '3':
       print(indication_live)
       time.sleep(2)
       T ,V,fig = mes.graphe_live(C0,s)
       
       reponse_live = input(menu_live) 
       if reponse_live =='1':
        a = int(input('A partir de quel nombre de mesure (U.A) le potentiel se stabilise (en entier)?'))
        moy_T, moy_V, sigma = mes.informations_1er_ordre(T,V,a)
        mes.enregistrement_csv(T,V,moy=moy_V,sigma=sigma)
        mes.enregistrement_png(fig)
   elif reponse == '4':
    C0 = 0
    print("Calibration réinitialisée (à 0)")
   elif reponse == '5':
        print("Merci d'avoir utilisé ce programme, à bientôt !")
        continuer = False


