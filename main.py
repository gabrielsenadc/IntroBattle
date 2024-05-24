import pygame

pygame.init()


largura = 1024 
altura = 768
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("The Ex Tour")


cor_fundo = (0, 0, 0)        # Preto
cor_jogador = (255, 255, 255)  # Branco


from personagens import *

from menu import *

seta = Seta(posicoes)

personagens = pygame.sprite.Group()

# Loop do jogo
executando = True
clock = pygame.time.Clock()
flag = 0
ruivo = 0
n = 0
counterH = 0
counterA = 0
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        flag = verifica_ruivo(evento, flag)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                seta.atualiza("l", ruivo, posicoes)
            elif evento.key == pygame.K_RIGHT:
                seta.atualiza("r", ruivo, posicoes)
            elif evento.key == pygame.K_DOWN:
                seta.atualiza("d", ruivo, posicoes)
            elif evento.key == pygame.K_UP:
                seta.atualiza("u", ruivo, posicoes)
            elif evento.key == 122:
                n += 1
                seleciona_personagem(n, seta, personagens)
            elif evento.key == pygame.K_a:
                counterH = 1
            elif evento.key == pygame.K_s:
                counterA = 1

    if(counterH > 0):           
        for personagem in personagens:
            counterH = personagem.animacao_habilidade(counterH)

    if(counterA > 0):           
        for personagem in personagens:
            counterA = personagem.animacao_ataque(counterA)

    if(flag == 5): 
        cria_EdSheeran(selecoes, posicoes)
        ruivo = 1
        seta.atualiza_ruivo(posicoes)

    # Preencher a janela com a cor de fundo
    janela.fill(cor_fundo)

    # Atualizar o jogador
    if(n < 3):
        for selecao in selecoes:
            selecao.desenha(janela)
        seta.desenha(janela)
    
    if(n >= 3):
        for personagem in personagens:
            personagem.desenhar(janela)

    # Atualizar a exibição
    pygame.display.flip()

    # Definir a taxa de quadros
    clock.tick(60)

# Encerrar o jogo
pygame.quit()