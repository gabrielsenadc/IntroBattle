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
escolhas = Escolhas()
escolhas.define_titulo("Taylor Swift")
escolhas.selecao_habilidade()

# Loop do jogo
clock = pygame.time.Clock()
counterH = 0
counterA = 0
counterV = 0
executando = menu(personagens, inimigos, janela, clock)
escolhas.retita_opcoes()
escolhas.selecao_inimigos(inimigos)
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        if evento.type == pygame.KEYDOWN:
            escolhas.atualiza_seta(evento.key)
            if evento.key == pygame.K_a:
                for personagem in personagens:
                    animacao("habilidade", personagem, 0, 0, personagens, inimigos, clock, janela)
            elif evento.key == pygame.K_s:
                for personagem in personagens:
                    animacao("ataque", personagem, 750, 325, personagens, inimigos, clock, janela)
            elif evento.key == pygame.K_q:
                for inimigo in inimigos:
                    animacao("ataque", inimigo, 50, 325, personagens, inimigos, clock, janela)
                           

    # Preencher a janela com a cor de fundo
    janela.fill(cor_fundo)

    # Atualizar o jogador
    for inimigo in inimigos:
        inimigo.desenhar(janela)
        
    for personagem in personagens:
        personagem.desenhar(janela)

    escolhas.desenha(janela)

    # Atualizar a exibição
    pygame.display.flip()

    # Definir a taxa de quadros
    clock.tick(60)

# Encerrar o jogo
pygame.quit()