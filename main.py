import pygame
import sys
import random

def desenhar_texto(tela, texto, posicao):
    fonte = pygame.font.SysFont('freesansbold.ttf', 50)
    superficie_texto = fonte.render(texto, True, (255, 255, 255))
    tela.blit(superficie_texto, posicao)
    pygame.display.flip()
    
def desenhar_contador(tela, texto, posicao):
    fonte = pygame.font.Font('freesansbold.ttf', 36)
    superficie_texto = fonte.render(texto, 1, (255, 255, 0))  # amarela
    tela.blit(superficie_texto, posicao)
    pygame.display.flip()

def desenhar_bairro(tela, posicao, pontos):
    poligono_bairro = pygame.Surface((max(pontos, key=lambda x: x[0])[0] - min(pontos, key=lambda x: x[0])[0],
                                      max(pontos, key=lambda x: x[1])[1] - min(pontos, key=lambda x: x[1])[1]), 
                                      pygame.SRCALPHA)
    pygame.draw.polygon(poligono_bairro, (0, 255, 0), [(pos[0] - min(pontos, key=lambda x: x[0])[0],
                                                        pos[1] - min(pontos, key=lambda x: x[1])[1]) for pos in pontos])
    tela.blit(poligono_bairro, (min(pontos, key=lambda x: x[0])[0], min(pontos, key=lambda x: x[1])[1]))

bairros = {
    'Aparecida': {'posicao': [(932.26, 437.63), (996.96, 385.49), (979.58, 371.01), (975.71, 351.70), (957.37, 338.18), (925.50, 364.25), (897.50, 400.94)]},
    'Estuário': {'posicao': [(956.40, 338.18), (976.68, 322.73), (1023.99, 388.39), (1023.99, 404.80), (980.54, 373.91), (976.68, 352.66)]},
    'Ponta da Praia': {'posicao': [(934.26, 438.04), (996.55, 388.20), (1025.21, 406.89), (1018.98, 452.99), (1022.72, 460.47), (972.88, 486.63), (952.95, 479.16), (940.49, 467.94), (937.99, 449.25)]},
    'Porto Ponta da Praia': {'posicao': [(1021.36, 458.39), (1017.48, 452.58), (1025.23, 414.83), (1025.23, 403.22), (1024.26, 388.70), (1021.36, 379.99), (1028.13, 375.15), (1028.13, 380.96), (1041.68, 400.31), (1041.68, 431.29), (1035.87, 442.90), (1032.00, 443.87), (1027.16, 455.48), (1022.32, 454.52)]},
    'Embaré' : {'posicao': [(863.24, 378.24), (873.21, 362.04), (876.94, 328.40), (883.17, 330.89), (888.16, 327.15), (881.93, 318.43), (884.42, 315.94), (879.44, 308.46), (893.14, 293.51), (955.44, 338.37), (924.29, 367.02), (898.12, 401.91)]},
    'Gonzaga' : {'posicao': [(763.56, 343.35), (768.55, 296.00), (829.60, 271.09), (819.63, 354.56)]},
    'Pompeia' : {'posicao': [(759.83, 340.86), (766.06, 294.76), (726.19, 313.45), (723.69, 338.37)]},
    'Campo Grande' : { 'posicao' : [(727.43, 310.96), (733.66, 252.40), (809.66, 234.95), (804.68, 277.32)]},
    'Vila Belmiro' : {'posicao' : [(732.42, 253.64), (734.91, 232.46), (767.30, 210.04), (810.91, 216.26), (809.66, 233.71)]},
    'Boqueirão' : {'posicao' : [(863.84, 377.41), (873.78, 363.06), (877.09, 324.44), (877.09, 306.78), (893.64, 292.44), (866.05, 270.37), (829.63, 268.16), (819.70, 355.34)]},
    'Macuco' : {'posicao' : [(956.68, 337.12), (975.37, 319.68), (954.19, 291.02), (937.99, 288.53), (937.99, 271.09), (936.75, 266.10), (919.31, 262.36), (921.80, 237.45), (914.88, 235.83), (914.88, 231.96), (907.16, 230.03), (903.30, 226.17), (868.53, 222.31), (865.64, 269.62)]},
    'Porto Macuco' : {'posicao' : [(1019.17, 379.70), (1028.82, 374.87), (944.82, 258.03), (943.85, 263.83), (936.13, 263.83), (937.09, 287.97), (953.51, 289.90)]},
    'Encruzilhada' : {'posicao' : [(863.71, 269.62), (868.53, 224.24), (811.56, 216.51), (803.84, 277.35), (829.91, 266.72)]},
    'Vila Mathias' : {'posicao' : [(769.65, 208.52), (882.74, 222.16), (887.61, 174.39), (873.97, 173.42), (855.44, 181.22), (835.94, 177.32), (837.89, 165.62), (823.27, 169.52), (820.35, 166.60), (816.45, 167.57), (813.52, 166.60), (809.62, 168.55), (807.67, 168.55), (803.77, 169.52), (799.87, 166.60), (795.00, 166.60), (789.15, 168.55), (785.25, 183.17), (780.38, 199.74)]},
    'Vila Nova' : {'posicao' : [(845.36, 179.82), (849.22, 141.20), (898.47, 154.72), (896.54, 159.54), (896.54, 163.41), (897.50, 166.30), (895.57, 175.96), (882.05, 174.99), (863.71, 180.79)]}
}

