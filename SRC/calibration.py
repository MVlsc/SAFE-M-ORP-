import Mesure as mes 
import numpy as np
import datetime
import locale
import calibration as cal
import keyboard
from pathlib import Path
import serial
import time
import matplotlib.pyplot as plt
import scipy.stats as stats

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
    E= float(input('quelle est le potentiel de la solution étalon (mV) ? '))
    C=[]
    for i in V :
        X = E-((2-i)*1000)
        C.append(X)
    C0 = np.mean(C)
    return C0
# s, portIN = mes.connexion_port()
# _,V = mes.data(s)
# calibration_etalon(V)

     
#if __name__ == '__main__':
    # T,V = data()
    # print(calibration_etalon(V))



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
#=======================================================
#Enregistrement des données de calibration :

def enregistrement_cal (C0, tendance = None,nb_etalons=None) :
    BASE = Path(__file__).parent.parent     
    now = datetime.datetime.now()
    if nb_etalons == 1:
        nom_fichier = now.strftime(f"Calibration à {nb_etalons} étalons %d %B, %Hh%M.csv")
    elif nb_etalons == 2:
        nom_fichier = now.strftime(f"Calibration à {nb_etalons} étalons %d %B, %Hh%M.csv")
    elif nb_etalons is None :
        nom_fichier = now.strftime(f"Calibration d'usine %d %B, %Hh%M.csv")
    chemin = BASE/"Data"/"données calibration"/nom_fichier      
    if tendance is None :
        resultat = np.atleast_2d(C0) #  garantit un array 2D pour savetxt
        with open(chemin, 'w', newline='', encoding='utf-8') as f:  #encodage explicite
            np.savetxt(f, resultat, fmt='%.2f', header=f"Donnees Calibration à {nb_etalons} étalons(Co,tendance)") 
    else : 
        slope, intercept = tendance.coeffs
        resultat = np.atleast_2d([C0, slope, intercept]) #  array 2D avec C0, slope et intercept
        with open(chemin, 'w', newline='', encoding='utf-8') as f:  #encodage explicite
            np.savetxt(f, resultat, fmt='%.2f', header=f"Donnees Calibration à {nb_etalons},tendance : E = {slope:.2f}*V + {intercept:.2f}") 

def enregistrement_cal2_png (fig) :
    BASE = Path(__file__).parent.parent
    now = datetime.datetime.now()
    nom_fichier = now.strftime("Graphique Calibration 2 étalons %d %B, %Hh%M.png")
    chemin = BASE/"Data"/'data_figures'/'data_figures_calibration'/nom_fichier      
    fig.savefig(chemin,bbox_inches='tight')
    return 'Le fichier png a bien été enregistré.'
# =======================================================================================================
# Calibration à 2 étalons :

def calibration_2_etalons(s, E1=None, E2=None,V1=None, V2=None) :
    if E1 is None and V1 is None:
        E1 = float(input('Potentiel de la solution étalon 1 (mV) : '))
        input('Placer votre sonde dans la solution étalon 1, quand vous êtes prêt, écrivez OK ===>')
        print('Début des mesures...')
        T, V1 = mes.data(s, N=100)
        print('Fin des mesures')
    if E2 is None and V2 is None:
        E2 = float(input('Potentiel de la solution étalon 2 (mV) : '))
        input('Nettoyer et sécher votre sonde, puis la placer dans la solution étalon 2 , quand vous êtes prêt, écrivez OK ===>')
        print('Début des mesures...')
        T, V2 = mes.data(s, N=100)
        print('Fin des mesures')

    V1_moy = np.mean(V1)
    V2_moy = np.mean(V2)
    
    tendance = slope, intercept, r_value, p_value, std_err = stats.linregress([V1_moy,V2_moy],[E1,E2])
    r_squared = (r_value)**2
    C0 = intercept 
    tendance = np.poly1d([slope, intercept])
    if r_squared <= 0.9 :
        print(f"R^2 ={r_squared},la courbe d'étalonnage n'est pas très précise, il est préférable de recommencer")
    else : 
        print(f"R^2 = {r_squared}, la coure d'étalonnage est précise, on peut l'utiliser pour calibrer la sonde.")
    print(f"L'offset moyen est de C0 = {C0:.2f} mV")
    print(f"L'équation de la droite est y= {slope:.2f}*x + {intercept:.2f}")
    return C0,V1_moy, V2_moy, tendance,r_squared,E1,E2

#Graphique de la tendance de l'étalonnage. 
def graphe_cal2(V1_moy, V2_moy, tendance, r_squared, E1, E2):
    slope, intercept = tendance.coeffs
    fig,ax = plt.subplots()
    # Axe X : de part et d'autre des deux mesures pour voir la droite
    x_plot = np.linspace(min(V1_moy, V2_moy) - 20, max(V1_moy, V2_moy) + 20, 100)
    ax.plot(x_plot, tendance(x_plot),label=f"y = {slope:.2f}·V + {intercept:.2f} | R²={r_squared:.4f}")

    # Points étalons : x = tension mesurée, y = potentiel théorique
    ax.scatter([V1_moy, V2_moy], [E1, E2], color='red', zorder=5, label='Étalons')

    ax.set_xlabel('Tension mesurée V (mV)')
    ax.set_ylabel('Potentiel théorique E (mV)')
    ax.set_title('Courbe de calibration à 2 étalons')
    ax.legend()
    ax.grid()
    plt.show()
    return fig


if __name__ == '__main__':
    portIN,s = mes.connexion_port()
    C0,V1_moy, V2_moy, tendance,r_squared,E1,E2 = calibration_2_etalons(s)
    graphe_cal2(V1_moy, V2_moy, tendance, r_squared,E1,E2)


