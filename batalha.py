import pygame

import math

from personagens import *

titulo = {"x": 100, "y": 585}
posicoes_escolhas = {"escolha1": {"x": 100, "y": 645}, 
                     "escolha2": {"x": 350, "y": 645},
                     "escolha3": {"x": 100, "y": 699},
                     "escolha4": {"x": 350, "y": 699}}

posicoes_vida = {"vida1": {"x": 710, "y": 575},
                 "vida2": {"x": 710, "y": 610},
                 "vida3": {"x": 710, "y": 645},
                 "vida4": {"x": 710, "y": 680},
                 "vida5": {"x": 710, "y": 715},}

largura_seta = 24

class Seta_Escolha():
    
    def __init__(self, posicoes_escolhas):
        self.image = pygame.image.load("./imagens/seta.png")
        self.rect = self.image.get_rect()

        w = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, largura_seta/w)
        self.image = pygame.transform.rotate(self.image, 90)

        self.rect.x = posicoes_escolhas["escolha1"]["x"] - largura_seta
        self.rect.y = posicoes_escolhas["escolha1"]["y"] 

    def desenha(self, janela):
        janela.blit(self.image, self.rect)

    def atualiza(self, dir, qtd):
        if qtd >= 2:
            if (dir == pygame.K_RIGHT and self.rect.x == (posicoes_escolhas["escolha1"]["x"] - largura_seta) and self.rect.y == posicoes_escolhas["escolha1"]["y"]):
                self.rect.x = posicoes_escolhas["escolha2"]["x"] - largura_seta
            if (dir == pygame.K_LEFT and self.rect.x == posicoes_escolhas["escolha2"]["x"] - largura_seta):
                self.rect.x = posicoes_escolhas["escolha1"]["x"] - largura_seta

        if qtd >= 3:
            if (dir == pygame.K_UP and self.rect.y == posicoes_escolhas["escolha3"]["y"]):
                self.rect.y = posicoes_escolhas["escolha1"]["y"]
            if (dir == pygame.K_DOWN and self.rect.y == (posicoes_escolhas["escolha1"]["y"])):
                self.rect.y = posicoes_escolhas["escolha3"]["y"]
                self.rect.x = posicoes_escolhas["escolha3"]["x"] - largura_seta

    def inicializa(self):
        self.rect.x = posicoes_escolhas["escolha1"]["x"] - largura_seta
        self.rect.y = posicoes_escolhas["escolha1"]["y"] 

    def get_posicao(self):
        i = 0
        for key in posicoes_escolhas.keys():
            if(self.rect.x == posicoes_escolhas[key]["x"] - largura_seta and self.rect.y == posicoes_escolhas[key]["y"]): return i
            i += 1

    

