import pygame

pygame.init()

from personagens import *

from menu import *


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
counterH = 0
counterA = 0
executando = menu(personagens, inimigos, janela, clock)
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                counterH = 1
            elif evento.key == pygame.K_s:
                counterA = 1

    if(counterH > 0):           
        for personagem in personagens:
            counterH = personagem.animacao_habilidade(counterH)

    if(counterA > 0):           
        for personagem in personagens:
            counterA = personagem.animacao_ataque(counterA)

    # Preencher a janela com a cor de fundo
    janela.fill(cor_fundo)

    # Atualizar o jogador
    for inimigo in inimigos:
        inimigo.desenhar(janela)
        
    for personagem in personagens:
        personagem.desenhar(janela)

    # Atualizar a exibição
    pygame.display.flip()

    # Definir a taxa de quadros
    clock.tick(60)

# Encerrar o jogo
pygame.quit()