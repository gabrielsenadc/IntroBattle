import pygame

from personagens import *

largura = 1024 
altura = 768

posicoes = {"Travis Kelce": {"x": (largura / 2) - 350, "y": 150},
            "Taylor Swift": {"x": (largura / 2) - 100, "y": 150},
            "Taylor Lautner": {"x": (largura / 2) + 150, "y": 150},
            "Harry Styles": {"x": (largura / 2) - 225, "y": 400},
            "Tom Hiddleston": {"x": (largura / 2) + 25, "y": 400},
            "Ed Sheeran": {"x": (largura / 2) + 150, "y": 400}}

cor_fundo = (0, 0, 0)        # Preto
cor_jogador = (255, 255, 255)  # Branco

altura_selecao = 200
largura_selecao = 200
altura_seta = 40




class Seta():
    """
    Propriedades:
    """

    def __init__(self, posicoes):
        self.image = pygame.image.load("./imagens/seta.png")
        self.rect = self.image.get_rect()

        y = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, altura_seta/y)

        self.x = (largura_selecao - self.image.get_width()) / 2

        self.rect.x = posicoes["Taylor Swift"]["x"] + self.x
        self.rect.y = posicoes["Taylor Swift"]["y"] - altura_seta


    def atualiza(self, dir, ruivo, posicoes):
        if dir == "l":
            if self.rect.x >= (posicoes["Taylor Swift"]["x"]):
                self.rect.x -= 250

        if dir == "r":
            if self.rect.x < posicoes["Taylor Lautner"]["x"]:
                if(ruivo == 0 and self.rect.x < posicoes["Tom Hiddleston"]["x"]): self.rect.x += 250
                if(ruivo == 1): self.rect.x += 250

        if dir == "d":
            if(self.rect.y <= posicoes["Taylor Swift"]["y"]):
                self.rect.y += 250
                if(ruivo == 0 and self.rect.x != posicoes["Taylor Lautner"]["x"] + self.x): self.rect.x += 125
                if(ruivo == 0 and self.rect.x == posicoes["Taylor Lautner"]["x"] + self.x): self.rect.x -= 125

        if dir == "u":
            if(self.rect.y >= posicoes["Harry Styles"]["y"] - altura_seta):
                self.rect.y -= 250
                if(ruivo == 0): self.rect.x -= 125

    def atualiza_ruivo(self, posicoes):
        self.rect.x = posicoes["Ed Sheeran"]["x"] + self.x
        self.rect.y = posicoes["Ed Sheeran"]["y"] - altura_seta

    def desenha(self, janela):
        janela.blit(self.image, self.rect)

    def get_personagem(self):
        for key in posicoes.keys():
            if(self.rect.x - self.x == posicoes[key]["x"] and self.rect.y + altura_seta == posicoes[key]["y"]):
                return key
      
        return "ninguem"


class Selecao(pygame.sprite.Sprite):
    """
    Propriedades:
    """

    def __init__(self, x, y, nome):
        super().__init__()
        self.tamanho = (largura_selecao, altura_selecao)
        self.rect = pygame.Rect((x, y), self.tamanho)
        self.nome = nome
        self.image = pygame.image.load(f"./imagens/{nome}.png" )
        self.rect_image = self.image.get_rect()

        h = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, 170/h)

        w = self.image.get_width()
        self.imagem_shift = (200 - w) / 2
        self.rect_image.y = y
        self.rect_image.x = self.rect.x + self.imagem_shift

        fonte = pygame.font.Font(None, 36)
        self.texto = fonte.render(nome, True, cor_fundo)
        self.rect_texto = self.texto.get_rect()
        self.rect_texto.y = self.rect_image.y + 170
        
        w = self.texto.get_width()
        self.texto_shift = (200 - w) / 2
        self.rect_texto.x = self.rect.x + self.texto_shift
    

    def desenha(self, janela):
        pygame.draw.rect(janela, cor_jogador, self.rect)
        janela.blit(self.image, self.rect_image)
        janela.blit(self.texto, (self.rect_texto.x ,self.rect_texto.y))

    def atualizar(self, x, y):
        self.rect.x = x 
        self.rect.y = y

        self.rect_image.x = x + self.imagem_shift
        self.rect_image.y = y

        self.rect_texto.x = x + self.texto_shift
        self.rect_texto.y = y + 170

selecoes = pygame.sprite.Group()
selecao1 = Selecao(posicoes["Travis Kelce"]["x"], posicoes["Travis Kelce"]["y"], "Travis Kelce")
selecao2 = Selecao(posicoes["Taylor Swift"]["x"], posicoes["Taylor Swift"]["y"], "Taylor Swift")
selecao3 = Selecao(posicoes["Taylor Lautner"]["x"], posicoes["Taylor Lautner"]["y"], "Taylor Lautner")
selecao4 = Selecao(posicoes["Harry Styles"]["x"], posicoes["Harry Styles"]["y"], "Harry Styles")
selecao5 = Selecao(posicoes["Tom Hiddleston"]["x"], posicoes["Tom Hiddleston"]["y"], "Tom Hiddleston")

selecoes.add(selecao1)
selecoes.add(selecao2)
selecoes.add(selecao3)
selecoes.add(selecao4)
selecoes.add(selecao5)

def verifica_ruivo(evento, flag):
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
            flag = 5
        else:
            flag = 0

    return flag

def cria_EdSheeran(selecoes, posicoes):
    selecao6 = Selecao(posicoes["Ed Sheeran"]["x"], posicoes["Ed Sheeran"]["y"], "Ed Sheeran")
    selecoes.add(selecao6)
    posicoes["Harry Styles"]["x"] = (largura / 2) - 350
    posicoes["Tom Hiddleston"]["x"] = (largura / 2) - 100
    selecao4.atualizar(posicoes["Harry Styles"]["x"], posicoes["Harry Styles"]["y"])
    selecao5.atualizar(posicoes["Tom Hiddleston"]["x"], posicoes["Tom Hiddleston"]["y"])

def seleciona_personagem(n, seta, personagens):
    if(seta.get_personagem() == "Taylor Swift"):
        personagem = TaylorSwift(seta.get_personagem(), n)
    if(seta.get_personagem() == "Taylor Lautner"):
        personagem = TaylorLautner(seta.get_personagem(), n)
    if(seta.get_personagem() == "Harry Styles"):
        personagem = HarryStyles(seta.get_personagem(), n)
    if(seta.get_personagem() == "Travis Kelce"):
        personagem = TravisKelce(seta.get_personagem(), n)
    if(seta.get_personagem() == "Tom Hiddleston"):
        personagem = TomHiddleston(seta.get_personagem(), n)
    if(seta.get_personagem() == "Ed Sheeran"):
        personagem = EdSheeran(seta.get_personagem(), n)
 
    personagens.add(personagem)

def desenha_menu(selecoes, seta, janela):
    for selecao in selecoes:
        selecao.desenha(janela)
    seta.desenha(janela)

def menu(personagens, janela, clock):
    seta = Seta(posicoes)
    ruivo = 0
    num = 0
    flag = 0
    while num < 3:
        for evento in pygame.event.get():
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
                    num += 1
                    seleciona_personagem(num, seta, personagens)
        
        if(flag == 5): 
            cria_EdSheeran(selecoes, posicoes)
            ruivo = 1
            seta.atualiza_ruivo(posicoes)

        # Preencher a janela com a cor de fundo
        janela.fill((0, 0, 0))

        # Atualizar o jogador
        desenha_menu(selecoes, seta, janela)
            
        # Atualizar a exibição
        pygame.display.flip()

        # Definir a taxa de quadros
        clock.tick(60)
