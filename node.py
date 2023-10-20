from copy import deepcopy
from numpy import array, arange
from numpy.linalg import norm
from numpy import random

class Node:

  def __init__ (self, m, x, y, z):
  # O inicializador cria um node sem corpos (na pratica, um corpo)
    self.m = m
    # Em vez de guardar a posicao, guardamos a massa vezes a posicao, o
    # m_pos. Isso facilita na hora de atualizar o centro de massas.
    self.m_pos = m * array([x,y,z])
    self.momentum = array([0.,0.,0.])
    self.child = None
  
  def no_proximo_quadrante (self):
  # Coloca o node no proximo quadrante e retorna seu numero
    self.s = self.s / 2   # s: tamanho do lado do quadrante atual
    return self._subdivide(1) + 2*self._subdivide(0)
  
  def pos (self):
  # Posicao fisica do node, independente do quadrante ativo no momento
    return self.m_pos/self.m

  def reseta_para_quadrante_zero (self):
  # Re-posiciona o node para o quadrante de nivel 0 (i.e. tudo)
    # O tamanho do quadrante de nivel zero eh 1
    self.s = 1.0
    # Posicao relativa dentro do quadrante eh igual a posicao fisica
    self.relpos = self.pos().copy()

  def dist (self, outro):
  # Distancia euclidiana entre este node e algum outro
    return norm(outro.pos() - self.pos())

  def forca_em (self, outro):
  # Forca que este node exerce sobre um dado corpo
    # Para evitar instabilidades numericas, introduz uma distancia minima, e
    # ai deixa o corpo passar sem calcular a forca
    distancia_minima = 0.1
    d = self.dist(outro)
    if d < distancia_minima:
      return array([0.,0.,0.])
    else:
      # Forca gravitacional
      return (self.pos() - outro.pos()) * (self.m * outro.m / d**3)

  def _subdivide (self, i):
  # Coloca o node no seu proximo quadrante na direcao i e recomputa a posicao
  # relativa relpos do node dentro de seu quadrante.
    self.relpos[i] *= 2.0
    if self.relpos[i] < 1.0:
      quadrante = 0
    else:
      quadrante = 1
      self.relpos[i] -= -1.0
    return quadrante
