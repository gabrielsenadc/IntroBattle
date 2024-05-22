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
altura_seta = 40
class Seta():
    def __init__(self, posicoes):
        self.image = pygame.image.load("./imagens/seta.png")
        self.rect = self.image.get_rect()

        y = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, altura_seta/y)

        self.x = (largura_quadrado - self.image.get_width()) / 2

        self.rect.x = posicoes["Taylor Swift"]["x"] + self.x
        self.rect.y = posicoes["Taylor Swift"]["y"] - altura_seta


    def atualiza(self, dir, ruivo, posicoes):
        if dir == "l":
            if self.rect.x >= (posicoes["Taylor Swift"]["x"]):
                self.rect.x -= 250

        if dir == "r":
            if self.rect.x < posicoes["Taylor Launter"]["x"]:
                if(ruivo == 0 and self.rect.x < posicoes["Tom Hiddleston"]["x"]): self.rect.x += 250
                if(ruivo == 1): self.rect.x += 250

        if dir == "d":
            if(self.rect.y <= posicoes["Taylor Swift"]["y"]):
                self.rect.y += 250
                if(ruivo == 0 and self.rect.x != posicoes["Taylor Launter"]["x"] + self.x): self.rect.x += 125
                if(ruivo == 0 and self.rect.x == posicoes["Taylor Launter"]["x"] + self.x): self.rect.x -= 125

        if dir == "u":
            if(self.rect.y >= posicoes["Harry Styles"]["y"] - altura_seta):
                self.rect.y -= 250
                if(ruivo == 0): self.rect.x -= 125

    def atualiza_ruivo(self, posicoes):
        self.rect.x = posicoes["Ed Sheeran"]["x"] + self.x
        self.rect.y = posicoes["Ed Sheeran"]["y"] - altura_seta

    def desenha(self):
        janela.blit(self.image, self.rect)

class Quadrado(pygame.sprite.Sprite):
    def __init__(self, x, y, nome):
        super().__init__()
        self.tamanho = (largura_quadrado, altura_quadrado)
        self.rect = pygame.Rect((x, y), self.tamanho)
        self.nome = nome
        self.image = pygame.image.load(f"./imagens/{nome}.png" )
        self.rect_image = self.image.get_rect()

        h = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, 200/h)

        w = self.image.get_width()
        self.x = (200 - w) / 2
        self.rect_image.y = y
        self.rect_image.x = self.rect.x + self.x

    def desenhar_quadrado(self, tela):
        pygame.draw.rect(tela, cor_jogador, self.rect)
        janela.blit(self.image, self.rect_image)

    def atualizar(self, x, y):
        self.rect.x = x 
        self.rect.y = y

        self.rect_image.x = x + self.x
        self.rect_image.y = y

posicoes = {"Travis Kelce": {"x": (largura / 2) - 350, "y": 150},
            "Taylor Swift": {"x": (largura / 2) - 100, "y": 150},
            "Taylor Launter": {"x": (largura / 2) + 150, "y": 150},
            "Harry Styles": {"x": (largura / 2) - 225, "y": 400},
            "Tom Hiddleston": {"x": (largura / 2) + 25, "y": 400},
            "Ed Sheeran": {"x": (largura / 2) + 150, "y": 400}}

quadrados = pygame.sprite.Group()
quadrado1 = Quadrado(posicoes["Travis Kelce"]["x"], posicoes["Travis Kelce"]["y"], "Travis Kelce")
quadrado2 = Quadrado(posicoes["Taylor Swift"]["x"], posicoes["Taylor Swift"]["y"], "Taylor Swift")
quadrado3 = Quadrado(posicoes["Taylor Launter"]["x"], posicoes["Taylor Launter"]["y"], "Taylor Launter")
quadrado4 = Quadrado(posicoes["Harry Styles"]["x"], posicoes["Harry Styles"]["y"], "Harry Styles")
quadrado5 = Quadrado(posicoes["Tom Hiddleston"]["x"], posicoes["Tom Hiddleston"]["y"], "Tom Hiddleston")

quadrados.add(quadrado1)
quadrados.add(quadrado2)
quadrados.add(quadrado3)
quadrados.add(quadrado4)
quadrados.add(quadrado5)

seta = Seta(posicoes)

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
            quadrado6 = Quadrado(posicoes["Ed Sheeran"]["x"], posicoes["Ed Sheeran"]["y"], "Ed Sheeran")
            quadrados.add(quadrado6)
            posicoes["Harry Styles"]["x"] = (largura / 2) - 350
            posicoes["Tom Hiddleston"]["x"] = (largura / 2) - 100
            quadrado4.atualizar(posicoes["Harry Styles"]["x"], posicoes["Harry Styles"]["y"])
            quadrado5.atualizar(posicoes["Tom Hiddleston"]["x"], posicoes["Tom Hiddleston"]["y"])
            flag = 5
        else:
            flag = 0

    return flag


# Loop do jogo
executando = True
clock = pygame.time.Clock()
flag = 0
ruivo = 0
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        flag = verificaRuivo(evento, flag)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                seta.atualiza("l", ruivo, posicoes)
            elif evento.key == pygame.K_RIGHT:
                seta.atualiza("r", ruivo, posicoes)
            elif evento.key == pygame.K_DOWN:
                seta.atualiza("d", ruivo, posicoes)
            elif evento.key == pygame.K_UP:
                seta.atualiza("u", ruivo, posicoes)
            

    if(flag == 5): 
        ruivo = 1
        seta.atualiza_ruivo(posicoes)

    # Preencher a janela com a cor de fundo
    janela.fill(cor_fundo)

    # Atualizar o jogador
    for quadrado in quadrados:
        quadrado.desenhar_quadrado(janela)
    seta.desenha()

    # Atualizar a exibição
    pygame.display.flip()

    # Definir a taxa de quadros
    clock.tick(60)

# Encerrar o jogo
pygame.quit()