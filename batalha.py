from personagens import *

posicoes_escolhas = {"escolha1": {"x": 100, "y": 580}, 
                     "escolha2": {"x": 100, "y": 600},
                     "escolha3": {"x": 350, "y": 580},
                     "escolha4": {"x": 350, "y": 600},}

class Escolhas():
    
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect((50, 570), (600, 175))

    def desenha(self, janela):
        pygame.draw.rect(janela, (255, 255, 255), self.rect)