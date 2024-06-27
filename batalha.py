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

        self.print_seta = 1

    def desenha(self, janela):
        pygame.draw.rect(janela, (255, 255, 255), self.rect)
        janela.blit(self.titulo, (titulo["x"], titulo["y"]))
        for i in range(len(self.texto)):
            janela.blit(self.texto[i], self.rect_texto[i])
        if self.print_seta: self.seta.desenha(janela)

    def retira_opcoes(self):
        for i in range(len(self.texto)):
            self.texto.remove(self.texto[0])
            self.rect_texto.remove(self.rect_texto[0])
            self.significado.remove(self.significado[0])

        self.qtd = 0

    def define_titulo(self, nome):
        fonte = pygame.font.Font(None, 42)
        self.titulo = fonte.render(f"{nome}'s turn", True, (0, 0, 0))

    def inic_selecao(self):
        self.retira_opcoes()
        self.seta.inicializa()
        self.print_seta = 1

    def selecao_habilidade(self, jogador):
        self.inic_selecao()

        frase = ""
        for key in posicoes_escolhas.keys():
            fonte = pygame.font.Font(None, 36)

            if(key == "escolha3" and jogador.habilidade_disponivel() == False): 
                frase = f"{jogador.get_cooldown()}"
                self.qtd -= 1

            if(key == "escolha1"): frase = "attack"
            if(key == "escolha2"): frase = "defend"
            if(key == "escolha3" and jogador.habilidade_disponivel() == True): frase = f"{jogador.get_nome_habilidade()}"
            if(key == "escolha4"): break

            texto = fonte.render(frase, True, (0, 0, 0))

            rect_texto = texto.get_rect()
            rect_texto.x = posicoes_escolhas[key]["x"]
            rect_texto.y = posicoes_escolhas[key]["y"]

            self.texto.append(texto)
            self.rect_texto.append(rect_texto)
            if(key == "escolha3"): frase = "skill"
            self.significado.append(frase)

            self.qtd += 1

    def selecao_inimigos(self, inimigos, habilidade):
        self.inic_selecao()
        
        i = 0
        for inimigo in inimigos:
            i += 1
            fonte = pygame.font.Font(None, 36)
            if not(habilidade): texto = fonte.render(inimigo.get_nome(), True, (0, 0, 0))
            if habilidade: texto = fonte.render(inimigo.get_nome_habilidade(), True, (0, 0, 0))

            rect_texto = texto.get_rect()
            rect_texto.x = posicoes_escolhas[f"escolha{i}"]["x"]
            rect_texto.y = posicoes_escolhas[f"escolha{i}"]["y"]

            self.texto.append(texto)
            self.rect_texto.append(rect_texto)
            self.significado.append(inimigo.get_nome())

            self.qtd += 1

    def selecao_aliados(self, aliados, personagem, mostrar_todos):
        self.inic_selecao()

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

    def set_print_seta_0(self):
        self.print_seta = 0


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


class Tela():

    def __init__(self, personagens, inimigos, janela, clock, escolhas, vidas):
        self.inimigos = inimigos
        self.janela = janela
        self.personagens = personagens 
        self.vidas = vidas
        self.escolhas = escolhas 
        self.clock = clock    

        self.fundo = pygame.image.load("./imagens/palco.png")

        w = self.fundo.get_width()
        self.fundo = pygame.transform.scale(self.fundo, (1024, 850))


    def desenha(self):
        self.janela.fill((0, 0, 0))
        self.janela.blit(self.fundo, (0, 0))

        for inimigo in self.inimigos:
            inimigo.desenhar(self.janela)
            
        for personagem in self.personagens:
            personagem.desenhar(self.janela)

        self.escolhas.desenha(self.janela)
        self.vidas.desenha(self.janela)

    def desenha_animacao(self, atacante):
        self.janela.fill((0, 0, 0))
        self.janela.blit(self.fundo, (0, 0))

        if(atacante.get_nome() == "Jake Gyllenhaal" or atacante.get_nome() == "John Mayer"):
            for personagem in self.personagens:
                personagem.desenhar(self.janela)

            for inimigo in self.inimigos:
                inimigo.desenhar(self.janela)
        else:
            for inimigo in self.inimigos:
                inimigo.desenhar(self.janela)

            for personagem in self.personagens:
                if atacante.get_nome() != personagem.get_nome(): personagem.desenhar(self.janela)

            for personagem in self.personagens:
                if atacante.get_nome() == personagem.get_nome(): personagem.desenhar(self.janela)
            
        self.escolhas.desenha(self.janela)
        self.vidas.desenha(self.janela)

    def atualiza_vidas(self):
        self.vidas.atualiza(self.personagens, self.inimigos)

    def atualiza_personagens(self):
        for inimigo in self.inimigos:
            if inimigo.get_vida_atual() <= 0: inimigo.morre()
            if inimigo.get_vivo() == 0: self.inimigos.remove(inimigo)
            
        for personagem in self.personagens:
            if personagem.get_vida_atual() <= 0: personagem.morre()
            if personagem.get_vivo() == 0: self.personagens.remove(personagem)

    def set_seta_printa_0(self):
        self.escolhas.set_print_seta_0()

    def clock_tick(self):
        self.clock.tick(60)     




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

        

