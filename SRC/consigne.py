import numpy as np
import Mesure as mes 
import matplotlib.pyplot as plt 
import datetime
import locale
import calibration as cal
import keyboard
from pathlib import Path
import serial

BASE = Path(__file__).parent.parent

chemin = BASE/"Data"/"données (T,V)"
menu = """
====================================
Que voulez vous faire ?
====================================
1) Calibration d'usine
2) Solution calibration à 1 étalon 
************************************
3) Mesure simple
4) Mesure en continu
************************************
5) Réinitialiser la calibration
6) Quitter
"""
menu_mesure="""
====================================
Quel résultat voulez-vous obtenir ?
====================================
1) Graphiques de Température et de Potentiel 
2) Données brut (T,V,csv) 
3) Quitter
"""

menu_live = """
====================================
Que voulez-vous faire ?
====================================
1) Sauvegarder les données
2) Quitter sans sauvegarder
"""
menu_mesure2 = """
====================================
Que souhaitez-vous faire de ce graphiques ?
====================================
1) Sauvegarder les données de Température et Potentiel
2) Sauvegarder la figure
3) Les deux
4) Quitter
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
     C0 =(cal.calibration_usine()) 
     print("Calibration d'usine appliquée (C0 = 0).")

   elif reponse == '2':
    T, V = mes.data(s)
    C0 = cal.calibration_etalon(V)
    print("Voici le terme correctif : %4.2f" % (C0))
    V_real = cal.V_real_f(V, C0)
    print('La nouvelle tension mesurée est contenue dans la liste "V_real" et les données de calibration sont sauvegardées automatiquement au nom de la solution')
    cal.enregistrement_cal(C0)
   elif reponse == '3' :      
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
           
   elif reponse == '4':
       print('Attention, le dernier calibrage enregistré sera utilisé.')
       print('Les mesures commencent, pour arreter appuyez sur q') 
       T ,V,fig = mes.graphe_live(C0,s)
       
       reponse_live = input(menu_live) 
       if reponse_live =='1':
        a = int(input('A partir de quel nombre de mesure (U.A) le potentiel se stabilise (en entier)?'))
        moy_V = np.mean(V[int(a):])
        sigma = np.std(V[int(a):])
        moy_T = np.mean(T[int(a):])

        print(f"moyenne Potentiel(mV) = {moy_V}")
        print(f'écart type (écart-type) = {sigma}')
        print(f'moyenne Température (°C)={moy_T}')
        mes.enregistrement_csv(T,V,moy=moy_V,sigma=sigma)
        mes.enregistrement_png(fig)
   elif reponse == '5':
    C0 = 0
    print("Calibration réinitialisée (à 0)")
   elif reponse == '6': 
        continuer = False

