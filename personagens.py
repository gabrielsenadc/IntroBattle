import pygame

import numpy

largura = 1024 
altura = 768

posicoes_jogo = {"personagem1": {"x": 150, "y": 10},
                 "personagem2": {"x": 350, "y": 175},
                 "personagem3": {"x": 150, "y": 325},
                 "personagem4": {"x": 800, "y": 15},
                 "personagem5": {"x": 800, "y": 325},}

def atribui_imagem(nome, tamanho):
    image = pygame.image.load(f"./imagens/{nome}")
    h = image.get_height()
    image = pygame.transform.scale_by(image, tamanho/h)

    return image

class Personagem(pygame.sprite.Sprite):
    """
    Propriedades:
    image: imagem do personagem
    rect: retangulo que o personagem se encontra
    x: posicao x do personagem
    y: posicao y do personagem
    dano: pontos de dano
    defesa: pontos de defesa 
    velocidade: pontos de velocidade
    vida_max: pontos de vida máxima
    vida_atual: pontos de vida atual
    """

    def __init__(self, nome, n, dano, defesa, vida, velocidade, nome_habilidade, tempo_cooldown):
        super().__init__()
        self.nome = nome
        self.image = pygame.image.load(f"./imagens/{nome}/default.png" )
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
        self.nome_habilidade = nome_habilidade
        self.tempo_cooldown = tempo_cooldown

        self.congelado = 0
        self.invisivel = 0
        self.envenenado = 0
        self.defesa_extra = 0
        self.chamativo = 0

        self.vivo = 1

        self.cooldown = 0

        self.ruivo = 0

        self.path = nome

        self.fox_image = atribui_imagem("fox.png", 50)
        self.fox_rect = self.fox_image.get_rect()
        self.fox_rect.x = self.x
        self.fox_rect.y = self.y

    def animacao_ataque(self, counter, x, y):
        if(counter == 1):
            self.set_image("attack")

        shift = self.x / 20

        self.rect.x += (x - self.x) / 70
        self.rect.y += (y - self.y - shift) / 70

        if(counter == 70): 
            if self.chamativo <= 0: self.set_image("default")
            else: self.set_image("skill")
            self.rect.x = self.x
            self.rect.y = self.y
            return 0
         
        return counter + 1
    
    def ataque(self, inimigo):
        dano = self.dano * (50 / (50 + inimigo.get_defesa()))
        inimigo.recebe_dano(dano)

    def desenhar_invisivel(self, janela):
        if self.invisivel > 0:
            self.image.set_alpha(69) 
            janela.blit(self.fox_image, self.fox_rect)


    def desenhar(self, janela): 
        janela.blit(self.image, self.rect)
        self.desenhar_invisivel(janela)


    ### Setters ###

    def set_image(self, tipo):
        self.image = pygame.image.load(f"./imagens/{self.path}/{tipo}.png")
        h = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, 225/h)
    
    def morre(self):
        self.vivo = 0

    def aumenta_defesa(self, aumento):
        self.defesa += aumento
    
    def recebe_dano(self, dano):
        self.vida_atual -= dano

    def recupera_vida(self, vida):
        self.vida_atual += vida
        if(self.vida_atual > self.vida_max): self.vida_atual = self.vida_max

    def congela(self):
        self.congelado = 2
        self.set_image("congelado")
    
    def descongela(self):
        self.congelado -= 1

        if self.congelado <= 0:
            self.set_image("default")

    def invisibilidade(self, n):
        self.invisivel = n

    def diminui_invisibilidade(self):
        self.invisivel -= 1
        if self.invisivel <= 0:
            self.image.set_alpha(250)
            
    def envenena(self):
        self.envenenado = 2

    def dano_veneno(self):
        if self.envenenado > 0: self.recebe_dano(35 * 0.25)
        self.envenenado -= 1

    def defende(self):
        self.defesa_extra = 1
        self.defesa *= 2

    def normaliza_defesa(self):
        if self.defesa_extra:
            self.defesa_extra = 0
            self.defesa /= 2

    def cooldown_habilidade(self):
        if self.cooldown > 0: self.cooldown -= 1

    def atrasa_habilidade(self):
        self.cooldown += 1

    def utiliza_habilidade(self, personagens):
        for personagem in personagens:
            if personagem.get_nome() != self.get_nome(): personagem.atrasa_habilidade()
        self.cooldown = self.tempo_cooldown

    def set_ruivo(self):
        self.ruivo = 1

        self.path = f"{self.nome}/ruivo"

        if self.congelado <= 0: self.set_image("default")
        else: self.set_image("congelado")

    def normaliza_chamativo(self):
        self.chamativo -= 1

        if self.chamativo == 0: 
            self.set_image("default")
    
    ## Getters ###

    def get_chamativo(self):
        return self.chamativo

    def get_nome_habilidade(self):
        return self.nome_habilidade

    def habilidade_disponivel(self):
        if self.cooldown <= 0: return True 
        else: return False

    def get_cooldown(self):
        return self.cooldown
        
    def get_dano(self):
        return self.dano
    
    def get_defesa(self):
        return self.defesa
    
    def get_velocidade(self):
        return self.velocidade
    
    def get_vida_atual(self):
        return self.vida_atual

    def get_vida_max(self):
        return self.vida_max
    
    def get_posicao_x(self):
        return self.x
    
    def get_posicao_y(self):
        return self.y
    
    def get_nome(self):
        return self.nome
    
    def get_congelado(self):
        return self.congelado
    
    def get_invisivel(self):
        return self.invisivel
    
    def get_envenenado(self):
        return self.envenenado
    
    def get_vivo(self):
        return self.vivo
    