def turno_inimigo(inimigo, personagens, tela):
    tela.set_seta_printa_0()
    if inimigo.get_congelado() <= 0:
        if(inimigo.get_turno() == 0 or inimigo.get_turno() == 2):
            alvo = get_personagem_menos_vida(personagens)
            animacao("ataque", inimigo, alvo.get_posicao_x(), alvo.get_posicao_y(), tela, 0, 0)
            inimigo.ataque(alvo)
        if(inimigo.get_turno() == 1):
            inimigo.defende()
        if(inimigo.get_turno() == 3):
                alvo = get_personagem_menos_vida(personagens)
                animacao("habilidade", inimigo, alvo.get_posicao_x(), alvo.get_posicao_y(), tela, 0, 0)
                if inimigo.get_nome() == "Jake Gyllenhaal": inimigo.habilidade(personagens)
                if inimigo.get_nome() == "John Mayer": inimigo.habilidade(alvo)
        inimigo.set_turno()

    inimigo.descongela()

    tela.atualiza_personagens()
    tela.atualiza_vidas()

    



def turno(jogador, personagens, inimigos, escolhas, tela):
    tela.atualiza_personagens()
    tela.atualiza_vidas()

    escolhas.define_titulo(jogador.get_nome())

    executando = True
    voltar = 0
    escolher_aliados = 0
    escolher_inimigos = 0
    habilidade = 0
    ataque = 0

    jogador.normaliza_chamativo()
    jogador.normaliza_defesa()
    jogador.diminui_invisibilidade()
    jogador.dano_veneno()


    if(jogador.get_nome() == "Jake Gyllenhaal" or jogador.get_nome() == "John Mayer"):
        escolhas.retira_opcoes()
        turno_inimigo(jogador, personagens, tela)
        return True
    
    escolhas.selecao_habilidade(jogador)
    jogador.cooldown_habilidade()
    while executando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False     
            if evento.type == pygame.KEYDOWN:
                escolhas.atualiza_seta(evento.key)

                if evento.key == pygame.K_x and voltar:
                    escolhas.selecao_habilidade(jogador)
                    voltar = 0
                    habilidade = 0
                    ataque = 0
                    if jogador.get_nome() == "Taylor Swift": jogador.set_roubado(" ")

                if evento.key == pygame.K_z:
                    acao = escolhas.get_significado_seta()

                    if acao == "defend":
                        jogador.defende()
                        return True
                    
                    if acao == "attack": 
                        escolhas.selecao_inimigos(inimigos, 0)
                        escolher_inimigos = 1
                        voltar = 1
                        ataque = 1
                            
                    if acao == "skill":
                        if jogador.get_nome() == "Taylor Swift":
                            escolhas.selecao_inimigos(inimigos, 1)
                            escolher_inimigos = 1
                            voltar = 1
                            habilidade = 1
                        else: 
                            animacao("habilidade", jogador, 0, 0, tela, 0, 0)
                            if jogador.get_nome() == "Ed Sheeran": 
                                jogador.habilidade(inimigos, personagens)
                                jogador.utiliza_habilidade()
                                return True
                            if jogador.get_nome() == "Harry Styles": 
                                escolhas.selecao_aliados(personagens, jogador, 0)
                                voltar = 1
                                escolher_aliados = 1
                            else:
                                jogador.habilidade(inimigos)
                                jogador.utiliza_habilidade()
                                return True
                        
                    if escolher_inimigos:
                        for inimigo in inimigos:
                            if acao == inimigo.get_nome():
                                escolher_inimigos = 0
                                if jogador.get_nome() == "Taylor Swift" and habilidade:
                                    if ataque:
                                        animacao("habilidade", jogador, inimigo.get_posicao_x(), inimigo.get_posicao_y(), tela, 0, 0)
                                        jogador.habilidade(inimigo)
                                        jogador.utiliza_habilidade()
                                        return True
                                    
                                    jogador.habilidade_taylor(inimigo)

                                    if inimigo.get_nome() == "John Mayer":
                                        escolhas.selecao_inimigos(inimigos, 0)
                                        escolher_inimigos = 1
                                        ataque = 1

                                    else:
                                        animacao("habilidade", jogador, 0, 0, tela, 0, 0)
                                        jogador.habilidade(inimigos)
                                        jogador.utiliza_habilidade()
                                        return True
                                    
                                elif jogador.get_nome() == "Ed Sheeran":
                                    enemy = inimigo 
                                    escolher_aliados = 1
                                    escolher_inimigos = 0
                                    escolhas.selecao_aliados(personagens, jogador, 1)

                                elif jogador.get_nome() == "Taylor Swift" and ataque:
                                    animacao("ataque", jogador, inimigo.get_posicao_x(), inimigo.get_posicao_y(), tela, 0, 0)
                                    jogador.aliado_attack(inimigo, tela)
                                    jogador.ataque(inimigo)
                                    return True
                                
                                else:
                                    animacao("ataque", jogador, inimigo.get_posicao_x(), inimigo.get_posicao_y(), tela, 0, 0)
                                    jogador.ataque(inimigo)
                                    return True

                    if escolher_aliados:
                        for personagem in personagens:
                            if acao == personagem.get_nome():
                                escolher_aliados = 0
                                if jogador.get_nome() == "Ed Sheeran":
                                    animacao("ataque", jogador, enemy.get_posicao_x(), enemy.get_posicao_y(), tela, personagem.get_posicao_x(), personagem.get_posicao_y())
                                    jogador.ataque(enemy, personagem)
                                else: 
                                    animacao("habilidade", jogador, 0, 0, tela, 0, 0)
                                    jogador.habilidade(personagem)
                                    jogador.utiliza_habilidade()
                                return True
                        

                   
                
        tela.atualiza_personagens()
        tela.atualiza_vidas()

        tela.desenha()

        pygame.display.flip()
        tela.clock_tick()


