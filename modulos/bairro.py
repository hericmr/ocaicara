import pygame as pg

class Bairro:
    def __init__(self, nome, posicoes):
        self.nome = nome
        self.posicoes = posicoes
        self.ponto_central = self.calcular_ponto_central()

    def calcular_ponto_central(self):
        soma_x = sum(pos[0] for pos in self.posicoes)
        soma_y = sum(pos[1] for pos in self.posicoes)
        media_x = soma_x / len(self.posicoes)
        media_y = soma_y / len(self.posicoes)
        return (media_x, media_y)

    def desenhar(self, tela, cor=(0, 255, 0, 180)):
        poligono_bairro = pg.Surface((max(self.posicoes, key=lambda x: x[0])[0] - min(self.posicoes, key=lambda x: x[0])[0],
                                      max(self.posicoes, key=lambda x: x[1])[1] - min(self.posicoes, key=lambda x: x[1])[1]), 
                                      pg.SRCALPHA)
        pg.draw.polygon(poligono_bairro, cor, [(pos[0] - min(self.posicoes, key=lambda x: x[0])[0],
                                                pos[1] - min(self.posicoes, key=lambda x: x[1])[1]) for pos in self.posicoes])
        tela.blit(poligono_bairro, (min(self.posicoes, key=lambda x: x[0])[0], min(self.posicoes, key=lambda x: x[1])[1]))
