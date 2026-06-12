import serial 
import time 
import matplotlib.pyplot as plt
import keyboard
import datetime
import numpy as np 
import serial
import serial.tools.list_ports
from pathlib import Path

def connexion_port(br=115200, portIN=''):
    # Si port fourni manuellement
    if portIN:
        try:
            s = serial.Serial(port=portIN, baudrate=br, timeout=5)
            print(f'Connexion établie avec {portIN}')
            return portIN, s
        except serial.SerialException as e:
            print(f"Erreur: impossible d'ouvrir {portIN}")
            return '', 'error'

    # Détection automatique
    ports = list(serial.tools.list_ports.comports())
    
    for port in ports:
        p = str(port)
        # Windows
        if 'Arduino' in p or'Périphérique série' in p or 'série USB' in p :
            portIN = port.device
            break
        # Linux
        if 'ttyACM' in port.device or 'ttyUSB' in port.device:
            portIN = port.device
            break

    if not portIN:
        print("/!\\ Aucun port Arduino détecté")
        return '', 'error'

    try:
        s = serial.Serial(port=portIN, baudrate=br, timeout=5)
        print(f'Connexion réussie sur {portIN}')
        return portIN, s
    except serial.SerialException as e:
        print(f"Erreur: impossible d'ouvrir {portIN} : {e}")
        return '', 'error'
    
def data(s,N=None): 
    """_summary_
    Acquiert un nombre fixe de mesures depuis le port série.
    Demande à l'utilisateur le nombre de mesures souhaitées, puis lit ce nombre
    de lignes sur le port série. Chaque ligne est décodée et séparée en tension
    (indice 0) et température (indice 1).

    Returns:
        tuple[list[float], list[float]]:
            - T : liste des températures mesurées (en °C).
            - V : liste des tensions mesurées (en V).
    """
    T=[]
    V=[]
    if N is None :
        N= int(input('Combien mesure veux-tu faire'))
    for k in range(N) :
        s.flushInput()
        time.sleep(0.08)
        try:
            line = s.readline().decode()
            a = line.strip("\r\n").split(",")
            T.append(float(a[1])) #1 a [1]valeurs de la liste et a[0]
            V.append(float(a[0]))
        except:
            print("problème de lecture de données")
    return T,V

# T,V = data()


def Graphe_T_V(x,y):
    """_summary_
    Affiche deux graphiques en nuage de points des tensions mesurées (corrigées en mV) et de températures(°C)
    Crée une nouvelle fenêtre matplotlib intitulée 'Graphique Voltage et Température et trace
    chaque valeur de y en fonction de son indice (axe temporel implicite).

    Args:
        x (list[float]): Liste des températures mesurées à afficher (en °C).
        y (list[float]): Liste des tensions corrigées à afficher (en V ou mV selon calibration).
    """
    fig, (ax1 , ax2)  = plt.subplots(1,2)
    ax1.plot(y,'o', color='red')
    ax1.set_xlabel("Nombre de mesure")
    ax1.set_ylabel("Tension calibré (mV)")

    ax2.plot(x,'o', color='blue')
    ax2.set_xlabel("Nombre de mesure")
    ax2.set_ylabel("Température (°C)")
    plt.show()
    return fig 




import threading

import matplotlib.pyplot as plt
import time

def graphe_live(C0, s):
    T = []
    V = []
    stop = False

    def on_key(event):
        nonlocal stop
        if event.key == 'q':
            stop = True

    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.canvas.mpl_connect('key_press_event', on_key)

    print("Mesure en cours... Appuie sur 'q' dans la fenêtre du graphe pour arrêter.")

    while not stop:
        s.flushInput()
        time.sleep(0.5)  # ~ 2 mesures / seconde

        try:
            line = s.readline().decode()
            a = line.strip("\r\n").split(",")

            v_cal = (2 - float(a[0])) * 1000 + C0
            print(v_cal)

            T.append(float(a[1]))
            if 10 < v_cal < 700:
                V.append(v_cal)

            ax1.clear()
            ax1.plot(V, color='blue')
            ax1.set_title("Tension")
            ax1.set_xlabel("Temps d'acquisition (u.a.)")
            ax1.set_ylabel("Tension calibrée (mV)")

            ax2.clear()
            ax2.plot(T, color='red')
            ax2.set_title("Température")
            ax2.set_xlabel("Temps d'acquisition (u.a.)")
            ax2.set_ylabel("Température (°C)")

            plt.tight_layout()
            plt.pause(0.01)

        except Exception as e:
            print(f"Problème de lecture des données : {e}")

    plt.ioff()   # ← stop le mode interactif
    plt.close(fig)

    return T, V, fig

