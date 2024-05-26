import pygame

largura = 1024 
altura = 768

posicoes_jogo = {"personagem1": {"x": 50, "y": 50},
                 "personagem2": {"x": 250, "y": 175},
                 "personagem3": {"x": 50, "y": 325},
                 "personagem4": {"x": 750, "y": 50},
                 "personagem5": {"x": 750, "y": 325},}

class Personagem(pygame.sprite.Sprite):
    """
    Propriedades:
    image: imagem do personagem
    rect: retangulo que o personagem se encontra
    x: posicao do x do personagem
    y: posicao do y do personagem
    dano: pontos de dano
    defesa: pontos de defesa 
    velocidade: pontos de velocidade
    vida_max: pontos de vida máxima
    vida_atual: pontos de vida atual
    """

    def __init__(self, nome, n, dano, defesa, vida, velocidade):
        super().__init__()
        self.nome = nome
        self.image = pygame.image.load(f"./imagens/{nome}.png" )
        self.rect = self.image.get_rect()

        h = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, 225/h)

        personagem = f"personagem{n}"
        for key in posicoes_jogo.keys():
            if key == personagem:
                self.x = self.rect.x = posicoes_jogo[key]["x"]
                self.y = self.rect.y = posicoes_jogo[key]["y"]

        self.dano = dano
        self.defesa = defesa
        self.vida_max = vida
        self.vida_atual = vida
        self.velocidade = velocidade

    def desenhar(self, janela):
        janela.blit(self.image, self.rect)

    def ataque(self, inimigo):
        dano = self.dano * (50 / (50 + inimigo.get_defesa()))
        inimigo.recebe_dano(dano)

    def aumenta_defesa(self, aumento):
        self.defesa += aumento
    
    def recebe_dano(self, dano):
        self.vida_atual -= dano

    def recupera_vida(self, vida):
        self.vida += vida
    
    def get_dano(self):
        return self.dano
    
    def get_defesa(self):
        return self.defesa
    
    def get_velocidade(self):
        return self.velocidade
    
    def get_vida_atual(self):
        return self.vida_atual
    

class TomHiddleston(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 30, 15, 200, 25)

    def animacao_habilidade(self, counter):
        if(counter == 1): 
            self.rect.x = 350
            self.rect.y = 175
            self.image = pygame.image.load(f"./imagens/Tom Hiddleston habilidade.png")
            h = self.image.get_height()
            self.image = pygame.transform.scale_by(self.image, 225/h)
        else: self.rect.x += 5

        if(counter > (largura - 300) / 5):
            self.rect.x = self.x
            self.rect.y = self.y
            self.image = pygame.image.load(f"./imagens/Tom Hiddleston.png")
            h = self.image.get_height()
            self.image = pygame.transform.scale_by(self.image, 225/h)
            return 0

        return counter + 1
    
    def animacao_ataque(self, counter):
        return counter

class TaylorLautner(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 40, 20, 225, 20)

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter):
        self.image = pygame.image.load(f"./imagens/Taylor Lautner attack.png")
        h = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, 225/h)
        self.image = pygame.transform.flip(self.image, True, False)

        if(counter == 50): 
            self.image = pygame.image.load(f"./imagens/Taylor Lautner.png")
            h = self.image.get_height()
            self.image = pygame.transform.scale_by(self.image, 225/h)
            return 0
         
        return counter + 1

class TaylorSwift(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 2, 2, 2, 2)

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter):
        return counter

class TravisKelce(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 15, 40, 300, 5)

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter):
        return counter

class EdSheeran(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 25, 10, 120, 15)

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter):
        return counter

class HarryStyles(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 35, 15, 150, 10)

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter):
        return counter

