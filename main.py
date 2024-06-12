import pygame

pygame.init()

from personagens import *

from menu import *

from batalha import *

largura = 1024 
altura = 768
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("The Ex Tour")

cor_fundo = (0, 0, 0)        # Preto
cor_jogador = (255, 255, 255)  # Branco

personagens = pygame.sprite.Group()
inimigos = pygame.sprite.Group()

# Loop do jogo
clock = pygame.time.Clock()
executando = menu(personagens, inimigos, janela, clock)
if executando == True: batalha(personagens, inimigos, janela, clock)

# Encerrar o jogo
pygame.quit()