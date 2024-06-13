import pygame

import numpy

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

    def animacao_ataque(self, counter, x, y):
        if(counter == 1):
            self.set_image("attack")

        self.rect.x += (x - self.x) / 70
        self.rect.y += (y - self.y) / 70

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


    def desenhar(self, janela):
        if self.invisivel > 0:
            self.image.set_alpha(69) 
        janela.blit(self.image, self.rect)


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
        self.cooldown -= 1

    def utiliza_habilidade(self):
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
        if(counter == 1): 
            self.rect.x = 350
            self.rect.y = 175
            self.set_image("skill")
        else: self.rect.x += 5

        if(counter > (largura - 300) / 5):
            self.rect.x = self.x
            self.rect.y = self.y
            self.set_image("default")
            return 0

        return counter + 1
    
    def habilidade(self, inimigos):
        for inimigo in inimigos:
            dano = 1.5 * self.dano * (50 / (50 + inimigo.get_defesa()))
            inimigo.recebe_dano(dano)
            

class TaylorLautner(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 40, 20, 225, 20, "Back to December", 4)

        self.neve_image =  pygame.image.load(f"./imagens/neve.png")
        h = self.neve_image.get_height()
        self.neve_image = pygame.transform.scale_by(self.neve_image, 225/h)

        self.neve_rect = []
        for i in range(4, 6):
            key = f"personagem{i}"
            self.neve_rect.append((posicoes_jogo[key]["x"] - 30, posicoes_jogo[key]["y"]))
        self.neve = 0

    def animacao_habilidade(self, counter):
        if(counter == 1): self.neve = 1

        if(counter == 30): self.neve = 2
        
        if(counter == 60):
            self.neve = 0
            return 0
        
        return counter + 1
    
    def desenhar(self, janela):
        janela.blit(self.image, self.rect)
        if(self.neve):
            for i in range(self.neve):
                janela.blit(self.neve_image, self.neve_rect[i])
    
    def habilidade(self, inimigos):
        for inimigo in inimigos:
            inimigo.congela()
            dano = 0.5 * self.dano * (50 / (50 + inimigo.get_defesa()))
            inimigo.recebe_dano(dano)

    
class TravisKelce(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 15, 40, 300, 5, "Touchdown", 4)

    def animacao_habilidade(self, counter):
        return counter
    
    def habilidade(self, inimigos):
        self.chamativo = 2

        self.set_image("skill")

class EdSheeran(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 25, 10, 120, 15, "End Game", 4)

        self.subtract_image = pygame.image.load(f"./imagens/subtract.jpeg")
        h = self.subtract_image.get_height()
        self.subtract_image = pygame.transform.scale_by(self.subtract_image, 25/h)
        self.subtract_rect = self.subtract_image.get_rect()
        self.subtract = 0

        self.plus_image = pygame.image.load(f"./imagens/plus.jpeg")
        h = self.plus_image.get_height()
        self.plus_image = pygame.transform.scale_by(self.plus_image, 25/h)
        self.plus_rect = self.plus_image.get_rect()
        self.plus = 0

    def animacao_habilidade(self, counter):
        return counter

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
            self.plus_rect.y = y + 50
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

class HarryStyles(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 35, 15, 150, 10, "I Know Places", 4)

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter, x, y):
        return counter
    
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
        super().__init__(nome, n, 2, 2, 100, 2, "Don't Blame Me", 2)

        self.roubado = ""

        self.aliado = 0

        self.ghost_image = pygame.image.load(f"./imagens/ghost.png")
        h = self.ghost_image.get_height()
        self.ghost_image = pygame.transform.scale_by(self.ghost_image, 150/h)
        self.ghost_rect = self.ghost_image.get_rect()
        self.ghost = 0

        self.fire_image = pygame.image.load(f"./imagens/fogo.png")
        h = self.fire_image.get_height()
        self.fire_image = pygame.transform.scale_by(self.fire_image, 225/h)
        self.fire_rect = []
        for i in range(4, 6):
            key = f"personagem{i}"
            self.fire_rect.append((posicoes_jogo[key]["x"], posicoes_jogo[key]["y"]))
        self.fire = 0


    def atribui_aliado(self, personagem):
        self.aliado = personagem

    def aliado_attack(self, inimigo, personagens, inimigos, clock, tela):
        if self.aliado != 0:
            animacao("ataque", self.aliado, inimigo.get_posicao_x(), inimigo.get_posicao_y(), personagens, inimigos, clock, tela, 0, 0)
            self.aliado.ataque(inimigo)

    def animacao_habilidade(self, counter, x, y):
        if self.roubado == "John Mayer": return animacao_JohnMayer(self, counter, x, y)
        if self.roubado == "Jake Gyllenhaal": return animacao_JakeGyllenhaal(self, counter)
    
    def habilidade_taylor(self, inimigo):
        self.habilidade = inimigo.habilidade
        self.roubado = inimigo.get_nome()

    def animacao_ataque(self, counter, x, y):
        return counter
    
    def get_roubado(self):
        return self.roubado
    
    def desenhar(self, janela):
        janela.blit(self.image, self.rect)
        if(self.ghost): janela.blit(self.ghost_image, self.ghost_rect)
        if(self.fire):
            for i in range(self.fire):
                if self.fire == 3: break
                janela.blit(self.fire_image, self.fire_rect[i])
  

