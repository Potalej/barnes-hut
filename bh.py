from node import Node
from copy import deepcopy

def adiciona (corpo, node):
# Barnes-Hut: Criacao do quad-tree. Essa funcao adiciona um novo
# corpo em um quad-tree, e retorna a versao atualizada do node.
  # 1. Se o node n nao tem nenhum corpo, coloca o corpo b nele
  novo_node = corpo if node is None else None
  # Para limitar a recursao, delimita o tamanho do quadrante
  menor_quadrante = 1.e-4
  if node is not None and node.s > menor_quadrante:
    # 3. Se o node n eh um node externo, o novo corpo b conflita com um corpo
    #    ja presente nessa regiao.
    if node.child is None:
      novo_node = deepcopy(node)
      # Subdivide de novo a regiao criando quatro filhos
      novo_node.child = [None for i in range(4)]
      # Para comecar, insere o corpo ja presente recursivamente no quadrante
      # apropriado
      quadrante = node.no_proximo_quadrante()
      novo_node.child[quadrante] = node
    # 2. Se o node n eh um node interno, nao modificamos
    else:
      novo_node = node
    
    # 2. e 3. Se o node n eh ou virou um node interno, atualiza sua massa e sua
    # posicao relativa (centro de massas vezes massa)
    novo_node.m += corpo.m
    novo_node.m_pos += corpo.m_pos

    # E recursivamente adiciona o novo corpo no quadrante apropriado
    quadrante = corpo.no_proximo_quadrante()
    novo_node.child[quadrante] = adiciona(corpo, novo_node.child[quadrante])

  return novo_node

def forca_em (corpo, node, theta:float)->float:
# Essa funcao computa a forca em um corpo exercida pelos corpos em um `node`.
  # 1. Se o node atual eh externo, calcula a forca exercida pelo node no corpo
  if node.child is None:
    return node.forca_em(corpo)
  
  # 2. Caso contrario, calcula a razao s/d. Se s/d < theta, trata como node
  #    interno e calcula a forca diretamente sobre b.
  if node.s < node.dist(corpo) * theta:
    return node.forca_em(corpo)
  
  # 3. Caso contrario, calcula recursivmente via forca bruta em cada corpo
  return sum(forca_em(corpo, c, theta) for c in node.child if c is not None)