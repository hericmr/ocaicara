import random, math, sys, pygame as pg, asyncio

def desenhar_texto(tela, texto, posicao, tamanho=50, cor=(255, 255, 255)):
    fonte = pg.font.SysFont('freesansbold.ttf', tamanho)
    superficie_texto = fonte.render(texto, True, cor)
    tela.blit(superficie_texto, posicao)


def desenhar_texto_centralizado(tela, texto, tamanho=80, cor=(255, 255, 255)):
    fonte = pg.font.SysFont('freesansbold.ttf', tamanho)
    superficie_texto = fonte.render(texto, True, cor)
    tela.blit(superficie_texto, ((tela.get_width() - superficie_texto.get_width()) // 2, (tela.get_height() - superficie_texto.get_height()) // 2))

def desenhar_caixa_texto(tela, texto, altura=180, cor_fundo=(0, 34, 0), cor_borda=(0, 0, 0), cor_texto=(255, 255, 255)):
    retangulo = pg.Rect(0, tela.get_height() - altura, tela.get_width(), altura)
    pg.draw.rect(tela, cor_fundo, retangulo)
    pg.draw.rect(tela, cor_borda, retangulo, 3)
    desenhar_texto_centralizado(tela, texto, tamanho=24, cor=cor_texto) 
    
def desenhar_contador(tela, texto, posicao, tamanho=16, cor=(0, 0, 0)):
    fonte = pg.font.SysFont('freesansbold.ttf', tamanho)
    superficie_texto = fonte.render(texto, True, cor)
    tela.blit(superficie_texto, posicao)

        
bairros = {
    'Monte Serrat' : {'posicao' : [(825.08, 140.29), (841.50, 146.08), (844.39, 152.84), (843.43, 159.60), (845.36, 164.43), (842.46, 167.33), (831.84, 170.22), (811.56, 170.22), (796.11, 171.19), (799.98, 157.67), (803.84, 154.77), (812.53, 141.26)]},
    'Embaré' : {'posicao': [(863.24, 378.24), (873.21, 362.04), (876.94, 328.40), (883.17, 330.89), (888.16, 327.15), (881.93, 318.43), (884.42, 315.94), (879.44, 308.46), (893.14, 293.51), (955.44, 338.37), (924.29, 367.02), (898.12, 401.91)]},
    'Estuário': {'posicao': [(956.40, 338.18), (976.68, 322.73), (1023.99, 388.39), (1023.99, 404.80), (980.54, 373.91), (976.68, 352.66)]},
    'Porto Macuco' : {'posicao' : [(1019.17, 379.70), (1028.82, 374.87), (944.82, 258.03), (943.85, 263.83), (936.13, 263.83), (937.09, 287.97), (953.51, 289.90)]},
    'Ponta da Praia': {'posicao': [(934.26, 438.04), (996.55, 388.20), (1025.21, 406.89), (1018.98, 452.99), (1022.72, 460.47), (972.88, 486.63), (952.95, 479.16), (940.49, 467.94), (937.99, 449.25)]},
    'Porto Ponta da Praia': {'posicao': [(1021.36, 458.39), (1017.48, 452.58), (1025.23, 414.83), (1025.23, 403.22), (1024.26, 388.70), (1021.36, 379.99), (1028.13, 375.15), (1028.13, 380.96), (1041.68, 400.31), (1041.68, 431.29), (1035.87, 442.90), (1032.00, 443.87), (1027.16, 455.48), (1022.32, 454.52)]},
    'Embaré' : {'posicao': [(863.24, 378.24), (873.21, 362.04), (876.94, 328.40), (883.17, 330.89), (888.16, 327.15), (881.93, 318.43), (884.42, 315.94), (879.44, 308.46), (893.14, 293.51), (955.44, 338.37), (924.29, 367.02), (898.12, 401.91)]},
    'Gonzaga' : {'posicao': [(763.56, 343.35), (768.55, 296.00), (829.60, 271.09), (819.63, 354.56)]},
    'Pompeia' : {'posicao': [(759.83, 340.86), (766.06, 294.76), (726.19, 313.45), (723.69, 338.37)]},
    'Campo Grande' : { 'posicao' : [(727.43, 310.96), (733.66, 252.40), (809.66, 234.95), (804.68, 277.32)]},
    'Vila Belmiro' : {'posicao' : [(732.42, 253.64), (734.91, 232.46), (767.30, 210.04), (810.91, 216.26), (809.66, 233.71)]},
    'Boqueirão' : {'posicao' : [(863.84, 377.41), (873.78, 363.06), (877.09, 324.44), (877.09, 306.78), (893.64, 292.44), (866.05, 270.37), (829.63, 268.16), (819.70, 355.34)]},
    'Macuco' : {'posicao' : [(956.68, 337.12), (975.37, 319.68), (954.19, 291.02), (937.99, 288.53), (937.99, 271.09), (936.75, 266.10), (919.31, 262.36), (921.80, 237.45), (914.88, 235.83), (914.88, 231.96), (907.16, 230.03), (903.30, 226.17), (868.53, 222.31), (865.64, 269.62)]},
    'Encruzilhada' : {'posicao' : [(863.71, 269.62), (868.53, 224.24), (811.56, 216.51), (803.84, 277.35), (829.91, 266.72)]},
    'Vila Mathias' : {'posicao' : [(769.65, 208.52), (882.74, 222.16), (887.61, 174.39), (873.97, 173.42), (855.44, 181.22), (835.94, 177.32), (837.89, 165.62), (823.27, 169.52), (820.35, 166.60), (816.45, 167.57), (813.52, 166.60), (809.62, 168.55), (807.67, 168.55), (803.77, 169.52), (799.87, 166.60), (795.00, 166.60), (789.15, 168.55), (785.25, 183.17), (780.38, 199.74)]},
    'Vila Nova' : {'posicao' : [(845.36, 179.82), (849.22, 141.20), (898.47, 154.72), (896.54, 159.54), (896.54, 163.41), (897.50, 166.30), (895.57, 175.96), (882.05, 174.99), (863.71, 180.79)]},
    'Paquetá' : {'posicao' : [(865.64, 146.03), (869.50, 114.16), (907.16, 126.71), (906.19, 145.06), (899.43, 153.75)]},
    'Marapé' : {'posicao' : [(733.35, 307.28), (685.07, 322.73), (703.42, 304.38), (705.35, 284.11), (689.90, 254.17), (690.86, 245.48), (743.97, 214.58), (743.97, 208.79), (775.84, 212.65), (741.08, 236.79)]},
    'Centro' : {'posicao' : [(864.67, 145.06), (849.22, 143.13), (845.36, 165.34), (844.39, 161.48), (844.39, 154.72), (842.46, 147.96), (827.98, 142.16), (825.08, 140.23), (812.53, 140.23), (792.25, 121.89), (804.80, 100.64), (815.43, 104.51), (867.57, 111.26)]},
    'Castelo' : {'posicao' : [(548.92, 226.17), (509.33, 219.41), (511.26, 211.69), (516.09, 206.86), (517.06, 201.06), (504.51, 193.34), (516.09, 180.79), (529.61, 187.55), (545.06, 177.89), (546.99, 163.41), (557.61, 171.13), (547.96, 195.27), (591.41, 234.86)]},
    'Bom Retiro' : {'posicao' : [(575.96, 182.72), (524.78, 146.03), (526.71, 140.23), (515.13, 131.54), (531.54, 117.06), (527.68, 128.64), (539.27, 129.61), (549.89, 137.34), (578.86, 118.99), (602.03, 143.13)]},
    'Rádio Clube' : {'posicao' : [(503.54, 192.37), (498.71, 181.75), (493.88, 181.75), (484.23, 182.72), (463.95, 164.37), (493.88, 135.40), (516.09, 129.61), (525.75, 139.27), (522.85, 144.09), (546.03, 160.51), (541.20, 178.86), (531.54, 187.55), (548.92, 197.20), (548.92, 224.24), (508.37, 218.45), (517.06, 204.93)]},
    'Areia Branca' : {'posicao' : [(547.96, 226.17), (558.58, 170.17), (594.31, 196.24), (567.27, 231.00)]},
    'Saboó' : {'posicao' : [(660.93, 115.13), (675.42, 92.92), (716.94, 101.61), (729.49, 94.85), (733.35, 101.61), (729.49, 105.47), (737.21, 112.23), (732.39, 113.20), (736.25, 118.99), (735.28, 127.68), (735.28, 131.54), (725.63, 133.47), (713.07, 128.64), (708.25, 128.64), (706.31, 134.44), (698.59, 128.64), (687.00, 128.64)]},
    'Jabaquara' : {'posicao' : [(743.97, 206.51), (753.63, 196.85), (741.08, 179.47), (741.08, 174.64), (751.70, 170.78), (750.73, 165.95), (757.49, 159.19), (767.15, 156.30), (774.87, 161.12), (783.56, 159.19), (789.36, 152.43), (801.91, 157.26), (789.36, 201.68), (774.87, 211.33)]},
    'José Menino' : {'posicao' : [(731.42, 339.14), (709.21, 340.11), (705.35, 358.46), (697.62, 343.97), (671.55, 341.08), (663.83, 323.69), (677.35, 326.59), (678.31, 331.42), (687.97, 331.42), (687.97, 323.69), (727.56, 304.38), (732.39, 305.35), (730.45, 323.69)]},
    'Morro da Santa Terezinha' : {'posicao' : [(690.05, 319.66), (672.61, 293.50), (673.86, 287.27), (673.86, 279.79), (673.86, 273.56), (687.56, 278.55), (702.51, 278.55), (705.01, 294.75), (700.02, 305.96)]},
    'Piratininiga' : {'posicao' : [(470.77, 84.18), (447.10, 69.23), (439.62, 67.99), (437.13, 65.50), (445.85, 59.27), (458.31, 56.77), (501.92, 66.74), (499.43, 76.71)]},
    'Alemoa' : {'posicao' : [(705.01, 100.38), (523.10, 75.46), (500.67, 77.95), (501.92, 69.23), (450.84, 56.77), (434.64, 64.25), (417.20, 55.53), (405.98, 44.31), (405.98, 39.33), (415.95, 29.36), (477.00, 31.86), (508.15, 39.33), (530.58, 31.86), (528.08, 50.54), (629.00, 66.74), (632.74, 69.23), (636.48, 61.76), (711.24, 76.71)]},
    'Morro do José Menino'  : {'posicao' : [(687.56, 332.12), (678.84, 330.88), (678.84, 325.89), (666.38, 323.40), (647.69, 286.02), (670.12, 278.55), (687.56, 317.17), (686.32, 323.40)]},
    'Morro do Embaré' : {'posicao' : [(650.19, 283.53), (633.99, 242.42), (647.69, 233.70), (670.12, 244.91), (676.35, 251.14), (676.35, 261.11), (675.10, 271.07), (673.86, 276.06)]},
    'Morro da Nova Cintra' : {'posicao' : [(633.89, 243.55), (631.96, 233.89), (635.83, 226.17), (636.79, 222.31), (657.07, 194.31), (662.86, 177.89), (661.90, 173.06), (681.21, 152.78), (691.83, 155.68), (696.66, 158.58), (699.55, 168.23), (710.18, 163.41), (711.14, 167.27), (719.83, 170.17), (724.66, 164.37), (732.39, 163.41), (736.25, 158.58), (739.14, 169.20), (730.45, 175.96), (717.90, 203.00), (690.86, 225.20), (680.24, 229.07), (677.35, 232.93), (676.38, 239.69), (674.45, 242.58)]},
    'Morro da Penha' : {'posicao' : [(754.59, 126.71), (752.66, 128.64), (746.87, 122.85), (730.45, 115.13), (734.32, 112.23), (729.49, 106.44), (732.39, 100.64), (730.45, 95.81), (738.18, 91.95), (750.73, 96.78), (750.73, 100.64), (755.56, 102.57), (760.39, 97.75), (762.32, 98.71), (760.39, 106.44), (761.35, 108.37), (754.59, 118.02), (756.52, 120.92)]},
    'Valongo' : {'posicao' : [(764.81, 100.38), (768.55, 94.15), (768.55, 94.15), (792.22, 102.87), (794.71, 97.89), (802.19, 101.63), (794.71, 115.33)]},
    'Porto Valongo' : {'posicao' : [(795.96, 97.89), (794.71, 89.17), (813.40, 84.18), (807.17, 95.40), (818.39, 101.63), (835.83, 105.36), (839.57, 110.35), (815.89, 106.61), (795.96, 96.64)]},
    'Porto Paqueta' : {'posicao' : [(839.57, 109.10), (840.81, 106.61), (869.47, 109.10), (913.08, 124.05), (914.32, 135.27), (904.35, 143.99), (904.35, 126.55), (868.22, 111.59), (832.09, 107.86), (832.09, 109.10), (832.09, 110.35)]},
    'Chinês' : {'posicao' : [(789.73, 122.81), (774.78, 115.33), (773.53, 115.33), (773.53, 109.10), (767.30, 107.86), (767.30, 107.86), (767.30, 102.87), (793.47, 116.58), (793.47, 116.58), (790.97, 124.05)]},
}

def desenhar_bairro(tela, pontos, cor_transparente=(0, 255, 0, 180)):
    min_x, min_y = min(pontos, key=lambda x: x[0])[0], min(pontos, key=lambda x: x[1])[1]
    max_x, max_y = max(pontos, key=lambda x: x[0])[0], max(pontos, key=lambda x: x[1])[1]
    poligono_bairro = pg.Surface((max_x - min_x, max_y - min_y), pg.SRCALPHA)
    pg.draw.polygon(poligono_bairro, cor_transparente, [(pos[0] - min_x, pos[1] - min_y) for pos in pontos])
    tela.blit(poligono_bairro, (min_x, min_y))

def calcular_ponto_central(posicoes):
    soma_x = sum(pos[0] for pos in posicoes)
    soma_y = sum(pos[1] for pos in posicoes)
    media_x = soma_x / len(posicoes)
    media_y = soma_y / len(posicoes)
    return (media_x, media_y)
pontos_centrais = {}
for bairro, dados in bairros.items():
    posicoes = dados['posicao']
    ponto_central = calcular_ponto_central(posicoes)
    pontos_centrais[bairro] = ponto_central

def desenhar_seta(tela, posicao_inicial, posicao_final, cor=(255, 0, 0), largura=3):
    angulo = math.atan2(posicao_final[1] - posicao_inicial[1], posicao_final[0] - posicao_inicial[0])
    comprimento = 10
    pg.draw.line(tela, cor, posicao_inicial, posicao_final, largura)
    for ang in [math.pi / 6, -math.pi / 6]:
        x = posicao_final[0] - comprimento * math.cos(angulo + ang)
        y = posicao_final[1] - comprimento * math.sin(angulo + ang)
        pg.draw.line(tela, cor, posicao_final, (x, y), largura)


chorao = pg.image.load('chorao.png')
bandeira = pg.image.load('bandeira2.png')
cor_verde = (0, 255, 0)
cor_vermelha = (255, 0, 0)
cor_verde_musgo = (0, 128, 0)

def carregar_mapa():
    mapa = pg.image.load("map.png")
    return mapa

async def game_over(tela):
    desenhar_caixa_texto(tela, ' ')

    fonte_aperte_s = pg.font.SysFont('freesansbold.ttf', 36)
    texto_aperte_s = fonte_aperte_s.render('Quer jogar de novo? S/N', True, (255, 255, 255))
    posicao_aperte_s = ((tela.get_width() - texto_aperte_s.get_width()) // 2, tela.get_height() - 50)
    tela.blit(texto_aperte_s, posicao_aperte_s)
    pg.display.flip()

    while True:
        for evento in pg.event.get():
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_s:
                    return True  
                elif evento.key == pg.K_n:
                    return False 
 
def inicializar_jogo():
    pg.init()
    pg.mixer.init()  
    pg.mixer.music.load('musica.ogg')  
    pg.mixer.music.play(-1)  
    pg.display.set_caption("O CAIÇARA")
    largura_tela = 1319
    altura_tela = 680
    tela = pg.display.set_mode((largura_tela, altura_tela))
    return tela


def desenhar_pontuacao(tela, pontuação):
    fonte_pontuacao = pg.font.SysFont('freesansbold.ttf', 26)
    texto_pontuacao = fonte_pontuacao.render(f'Pontuação: {int(pontuação)}', True, (255, 255, 255))
    tela.blit(texto_pontuacao, (10, 10))


async def introducao(tela, mapa, texto_titulo):
    iniciar_jogo = False
    sair = False
    i = 0
    try:
        while not iniciar_jogo and not sair:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif evento.type == pg.MOUSEBUTTONDOWN:
                    posicao_mouse = pg.mouse.get_pos()
                    if 200 <= posicao_mouse[0] <= 400 and 550 <= posicao_mouse[1] <= 650:
                        iniciar_jogo = True
                        print("Iniciar jogo clicado")
                    elif 600 <= posicao_mouse[0] <= 800 and 550 <= posicao_mouse[1] <= 650:  
                        sair = True
                        print("Sair clicado")
            tela.blit(mapa, (0, 0))
            tamanho_personagem = int(i / 1)
            posicao_personagem = (100 + i * 2, 50 + i * 0.6)
            personagem_redimensionado = pg.transform.scale(chorao, (tamanho_personagem, tamanho_personagem))
            tela.blit(personagem_redimensionado, posicao_personagem)
            tela.blit(texto_titulo, ((tela.get_width() - texto_titulo.get_width()) // 2, 50))
            desenhar_caixa_texto(tela, ' ')
            pg.draw.rect(tela, (cor_verde_musgo), (200, 550, 200, 100))  #
            pg.draw.rect(tela, (255, 0, 0), (600, 550, 200, 100))  
            fonte_botao = pg.font.SysFont('freesansbold.ttf', 50)
            texto_botao_iniciar = fonte_botao.render('Iniciar Jogo', True, (0, 0, 0))
            texto_botao_sair = fonte_botao.render('Sair', True, (255, 255, 255))
            posicao_botao_iniciar = (230, 575)
            posicao_botao_sair = (630, 575)
            tela.blit(texto_botao_iniciar, posicao_botao_iniciar)
            tela.blit(texto_botao_sair, posicao_botao_sair)
            texto = f'Aprenda a geografia. Encontre os bairros de Santos!'
            desenhar_texto(tela, texto, (120, 510))
            pg.display.flip()
            await asyncio.sleep(1)
            tela.blit(texto_titulo, ((tela.get_width() - texto_titulo.get_width()) // 2, 50))
            i += 1
            if i >= 500:
                i = 0
        if sair:
            pg.quit()
            sys.exit()
        return iniciar_jogo
    except Exception as e:
        print(f"Erro na função introdução: {e}")
        pg.quit()
        sys.exit()

def desenhar_barra_tempo(tela, tempo_restante):
    comprimento_total = 1319  
    largura_barra = int((tempo_restante / 10) * comprimento_total)
    cor = cor_verde_musgo if tempo_restante > 5 else cor_vermelha  
    cor2 = (0, 0, 0)
    pg.draw.rect(tela, cor2, (0, 502, comprimento_total, 77))    
    pg.draw.rect(tela, cor, (0, 502, largura_barra, 75))


def desenhar_barra_tempo(tela, tempo_restante):
    comprimento_total = 1319  
    largura_barra = int((tempo_restante / 10) * comprimento_total)
    cor = cor_verde_musgo if tempo_restante > 5 else cor_vermelha  
    cor2 = (0, 0, 0)
    pg.draw.rect(tela, cor2, (0, 502, comprimento_total, 77))    
    pg.draw.rect(tela, cor, (0, 502, largura_barra, 75))


def calcular_pontuacao(comprimento_seta, tempo_decorrido):

    if comprimento_seta > 80:
        pontuacao = - (1/comprimento_seta) * (tempo_decorrido / 30)
    else:
        pontuacao = (1 / comprimento_seta) * (20 / tempo_decorrido) 
    return pontuacao


async def parabens(tela, duracao=3, texto="Parabéns!", cor_texto=(255, 255, 255)):
    pg.mixer.music.stop()
    for _ in range(20): 
        tela.fill((0, 0, 0)) 
        desenhar_texto_centralizado(tela, texto, cor=cor_texto)
        pg.display.flip()
        await asyncio.sleep(duracao / 20)  
    pg.mixer.music.play(-1)

async def loop_jogo_principal(tela, mapa):
    print("Iniciando a função do jogo principal...")
    lista_bairros = list(bairros.keys())
    tela.blit(mapa, (0, 0))
    relogio = pg.time.Clock()
    pontuação = 0

    contador = 10  

    while True:
        relogio.tick(30) 
        tela.blit(mapa, (0, 0))  
        desenhar_barra_tempo(tela, contador)
        desenhar_pontuacao(tela, pontuação)

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif evento.type == pg.MOUSEBUTTONDOWN:
                await tratar_clique_mouse(evento, tela, lista_bairros, contador, pontuação)
        
        pg.display.flip()  
        contador -= 0.01 

        if contador <= 0 or pontuação < -10:
            if not await game_over(tela): 
                pg.quit()
                sys.exit()
            else:
                contador = 10  
                pontuação = 0 

async def main():
    tela = inicializar_jogo()
    mapa = carregar_mapa()
    texto_titulo = pg.font.SysFont(None, 120).render("O CAIÇARA", True, (255, 255, 255))
    
    iniciar_jogo = await introducao(tela, mapa, texto_titulo)
    
    if iniciar_jogo:
        await loop_jogo_principal(tela, mapa)
    else:
        pg.quit()

if __name__ == "__main__":
    asyncio.run(main())