class Escolhas():
    
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect((50, 570), (600, 175))

        self.seta = Seta_Escolha(posicoes_escolhas)

        self.texto = []
        self.rect_texto = []
        self.significado = []

        self.qtd = 0

    def desenha(self, janela):
        pygame.draw.rect(janela, (255, 255, 255), self.rect)
        janela.blit(self.titulo, (titulo["x"], titulo["y"]))
        for i in range(len(self.texto)):
            janela.blit(self.texto[i], self.rect_texto[i])
        self.seta.desenha(janela)

    def retita_opcoes(self):
        for i in range(self.qtd):
            self.texto.remove(self.texto[0])
            self.rect_texto.remove(self.rect_texto[0])
            self.significado.remove(self.significado[0])

        self.qtd = 0

    def define_titulo(self, nome):
        fonte = pygame.font.Font(None, 42)
        self.titulo = fonte.render(f"{nome}'s turn", True, (0, 0, 0))

    def selecao_habilidade(self):
        self.retita_opcoes()
        self.seta.inicializa()

        frase = ""
        for key in posicoes_escolhas.keys():
            fonte = pygame.font.Font(None, 36)

            if(key == "escolha1"): frase = "attack"
            if(key == "escolha2"): frase = "defend"
            if(key == "escolha3"): frase = "skill"
            if(key == "escolha4"): break

            texto = fonte.render(frase, True, (0, 0, 0))

            rect_texto = texto.get_rect()
            rect_texto.x = posicoes_escolhas[key]["x"]
            rect_texto.y = posicoes_escolhas[key]["y"]

            self.texto.append(texto)
            self.rect_texto.append(rect_texto)
            self.significado.append(frase)

            self.qtd += 1

    def selecao_inimigos(self, inimigos):
        self.retita_opcoes()
        self.seta.inicializa()
        
        i = 0
        for inimigo in inimigos:
            i += 1
            fonte = pygame.font.Font(None, 36)
            texto = fonte.render(inimigo.get_nome(), True, (0, 0, 0))

            rect_texto = texto.get_rect()
            rect_texto.x = posicoes_escolhas[f"escolha{i}"]["x"]
            rect_texto.y = posicoes_escolhas[f"escolha{i}"]["y"]

            self.texto.append(texto)
            self.rect_texto.append(rect_texto)
            self.significado.append(inimigo.get_nome())

            self.qtd += 1

    def selecao_aliados(self, aliados, personagem, mostrar_todos):
        self.retita_opcoes()
        self.seta.inicializa()

        i = 0
        for aliado in aliados:
            if(aliado.get_nome() != personagem.get_nome() or mostrar_todos):
                i += 1
                fonte = pygame.font.Font(None, 36)
                texto = fonte.render(aliado.get_nome(), True, (0, 0, 0))

                rect_texto = texto.get_rect()
                rect_texto.x = posicoes_escolhas[f"escolha{i}"]["x"]
                rect_texto.y = posicoes_escolhas[f"escolha{i}"]["y"]

                self.texto.append(texto)
                self.rect_texto.append(rect_texto)
                self.significado.append(aliado.get_nome())

                self.qtd += 1


    def get_significado_seta(self):
        return self.significado[self.seta.get_posicao()]
    
    def atualiza_seta(self, dir):
        self.seta.atualiza(dir, self.qtd)


class Menu_Vida():

    def __init__(self):
        self.rect = pygame.Rect((700, 570), (300, 175))

        self.texto = []
        self.rect_texto = []

    def desenha(self, janela):
        pygame.draw.rect(janela, (255, 255, 255), self.rect)
        for i in range(len(self.texto)):
            janela.blit(self.texto[i], self.rect_texto[i])

    def remove_texto(self):
        qtd = len(self.texto)

        for i in range(qtd):
            self.texto.pop(0)
            self.rect_texto.pop(0)       

    def atualiza(self, personagens, inimigos):
        self.remove_texto()

        i = 0
        fonte = pygame.font.Font(None, 24)
        for personagem in personagens:
            i += 1
            key = f"vida{i}"

            texto = fonte.render(f"{personagem.get_nome()}: {math.ceil(personagem.get_vida_atual())} / {personagem.get_vida_max()}", True, (0, 0, 0))

            rect_texto = texto.get_rect()
            rect_texto.x = posicoes_vida[key]["x"]
            rect_texto.y = posicoes_vida[key]["y"]

            self.texto.append(texto)
            self.rect_texto.append(rect_texto)

        for inimigo in inimigos:
            i += 1
            key = f"vida{i}"

            texto = fonte.render(f"{inimigo.get_nome()}: {math.ceil(inimigo.get_vida_atual())} / {inimigo.get_vida_max()}", True, (0, 0, 0))

            rect_texto = texto.get_rect()
            rect_texto.x = posicoes_vida[key]["x"]
            rect_texto.y = posicoes_vida[key]["y"]

            self.texto.append(texto)
            self.rect_texto.append(rect_texto)




def ordena_turnos(personagens, inimigos):
    ordem = []
    velocidades = []

    for personagem in personagens:
        index = 0
        for i in range(len(ordem)):
            if (personagem.get_velocidade() > velocidades[i]):
                break
            index += 1
        ordem.insert(index, personagem.get_nome())
        velocidades.insert(index, personagem.get_velocidade())

    for inimigo in inimigos:
        index = 0
        for i in range(len(ordem)):
            if (inimigo.get_velocidade() > velocidades[i]): 
                break
            index += 1
        ordem.insert(index, inimigo.get_nome())
        velocidades.insert(index, inimigo.get_velocidade())

    return ordem