chorao = pygame.image.load('chorao.png')

def inicializar_jogo():
    pygame.init()
    pygame.mixer.init()  
    pygame.mixer.music.load('musica.ogg')  
    pygame.mixer.music.play(-1)  
    pygame.display.set_caption("O CAIÇARA")
    largura_tela = 1319
    altura_tela = 519
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    return tela

def carregar_mapa():
    mapa = pygame.image.load("map.png")
    return mapa

def game_over(tela):
    fonte = pygame.font.SysFont('freesansbold.ttf', 250)
    texto = fonte.render('Perdeu mané', True, (255, 0, 0))
    tela.blit(texto, (tela.get_width() // 2 - texto.get_width() // 2, tela.get_height() // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)


def introducao(tela, mapa, texto_titulo):
    for i in range(550):
        # preciso criar a menssagem na tela de aperte enter para pular a introducao
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return
        
        tela.blit(mapa, (0, 0))
        tamanho_personagem = int(i / 1)
        posicao_personagem = (100 + i * 2, 50 + i * 0.6)
        personagem_redimensionado = pygame.transform.scale(chorao, (tamanho_personagem, tamanho_personagem))
        tela.blit(personagem_redimensionado, posicao_personagem)

        # Posição do título
        fonte_titulo = pygame.font.SysFont('freesansbold.ttf', 100)
        texto_titulo = fonte_titulo.render('O Caiçara', True, (255, 255, 255))
        posicao_titulo = ((tela.get_width() - texto_titulo.get_width()) // 2, 50)
        tela.blit(texto_titulo, posicao_titulo)

        pygame.display.flip()
        pygame.time.wait(5)


def loop_jogo_principal(tela, mapa):
    lista_bairros = list(bairros.keys())
    tela.blit(mapa, (0, 0))
    relogio = pygame.time.Clock()
    contador = 10
    fonte_titulo = pygame.font.SysFont(None, 120)
    texto_titulo = fonte_titulo.render("O CAIÇARA", True, (255, 255, 255)) 

    introducao(tela, mapa, texto_titulo)

    pygame.display.flip()
    pygame.time.wait(2000) 


    while True:
        tela.blit(chorao, (10, 50))
        relogio.tick(120)

        bairro_aleatorio = random.choice(lista_bairros)
        encontre = f'Encontre o bairro... {bairro_aleatorio}!'
        desenhar_texto(tela, encontre, (10, 40))
        desenhar_contador(tela, f"vidas: {contador}", (1100, 10))

        bairro_clicado = None
        while bairro_clicado is None:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    posicao_mouse = pygame.mouse.get_pos()
                    pygame.draw.circle(tela, (255, 0, 0), posicao_mouse, 1)
                    pygame.display.flip()
                    for bairro, dados in bairros.items():
                        posicao = dados['posicao']
                        min_x = min(pos[0] for pos in posicao)
                        min_y = min(pos[1] for pos in posicao)
                        max_x = max(pos[0] for pos in posicao)
                        max_y = max(pos[1] for pos in posicao)
                        retangulo_bairro = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
                        if retangulo_bairro.collidepoint(posicao_mouse):
                            bairro_clicado = bairro
                            
                            if bairro == bairro_aleatorio:
                                texto = f'Muito bem! Você clicou no bairro {bairro}!'
                                desenhar_texto(tela, texto, (0, 10))
                                desenhar_bairro(tela, (0, 0), bairros[bairro]['posicao'])
                                pygame.display.flip()
                                pygame.time.wait(1000)
                                tela.blit(mapa, (0, 0))
                                pygame.display.flip()
                                break

        if bairro_clicado != bairro_aleatorio:
            contador -= 1
            texto = f'Ops! Você clicou no bairro {bairro_clicado}, mas o bairro correto era {bairro_aleatorio}.'
            desenhar_texto(tela, texto, (0, 10))
            pygame.display.flip()
            pygame.time.wait(3000)
        tela.blit(mapa, (0, 0))
        pygame.display.flip()

        if contador == 0:
            game_over(tela)
            pygame.quit()
            sys.exit()



def main():
    mapa = carregar_mapa()
    tela = inicializar_jogo()
    loop_jogo_principal(tela, mapa)

if __name__ == "__main__":
    main()
