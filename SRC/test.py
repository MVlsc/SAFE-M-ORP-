from Mesure import *
import Mesure as mes
import numpy as np
import datetime
import locale
import calibration as cal
import keyboard
from pathlib import Path
import serial
from scipy import  stats

portIN, s = mes.connexion_port(br=115200, portIN='')

def calibration_2_etalons(s, E1=None, E2=None,V1=None, V2=None) :
    while True :
        if E1 is None and V1 is None:
            E1 = float(input('Potentiel de la solution étalon 1 (mV) : '))
            print('Placer votre sonde dans la solution étalon 1, /!\ vous avez 30 sec')
            time.sleep(30)
            print('Début des mesures...')
            T, V1 = mes.data(s, N=100)
        if E2 is None and V2 is None:
            E2 = float(input('Potentiel de la solution étalon 2 (mV) : '))
            print('Nettoyer et sécher votre sonde, puis la placer dans la solution étalon 2','/!\ vous avez 1 min')
            time.sleep(60)
            print('Début des mesures...')
            T, V2 = mes.data(s, N=100)

        V1_moy = np.mean(V1)
        V2_moy = np.mean(V2)
        
        tendance = slope, intercept, r_value, p_value, std_err = stats.linregress([V1_moy,V2_moy],[E1,E2])
        r_squared = (r_value)**2
        print(slope)
        C0 = intercept 
        tendance = np.poly1d([slope, intercept])
        if r_squared <= 0.9 :
            print(f"R^2 ={r_squared},la courbe d'étalonnage n'est pas très précise, il est préférable de recommencer")
            break
        else : 
            print(f"R^2 = {r_squared}, la coure d'étalonnage est précise, on peut l'utiliser pour calibrer la sonde.")
        print(f"L'offset moyen est de C0 = {C0:.2f} mV")
        print(f"l'équation de la droite est y= {slope:.2f}*x + {intercept}")
        return C0,V1_moy, V2_moy, tendance,r_squared

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