def batalha(personagens, inimigos, janela, clock):
    escolhas = Escolhas()
    vidas = Menu_Vida()
    tela = Tela(personagens, inimigos, janela, clock, escolhas, vidas)
 
    ordem = ordena_turnos(personagens, inimigos)

    index = 0
    executando = True
    while executando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        for personagem in personagens:
            if(ordem[index] == personagem.get_nome()):
                executando = turno(personagem, personagens, inimigos, escolhas, tela)

        for inimigo in inimigos:
            if(ordem[index] == inimigo.get_nome()):
                executando = turno(inimigo, personagens, inimigos, escolhas, tela)
        
        index += 1
        if index == 5: index = 0

        tela.atualiza_personagens()
        tela.atualiza_vidas()

        for inimigo in inimigos:
            if inimigo.get_vida_atual() <= 0: inimigo.morre()
            if inimigo.get_vivo() == 0: inimigos.remove(inimigo)
            
        for personagem in personagens:
            if personagem.get_vida_atual() <= 0: personagem.morre()
            if personagem.get_vivo() == 0: personagens.remove(personagem)

        i = 0
        for inimigo in inimigos:
            i += 1
        if i == 0: return False

        i = 0
        for personagem in personagens:
            i += 1
        if i == 0: return False
                

        tela.desenha()

        pygame.display.flip()
        clock.tick(60)