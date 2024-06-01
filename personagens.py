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

        self.vivo = 1

        self.cooldown = 0

    def animacao_ataque(self, counter, x, y):
        if(counter == 1):
            self.image = pygame.image.load(f"./imagens/{self.nome}/attack.png")
            h = self.image.get_height()
            self.image = pygame.transform.scale_by(self.image, 225/h)

        self.rect.x += (x - self.x) / 70
        self.rect.y += (y - self.y) / 70

        if(counter == 70): 
            self.image = pygame.image.load(f"./imagens/{self.nome}/default.png")
            h = self.image.get_height()
            self.image = pygame.transform.scale_by(self.image, 225/h)
            self.rect.x = self.x
            self.rect.y = self.y
            return 0
         
        return counter + 1
    
    def ataque(self, inimigo):
        dano = self.dano * (50 / (50 + inimigo.get_defesa()))
        inimigo.recebe_dano(dano)


    def desenhar(self, janela):
        janela.blit(self.image, self.rect)

    ### Setters ###

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
        self.image = pygame.image.load(f"./imagens/{self.nome}/congelado.png" )

        h = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, 225/h)
    
    def descongela(self):
        self.congelado -= 1

        if self.congelado <= 0:
            self.image = pygame.image.load(f"./imagens/{self.nome}/default.png" )

            h = self.image.get_height()
            self.image = pygame.transform.scale_by(self.image, 225/h)

    def invisibilidade(self):
        self.invisivel = 2

    def diminui_invisibilidade(self):
        self.invisivel -= 1

    def envenena(self):
        self.envenenado = 2

    def dano_veneno(self):
        self.envenenado -= 1
        self.recebe_dano(35 * 0.25)

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
    
    ## Getters ###

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
    

class TomHiddleston(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 30, 15, 200, 25, "Getaway Car", 2)

    def animacao_habilidade(self, counter):
        if(counter == 1): 
            self.rect.x = 350
            self.rect.y = 175
            self.image = pygame.image.load(f"./imagens/Tom Hiddleston/habilidade.png")
            h = self.image.get_height()
            self.image = pygame.transform.scale_by(self.image, 225/h)
        else: self.rect.x += 5

        if(counter > (largura - 300) / 5):
            self.rect.x = self.x
            self.rect.y = self.y
            self.image = pygame.image.load(f"./imagens/Tom Hiddleston/default.png")
            h = self.image.get_height()
            self.image = pygame.transform.scale_by(self.image, 225/h)
            return 0

        return counter + 1
    
    def habilidade(self, inimigos):
        for inimigo in inimigos:
            dano = 1.5 * self.dano * (50 / (50 + inimigo.get_defesa()))
            inimigo.recebe_dano(dano)
            

class TaylorLautner(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 40, 20, 225, 20, "Back to December", 4)

    def animacao_habilidade(self, counter):
        return counter
    
    def habilidade(self, inimigos):
        for inimigo in inimigos:
            inimigo.congela()
            dano = 0.5 * self.dano * (50 / (50 + inimigo.get_defesa()))
            inimigo.recebe_dano(dano)

    
class TaylorSwift(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 2, 2, 2, 2, "", 2)

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter, x, y):
        return counter

class TravisKelce(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 15, 40, 300, 5, "", 4)

    def animacao_habilidade(self, counter):
        return counter


class EdSheeran(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 25, 10, 120, 15, "End Game", 4)

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter, x, y):
        return counter
    
    def ataque(self, inimigo, aliado):
        dano = self.dano * (50 / (50 + inimigo.get_defesa()))
        inimigo.recebe_dano(dano)
        aliado.recupera_vida(dano * 0.5)

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
        self.invisibilidade()
        aliado.invisibilidade()
        

class JohnMayer(Personagem):
    def __init__(self, nome, n):
        super().__init__(nome, n, 35, 25, 225, 13, "", 2)

        self.turno = 0

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter, x, y):
        return counter
    
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
        super().__init__(nome, n, 45, 15, 175, 12, "", 2)

        self.turno = 0

        self.fogo_image = pygame.image.load(f"./imagens/fogo.png")
        h = self.fogo_image.get_height()
        self.fogo_image = pygame.transform.scale_by(self.fogo_image, 50/h)
        self.fogo_image = pygame.transform.rotate(self.fogo_image, -90)
        self.fogo_rect = self.fogo_image.get_rect()
        self.fogo = 0

    def animacao_habilidade(self, counter):
        return counter

    def animacao_ataque(self, counter, x, y):
        if(counter == 1):
            self.fogo_rect.x = posicoes_jogo["personagem4"]["x"]
            self.fogo_rect.y = posicoes_jogo["personagem4"]["y"] + 25
            self.fogo = 1

            self.image = pygame.image.load(f"./imagens/Jake Gyllenhaal/attack.png")
            h = self.image.get_height()
            self.image = pygame.transform.scale_by(self.image, 225/h)

        
        self.fogo_rect.x += (x + 50 - self.x) / 50
        self.fogo_rect.y += (y + 25 - self.y) / 50

        if(counter > 50):
            self.image = pygame.image.load(f"./imagens/Jake Gyllenhaal/default.png")
            h = self.image.get_height()
            self.image = pygame.transform.scale_by(self.image, 225/h)
            self.fogo = 0
            return 0
        
        return counter + 1
    
    def desenhar(self, janela):
        janela.blit(self.image, self.rect)
        if(self.fogo): janela.blit(self.fogo_image, self.fogo_rect)

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



def animacao(tipo, atacante, alvo_x, alvo_y, personagens, inimigos, clock, janela, escolhas, vidas):
    counter = 1
    while counter >= 1:
        if(tipo == "ataque"): counter = atacante.animacao_ataque(counter, alvo_x, alvo_y)
        if(tipo == "habilidade"): counter = atacante.animacao_habilidade(counter)
        if(counter == 1): break

        # Preencher a janela com a cor de fundo
        janela.fill((0, 0, 0))

        # Atualizar o jogador
        if(atacante.get_nome() == "Jake Gyllenhaal" or atacante.get_nome() == "John Mayer"):
            for personagem in personagens:
                personagem.desenhar(janela)

            for inimigo in inimigos:
                inimigo.desenhar(janela)
        else:
            for inimigo in inimigos:
                inimigo.desenhar(janela)

            for personagem in personagens:
                personagem.desenhar(janela)
            
        escolhas.desenha(janela)
        vidas.desenha(janela)


        # Atualizar a exibição
        pygame.display.flip()

        # Definir a taxa de quadros
        clock.tick(60)