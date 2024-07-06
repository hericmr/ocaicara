import pygame as pg
import math

class Interface:
    def __init__(self, tela, personagem):
        self.tela = tela
        self.personagem = personagem

    def desenhar_texto(self, texto, posicao, cor=(255, 255, 255), tamanho=50):
        fonte = pg.font.SysFont('freesansbold.ttf', tamanho)
        superficie_texto = fonte.render(texto, True, cor)
        self.tela.blit(superficie_texto, posicao)
        pg.display.flip()

    def desenhar_caixa_texto(self):
        cor_fundo = (0, 34, 0)
        cor_borda = (0, 0, 0)
        retangulo = pg.Rect(0, self.tela.get_height() - 180, self.tela.get_width(), 180)
        pg.draw.rect(self.tela, cor_fundo, retangulo)
        pg.draw.rect(self.tela, cor_borda, retangulo, 3)

    def desenhar_barra_tempo(self, tempo_restante, comprimento_total=1319):
        largura_barra = int((tempo_restante / 10) * comprimento_total)
        cor = (0, 128, 0) if tempo_restante > 5 else (255, 0, 0)
        cor2 = (0, 0, 0)
        pg.draw.rect(self.tela, cor2, (0, 502, comprimento_total, 77))
        pg.draw.rect(self.tela, cor, (0, 502, largura_barra, 75))


    def animar_seta(self, posicao_inicial, posicao_final, duracao=1000):
        tempo_inicial = pg.time.get_ticks()
        while pg.time.get_ticks() - tempo_inicial < duracao:
            tempo_decorrido = pg.time.get_ticks() - tempo_inicial
            progressao = tempo_decorrido / duracao
            posicao_atual = (posicao_inicial[0] + (posicao_final[0] - posicao_inicial[0]) * progressao,
                             posicao_inicial[1] + (posicao_final[1] - posicao_inicial[1]) * progressao)
            self.tela.blit(self.tela, (0, 0))
            self.desenhar_seta(posicao_inicial, posicao_atual)
            pg.display.flip()
            pg.time.wait(10)

    def desenhar_seta(self, posicao_inicial, posicao_final):
        angulo = math.atan2(posicao_final[1] - posicao_inicial[1], posicao_final[0] - posicao_inicial[0])
        comprimento = 15  
        espessura = 2  
        cor = (255, 0, 0)  
        pg.draw.line(self.tela, cor, posicao_inicial, posicao_final, espessura)

        ponta1 = (posicao_final[0] - comprimento * math.cos(angulo - math.pi / 6),
                  posicao_final[1] - comprimento * math.sin(angulo - math.pi / 6))
        ponta2 = (posicao_final[0] - comprimento * math.cos(angulo + math.pi / 6),
                  posicao_final[1] - comprimento * math.sin(angulo + math.pi / 6))

        pg.draw.line(self.tela, cor, posicao_final, ponta1, espessura)
        pg.draw.line(self.tela, cor, posicao_final, ponta2, espessura)

    def __init__(self, tela, personagem):
        self.tela = tela
        self.personagem = personagem

    def desenhar_texto(self, texto, posicao, cor=(255, 255, 255), tamanho=50):
        fonte = pg.font.SysFont('freesansbold.ttf', tamanho)
        superficie_texto = fonte.render(texto, True, cor)
        self.tela.blit(superficie_texto, posicao)
        pg.display.flip()

    def desenhar_caixa_texto(self):
        cor_fundo = (0, 34, 0)
        cor_borda = (0, 0, 0)
        retangulo = pg.Rect(0, self.tela.get_height() - 180, self.tela.get_width(), 180)
        pg.draw.rect(self.tela, cor_fundo, retangulo)
        pg.draw.rect(self.tela, cor_borda, retangulo, 3)

    def desenhar_barra_tempo(self, tempo_restante, comprimento_total=1319):
        largura_barra = int((tempo_restante / 10) * comprimento_total)
        cor = (0, 128, 0) if tempo_restante > 5 else (255, 0, 0)
        cor2 = (0, 0, 0)
        pg.draw.rect(self.tela, cor2, (0, 502, comprimento_total, 77))
        pg.draw.rect(self.tela, cor, (0, 502, largura_barra, 75))