def informations_1er_ordre (T,V,a) :
    """_summary_
    Calcule et affiche les statistiques de base d'une session de mesures : moyenne et écart-type
    des tensions calibrées et des températures mesurées. Affiche les résultats dans la console.

    Args:
        T (list[float]): Liste des températures mesurées (en °C).
        V (list[float]): Liste des tensions calibrées (en mV).
    """
    moy_V = np.mean(V[int(a):])
    sigma = np.std(V[int(a):])
    moy_T = np.mean(T[int(a):])
    print(f"moyenne Potentiel(mV) = {moy_V}")
    print(f'écart type (écart-type) = {sigma}')
    print(f'moyenne Température (°C)={moy_T}')
    return moy_T , moy_V, sigma 



def data_live(s): 
    """_summary_
    Acquiert des données en continu depuis le port série jusqu'à ce que l'utilisateur
    appuie sur la touche 'q'. À chaque itération, lit une ligne du port série, la décode
    et en extrait la température (indice 1) et la tension (indice 0) séparées par une virgule.
    Affiche chaque mesure en temps d'acquisition dans la console.

    Returns:
        [list[float], list[float]]: 
            - T : liste des températures mesurées (en °C).
            - V : liste des tensions mesurées (en V).
    """
    T=[]
    V=[]
    plt.ion()   #plt.subplots() crée la fenêtre graphique et retourne deux objets : ax = axe, labels... et fig = fênetre entière
    fig, ax = plt.subplots()
    print('En cours... appuyez sur q pour arreter')
    while not keyboard.is_pressed ('q') :
        s.flushInput()
        time.sleep(0.1)
        try:
            line = s.readline().decode()
            a = line.strip("\r\n").split(",")
            T.append(float(a[1])) #1 a [1]valeurs de la liste et a[0]
            V.append(float(a[0]))
            print(f"{float(a[1]):.2f},{float(a[0]):.2f}") 
        except:
            print("problème de lecture de données")
    return T,V,fig

def enregistrement_csv (T,V_real,moy = None,sigma=None) :
    BASE = Path(__file__).parent.parent
    now = datetime.datetime.now()
    nom_fichier = now.strftime("Mesure Température et Voltage %d %B, %Hh%M.csv")
    chemin = BASE/"Data"/'données (T,V)'/nom_fichier      
    n = min(len(T), len(V_real))
    if moy is None:
        moy = np.mean(V_real[:n])
    if sigma is None:
        sigma = np.std(V_real[:n])
    resultat = np.column_stack((T[:n], V_real[:n]))
    with open(chemin, 'w') as f:
        np.savetxt(f,resultat, delimiter=',', fmt='%.2f',header=f'Donnees Temperature / Potentiel(calibré),pour V :  écart type ={sigma} et moyenne = {moy}')
    return 'Le fichier csv a bien été enregistré.'

def enregistrement_png (figure) :
    BASE = Path(__file__).parent.parent
    now = datetime.datetime.now()
    nom_fichier = now.strftime("Graphique Température et Potentiel %d %B, %Hh%M.png")
    chemin = BASE/"Data"/'data_figures'/'data_figures_mesures'/nom_fichier      
    figure.savefig(chemin,bbox_inches='tight')
    return 'Le fichier png a bien été enregistré.'

# portIN,s = connexion_port(br= 115200 , portIN ='')
# C0 = 0
# graphe_live(C0,s)