import pygame

from personagens import *

largura = 1024 
altura = 768

posicoes_selecao = {"Travis Kelce": {"x": (largura / 2) - 350, "y": 150},
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

bg_image = bg_image = pygame.image.load("./imagens/background.jpg")
title_image = pygame.image.load("./imagens/title.png")

w = bg_image.get_width()
bg_image = pygame.transform.scale_by(bg_image, 1024/w)

bg_image.set_alpha(75) 


class Seta():
    """
    Propriedades:
    """

    def __init__(self, posicoes_selecao):
        self.image = pygame.image.load("./imagens/seta.png")
        self.rect = self.image.get_rect()

        y = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, altura_seta/y)

        self.shift = (largura_selecao - self.image.get_width()) / 2

        self.rect.x = posicoes_selecao["Taylor Swift"]["x"] + self.shift
        self.rect.y = posicoes_selecao["Taylor Swift"]["y"] - altura_seta

        self.escolhidos = {"Travis Kelce": 0,
                           "Taylor Swift": 0,
                           "Taylor Lautner": 0,
                           "Harry Styles": 0,
                           "Tom Hiddleston": 0,
                           "Ed Sheeran": 0}

    def atualiza(self, dir, ruivo, posicoes_selecao):
        if dir == pygame.K_LEFT:
            if self.rect.x >= (posicoes_selecao["Taylor Swift"]["x"]):
                self.rect.x -= 250

        if dir == pygame.K_RIGHT:
            if self.rect.x < posicoes_selecao["Taylor Lautner"]["x"]:
                if(ruivo == 0 and self.rect.x < posicoes_selecao["Tom Hiddleston"]["x"]): self.rect.x += 250
                if(ruivo == 1): self.rect.x += 250

        if dir == pygame.K_DOWN:
            if(self.rect.y <= posicoes_selecao["Taylor Swift"]["y"]):
                self.rect.y += 250
                if(ruivo == 0 and self.rect.x != posicoes_selecao["Taylor Lautner"]["x"] + self.shift): self.rect.x += 125
                if(ruivo == 0 and self.rect.x == posicoes_selecao["Taylor Lautner"]["x"] + self.shift): self.rect.x -= 125

        if dir == pygame.K_UP:
            if(self.rect.y >= posicoes_selecao["Harry Styles"]["y"] - altura_seta):
                self.rect.y -= 250
                if(ruivo == 0): self.rect.x -= 125

    def atualiza_ruivo(self, posicoes_selecao):
        self.rect.x = posicoes_selecao["Ed Sheeran"]["x"] + self.shift
        self.rect.y = posicoes_selecao["Ed Sheeran"]["y"] - altura_seta

    def desenha(self, janela):
        janela.blit(self.image, self.rect)

    def get_personagem(self):
        for key in posicoes_selecao.keys():
            if(self.rect.x - self.shift == posicoes_selecao[key]["x"] and self.rect.y + altura_seta == posicoes_selecao[key]["y"]):
                if self.escolhidos[key] == 0: return key
      
        return "ninguem"
    
    def escolhe_personagem(self, nome):
        self.escolhidos[nome] = 1


class Selecao(pygame.sprite.Sprite):
    """
    Propriedades:
    """

    def __init__(self, x, y, nome):
        super().__init__()
        self.nome = nome

        self.rect = pygame.Rect((x, y), (largura_selecao, altura_selecao))
        self.image = pygame.image.load(f"./imagens/{nome}/default.png" )
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

    def seleciona_personagem(self):
        self.image = pygame.image.load(f"./imagens/{self.nome}/selected.png" )
        h = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, 170/h)


selecoes = pygame.sprite.Group()
for key in posicoes_selecao.keys():
    if(key != "Ed Sheeran"):
        selecao = Selecao(posicoes_selecao[key]["x"], posicoes_selecao[key]["y"], key)
        selecoes.add(selecao)


