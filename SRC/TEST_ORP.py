import numpy as np
import Mesure as mes 
import matplotlib.pyplot as plt 
import datetime
import locale
import calibration as cal
from pathlib import Path

#Résultat des sondes ORP sur plus de 100 mesures: 
# E = eau déminéralisé : 
mesureE1 = [183.63,192.38,187.81,239.8,245.14,197.5,310]
mesureE2 = [180,157.11,199.7,232.55,163.6,165,302.7]
sigmaE1 = [8.6,7.22,4.5,5.4,5.9,4.33,5.65]
sigmaE2 = [4.12,5.16,4.56,8.17,6.2,3.8,5.8]

# C = solution calibré (240mV) :
mesureC1= [229.9,229.67,230.0,228.26,228.11,228.86,220.4]
mesureC2 = [229,230.19,230.0,226.66,227.15,229.3,220.79]
sigmaC1 = [2.5,4.25,4.57,4.61,4.92,5.2,4.69]
sigmaC2 = [4.37,4.4,1.89,6.29,5.48,4.42,5]

# D = solution calibré (470 mV):
mesureD1 = [425,436.69,450.84,449.65,449.69,454.58,423.68,439.19,440]
mesureD2 =[394.3 ,427.8,447.4,440,443,444,442, 433,437  ]
sigmaD1 = [7,5.74,6.15,3.21,2.64,6.08,2.17 , 4.52,4.52]
sigmaD2 =[5.5,4.8,4.85,3.44,6.7,6.52, 5.3, 6.76   ,5.77]

# Eb = eau déminéralisée tester avec D
mesureEb1= [159.5 ,185.8,236.8,266.17,238.27,184.1,233 , 429.5  ,246.9]
mesureEb2= [360.42, 370.36,375.9,385.4,414.1,391.7, 359.21 , 466  ,384.4]
sigmaEb1 = [13.05 ,13.55,5.96,5.4,4.27,5.9,7.31   ,5.58    ,5.61  ]
sigmaEb2 =[15,8.6,4,6.81,5.57,5.4,3.08  ,5.5 ,5.84]


moyEb = np.mean(mesureEb1 + mesureEb2)
moyD= np.mean(mesureD1 + mesureD2)
#A VOIR AVEC PROF 
sigmaEb = np.mean(sigmaEb1 + sigmaEb2)   # écart-type moyen d'une mesure
sigmaD = np.mean(sigmaD1 + sigmaD2)
# Valeurs mesurées par chaque sonde (en mV)
sondes = ['Sonde 1','Sonde 2','Sonde 3','Sonde 4','Sonde 5','Sonde 6','Sonde 7','Sonde 8','Sonde 9']

#position des barres sur l'axe des x, w = largeur des barres
x = np.arange(len(sondes))
print(x)
w = 0.35
fig, axes = plt.subplots(1,2, figsize=(14, 6))
#edgecolor = contour des bar, linewidth = épaisseur des barres d'erreur, capsize = longueur des "chapeaux" aux extrémités des barres d'erreur
kw = dict(edgecolor='black', linewidth=0.5, capsize=5)

# axes = [graphique_gauche (eau déminéralisée), graphique_droite (solution calibrée)]
#          axes[0]            axes[1]

#yerr = sigmaE1 et sigmaE2 pour les barres d'erreur 
# x -w/2 et x + w/2 pour positionner les barres de mesure 1 et mesure 2 côte à côte pour chaque sonde
axes[0].bar(x - w/2, mesureEb1, w, yerr=sigmaEb1, label='Mesure 1', color='steelblue',      **kw)
axes[0].bar(x + w/2, mesureEb2, w, yerr=sigmaEb2, label='Mesure 2', color='cornflowerblue', **kw)
axes[0].set(title="Eau déminéralisée", xlabel="Sondes", ylabel="Potentiel (mV)")
axes[0].axhline(moyEb,color='gray', linestyle='--', label=f'Moyenne: {moyEb:.2f} mV')
axes[0].axhspan(moyEb - sigmaEb, moyEb + sigmaEb, color='pink', alpha=0.15)

#axhspan = zone colorée entre moyE - sigmaE et moyE + sigmaE pour visualiser l'écart type sur une ligne 

axes[1].bar(x - w/2, mesureD1, w, yerr=sigmaD1, label='Mesure 1', color='tomato',  **kw)
axes[1].bar(x + w/2, mesureD2, w, yerr=sigmaD2, label='Mesure 2', color='salmon',  **kw)
axes[1].set(title="Solution calibrée (470 mV)", xlabel="Sondes", ylabel="Potentiel (mV)")
axes[1].axhline(moyD,color='gray', linestyle='--', label=f'Moyenne: {moyD:.2f} mV')
axes[1].axhspan(moyD - sigmaD, moyD + sigmaD, color='pink', alpha=0.15)
for ax in axes:
    ax.set_xticks(x)
    ax.set_xticklabels(sondes, rotation=15)
    ax.legend()

plt.suptitle("Comparaison des mesures ORP par sonde", fontsize=13)
plt.show()


