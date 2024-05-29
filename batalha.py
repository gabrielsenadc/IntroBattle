from personagens import *

titulo = {"x": 100, "y": 585}
posicoes_escolhas = {"escolha1": {"x": 100, "y": 645}, 
                     "escolha2": {"x": 350, "y": 645},
                     "escolha3": {"x": 100, "y": 699},
                     "escolha4": {"x": 350, "y": 699}}

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
            if (dir == pygame.K_DOWN and self.rect.x == (posicoes_escolhas["escolha1"]["x"]) - largura_seta):
                self.rect.y = posicoes_escolhas["escolha3"]["y"]
                self.rect.x = posicoes_escolhas["escolha3"]["x"] - largura_seta


    def get_posicao(self):
        i = 0
        for key in posicoes_escolhas.keys():
            i += 1
            if(self.rect.x == posicoes_escolhas[key]["x"] - largura_seta and self.rect.y == posicoes_escolhas[key]["y"]):
                return i

    

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

    def selecao_aliados(self, aliados, personagem):
        for aliado in aliados:
            if(aliado.get_nome() != personagem.get_nome()):
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
