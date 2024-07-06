import pygame as pg

class Personagem:
    def __init__(self, imagem_path, posicao_inicial, tamanho):
        self.imagem = pg.image.load(imagem_path)
        self.imagem = pg.transform.scale(self.imagem, tamanho)
        self.posicao = posicao_inicial

    def desenhar(self, tela):
        tela.blit(self.imagem, self.posicao)

    def mover(self, nova_posicao):
        self.posicao = nova_posicao