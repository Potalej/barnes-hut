from integrador import integracao_continua
from animacaopygame import Animacao
from numpy import random, array, arange, sqrt, cos, sin, pi
from numpy.linalg import norm
from node import Node
from energia import energia


# Criterio theta do Barnes-Hut
theta = 0.5
# Raio do disco onde os corpos sao distribuidos inicialmente
raio_inicial = 500
# Velocidade maxima inicial dos corpos
inivel = 0.1
# Constante gravitacional
G = 4.e-3
# Tamanho do passo
h = 1.e-1
# Numero de corpos
N = 1000
# Numero de passos 
max_iter = 100000

# Define a seed do gerador de numeros pseudo-aleatorios, assim eh
# possivel gerar um mesmo padrao (dado um N) para fazer testes
random.seed(1)

# Gera pontos dentro de um quadradao
posx = random.random(N) * 2. * raio_inicial + 0.5 - raio_inicial
posy = random.random(N) * 2. * raio_inicial + 0.5 - raio_inicial
posz = random.random(N) * 2. * raio_inicial + 0.5 - raio_inicial

min_massa = 200
max_massa = 500

# Se quiser filtrar, mantem apenas os corpos que estao dentro do circulo
corpos = [ 
  Node(random.random() * max_massa + min_massa, px, py, pz) for (px,py,pz) in zip(posx,posy,posz) 
  # if (px-0.5)**2 + (py-0.5)**2 < raio_inicial**2 
]

posicoes, momentos = [], []

# Adiciona momentum nos corpos
for corpo in corpos:
  r = corpo.pos() - array([0.5, 0.5, corpo.pos()[2]])
  corpo.momentum = array([-r[1], r[0], 0.])*1000/corpo.m

  posicoes.append(corpo.pos())
  momentos.append(corpo.momentum)

# Calculo da energia
E, pot = energia(G, posicoes, momentos, anular=True)
posicoes, momentos = [], []
for corpo in corpos:
  # corpo.m_pos = corpo.m_pos * pot/(E + pot)
  corpo.momentum = corpo.momentum * (pot/(E+pot))**0.5
  posicoes.append(corpo.pos())
  momentos.append(corpo.momentum)

print('Energia: ', energia(G, posicoes, momentos))

def func ():
  return integracao_continua(corpos, max_iter, theta, G, h)

Animacao().animar([corpo.m for corpo in corpos], func)