def get_personagem_menos_vida(personagens):
    menor_vida = 300
    for personagem in personagens:
        if personagem.get_vida_atual() < menor_vida and personagem.get_invisivel() <= 0:
            menor_vida = personagem.get_vida_atual()
        if personagem.get_chamativo() > 0: return personagem
    
    for personagem in personagens:
        if personagem.get_vida_atual() == menor_vida:
            return personagem


class TomHiddleston(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 30, 15, 200, 25, "Getaway Car", 2)

    def animacao_habilidade(self, counter):
        if counter == 1: 
            pygame.mixer.music.load("music/getaway_car.mp3")
            pygame.mixer.music.play()

        if(counter == 1): 
            self.rect.x = 350
            self.rect.y = 175
            self.set_image("skill")
        else: self.rect.x += 5

        if(counter > (largura - 300) / 5):
            self.rect.x = self.x
            self.rect.y = self.y
            self.set_image("default")
        
        if counter > 200:
            return 0

        return counter + 1
    
    def habilidade(self, inimigos):
        for inimigo in inimigos:
            dano = 1.5 * self.dano * (50 / (50 + inimigo.get_defesa()))
            inimigo.recebe_dano(dano)
            
class TaylorLautner(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 25, 20, 225, 20, "Back to December", 4)

        self.neve_image =  atribui_imagem("neve.png", 40)

        self.neve_rect = []
        for i in range(4, 6):
            key = f"personagem{i}"
            for j in range(5):
                if(j%2 == 0): self.neve_rect.append((posicoes_jogo[key]["x"] + 25, posicoes_jogo[key]["y"] + 10 + (j * 25)))
                else: self.neve_rect.append((posicoes_jogo[key]["x"] + 55, posicoes_jogo[key]["y"] + 10 + (j * 25)))
                
        self.neve = 0

    def animacao_habilidade(self, counter):
        if counter == 1: 
            pygame.mixer.music.load("music/back_to_december.mp3")
            pygame.mixer.music.play()

        if(counter%17 == 0): self.neve += 1
        
        if(counter == 200):
            self.neve = 0
            return 0
        
        return counter + 1
    
    def desenhar(self, janela):
        janela.blit(self.image, self.rect)
        if(self.neve):
            for i in range(self.neve):
                if self.neve > len(self.neve_rect): break
                janela.blit(self.neve_image, self.neve_rect[i])
        self.desenhar_invisivel(janela)
    
    def habilidade(self, inimigos):
        for inimigo in inimigos:
            inimigo.congela()
            dano = 0.5 * self.dano * (50 / (50 + inimigo.get_defesa()))
            inimigo.recebe_dano(dano)
  
