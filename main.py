import pygame

pygame.init()


largura = 1024 
altura = 768
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pega Pega")


cor_fundo = (0, 0, 0)        # Preto
cor_jogador = (255, 255, 255)  # Branco

altura_quadrado = 200
largura_quadrado = 200
class Quadrado(pygame.sprite.Sprite):
    def __init__(self, x, y, nome):
        super().__init__()
        self.tamanho = (largura_quadrado, altura_quadrado)
        self.rect = pygame.Rect((x, y), self.tamanho)
        self.nome = nome
        self.image = pygame.image.load(f"./imagens/{nome}.png" )

        y = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, 200/y)

    def desenhar_quadrado(self, tela):
        pygame.draw.rect(tela, cor_jogador, self.rect)
        fonte = pygame.font.Font(None, 20)
        texto = fonte.render(self.nome, True, cor_fundo)
        janela.blit(self.image, self.rect)


    def atualizar(self, x, y):
        self.rect.x = x
        self.rect.y = y

# Criar o sprite do jogador
quadrados = pygame.sprite.Group()
quadrado1 = Quadrado((largura / 2) - 350, 150, "Travis Kelce")
quadrado2 = Quadrado((largura / 2) - 100, 150, "Taylor Swift")
quadrado3 = Quadrado((largura / 2) + 150, 150, "Taylor Launter")
quadrado4 = Quadrado((largura / 2) - 225, 400, "Harry Styles")
quadrado5 = Quadrado((largura / 2) + 25, 400, "Tom Hiddleston")

quadrados.add(quadrado1)
quadrados.add(quadrado2)
quadrados.add(quadrado3)
quadrados.add(quadrado4)
quadrados.add(quadrado5)

def verificaRuivo(evento, flag):
    if evento.type == pygame.KEYDOWN:
        if evento.key == 114:
            flag = 1
        elif (evento.key == 117 and flag == 1):
            flag = 2
        elif (evento.key == 105 and flag == 2):
            flag = 3
        elif (evento.key == 118 and flag == 3):
            flag = 4
        elif (evento.key == 111 and flag == 4):
            quadrado6 = Quadrado((largura / 2) + 150, 400, "Ed Sheeran")
            quadrados.add(quadrado6)
            quadrado4.atualizar((largura / 2) - 350, 400)
            quadrado5.atualizar((largura / 2) - 100, 400)
        else:
            flag = 0

    return flag


# Loop do jogo
executando = True
clock = pygame.time.Clock()
flag = 0
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        flag = verificaRuivo(evento, flag)

    # Preencher a janela com a cor de fundo
    janela.fill(cor_fundo)

    # Atualizar o jogador
    for quadrado in quadrados:
        quadrado.desenhar_quadrado(janela)


    # Atualizar a exibição
    pygame.display.flip()

    # Definir a taxa de quadros
    clock.tick(60)

# Encerrar o jogo
pygame.quit()