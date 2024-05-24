import pygame

pygame.init()


largura = 1024 
altura = 768
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("The Ex Tour")


cor_fundo = (0, 0, 0)        # Preto
cor_jogador = (255, 255, 255)  # Branco

altura_selecao = 200
largura_selecao = 200
altura_seta = 40

from personagens import *

class Seta():
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

    def desenha(self):
        janela.blit(self.image, self.rect)

    def get_personagem(self):
        if(self.rect.x - self.x == posicoes["Taylor Swift"]["x"] and self.rect.y + altura_seta == posicoes["Taylor Swift"]["y"]):
            return "Taylor Swift"
        if(self.rect.x - self.x == posicoes["Taylor Lautner"]["x"] and self.rect.y + altura_seta == posicoes["Taylor Lautner"]["y"]):
            return "Taylor Lautner"
        if(self.rect.x - self.x == posicoes["Travis Kelce"]["x"] and self.rect.y + altura_seta == posicoes["Travis Kelce"]["y"]):
            return "Travis Kelce"
        if(self.rect.x - self.x == posicoes["Harry Styles"]["x"] and self.rect.y + altura_seta == posicoes["Harry Styles"]["y"]):
            return "Harry Styles"
        if(self.rect.x - self.x == posicoes["Tom Hiddleston"]["x"] and self.rect.y + altura_seta == posicoes["Tom Hiddleston"]["y"]):
            return "Tom Hiddleston"
        if(self.rect.x - self.x == posicoes["Ed Sheeran"]["x"] and self.rect.y + altura_seta == posicoes["Ed Sheeran"]["y"]):
            return "Ed Sheeran"
        return "ninguem"

class Selecao(pygame.sprite.Sprite):
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
    

    def desenhar_selecao(self, tela):
        pygame.draw.rect(tela, cor_jogador, self.rect)
        janela.blit(self.image, self.rect_image)
        janela.blit(self.texto, (self.rect_texto.x ,self.rect_texto.y))

    def atualizar(self, x, y):
        self.rect.x = x 
        self.rect.y = y

        self.rect_image.x = x + self.imagem_shift
        self.rect_image.y = y

        self.rect_texto.x = x + self.texto_shift
        self.rect_texto.y = y + 170

posicoes = {"Travis Kelce": {"x": (largura / 2) - 350, "y": 150},
            "Taylor Swift": {"x": (largura / 2) - 100, "y": 150},
            "Taylor Lautner": {"x": (largura / 2) + 150, "y": 150},
            "Harry Styles": {"x": (largura / 2) - 225, "y": 400},
            "Tom Hiddleston": {"x": (largura / 2) + 25, "y": 400},
            "Ed Sheeran": {"x": (largura / 2) + 150, "y": 400}}

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
            selecao6 = Selecao(posicoes["Ed Sheeran"]["x"], posicoes["Ed Sheeran"]["y"], "Ed Sheeran")
            selecoes.add(selecao6)
            posicoes["Harry Styles"]["x"] = (largura / 2) - 350
            posicoes["Tom Hiddleston"]["x"] = (largura / 2) - 100
            selecao4.atualizar(posicoes["Harry Styles"]["x"], posicoes["Harry Styles"]["y"])
            selecao5.atualizar(posicoes["Tom Hiddleston"]["x"], posicoes["Tom Hiddleston"]["y"])
            flag = 5
        else:
            flag = 0

    return flag

personagens = pygame.sprite.Group()

def seleciona_personagem(n, seta, personagens):
    dano = 0
    defesa = 0
    vida = 0
    velocidade = 0
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
        ruivo = 1
        seta.atualiza_ruivo(posicoes)

    # Preencher a janela com a cor de fundo
    janela.fill(cor_fundo)

    # Atualizar o jogador
    if(n < 3):
        for selecao in selecoes:
            selecao.desenhar_selecao(janela)
        seta.desenha()
    
    if(n >= 3):
        for personagem in personagens:
            personagem.desenhar(janela)

    # Atualizar a exibição
    pygame.display.flip()

    # Definir a taxa de quadros
    clock.tick(60)

# Encerrar o jogo
pygame.quit()