class TravisKelce(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 15, 40, 300, 5, "Touchdown", 4)

    def animacao_habilidade(self, counter):
        if counter == 1: 
            pygame.mixer.music.load("music/touchdown.mp3")
            pygame.mixer.music.play()

        if counter == 50:
            return 0

        return counter + 1
    
    def habilidade(self, inimigos):
        self.chamativo = 2

        self.set_image("skill")

class EdSheeran(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 25, 10, 120, 15, "End Game", 4)

        self.subtract_image = atribui_imagem("subtract.jpeg", 25)
        self.subtract_rect = self.subtract_image.get_rect()
        self.subtract = 0

        self.plus_image = atribui_imagem("plus.jpeg", 25)
        self.plus_rect = self.plus_image.get_rect()
        self.plus = 0

        self.skill_image = pygame.image.load(f"./imagens/{self.path}/skill.jpeg")
        self.skill_image = pygame.transform.scale(self.skill_image, (1024, 768))
        self.skill_rect = self.skill_image.get_rect()
        self.skill = 0
        self.skill_image.set_alpha(150)

    def animacao_habilidade(self, counter):
        if counter == 1: 
            pygame.mixer.music.load("music/endgame.mp3")
            pygame.mixer.music.play()

        self.skill = 1

        alpha = self.skill_image.get_alpha() - 20
        if(alpha <= 10): alpha = 150

        self.skill_image.set_alpha(alpha)

        if counter > 250: 
            self.skill = 0
            return 0

        return counter + 1

    def animacao_ataque(self, counter, x, y, x2, y2):
        if(counter == 1):
            self.subtract_rect.x = self.x
            self.subtract_rect.y = self.y + 25
            self.subtract = 1

            self.set_image("attack")

        if (counter >= 1 and counter < 70):
            self.subtract_rect.x += (x + 50 - self.x) / 70
            self.subtract_rect.y += (y + 25 - self.y) / 70

        if(counter == 70):
            self.subtract = 0

            self.plus_rect.x = x
            self.plus_rect.y = y + 25
            self.plus = 1

        if (counter >= 70):
            self.plus_rect.x += (x2 + 50 - x) / 70
            self.plus_rect.y += (y2 + 25 - y) / 70

        if(counter > 140):
            self.set_image("default")
            self.plus = 0
            return 0
        
        return counter + 1
    
    def desenhar(self, janela):
        janela.blit(self.image, self.rect)
        if(self.subtract): janela.blit(self.subtract_image, self.subtract_rect)
        if(self.plus): janela.blit(self.plus_image, self.plus_rect)
        if(self.skill): janela.blit(self.skill_image, self.skill_rect)
        self.desenhar_invisivel(janela)
    
    def ataque(self, inimigo, aliado):
        dano = self.dano * (50 / (50 + inimigo.get_defesa()))
        inimigo.recebe_dano(dano)
        aliado.recupera_vida(dano)
        inimigo.set_ruivo()

    def habilidade(self, inimigos, aliados):
        defesa = 0
        for inimigo in inimigos:
            defesa += inimigo.get_defesa()

        defesa *= 0.5
        for aliado in aliados:
            aliado.aumenta_defesa(defesa / 3)

