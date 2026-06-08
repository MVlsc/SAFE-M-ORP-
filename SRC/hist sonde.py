import numpy as np
import Mesure as mes 
import matplotlib.pyplot as plt 
import datetime
import locale
import calibration as cal
from pathlib import Path

BASE = Path(__file__).parent.parent
#SONDE 9
#On alterne la mesure dans l'eau déminéraliser et Soluition calibré (270mV)

#calibré
data = np.loadtxt(BASE/"Data"/"données (T,V)"/"Mesure Température et Voltage 29 May, 17h33.csv",delimiter =',',skiprows=1)
#eau
data2 = np.loadtxt(BASE/"Data"/"données (T,V)"/"Mesure Température et Voltage 29 May, 17h40.csv",delimiter =',',skiprows=1)
#calibré
data3 = np.loadtxt(BASE/"Data"/"données (T,V)"/"Mesure Température et Voltage 29 May, 17h44.csv",delimiter =',',skiprows=1)
#eau
data4 = np.loadtxt(BASE/"Data"/"données (T,V)"/"Mesure Température et Voltage 29 May, 17h47.csv",delimiter =',',skiprows=1)



V = data[:,1]
moy = np.mean(V)
sigma = np.std(V)

print(f"moyenne = {moy}")
print(f'écart type = {sigma}')


# sondes = [7,8,9]
# plt.xlim = ([0,5])
# plt.scatter(sondes[0],Moy_eau,color = 'red',label = "Solution d'eau déminéraliser")
# plt.scatter(sondes[0],Moy_cal,color = "green",label= 'Solution calibré (240mV)')
# plt.xlabel('numéro de la sonde')
# plt.ylabel('Potentiel moyen (mV )')
plt.show()