def turno(jogador, personagens, inimigos, janela, clock, escolhas, vidas):
    escolhas.define_titulo(jogador.get_nome())
    escolhas.selecao_habilidade()

    executando = True
    acao = ""
    voltar = 0
    escolher_aliados = 0
    escolher_inimigos = 0

    enemy = ""

    jogador.normaliza_defesa()
    if jogador.get_envenenado():
        jogador.dano_veneno()

    if(jogador.get_nome() == "Jake Gyllenhaal" or jogador.get_nome() == "John Mayer"): return True
    while executando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False     
            if evento.type == pygame.KEYDOWN:
                escolhas.atualiza_seta(evento.key)
                if evento.key == pygame.K_x and voltar:
                    escolhas.selecao_habilidade()
                    voltar = 0
                if evento.key == pygame.K_z:
                    acao = escolhas.get_significado_seta()

                    if acao == "defend":
                        jogador.defende()
                        return True
                    
                    if acao == "attack": 
                        escolhas.selecao_inimigos(inimigos)
                        escolher_inimigos = 1
                        voltar = 1
                            
                    if acao == "skill":
                        animacao("habilidade", jogador, 0, 0, personagens, inimigos, clock, janela, escolhas, vidas)
                        if jogador.get_nome() == "Ed Sheeran": 
                            jogador.habilidade(inimigos, personagens)
                            return True
                        if jogador.get_nome() == "Harry Styles": 
                            escolhas.selecao_aliados(personagens, jogador, 0)
                            voltar = 1
                            escolher_aliados = 1
                        else:
                            jogador.habilidade(inimigos)
                            return True
                        
                    if escolher_inimigos:
                        for inimigo in inimigos:
                            if acao == inimigo.get_nome():
                                escolher_inimigos = 0
                                animacao("ataque", jogador, inimigo.get_posicao_x(), inimigo.get_posicao_y(), personagens, inimigos, clock, janela, escolhas, vidas)
                                if jogador.get_nome() == "Ed Sheeran":
                                    enemy = inimigo 
                                    escolher_aliados = 1
                                    escolhas.selecao_aliados(personagens, jogador, 1)
                                else:
                                    jogador.ataque(inimigo)
                                    return True

                    if escolher_aliados:
                        for personagem in personagens:
                            if acao == personagem.get_nome():
                                escolher_aliados = 0
                                if jogador.get_nome() == "Ed Sheeran":
                                    animacao("ataque", jogador, inimigo.get_posicao_x(), inimigo.get_posicao_y(), personagens, inimigos, clock, janela, escolhas, vidas)
                                    jogador.ataque(enemy, personagem)
                                else: 
                                    animacao("habilidade", jogador, 0, 0, personagens, inimigos, clock, janela, escolhas, vidas)
                                    jogador.habilidade(personagem)
                                return True
                        

                   
                
        # Preencher a janela com a cor de fundo
        janela.fill((0, 0, 0))

        # Atualizar o jogador
        for inimigo in inimigos:
            if inimigo.get_vida_atual() <= 0: inimigo.morre()
            if inimigo.get_vivo() == 0: inimigos.remove(inimigo)
            inimigo.desenhar(janela)
            
        for personagem in personagens:
            if personagem.get_vida_atual() <= 0: personagem.morre()
            if personagem.get_vivo() == 0: personagens.remove(personagem)
            personagem.desenhar(janela)

        vidas.atualiza(personagens, inimigos)

        escolhas.desenha(janela)
        vidas.desenha(janela)

        i = 0
        for inimigo in inimigos:
            i += 1
        if i == 0: return False


        pygame.display.flip()
        clock.tick(60)


def batalha(personagens, inimigos, janela, clock):
    escolhas = Escolhas()
    vidas = Menu_Vida()
 
    ordem = ordena_turnos(personagens, inimigos)
    print(ordem)

    index = 0
    executando = True
    while executando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        for personagem in personagens:
            if(ordem[index] == personagem.get_nome()):
                executando = turno(personagem, personagens, inimigos, janela, clock, escolhas, vidas)

        for inimigo in inimigos:
            if(ordem[index] == inimigo.get_nome()):
                executando = turno(inimigo, personagens, inimigos, janela, clock, escolhas, vidas)
        
        index += 1
        if index == 5: index = 0
                
        # Preencher a janela com a cor de fundo
        janela.fill((0, 0, 0))

        # Atualizar o jogador
        for inimigo in inimigos:
            inimigo.desenhar(janela)
            
        for personagem in personagens:
            personagem.desenhar(janela)



        pygame.display.flip()
        clock.tick(60)