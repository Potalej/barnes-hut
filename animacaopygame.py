import pygame
from copy import deepcopy
from energia import energia
from math import log

class Animacao:

  LARGURA = 800
  ALTURA  = 800
  ESCALA  = 2
  DENSIDADE = 4

  def iniciarPyGame (self, titulo:str='Animacao'):
    self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
    self.superficie = pygame.Surface((self.LARGURA*self.ESCALA, self.ALTURA*self.ESCALA))
    pygame.display.set_caption(titulo)

  def desenhar (self, R:list):
  # Animacao de um passo
    for corpo in range(self.N):
      x = R[corpo][0] + self.ESCALA * self.LARGURA / 2
      y = R[corpo][1] + self.ESCALA * self.ALTURA / 2
      pygame.draw.circle(
        self.superficie,
        (255, 192, 203),
        (x,y),
        log(self.massas[corpo])/self.DENSIDADE
      )

  def animar (self, massas:list, geradora):
    self.iniciarPyGame('Animação')
    pygame.init()
    clock = pygame.time.Clock()

    self.massas = massas
    self.N = len(massas)

    # FPS
    texto_fps = pygame.font.SysFont("Verdana", 18)

    # Roda a funcao de integracao
    for frame in geradora():
      R = frame
      clock.tick(60)

      self.superficie.fill((0,0,0))

      for evento in pygame.event.get():
        if evento.type == pygame.QUIT: return
      
      self.desenhar(R)

      redimensionado = pygame.transform.smoothscale(self.superficie, self.tela.get_size())
      self.tela.blit(redimensionado, (0,0))

      fps = texto_fps.render(f"FPS: {round(clock.get_fps(), 2)}", True, (255,255,255))
      self.tela.blit(fps, (self.LARGURA-150,0))

      pygame.display.update()