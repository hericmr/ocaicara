import random
import math
import pygame as pg
import sys
from modulos.personagem import Personagem
from modulos.bairro import Bairro
from modulos.interface import Interface
from modulos.audio import Audio
from modulos.lista_bairros import bairros


class Jogo:
    def __init__(self):
        pg.init()
        pg.display.set_caption("O CAIÇARA")
        self.largura_tela = 1319
        self.altura_tela = 680
        self.tela = pg.display.set_mode((self.largura_tela, self.altura_tela))
        self.chorao = Personagem('recursos/chorao.png', (-200, 50), (700, 700))
        self.interface = Interface(self.tela, self.chorao)
        self.audio = Audio()
        self.audio.carregar_musica_de_fundo('recursos/musica.ogg')
        self.bairros = self.carregar_bairros()
        self.pontos_centrais = self.calcular_pontos_centrais()
        self.bandeira = pg.image.load('recursos/bandeira2.png')
        self.mapa = self.carregar_mapa()
        self.pontuacao = 0
        self.distanciamento_acumulado = 0 

    def animar_movimento_chorao(self, posicao_final, duracao):
        posicao_inicial = (-self.chorao.imagem.get_width(), posicao_final[1])
        tempo_inicial = pg.time.get_ticks()
        while pg.time.get_ticks() - tempo_inicial < duracao:
            tempo_decorrido = pg.time.get_ticks() - tempo_inicial
            progressao = tempo_decorrido / duracao

            posicao_atual = (
                posicao_inicial[0] + (posicao_final[0] - posicao_inicial[0]) * progressao,
                posicao_inicial[1]  
            )

            tamanho_atual = max(1, int(self.chorao.imagem.get_width() * (1 - progressao)))  
            personagem_redimensionado = pg.transform.scale(self.chorao.imagem, (tamanho_atual, tamanho_atual))

            self.tela.blit(self.mapa, (0, 0))  
            self.interface.desenhar_caixa_texto()
            self.tela.blit(personagem_redimensionado, posicao_atual)  
            pg.display.flip()  
            pg.time.wait(10)  

    def carregar_bairros(self):
        return bairros
    
    def animar_bairro(self, bairro):
        duracao = 500  
        tempo_inicial = pg.time.get_ticks()
        
        while pg.time.get_ticks() - tempo_inicial < duracao:
            tempo_decorrido = pg.time.get_ticks() - tempo_inicial
            progressao = tempo_decorrido / duracao
            cor_opaca = (0, 255, 0, int(180 * progressao))
            self.tela.blit(self.mapa, (0, 0)) 
            bairro.desenhar(self.tela, cor=cor_opaca)
            pg.display.flip()
            pg.time.wait(10)

    def carregar_mapa(self):
        return pg.image.load("recursos/map.png")

    def calcular_pontos_centrais(self):
        pontos_centrais = {}
        for bairro, dados in self.bairros.items():
            posicoes = dados['posicao']
            ponto_central = self.calcular_ponto_central(posicoes)
            pontos_centrais[bairro] = ponto_central
        return pontos_centrais

    def calcular_ponto_central(self, posicoes):
        soma_x = sum(pos[0] for pos in posicoes)
        soma_y = sum(pos[1] for pos in posicoes)
        media_x = soma_x / len(posicoes)
        media_y = soma_y / len(posicoes)
        return (media_x, media_y)

    def desenhar_contador(self, texto, posicao):
        fonte = pg.font.Font('freesansbold.ttf', 16)
        superficie_texto = fonte.render(texto, 5, (0, 0, 0))
        self.tela.blit(superficie_texto, posicao)

    def desenhar_seta(self, posicao_inicial, posicao_final):
        angulo = math.atan2(posicao_final[1] - posicao_inicial[1], posicao_final[0] - posicao_inicial[0])
        comprimento = 5
        pg.draw.line(self.tela, (255, 0, 0), posicao_inicial, posicao_final, 3)
        ponta1 = (posicao_final[0] - comprimento * math.cos(angulo - math.pi / 6),
                  posicao_final[1] - comprimento * math.sin(angulo - math.pi / 6))
        ponta2 = (posicao_final[0] - comprimento * math.cos(angulo + math.pi / 6),
                  posicao_final[1] - comprimento * math.sin(angulo + math.pi / 6))
        pg.draw.line(self.tela, (255, 0, 0), posicao_final, ponta1, 3)
        pg.draw.line(self.tela, (255, 0, 0), posicao_final, ponta2, 3)

    def desenhar_pontuacao(self):
        fonte_pontuacao = pg.font.SysFont('freesansbold.ttf', 26)
        texto_pontuacao = fonte_pontuacao.render(f'Pontuação: {int(self.pontuacao)}', True, (255, 255, 255))
        self.tela.blit(texto_pontuacao, (10, 10))

    def calcular_pontuacao(self, comprimento_seta, tempo_decorrido):
        if comprimento_seta > 50:
            pontuacao = - (comprimento_seta * 2) * (tempo_decorrido / 40)
        else:
            pontuacao = (comprimento_seta) * (10 / tempo_decorrido)
        return pontuacao

    def game_over(self):
        self.interface.desenhar_caixa_texto()
        fonte_aperte_s = pg.font.SysFont('freesansbold.ttf', 36)
        texto_aperte_s = fonte_aperte_s.render('Você perdeu. Quer jogar de novo? S/N', True, (255, 255, 255))
        posicao_aperte_s = ((self.tela.get_width() - texto_aperte_s.get_width()) // 2, self.tela.get_height() - 50)
        self.tela.blit(texto_aperte_s, posicao_aperte_s)
        pg.display.flip()

        while True:
            for evento in pg.event.get():
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_s:
                        return True  
                    elif evento.key == pg.K_n:
                        return False  

    def parabens(self):
        pg.mixer.music.stop()

        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif evento.type == pg.KEYDOWN and evento.key == pg.K_RETURN:
                    pg.mixer.music.play(-1)
                    return True 

            cor_fundo = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.tela.fill(cor_fundo)

            self.interface.desenhar_texto("Parabéns!", ((self.tela.get_width() - 200) // 2, (self.tela.get_height() - 100) // 2), cor=(255, 255, 255), tamanho=80)

            tamanho_personagem = (random.randint(50, 150), random.randint(50, 150))
            posicao_personagem = (random.randint(0, self.largura_tela - tamanho_personagem[0]), random.randint(0, self.altura_tela - tamanho_personagem[1]))
            personagem_redimensionado = pg.transform.scale(self.chorao.imagem, tamanho_personagem)
            self.tela.blit(personagem_redimensionado, posicao_personagem)

            pg.display.flip()
            pg.time.wait(300)

            pg.mixer.music.stop()
            for i in range(999):
                cor_fundo = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.tela.fill(cor_fundo)
                
                self.interface.desenhar_texto("Parabéns!", ((self.tela.get_width() - 200) // 2, (self.tela.get_height() - 100) // 2), cor=(255, 255, 255), tamanho=80)
                
                tamanho_personagem = (random.randint(50, 150), random.randint(50, 150))
                posicao_personagem = (random.randint(0, self.largura_tela - tamanho_personagem[0]), random.randint(0, self.altura_tela - tamanho_personagem[1]))
                personagem_redimensionado = pg.transform.scale(self.chorao.imagem, tamanho_personagem)
                self.tela.blit(personagem_redimensionado, posicao_personagem)
                
                pg.display.flip()
                pg.time.wait(100)
            
            pg.mixer.music.play(-1)
            return True


    def introducao(self, texto_titulo):
        iniciar_jogo = False
        sair = False
        i = 0

        while not iniciar_jogo and not sair:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif evento.type == pg.MOUSEBUTTONDOWN:
                    posicao_mouse = pg.mouse.get_pos()
                    if 200 <= posicao_mouse[0] <= 400 and 550 <= posicao_mouse[1] <= 650:
                        iniciar_jogo = True
                    elif 600 <= posicao_mouse[0] <= 1200 and 550 <= posicao_mouse[1] <= 650:
                        sair = True

            self.tela.blit(self.mapa, (0, 0))

            tamanho_personagem = int(i / 1)
            posicao_personagem = (100 + i * 2, 50 + i * 0.6)
            personagem_redimensionado = pg.transform.scale(self.chorao.imagem, (tamanho_personagem, tamanho_personagem))
            self.tela.blit(personagem_redimensionado, posicao_personagem)

            self.tela.blit(texto_titulo, ((self.tela.get_width() - texto_titulo.get_width()) // 2, 50))

            self.interface.desenhar_caixa_texto()
            pg.draw.rect(self.tela, (0, 128, 0), (540, 550, 250, 100))
            fonte_botao = pg.font.SysFont('freesansbold.ttf', 50)
            texto_botao = fonte_botao.render('Iniciar Jogo', True, (0, 0, 0))
            posicao_botao = (570, 575)
            self.tela.blit(texto_botao, posicao_botao) 

            texto_temp = 'Aprenda a geografia de Santos. Encontre os bairros da cidade!'
            self.interface.desenhar_texto(texto_temp, (85, 510))

            pg.display.flip()
            pg.time.wait(4)

            self.tela.blit(texto_titulo, ((self.tela.get_width() - texto_titulo.get_width()) // 2, 50))
            i += 1

            if i >= 500:
                i = 0

        return iniciar_jogo

    def loop_jogo_principal(self):
        lista_bairros = list(self.bairros.keys())
        self.tela.blit(self.mapa, (0, 0))
        relogio = pg.time.Clock()
        relogio.tick(60)
        fonte_titulo = pg.font.SysFont(None, 120)
        texto_titulo = fonte_titulo.render("O CAIÇARA", True, (255, 255, 255))

        self.introducao(texto_titulo)

        pg.display.flip()
        pg.time.wait(1000)

        while True:
            contador = 10
            self.interface.desenhar_barra_tempo(contador)
            bairro_aleatorio = random.choice(lista_bairros)
            bairro_clicado = None

            while bairro_clicado is None:
                self.tela.blit(self.mapa, (0, 0))
                self.interface.desenhar_caixa_texto()
                self.interface.desenhar_barra_tempo(contador)
                self.desenhar_contador(f"Tempo restante: {contador:.2f}", (10, 522))
                encontre = f'{bairro_aleatorio}!'
                self.interface.desenhar_texto(f"{encontre}", ((self.tela.get_width() - pg.font.SysFont('freesansbold.ttf', 90).size(f"{encontre}")[0]) // 2, self.tela.get_height() - 170), tamanho=90)
                self.desenhar_pontuacao()

                pg.display.flip()
                for evento in pg.event.get():
                    if evento.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif evento.type == pg.MOUSEBUTTONDOWN:
                        posicao_mouse = pg.mouse.get_pos()
                        posicao_bandeira = (posicao_mouse[0] - 27, posicao_mouse[1] - 52)
                        self.tela.blit(self.bandeira, posicao_bandeira)
                        tempo_decorrido = (10 - contador)
                        pg.display.flip()
                        pg.time.wait(1000)

                        ponto_central = self.pontos_centrais[bairro_aleatorio]
                        distancia_centro = math.sqrt((ponto_central[0] - posicao_mouse[0]) ** 2 + (ponto_central[1] - posicao_mouse[1]) ** 2)
                        metros = distancia_centro * 22

                        bairro_clicado = None
                        for bairro, dados in self.bairros.items():
                            posicao = dados['posicao']
                            min_x = min(pos[0] for pos in posicao)
                            min_y = min(pos[1] for pos in posicao)
                            max_x = max(pos[0] for pos in posicao)
                            max_y = max(pos[1] for pos in posicao)
                            retangulo_bairro = pg.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
                            if retangulo_bairro.collidepoint(posicao_mouse):
                                bairro_clicado = bairro
                                break

                        if bairro_clicado == bairro_aleatorio:
                            self.interface.desenhar_caixa_texto()
                            self.pontuacao += 10  
                            self.pontuacao += self.calcular_pontuacao(distancia_centro, tempo_decorrido)
                            bairro_objeto = Bairro(bairro, self.bairros[bairro]['posicao'])
                            self.animar_bairro(bairro_objeto) 
                            self.animar_movimento_chorao(self.pontos_centrais[bairro_aleatorio], 1000)
                            texto = f'Boa!! Em apenas {tempo_decorrido:.2f} segundos você conseguiu clicar'
                            self.interface.desenhar_texto(texto, (250, 545))
                            texto2 = f'no bairro {bairro_aleatorio}.'
                            self.interface.desenhar_texto(texto2, (450, 590))
                            bairro_objeto.desenhar(self.tela)
                            self.tela.blit(self.bandeira, posicao_bandeira)
                            pg.display.flip()
                            pg.time.wait(2000)

                        else:
                            self.pontuacao += self.calcular_pontuacao(distancia_centro, tempo_decorrido)
                            self.pontuacao = max(self.pontuacao, -1500000)
                            self.distanciamento_acumulado += metros

                            bairro_objeto = Bairro(bairro_aleatorio, self.bairros[bairro_aleatorio]['posicao'])
                            bairro_objeto.desenhar(self.tela)
                            pg.time.wait(1000)
                            texto = f'Em {tempo_decorrido:.2f} segundos, você clicou a uma distância de'
                            self.interface.desenhar_texto(texto, (250, 590))
                            texto2 = f'{metros:.2f} metros do bairro {bairro_aleatorio}.'
                            self.interface.desenhar_texto(texto2, (350, 635))
                            self.interface.animar_seta(posicao_mouse, ponto_central)
                            self.tela.blit(self.bandeira, posicao_bandeira)
                            pg.display.flip()
                            pg.time.wait(2000)


                contador -= 0.01
                pg.display.flip()

                if contador <= 0 or self.pontuacao <= -200 or self.distanciamento_acumulado > 10000:
                    if not self.game_over():
                        pg.quit()
                        sys.exit()
                    else:
                        self.pontuacao = 0  
                        self.distanciamento_acumulado = 0
                        self.loop_jogo_principal()
                        return  

                if self.pontuacao >= 5000:
                    if self.parabens():
                        self.pontuacao = 0 
                        self.distanciamento_acumulado = 0
                        self.loop_jogo_principal()
                        return

def main():
    jogo = Jogo()
    jogo.loop_jogo_principal()

if __name__ == "__main__":
    main()
