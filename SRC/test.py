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

def calibration_2_etalons(s, E1=None, E2=None):
    if E1 is None:
        E1 = float(input('Potentiel de la solution étalon 1 (mV) : '))
    if E2 is None:
        E2 = float(input('Potentiel de la solution étalon 2 (mV) : '))

    print('Placer votre sonde dans la solution étalon 1, /!\ vous avez 30 sec')
    time.sleep(30)
    print('Début des mesures...')
    T, V1 = mes.data(s, N=100)
    print('Nettoyer et sécher votre sonde, puis la placer dans la solution étalon 2','/!\ vous avez 1 min')
    time.sleep(60)
    print('Début des mesures...')
    T, V2 = mes.data(s, N=100)

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
    print(f"l'équation de la droite est y= {slope:.2f}*x + {intercept}")
    return C0,V1_moy, V2_moy, tendance,r_squared

def graphe_cal2 (x,y,tendance,r_squared,E1,E2) : 
    C0, V1_moy, V2_moy, tendance, r_squared = calibration_2_etalons(s)
    slope, intercept = tendance.coeffs

    x_plot = [V1_moy, V2_moy]
    plt.plot(x_plot, tendance(x_plot), label=f"y = {slope:.2f}·V + {intercept:.2f} | R²={r_squared:.3f}")
    plt.plot(x_plot, [E1, E2], 'o', color='red', label='étalons')
    plt.xlabel("Potentiel mesuré (mV)")
    plt.ylabel("Potentiel réel (mV)")
    plt.legend()
    plt.show()