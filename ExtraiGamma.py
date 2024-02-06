
# -*- coding: utf-8 -*-
"""
3. Encontra valores de Gamma
Método 2, ajusta gamma foto com referencia. 
Ver se referencia esta correta

Created on Wed Apr  11 13:20:11 2020
Atualizado em 12-09-23 Raquel Pantojo

se tiver erro no aruco:
pip install opencv-contrib-python==4.7.0.68 opencv-python==4.7.0.68
pip install opencv-contrib-python-headless
@author: takar
"""


import getColorchart2 as gc
from sklearn.linear_model import LinearRegression
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import csv



def exp_fit(x,a,b,c):
    return  a**(x+b) + c
    #return  a*x+b+c
    
def gamma_fit(x, a, b, c):
    result =(a * x) ** b + c
    return result

    
def inv_gamma_fit(x,a,b,c):
    result = ((x-c)/a)**(1/b)
    return result 
    #return  a*x+b+c



# Carregue a imagem
name_smp ='Natansol.jpeg'
img_smp = cv2.imread(name_smp)
color_smp = (gc.getColorChart(img_smp))/255.0



with open('referencia_RGB_Logitech_cinza.csv') as f:
    reader = csv.reader(f)
    lc = [row for row in reader]

color_ref = np.zeros((6, 3))
for i in range(6):
    for j in range(3):
        color_ref[i,3-j-1] = float(lc[i][j])/255.0


# Valores iniciais para todos os canais
initial_guess = [0.1, 0.1, 0.1]

param_smp_R, c_r = curve_fit(gamma_fit, color_ref[0:6, 2], color_smp[0:6, 2])
param_smp_G, c_g = curve_fit(gamma_fit, color_ref[0:6, 1], color_smp[0:6, 1])
param_smp_B, c_b = curve_fit(gamma_fit, color_ref[0:6, 0], color_smp[0:6, 0])


# calculo do gamma:

print("Canal R - Valor de gamma estimado:", param_smp_R[1])
print("Canal G - Valor de gamma estimado:", param_smp_G[1])
print("Canal B - Valor de gamma estimado:", param_smp_B[1])

# Pesos para cada canal (valores de luminância)
weight_B = 0.2126
weight_G = 0.7152
weight_R = 0.0722


# Cálculo da média ponderada de correção gamma
average_gamma = (weight_B *  param_smp_B[1] + weight_G *  param_smp_G[1] + weight_R *  param_smp_R[1]) / (weight_B + weight_G + weight_R)

print("Valor médio ponderado de correção gamma:", average_gamma)


fit_xR = color_ref[:, 2]
fit_yR = gamma_fit(color_ref[:, 2], param_smp_R[0], param_smp_R[1], param_smp_R[2])

fit_xG = color_ref[:, 1]
fit_yG = gamma_fit(color_ref[:, 1], param_smp_G[0], param_smp_G[1], param_smp_G[2])

fit_xB = color_ref[:, 0]
fit_yB = gamma_fit(color_ref[:, 0], param_smp_B[0], param_smp_B[1], param_smp_B[2])

# Calcula o R^2 para o canal R
y_true_R = color_smp[0:6, 2]  # Valores de referência para o canal R
r_squared_R = r2_score(y_true_R, fit_yR)

# Calcula o R^2 para o canal G
y_true_G = color_smp[0:6, 1]  # Valores de referência para o canal G
r_squared_G = r2_score(y_true_G, fit_yG)

# Calcula o R^2 para o canal B
y_true_B = color_smp[0:6, 0]  # Valores de referência para o canal B
r_squared_B = r2_score(y_true_B, fit_yB)


# Plota os pontos calculados e o R²
plt.figure(figsize=(12, 8))
plt.subplot(131)
plt.plot(fit_xR, fit_yR, color='r', label='Valores Ajustados', linewidth=2)
plt.scatter(color_ref[0:6, 2], color_smp[0:6, 2], label='Valores de Referência')
plt.legend()
plt.xlabel('Reference-Colorimeter')
plt.ylabel('Channel R image')
plt.title('CANAL R - Gamma: {:.3f}, R²: {:.3f}'.format(param_smp_R[1], r_squared_R))

plt.subplot(132)
#plt.scatter(fit_xG, fit_yG, color='g')
plt.plot(fit_xG, fit_yG, color='g', label='Valores Ajustados', linewidth=2)
plt.scatter(color_ref[0:6, 1], color_smp[0:6, 1], label='Valores de Referência')
plt.legend()
plt.xlabel('Reference-Colorimeter')
plt.ylabel('Channel G Image')
plt.title('CANAL G - Gamma: {:.3f}, R²: {:.3f}'.format(param_smp_G[1], r_squared_G))

plt.subplot(133)
plt.plot(fit_xB, fit_yB, color='b', label='Valores Ajustados', linewidth=2)
plt.scatter(color_ref[0:6, 0], color_smp[0:6,0], label='Valores de Referência')
plt.legend()
plt.xlabel('Reference-Colorimeter')
plt.ylabel('Channel B Image')
plt.title('CANAL B - Gamma: {:.3f}, R²: {:.3f}'.format(param_smp_B[1], r_squared_B))

plt.tight_layout()
plt.show()



# Criar DataFrames a partir dos valores de color_smp e color_ref
df_color_smp = pd.DataFrame(data=color_smp, columns=['Canal R', 'Canal G', 'Canal B'])
df_color_ref = pd.DataFrame(data=color_ref, columns=['Canal R', 'Canal G', 'Canal B'])

#Salva dados no arquivo do Excel
nome_arquivo_excel = 'Diferentesposições.xlsx'


# Criar um objeto ExcelWriter para gravar múltiplas planilhas no mesmo arquivo
with pd.ExcelWriter(nome_arquivo_excel) as writer:
    # Salvar color_smp na primeira planilha
    df_color_smp.to_excel(writer, sheet_name='Color_smp', index=False)
    
    # Salvar color_ref na segunda planilha
    df_color_ref.to_excel(writer, sheet_name='Color_ref', index=False)

print(f'Valores de color_ref e color_smp salvos em {nome_arquivo_excel}')
#"""