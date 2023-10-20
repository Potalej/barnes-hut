from bh import adiciona, forca_em
from copy import deepcopy
from numpy import array, arange
from numpy.linalg import norm
from numpy import random

def verlet (corpos:list, raiz, theta:float, G:float, h:float)->None:
# Faz a integracao de um passo usando o metodo de Verlet
  for corpo in corpos:
    forca = G * forca_em(corpo, raiz, theta)
    corpo.momentum += h * forca
    corpo.m_pos += h * corpo.momentum  

def integracao (corpos, max_iter:int, theta:float=0.5, G:float=1.0, h:float=1.e-3):
  posicoes = []
  
  for _ in range(max_iter):
    # A quad-tree eh recalculada em cada passo
    raiz = None

    for corpo in corpos:
      corpo.reseta_para_quadrante_zero()
      raiz = adiciona(corpo, raiz)
    
    # Passo de integracao
    verlet(corpos, raiz, theta, G, h)

    # Salva
    posicoes.append([corpo.pos() for corpo in corpos])

    if _ % 1000 == 0: print('Passo:', i)
  
  return posicoes

def integracao_continua (corpos, max_iter:int, theta:float=0.5, G:float=1.0, h:float=1.e-3):
  for _ in range(max_iter):
    for __ in range(1):
      # A quad-tree eh recalculada em cada passo
      raiz = None

      for corpo in corpos:
        corpo.reseta_para_quadrante_zero()
        raiz = adiciona(corpo, raiz)
      
      # Passo de integracao
      verlet(corpos, raiz, theta, G, h)

    # Retorna
    yield [corpo.pos() for corpo in corpos]