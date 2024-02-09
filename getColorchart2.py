# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 20:41:08 2020
@author: takar and rpsb
Atualizado em 12-09-23 Raquel Pantojo
"""

import cv2
from cv2 import aruco
import numpy as np

def getColorChart(img):
    
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    
    
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, dictionary)
    # Verificar se há marcadores detectados
     # Verificar se há marcadores detectados
    if ids is not None:
        for i in range(len(ids)):
            # Desenhar retângulos ao redor dos marcadores detectados
            aruco.drawDetectedMarkers(img, corners)
        # Obter as coordenadas do centro do marcador
            cX = int(corners[i][0][:, 0].mean())
            cY = int(corners[i][0][:, 1].mean())
                
                # Escrever o ID do marcador na imagem
            cv2.putText(img, str(ids[i][0]), (cX - 10, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    
# Resto do código...
    img_c = np.copy(img)
    
    mark1 = corners[ids[1,0]-5][0]
    mark2 = corners[ids[0,0]-5][0]
    
    #mark1 = corners[ids[1,0]-3][0]
    #mark2 = corners[ids[0,0]-3][0]
    
    vec1_1 = mark1[1] - mark1[2]
    vec1_2 = mark1[0] - mark1[1]
    
    vec2_1 = mark2[1] - mark2[2]
    vec2_2 = mark2[0] - mark2[1]
    
    checker = [mark2[1]+vec2_1*0.2+vec2_2*5, mark1[3]-vec1_1*0.2, mark1[3]-vec1_1*0.2-vec1_2*5, mark2[1]+vec2_1*0.2]

    checker_w = 720
    checker_h = 600
    perspective1 = np.float32(checker)
    perspective2 = np.float32([[0, 0],[checker_w, 0],[checker_w, checker_h],[0, checker_h]])
    
    psp_matrix = cv2.getPerspectiveTransform(perspective1,perspective2)
    img_psp = cv2.warpPerspective(img_c, psp_matrix,(checker_w, checker_h))
    
    psize = checker_w/6
    color_array = np.zeros((30,3))
    checker_paths = [
        [checker[0], checker[3], checker[2], checker[1], checker[0]]
    ]
    for i in range(5):
        for j in range(6):
            patch = img_psp[int(psize*i+psize/3):int(psize*i+psize*2/3), int(psize*j+psize/3):int(psize*j+psize*2/3)]
            # Desenhar um retângulo ao redor do patch
            cv2.rectangle(img_psp, (int(psize * j + psize / 3), int(psize * i + psize / 3)), (int(psize * j + psize * 2 / 3), int(psize * i + psize * 2 / 3)), (0, 0, 255), 4)
            # Adicionar número ao patch
            patch_number = i * 6 + j + 1  # Calcula o número do patch
            cv2.putText(img_psp, str(patch_number), (int(psize * j + psize / 3) + 10, int(psize * i + psize / 3) + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
            color_array[i*6+j] = np.mean(patch, axis=(0, 1))
            
    
    
    return  color_array