def verifica_ruivo(evento, flag):
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_r: flag = 1
        elif evento.key == pygame.K_u and flag == 1: flag = 2
        elif evento.key == pygame.K_i and flag == 2: flag = 3
        elif evento.key == pygame.K_v and flag == 3: flag = 4
        elif evento.key == pygame.K_o and flag == 4: flag = 5
        else: flag = 0

    return flag

def cria_EdSheeran(selecoes, posicoes_selecao):
    selecao6 = Selecao(posicoes_selecao["Ed Sheeran"]["x"], posicoes_selecao["Ed Sheeran"]["y"], "Ed Sheeran")
    selecoes.add(selecao6)
    posicoes_selecao["Harry Styles"]["x"] = (largura / 2) - 350
    posicoes_selecao["Tom Hiddleston"]["x"] = (largura / 2) - 100
    for selecao in selecoes:
        if selecao.nome == "Harry Styles": selecao.atualizar(posicoes_selecao["Harry Styles"]["x"], posicoes_selecao["Harry Styles"]["y"])
        if selecao.nome == "Tom Hiddleston": selecao.atualizar(posicoes_selecao["Tom Hiddleston"]["x"], posicoes_selecao["Tom Hiddleston"]["y"])

    return -1

def seleciona_personagem(n, seta, personagens, selecoes):
    if seta.get_personagem() != "ninguem":
        n += 1
        for selecao in selecoes:
            if selecao.nome == seta.get_personagem(): selecao.seleciona_personagem()

        personagem = globals()["".join(seta.get_personagem().split(" "))](seta.get_personagem(), n)
        personagens.add(personagem)

        seta.escolhe_personagem(seta.get_personagem())
        

    return n

def desenha_menu(selecoes, seta, janela):
    for selecao in selecoes:
        selecao.desenha(janela)
    seta.desenha(janela)

def menu(personagens, inimigos, janela, clock):
    seta = Seta(posicoes_selecao)
    ruivo = 0
    num = 0
    flag = 0
    break_flag = 0

    rect = pygame.Rect(((largura / 2) - (title_image.get_width() / 2) - 25, (altura / 2) - (title_image.get_height() / 2) - 25), (title_image.get_width() + 50 ,title_image.get_height() + 50))

    while not(break_flag):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                break_flag = 1

        janela.fill((0, 0, 0))
        janela.blit(bg_image, (0, 0))


        pygame.draw.rect(janela, cor_jogador, rect)
        janela.blit(title_image, ((largura / 2) - (title_image.get_width() / 2), (altura / 2) - (title_image.get_height() / 2)))

        pygame.display.flip()
        clock.tick(60)


    while num < 3:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if flag != -1: flag = verifica_ruivo(evento, flag)
            if evento.type == pygame.KEYDOWN:
                seta.atualiza(evento.key, ruivo, posicoes_selecao)
                if evento.key == pygame.K_z:
                    num = seleciona_personagem(num, seta, personagens, selecoes)
        
        if(flag == 5): 
            flag = cria_EdSheeran(selecoes, posicoes_selecao)
            ruivo = 1
            seta.atualiza_ruivo(posicoes_selecao)

        # Preencher a janela com a cor de fundo
        janela.fill((0, 0, 0))
        janela.blit(bg_image, (0, 0))

        # Atualizar o jogador
        desenha_menu(selecoes, seta, janela)
            
        # Atualizar a exibição
        pygame.display.flip()

        # Definir a taxa de quadros
        clock.tick(60)

        if(num == 3): 
            inimigo1 = JakeGyllenhaal("Jake Gyllenhaal", 4)
            inimigo2 = JohnMayer("John Mayer", 5)
            inimigos.add(inimigo1)
            inimigos.add(inimigo2)
            
    for personagem in personagens:
        if personagem.get_nome() == "Taylor Swift":
            for aliado in personagens:
                if aliado.get_nome() == "Travis Kelce":
                    personagem.atribui_aliado(aliado)
    
    return True