import pygame as pg

class Audio:
    def __init__(self):
        pg.mixer.init()
        self.musica_de_fundo = 'musica.ogg'
        self.efeitos = {}

    def carregar_musica_de_fundo(self, caminho):
        self.musica_de_fundo = caminho
        pg.mixer.music.load(self.musica_de_fundo)
        pg.mixer.music.play(-1)

    def adicionar_efeito_sonoro(self, nome, caminho):
        self.efeitos[nome] = pg.mixer.Sound(caminho)

    def tocar_efeito_sonoro(self, nome):
        if nome in self.efeitos:
            self.efeitos[nome].play()
