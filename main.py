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

defeat_image = pygame.image.load("./imagens/defeat.jpg")
defeat_image = pygame.transform.scale(defeat_image, (1024, 768))

lose_image = pygame.image.load("./imagens/lose.png")
rect = pygame.Rect(((largura / 2) - (lose_image.get_width() / 2) - 25, (altura / 2) - (lose_image.get_height() / 2) - 25), (lose_image.get_width() + 50 ,lose_image.get_height() + 50))



# Loop do jogo
clock = pygame.time.Clock()
executando = menu(personagens, inimigos, janela, clock)
if executando == True: 
    vitoria = batalha(personagens, inimigos, janela, clock)
    if not vitoria:
        while executando:

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False     
            janela.blit(defeat_image, (0, 0))

            pygame.draw.rect(janela, cor_jogador, rect)
            janela.blit(lose_image, ((largura / 2) - (lose_image.get_width() / 2), (altura / 2) - (lose_image.get_height() / 2)))

            pygame.display.flip()
            clock.tick(60)

# Encerrar o jogo
pygame.quit()