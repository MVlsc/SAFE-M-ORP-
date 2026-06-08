from Mesure import data
import numpy as np
import datetime
import locale
import calibration as cal
import keyboard
from pathlib import Path
import serial

#calibration d'usine : 
def calibration_usine():
    """_summary_
    Applique la formule de calibration d'usine à une liste de tensions mesurées.
    Pour chaque valeur de V ('brut'), on convertit : E = (2 - i) * 1000 (qui sera calculé par V_real), mais retourne
    systématiquement C0 = 0 (aucun offset correctif n'est appliqué).
    Cette fonction sert de référence sans correction : elle suppose que le capteur
    est déjà calibré en sortie d'usine. 

Remarque : on ne savait pas si on devait définir une fonction (cacalibration_usine) ou  juste mettre C0 = 0 pour l'option 1 du menu

    Args:
       none 

    Returns:
        int: C0 = 0, terme correctif nul (calibration d'usine sans offset).
    """
    C0 = 0
    return C0

#calibration a un étalon
def calibration_etalon(V):
    """_summary_
    Calcule le terme correctif C0 par calibration à un étalon.
    Demande à l'utilisateur la valeur du potentiel de la solution étalon,
    puis calcule pour chaque tension mesurée l'écart entre la valeur attendue
    et la valeur convertie. C0 est la moyenne de ces écarts, utilisée ensuite
    pour corriger les mesures réelles.

    Args:
        V (list[float]): Liste des tensions brutes mesurées sur la solution étalon (en volts).

    Returns:
        float: C0, terme correctif moyen (offset en mV) à appliquer aux mesures futures.
    """
    E= float(input('quelle est le potentiel de la solution'))
    C=[]
    for i in V :
        X = E-((2-i)*1000)
        C.append(X)
    C0 = np.mean(C)
    return C0

     
#if __name__ == '__main__':
    T,V = data()
    print(calibration_etalon(V))



def V_real_f (V,C0):
    """_summary_
    Convertit une liste de tensions brutes en valeurs de potentiel corrigées (en mV),
    en appliquant la formule de conversion du capteur et l'offset de calibration C0.
    La conversion utilisée est : V_corrigé = (2 - i) * 1000 + C0.

    Args:
        V (list[float]): Liste des tensions brutes mesurées par le capteur (en volts).
        C0 (float): Terme correctif issu de la calibration (en mV), peut être = 0 si
         calibration d'usine, ou une valeur calculée via calibration_etalon().

    Returns:
        list[float]: Liste des potentiels corrigés (en mV), de même longueur que V.
    """
    V_real =[]
    for i in V : 
            a = (2-i)*1000 + C0
            V_real.append(float(a))
    return V_real 

def enregistrement_cal (figure,C0) :
    BASE = Path(__file__).parent.parent
    chemin = BASE/"Data"/'data_figures'/nom_fichier      
    a = input('Quel est le nom de la solution ? ')
    now = datetime.datetime.now()
    nom_fichier = now.strftime(f"Calibration {a} %d %B, %Hh%M.csv")
    chemin = BASE/"Data"/"données calibration"/nom_fichier      
    resultat = np.atleast_2d(C0) #  garantit un array 2D pour savetxt
    with open(chemin, 'w', newline='', encoding='utf-8') as f:  #encodage explicite
        np.savetxt(f, resultat, fmt='%.2f', header=f"Donnees Calibration de la solution {a} (=Co)")   
    
    return 'Le fichier csv a bien été enregistré.'


#if __name__ == '__main__':
    T,V = data()
    C0=0
    V_real = V_real_f(V,C0)
    print(V_real) 
    print (V)

