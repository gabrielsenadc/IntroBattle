from personagens import *


posicoes_escolhas = {"titulo": {"x": 100, "y": 585},
                     "escolha1": {"x": 100, "y": 645}, 
                     "escolha2": {"x": 100, "y": 699},
                     "escolha3": {"x": 350, "y": 645},
                     "escolha4": {"x": 350, "y": 699}}

altura_seta = 14

class Seta_Escolha():
    
    def __init__(self, posicoes_escolhas):
        self.image = pygame.image.load("./imagens/seta.png")
        self.rect = self.image.get_rect()

        h = self.image.get_height()
        self.image = pygame.transform.scale_by(self.image, altura_seta/h)

        self.rect.x = posicoes_escolhas["escolha1"]["x"] 
        self.rect.y = posicoes_escolhas["escolha1"]["y"] - altura_seta

    def deseha(self, janela):
        janela.blit(self.image, self.rect)

    

class Escolhas():
    
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect((50, 570), (600, 175))

        self.seta = Seta_Escolha(posicoes_escolhas)

        self.texto = []
        self.rect_texto = []
        frase = ""
        for key in posicoes_escolhas.keys():
            if(key == "titulo"): fonte = pygame.font.Font(None, 42)
            else: fonte = pygame.font.Font(None, 36)

            if(key == "titulo"): frase = "Taylor Swift's turn"  
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

    def desenha(self, janela):
        pygame.draw.rect(janela, (255, 255, 255), self.rect)
        for i in range(len(self.texto)):
            janela.blit(self.texto[i], self.rect_texto[i])
        self.seta.deseha(janela)