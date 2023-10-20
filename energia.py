from numpy.linalg import norm

def energia (G, posicoes, momentos, anular=False):
  pot = 0
  ec = 0
  for a in range(len(posicoes)): # N
    ra, pa = posicoes[a], momentos[a]
    ec += 0.5 * norm(pa)**2

    for b in range(a):
      rb = posicoes[b]
      pot += G / norm(rb - ra)
  
  print('Ec:', ec, ' / Ep:', pot)

  if not anular:
    return ec - pot
  else:
    return ec - pot, pot