class JohnMayer(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 35, 25, 225, 19, "", 2)

        self.turno = 0

        self.ghost_image = pygame.image.load(f"./imagens/ghost.png")
        h = self.ghost_image.get_height()
        self.ghost_image = pygame.transform.scale_by(self.ghost_image, 150/h)
        self.ghost_rect = self.ghost_image.get_rect()
        self.ghost = 0

        self.raio_image = pygame.image.load(f"./imagens/raio.png")
        self.raio = 0


    def animacao_habilidade(self, counter, x, y):
        return animacao_JohnMayer(self, counter, x, y)
    
    def animacao_ataque(self, counter, x, y):
        if counter == 1:
            self.set_image("attack")
            self.raio = 1


            w = self.raio_image.get_width()
            self.raio_rect = (x, y)
            d = ((self.x - x)**2 + (self.y - y)**2)**(1/2)
            self.raio_image = pygame.transform.scale_by(self.raio_image, d/w)
            a = numpy.arcsin((x - self.x) / d)
            self.raio_image = pygame.transform.rotate(self.raio_image, a)

        if counter >= 50: 
            self.set_image("default")
            self.raio = 0
            return 0

        return counter + 1
    
    def desenhar(self, janela):
        janela.blit(self.image, self.rect)
        if(self.ghost): janela.blit(self.ghost_image, self.ghost_rect)
        if(self.raio): janela.blit(self.raio_image, self.raio_rect)
    
    def habilidade(self, inimigos):
        inimigo = get_personagem_menos_vida(inimigos)
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
        super().__init__(nome, n, 45, 15, 175, 13, "", 2)

        self.turno = 0

        self.fogo_image = pygame.image.load(f"./imagens/fogo.png")
        h = self.fogo_image.get_height()
        self.fogo_image = pygame.transform.scale_by(self.fogo_image, 50/h)
        self.fogo_image = pygame.transform.rotate(self.fogo_image, -90)
        self.fogo_rect = self.fogo_image.get_rect()
        self.fogo = 0

        self.fire_image = pygame.image.load(f"./imagens/fogo.png")
        h = self.fire_image.get_height()
        self.fire_image = pygame.transform.scale_by(self.fire_image, 225/h)
        self.fire_rect = []
        for i in range(5):
            key = f"personagem{i + 1}"
            self.fire_rect.append((posicoes_jogo[key]["x"], posicoes_jogo[key]["y"]))
        self.fire = 0

            

    def animacao_habilidade(self, counter, taylor):
        return animacao_JakeGyllenhaal(self, counter)

    def animacao_ataque(self, counter, x, y):
        if(counter == 1):
            self.fogo_rect.x = self.x
            self.fogo_rect.y = self.y + 25
            self.fogo = 1

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



def animacao(tipo, atacante, alvo_x, alvo_y, personagens, inimigos, clock, tela, aliado_x, aliado_y):
    counter = 1
    while counter >= 1:
        if(tipo == "ataque"):
            if atacante.get_nome() == "Ed Sheeran": counter = atacante.animacao_ataque(counter, alvo_x, alvo_y, aliado_x, aliado_y)
            else: counter = atacante.animacao_ataque(counter, alvo_x, alvo_y)
        if(tipo == "habilidade"): 
            if atacante.get_nome() == "Jake Gyllenhaal": counter = atacante.animacao_habilidade(counter, 0)
            elif atacante.get_nome() == "John Mayer" or atacante.get_nome() == "Taylor Swift": counter = atacante.animacao_habilidade(counter, alvo_x, alvo_y)
            else: counter = atacante.animacao_habilidade(counter)
        if(counter == 1): break

        tela.desenha_animacao(atacante)


        # Atualizar a exibição
        pygame.display.flip()

        # Definir a taxa de quadros
        clock.tick(60)