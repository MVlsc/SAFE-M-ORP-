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
        if 'Périphérique série' in p or 'série USB' in p or 'Arduino' in p:
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


def graphe_live(C0,s):
    """ _summary_
    Acquiert et affiche en temps d'acquisition la tension et la température via le port série,
    jusqu'à ce que l'utilisateur appuie sur 'q'. Utilise deux sous-graphiques superposés
    (tension en haut, température en bas) mis à jour dynamiquement à chaque nouvelle mesure.
    Ferme la fenêtre graphique automatiquement à l'arrêt.

    Returns:
        [list[float], list[float]]:
            - T : liste des températures acquises pendant la session (en °C).
            - V : liste des tensions acquises pendant la session (en mV).
    """
    T = []
    V = []
    t = 0

    plt.ion() 
    fig, (ax1 , ax2)  = plt.subplots(2,1)

    print("Mesure en cours... Appuie sur Q pour arrêter")
    while True : 
        if keyboard.is_pressed('q'):
            plt.close(fig)
            break 
        s.flushInput()
        time.sleep(0.1)
        try:
            line = s.readline().decode()
            a = line.strip("\r\n").split(",")
            v_cal = (2 - float(a[0])) * 1000 + C0
            T.append(float(a[1]))
            V.append(v_cal)
            t = t + 0.1

            ax1.clear() #ax.clear() efface tt ce qu'il y a dans le graphe 
            ax1.plot(V, color='blue')
            ax1.set_xlabel("Temps d'acquisition (u.a)")
            ax1.set_ylabel("Tension calibré (mV)")

            ax2.clear() #ax.clear() efface tt ce qu'il y a dans le graphe 
            ax2.plot(T, color='blue')
            ax2.set_xlabel("Temps d'acquisition (u.a)")
            ax2.set_ylabel("Température(T)")
            plt.pause(0.2)
            
        except:
            print("problème de lecture de données")

    return T, V,fig


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
    chemin = BASE/"Data"/'data_figures'/nom_fichier      
    figure.savefig(chemin,bbox_inches='tight')
    return 'Le fichier png a bien été enregistré.'

connexion_port(br= 115200 , portIN ='')