import pygame

largura = 1024 
altura = 768

class Personagem(pygame.sprite.Sprite):
    """
    Propriedades:
    image: imagem do personagem
    rect: retangulo que o personagem se encontra
    x: posicao do x do personagem
    y: posicao do y do personagem
    """

    def __init__(self, nome, n):
        super().__init__()
        self.image = pygame.image.load(f"./imagens/{nome}.png" )
        self.rect = self.image.get_rect()

        h = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, 225/h)

        if(n == 1): 
            self.x = 50
            self.y = 50
        if(n == 2):
            self.x = 250
            self.y = 175
        if(n == 3):
            self.x = 50
            self.y = 325

        self.rect.x = self.x
        self.rect.y = self.y


    def desenhar(self, janela):
        janela.blit(self.image, self.rect)

class TomHiddleston(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n)

        self.dano = 30
        self.defesa = 15
        self.vida_max = 200
        self.vida_atual = 200
        self.velocidade = 25

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
        print(counter)

        return counter + 1
    
    def animacao_ataque(self, counter):
        return counter

class TaylorLautner(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n)

        self.dano = 40
        self.defesa = 20
        self.vida_max = 225
        self.vida_atual = 225
        self.velocidade = 20

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
        super().__init__(nome, n)

        self.dano = 2
        self.defesa = 2
        self.vida_max = 2
        self.vida_atual = 2
        self.velocidade = 2

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter):
        return counter

class TravisKelce(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n)

        self.dano = 15
        self.defesa = 40
        self.vida_max = 300
        self.vida_atual = 300
        self.velocidade = 5

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter):
        return counter

class EdSheeran(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n)

        self.dano = 25
        self.defesa = 10
        self.vida_max = 120
        self.vida_atual = 120
        self.velocidade = 15

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter):
        return counter

class HarryStyles(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n)

        self.dano = 35
        self.defesa = 15
        self.vida_max = 150
        self.vida_atual = 150
        self.velocidade = 10

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter):
        return counter