class SabrinaCarpenter(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 25, 15, 150, 23, "Tornado Warnings", 2)

        self.tornado_image = pygame.image.load(f"./imagens/tornado.png")
        self.tornado_image = pygame.transform.scale(self.tornado_image, (200, 600))
        self.tornado_rect = self.tornado_image.get_rect()
        self.tornado = 0

        self.feather_image = atribui_imagem("feather.png", 50)
        self.feather_rect = self.feather_image.get_rect()
        self.feather = 0

        self.email_image = atribui_imagem("email.png", 40)
        self.email_rect = self.email_image.get_rect()
        self.email = 0

        self.type = 0


    def animacao_ataque(self, counter, x, y):
        if self.type % 2 == 0:
            if(counter == 1):
                self.feather_rect.x = self.x
                self.feather_rect.y = self.y + 25
                self.feather = 1

                self.feather_image = atribui_imagem("feather.png", 50)
                a = numpy.arctan((y - self.y) / (self.x - x)) * 180 / 3.14
                self.feather_image = pygame.transform.rotate(self.feather_image, a - 40)


            
            self.feather_rect.x += (x + 50 - self.x) / 100
            self.feather_rect.y += (y - self.y) / 100

            if(counter > 100):
                self.feather = 0
                self.type += 1
                return 0

        else:
            if(counter == 1):
                self.email_rect.x = self.x
                self.email_rect.y = self.y + 25
                self.email = 1

                self.email_image = atribui_imagem("email.png", 40)
                a = numpy.arctan((y - self.y) / (self.x - x)) * 180 / 3.14
                self.email_image = pygame.transform.rotate(self.email_image, a)


            
            self.email_rect.x += (x + 50 - self.x) / 70
            self.email_rect.y += (y - self.y) / 70

            if(counter > 70):
                self.email = 0
                self.type += 1
                return 0
        
        return counter + 1

    def animacao_habilidade(self, counter):
        if counter == 1:
            self.tornado_rect.x = posicoes_jogo["personagem4"]["x"] - 50
            self.tornado_rect.y = posicoes_jogo["personagem4"]["y"] - 10

            self.tornado = 1

        if (counter // 10) % 2 == 0: self.tornado_rect.x += 5
        else: self.tornado_rect.x -= 5

        if counter >= 70:
            self.tornado = 0
            return 0

        return counter + 1
        
    def habilidade(self, inimigos):
        for inimigo in inimigos:
            dano = 1.5 * self.dano * (50 / (50 + inimigo.get_defesa()))
            inimigo.recebe_dano(dano)

    def desenhar(self, janela):
        janela.blit(self.image, self.rect)
        if(self.tornado): janela.blit(self.tornado_image, self.tornado_rect)
        if(self.feather): janela.blit(self.feather_image, self.feather_rect)
        if(self.email): janela.blit(self.email_image, self.email_rect)
        self.desenhar_invisivel(janela)

class HarryStyles(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 25, 15, 150, 10, "I Know Places", 4)

        self.glitter_image = atribui_imagem("glitter.png", 50)
        self.glitter_image = pygame.transform.rotate(self.glitter_image, -90)
        self.glitter_rect = self.glitter_image.get_rect()
        self.glitter = 0

    def animacao_habilidade(self, counter):
        if counter == 1: 
            pygame.mixer.music.load("music/i_know_places.mp3")
            pygame.mixer.music.play()
        
        if counter > 200:
            return 0
        
        return counter + 1

    def animacao_ataque(self, counter, x, y):
        if(counter == 1):
            self.glitter_rect.x = self.x
            self.glitter_rect.y = self.y + 25
            self.glitter = 1

            self.set_image("attack")

        
        self.glitter_rect.x += (x + 50 - self.x) / 50
        self.glitter_rect.y += (y + 25 - self.y) / 50

        if(counter > 50):
            self.set_image("default")
            self.glitter = 0
            return 0
        
        return counter + 1
    

    def desenhar(self, janela):
        janela.blit(self.image, self.rect)
        if(self.glitter): janela.blit(self.glitter_image, self.glitter_rect)
        self.desenhar_invisivel(janela)
    
    def habilidade(self, aliado):
        self.invisibilidade(2)
        aliado.invisibilidade(3)


def animacao_JohnMayer(personagem, counter, x, y):
    if(counter == 1):
        personagem.ghost_rect.x = personagem.x
        personagem.ghost_rect.y = personagem.y + 65
        personagem.ghost = 1

        personagem.set_image("attack")

    
    personagem.ghost_rect.x += (x + 50 - personagem.x) / 50
    personagem.ghost_rect.y += (y - personagem.y - 65) / 50

    if(counter > 50):
        personagem.set_image("default")
        personagem.ghost = 0
        return 0
    
    return counter + 1

def animacao_JakeGyllenhaal(personagem, counter):
    if(counter == 1):
        personagem.set_image("skill")
        personagem.fire = 1

    if(counter == 20): personagem.fire = 2

    if(counter == 40): personagem.fire = 3

    if(counter == 60):
        personagem.set_image("default")
        personagem.fire = 0
        return 0
    
    return counter + 1
    
     
class TaylorSwift(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 33, 13, 180, 22, "Don't Blame Me", 2)

        self.roubado = ""

        self.aliado = 0

        self.ghost_image = atribui_imagem("ghost.png", 150)
        self.ghost_rect = self.ghost_image.get_rect()
        self.ghost = 0

        self.fire_image = atribui_imagem("fogo.png", 225)
        self.fire_rect = []
        for i in range(4, 6):
            key = f"personagem{i}"
            self.fire_rect.append((posicoes_jogo[key]["x"], posicoes_jogo[key]["y"]))
        self.fire = 0

        self.snake_image = atribui_imagem("snake.png", 100)
        self.snake_rect = self.snake_image.get_rect()
        self.snake = 0


    def atribui_aliado(self, personagem):
        self.aliado = personagem

    def aliado_attack(self, inimigo, tela):
        if self.aliado != 0:
            animacao("ataque", self.aliado, inimigo.get_posicao_x(), inimigo.get_posicao_y(), tela, 0, 0)
            self.aliado.ataque(inimigo)

    def animacao_habilidade(self, counter, x, y):
        if self.roubado == "John Mayer": return animacao_JohnMayer(self, counter, x, y)
        if self.roubado == "Jake Gyllenhaal": return animacao_JakeGyllenhaal(self, counter)
    
    def habilidade_taylor(self, inimigo):
        self.habilidade = inimigo.habilidade
        self.roubado = inimigo.get_nome()

    def animacao_ataque(self, counter, x, y):
        if(counter == 1):
            self.snake_image = atribui_imagem("snake.png", 100)

            a = numpy.arctan((y - self.y) / (self.x - x)) * 180 / 3.14
            self.snake_image = pygame.transform.rotate(self.snake_image, a)

            self.snake_rect.x = self.x
            self.snake_rect.y = self.y + 25
            self.snake = 1

            self.set_image("attack")

        
        self.snake_rect.x += (x + 50 - self.x) / 70
        self.snake_rect.y += (y - self.y) / 70

        if(counter > 70):
            self.set_image("default")
            self.snake = 0
            return 0
        
        return counter + 1
    
    def get_roubado(self):
        return self.roubado
    
    def set_roubado(self, nome):
        self.roubado = nome
    
    def desenhar(self, janela):
        janela.blit(self.image, self.rect)
        if(self.ghost): janela.blit(self.ghost_image, self.ghost_rect)
        if(self.snake): janela.blit(self.snake_image, self.snake_rect)
        if(self.fire):
            for i in range(self.fire):
                if self.fire == 3: break
                janela.blit(self.fire_image, self.fire_rect[i])
        self.desenhar_invisivel(janela)
  
class JohnMayer(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 35, 25, 225, 19, "Haunted", 2)

        self.turno = 1

        self.ghost_image = atribui_imagem("ghost.png", 150)
        self.ghost_rect = self.ghost_image.get_rect()
        self.ghost = 0

        self.raio_image = pygame.image.load(f"./imagens/raio.png")
        self.raio = 0


    def animacao_habilidade(self, counter, x, y):
        return animacao_JohnMayer(self, counter, x, y)
    
    def animacao_ataque(self, counter, x, y):
        
        if counter == 1:
            self.raio_image = pygame.image.load(f"./imagens/raio.png")
            
            w = self.raio_image.get_width()
            self.raio_rect = (x, y)
            d = ((self.x - x)**2 + (self.y - y)**2)**(1/2)
            a = ((numpy.arccos((self.x - x) / d) * 180) / 3.14) 
            if(self.y == y): d += 20
            else: d += (self.y - y) / 60

            self.set_image("attack")
            self.raio = 1

            self.raio_image = pygame.transform.scale_by(self.raio_image, (d + 10)/w)
            self.raio_image = pygame.transform.rotate(self.raio_image, -a)

        if counter >= 50: 
            self.set_image("default")
            self.raio = 0
            return 0

        return counter + 1
    
    def desenhar(self, janela):
        janela.blit(self.image, self.rect)
        if(self.ghost): janela.blit(self.ghost_image, self.ghost_rect)
        if(self.raio): janela.blit(self.raio_image, self.raio_rect)
    
    def habilidade(self, inimigo):
        dano = self.dano * (50 / (50 + inimigo.get_defesa()))
        inimigo.recebe_dano(dano)
        inimigo.envenena()

    def ataque(self, inimigo):
        if(inimigo.get_vida_atual() < (inimigo.get_vida_max() * 0.20)): dano = inimigo.get_vida_atual()
        else: dano = self.dano * (50 / (50 + inimigo.get_defesa()))
        inimigo.recebe_dano(dano)

    def get_turno(self):
        return self.turno
    
    def set_turno(self):
        self.turno += 1
        if(self.turno > 3):
            self.turno = 0
    
class JakeGyllenhaal(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 45, 22, 175, 13, "Burning Red", 2)

        self.turno = 0

        self.fogo_image = atribui_imagem("fogo.png", 50)
        self.fogo_image = pygame.transform.rotate(self.fogo_image, -90)
        self.fogo_rect = self.fogo_image.get_rect()
        self.fogo = 0

        self.fire_image = atribui_imagem("fogo.png", 225)
        self.fire_rect = []
        for i in range(5):
            key = f"personagem{i + 1}"
            self.fire_rect.append((posicoes_jogo[key]["x"], posicoes_jogo[key]["y"]))
        self.fire = 0

            

    def animacao_habilidade(self, counter):
        return animacao_JakeGyllenhaal(self, counter)

    def animacao_ataque(self, counter, x, y):
        if(counter == 1):
            self.fogo_rect.x = self.x
            self.fogo_rect.y = self.y + 25
            self.fogo = 1

            self.fogo_image = atribui_imagem("fogo.png", 50)
            a = numpy.arctan((y - self.y) / (self.x - x)) * 180 / 3.14
            self.fogo_image = pygame.transform.rotate(self.fogo_image, a - 90)

            self.set_image("attack")

        
        self.fogo_rect.x += (x + 50 - self.x) / 50
        self.fogo_rect.y += (y + 25 - self.y) / 50

        if(counter > 50):
            self.set_image("default")
            self.fogo = 0
            return 0
        
        return counter + 1
    
    def desenhar(self, janela):
        janela.blit(self.image, self.rect)
        if(self.fogo): janela.blit(self.fogo_image, self.fogo_rect)
        if(self.fire):
            for i in range(self.fire):
                if self.fire >= 4 and i <= 2: continue
                janela.blit(self.fire_image, self.fire_rect[i])

    def habilidade(self, inimigos):
        for inimigo in inimigos:
            dano = 1.5 * self.dano * (50 / (50 + inimigo.get_defesa()))
            inimigo.recebe_dano(dano)

    def get_turno(self):
        return self.turno
    
    def set_turno(self):
        self.turno += 1
        if(self.turno > 3):
            self.turno = 0



def animacao(tipo, atacante, alvo_x, alvo_y, tela, aliado_x, aliado_y):
    counter = 1
    while counter >= 1:
        if(tipo == "ataque"):
            if atacante.get_nome() == "Ed Sheeran": counter = atacante.animacao_ataque(counter, alvo_x, alvo_y, aliado_x, aliado_y)
            else: counter = atacante.animacao_ataque(counter, alvo_x, alvo_y)
        if(tipo == "habilidade"): 
            if atacante.get_nome() == "Jake Gyllenhaal": counter = atacante.animacao_habilidade(counter)
            elif atacante.get_nome() == "John Mayer" or atacante.get_nome() == "Taylor Swift": counter = atacante.animacao_habilidade(counter, alvo_x, alvo_y)
            else: counter = atacante.animacao_habilidade(counter)
        if(counter == 1): break

        tela.desenha_animacao(atacante)

        pygame.display.flip()
        tela.clock_tick()