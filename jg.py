import pygame, random, sys
from pygame.locals import *
pygame.init()
# Introduzindo as configurações do jogo
LARGURA = 1200
ALTURA = 600
VELOMININIMIGO = 1
VELOMAXINIMIGO = 7
NOVOINIMIGORATE = 40
DIFICULDADE = 1
level = 1
contlevel = 200
#Função do jogo
def jogo(screem):
    global VELOMAXINIMIGO
    global VELOMININIMIGO
    global NOVOINIMIGORATE
    global DIFICULDADE
    global contlevel
    global level
    global pontuacao
    # Definindo os paremetros do jogo e as variaveis
    CORDOTEXTO = (0, 100, 0)
    CORDOFUNDO = (0, 0, 0)
    FPS = 40
    TAMANHOMININIMIGO = 40
    TAMANHOMAXINIMIGO = 100
    PLAYERMOVERATE = 12
    pontuacao = 0
    MaxPontuacao = 0
    global poder
    poder = 0
    TempoPoder = 0
    #CORES
    BRANCO = (255,255,255)
    PRETO = (0,0,0)
    VERDE = (0, 255, 0)
    VERMELHO = (255, 0, 0)
    AMARELO = (255,255, 0)

    # Setar imagens
    ImagemDoJogador = pygame.image.load('Imagens/nave.png')
    PlayerMask = pygame.mask.from_surface(ImagemDoJogador, 50)
    RetanguloDoJogador = ImagemDoJogador.get_rect()
    ImagemDoUniverso = pygame.image.load('Imagens/Universo.png')
    ImagemTiro = pygame.image.load('Imagens/tiro.png')
    Explosao = pygame.image.load('Imagens/explosion00.png')
	#Imagens dos inimigos
    InimigoImagem = [0,1,2,3,4,5,6,7]
    InimigoImagem[0] = pygame.image.load('Imagens/cress.png')
    InimigoImagem[1] = pygame.image.load('Imagens/draken-armor.png')
    InimigoImagem[2] = pygame.image.load('Imagens/lotus.png')
    InimigoImagem[3] = pygame.image.load('Imagens/nave2.png')
    InimigoImagem[4] = pygame.image.load('Imagens/nave3.png')
    InimigoImagem[5] = pygame.image.load('Imagens/nave4.png')
    InimigoImagem[6] = pygame.image.load('Imagens/nave5.png')
    InimigoImagem[7] = pygame.image.load('Imagens/ship.png')


    # setar fontes
    fonte = pygame.font.SysFont('Waste of time', 30)

    # setar sons
    gameOverSound = pygame.mixer.Sound('Sound/gameover.wav')
    SomDoTiro = pygame.mixer.Sound('Sound/tiro.wav')
    SomExplosao = pygame.mixer.Sound('Sound/explosao.wav')
    #pygame.mixer.music.load('background.mid')


    def encerrar():
        pygame.quit()
        sys.exit()

    def EsperarJogadorApertarAlgumaTecla():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    encerrar()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        encerrar()
                    return

    def AcertouInimigo(RetanguloDoJogador, inimigos):
        for b in inimigos:
            if RetanguloDoJogador.colliderect(b['rect']):
                InimigoMask = pygame.mask.from_surface(b['surface'], 50)
                bx, by = (RetanguloDoJogador[0], RetanguloDoJogador[1])
                offset_x = bx - b['rect'][0]
                offset_y = by - b['rect'][1]
                overlap = InimigoMask.overlap(PlayerMask, (offset_x, offset_y))
                if overlap:
                    return True
        return False

    def Colisao(disparos, inimigos):
        global pontuacao
        global poder
        for x in disparos:
            for b in inimigos:
                if x['rect'].colliderect(b['rect']):
                    SuperficieDaJanela.blit(Explosao, b['rect'])
                    pygame.display.update()
                    if not PoderReverter and not PoderLento:
                        poder+=0.05
                        barrapoder(poder)
                    x['rect'].move_ip(0, -6000)
                    b['rect'].move_ip(0, 6000)
                    disparos.remove(x)
                    inimigos.remove(b)
                    SomExplosao.play()
                    pontuacao += 5

    def barrapoder(poder):
        if poder > 1.0:
            poder = 1.0
        largurab = 100
        alturab = 20
        fill = poder*largurab
        borda_rect = pygame.Rect(10, 100, largurab, alturab)
        fill_rect = pygame.Rect(10, 100, fill, alturab)
        if poder >= 1.0:
            corbarra = VERDE
        elif poder > 0.5:
            corbarra = AMARELO
        else:
            corbarra = VERMELHO
        pygame.draw.rect(SuperficieDaJanela, BRANCO, borda_rect)
        pygame.draw.rect(SuperficieDaJanela, corbarra, fill_rect)
        CriarTexto("Poder", fonte, SuperficieDaJanela, 30, 100)

    def CriarTexto(texto, fonte, superficie, x, y):
        textobj = fonte.render(texto, 1, CORDOTEXTO)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        superficie.blit(textobj, textrect)

    def Rank(Pontuacao):
        RANK = open("Rank/lista.txt", 'r')
        texto = RANK.readlines()
        Pontos = []
        for linha in texto:
            Pontos.append(int(linha))
        for x in range(len(Pontos)):
            if Pontuacao > Pontos[x]:
                Armazenar = [Pontos[x]]
                Pontos[x] = Pontuacao
                Count = 1
                for y in range(x+1, len(Pontos)):
                    Armazenar.append(Pontos[x+Count])
                    Count+=1
                for xy in range(len(Pontos)-len(Armazenar)+1, len(Pontos)):
                    Pontos[xy] = Armazenar[xy-x-1]
                break
        RANK = open("Rank/lista.txt", 'w')
        Ponto = str(Pontos[0])+'\n'+str(Pontos[1])+'\n'+str(Pontos[2])+'\n'+str(Pontos[3])+'\n'+str(Pontos[4])+'\n'+str(Pontos[5])+'\n'+str(Pontos[6])+'\n'+str(Pontos[7])+'\n'+str(Pontos[8])+'\n'+str(Pontos[9])
        RANK.write(Ponto)
        RANK.close()

    # iniciar o pygames
    pygame.init()
    mainClock = pygame.time.Clock()
    SuperficieDaJanela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption('Space Dark')
    pygame.mouse.set_visible(False)

    # Verificar se voltou para o menu
    global VoltouMenu
    if VoltouMenu == 1:
        VoltouMenu = 0
        global menu_selecao
        menu_selecao = 1
        return

    # mostrar tela inicial
    CriarTexto('Space Dark', fonte, SuperficieDaJanela, (LARGURA / 3), (ALTURA / 3))
    CriarTexto('Usar mouse ou teclas para se mover', fonte, SuperficieDaJanela, (LARGURA / 5) - 35, (ALTURA / 3) + 50)
    CriarTexto('Pressione Z ou X para usar poderes', fonte, SuperficieDaJanela, (LARGURA / 5) - 35, (ALTURA / 3) + 100)
    CriarTexto('Pressione alguma tecla para iniciar o  jogo !', fonte, SuperficieDaJanela, (LARGURA / 3) - 30, (ALTURA / 3) + 220)
    CriarTexto('(w)Para cima  (s)Para baixo  (d)Para direita  (a)Para esquerda (Espaço)Para atirar', fonte, SuperficieDaJanela, (LARGURA / 5) - 35, (ALTURA / 3) + 180)
    pygame.display.update()
    EsperarJogadorApertarAlgumaTecla()


    while True:
        # iniciar o Jogo
        inimigos = []
        disparos = []
        Atirando =  False
        RetanguloDoJogador.topleft = (LARGURA / 2, ALTURA - 50)
        moverEsquerda = moverDireita = moverCima = moverBaixo = False
        PoderReverter = PoderLento = False
        inimigoAddCounter = 0
        pygame.mixer.music.play(-1, 0.0)
        UsouPoder = False
        while True:
            pontuacao += 0.1*DIFICULDADE

            for event in pygame.event.get():
                if event.type == QUIT:
                    encerrar()

                if event.type == KEYDOWN:
    				# mudar as variaveis do teclado
                    if event.key == ord('z'):
                        if TempoPoder < 15 and poder >= 1.0:
                            PoderReverter = True
                            UsouPoder = True
                    if event.key == ord('x'):
                        if TempoPoder < 15 and poder >= 1.0:
                            PoderLento = True
                            UsouPoder = True
                    if event.key == K_LEFT or event.key == ord('a'):
                        moverDireita = False
                        moverEsquerda = True
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moverEsquerda = False
                        moverDireita = True
                    if event.key == K_UP or event.key == ord('w'):
                        moverBaixo = False
                        moverCima = True
                    if event.key == K_DOWN or event.key == ord('s'):
                        moverCima = False
                        moverBaixo = True
                    if event.key == K_SPACE:
                        Atirando = True
                if event.type == KEYUP:
                    if event.key == ord('z'):
                        PoderReverter = False
                    if event.key == ord('x'):
                        PoderLento = False
                    if event.key == K_ESCAPE:
                        VoltouMenu = 1
                        break

                    if event.key == K_LEFT or event.key == ord('a'):
                        moverEsquerda = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moverDireita = False
                    if event.key == K_UP or event.key == ord('w'):
                        moverCima = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        moverBaixo = False

                if event.type == MOUSEMOTION:
                    RetanguloDoJogador.move_ip(event.pos[0] - RetanguloDoJogador.centerx, event.pos[1] - RetanguloDoJogador.centery)

            #Verifica se o poder foi utilizado
            if UsouPoder == True:
                if TempoPoder < 15:
                    TempoPoder+=0.1
                else:
                    TempoPoder=0
                    UsouPoder = False
                    poder=0

            # adicionar inimigos no topo da tela se precisar
            if not PoderReverter and not PoderLento:
                inimigoAddCounter += 1
            if inimigoAddCounter == NOVOINIMIGORATE:
                inimigoAddCounter = 0
                TamanhoDoInimigo = random.randint(TAMANHOMININIMIGO, TAMANHOMAXINIMIGO)
                SortearInimigo = random.randint(0,7)
                NovoInimigo = {'rect': pygame.Rect(random.randint(0, LARGURA-TamanhoDoInimigo), 0 - TamanhoDoInimigo, TamanhoDoInimigo, TamanhoDoInimigo),
                            'speed': random.randint(VELOMININIMIGO, VELOMAXINIMIGO),
                            'surface':pygame.transform.scale(InimigoImagem[SortearInimigo], (TamanhoDoInimigo, TamanhoDoInimigo)),
                            }
                inimigos.append(NovoInimigo)

            # adicionar tiros na tela
            if Atirando == True:
                NovoDisparo = {'rect': pygame.Rect(RetanguloDoJogador.centerx , RetanguloDoJogador.centery - 15, 15, 15),
                            'speed': 30,
                            'surface':pygame.transform.scale(ImagemTiro, (7, 15)),
                            }
                disparos.append(NovoDisparo)
                SomDoTiro.play()
                Atirando = False

            # mover jogador
            if moverEsquerda and RetanguloDoJogador.left > 0:
                RetanguloDoJogador.move_ip(-1 * PLAYERMOVERATE, 0)
            if moverDireita and RetanguloDoJogador.right < LARGURA:
                RetanguloDoJogador.move_ip(PLAYERMOVERATE, 0)
            if moverCima and RetanguloDoJogador.top > 0:
                RetanguloDoJogador.move_ip(0, -1 * PLAYERMOVERATE)
            if moverBaixo and RetanguloDoJogador.bottom < ALTURA:
                RetanguloDoJogador.move_ip(0, PLAYERMOVERATE)

            # mover o mouse para começar a partida
            pygame.mouse.set_pos(RetanguloDoJogador.centerx, RetanguloDoJogador.centery)

            # mover inimigos para baixo
            for b in inimigos:
                if not PoderReverter and not PoderLento:
                    b['rect'].move_ip(0, b['speed'])
                elif PoderReverter:
                    b['rect'].move_ip(0, -5)
                elif PoderLento:
                    b['rect'].move_ip(0, 1)

            # mover balas para cima
            for t in disparos:
                if not PoderReverter and not PoderLento:
                    t['rect'].move_ip(0, -t['speed'])
                elif PoderReverter:
                    t['rect'].move_ip(0, 5)
                elif PoderLento:
                    t['rect'].move_ip(0, -1)

             # remover os inimigos quando sairem da tela
            for b in inimigos[:]:
                if b['rect'].top > ALTURA:
                    inimigos.remove(b)

            # remover balas da tela ao sairem

            for t in disparos[:]:
                if t['rect'].top < -ALTURA:
                    disparos.remove(t)

            # desenhar o mundo do jogo na janela
            SuperficieDaJanela.blit(ImagemDoUniverso, [0,0])

            # DESENHAR A PONTUACAO E A MELHOR PONTUACAO.
            CriarTexto('Pontuação: %.1f'%pontuacao, fonte, SuperficieDaJanela, 10, 20)
            CriarTexto('Pontuacao Maxíma: %.1f'%MaxPontuacao, fonte, SuperficieDaJanela, 10, 60)
            CriarTexto("LEVEL: %d "%level, fonte, SuperficieDaJanela, 10, 150)

            # desenhar retângulo
            SuperficieDaJanela.blit(ImagemDoJogador, RetanguloDoJogador)

            # desenha os inimigos
            for b in inimigos:
                SuperficieDaJanela.blit(b['surface'], b['rect'])

            # desenha os tiros
            for t in disparos:
                SuperficieDaJanela.blit(t['surface'], t['rect'])
            barrapoder(poder)
            pygame.display.update()

            # checar se os inimigos encostaram no jogador
            if AcertouInimigo(RetanguloDoJogador, inimigos):
                if pontuacao > MaxPontuacao:
                    MaxPontuacao = pontuacao
                Rank(int(pontuacao))
                pontuacao = 0
                poder = 0
                level = 1
                contlevel = 200
                if DIFICULDADE == 1:
                    NOVOINIMIGORATE = 40
                    VELOMAXINIMIGO = 5
                    VELOMININIMIGO = 1
                elif DIFICULDADE == 2:
                    VELOMAXINIMIGO = 8
                    VELOMININIMIGO = 4
                    NOVOINIMIGORATE = 20
                elif DIFICULDADE == 3:
                    NOVOINIMIGORATE = 10
                    VELOMAXINIMIGO = 11
                    VELOMININIMIGO = 7
                break

            # Condição para o level funcionar e aumentar a dificuldade do jogo
            if pontuacao > contlevel:
                contlevel = contlevel + 200
                level = level + 1
                VELOMININIMIGO = VELOMININIMIGO + 1
                VELOMAXINIMIGO = VELOMAXINIMIGO + 1
                NOVOINIMIGORATE -= 5
                if NOVOINIMIGORATE < 1:
                    NOVOINIMIGORATE = 1
                inimigoAddCounter = 0
            print(NOVOINIMIGORATE)
            #Checar se apertou ESC
            if VoltouMenu == 1:
                break
            # checar se os tiros acertaram os inimigos
            Colisao(disparos, inimigos)

            # FRAMES POR SEGUNDO (FPS)
            mainClock.tick(FPS)

        pygame.mixer.music.stop()
        if VoltouMenu == 1:
            break
        else:
            # parar o jogo e mostrar o game over
            gameOverSound.play()
            CriarTexto('VOCÊ PERDEU!', fonte, SuperficieDaJanela, (LARGURA / 3), (ALTURA / 3))
            CriarTexto('Pressione qualquer tecla para jogar novamente...', fonte, SuperficieDaJanela, (LARGURA / 3) - 80, (ALTURA / 3) + 50)
            pygame.display.update()
            EsperarJogadorApertarAlgumaTecla()
            gameOverSound.stop()

global VoltouMenu
VoltouMenu = 0

# Cabeçalho do menu
fixo = True
selecao = True
ImagemDoJogador = pygame.image.load('Imagens/nave.png')
ImagemDoUniverso = pygame.image.load('Imagens/menu_background.png')
screem = pygame.display.set_mode( (LARGURA, ALTURA), 0, 32 )
screem_menu = pygame.Surface( (LARGURA, ALTURA), 0, 32 )
musica = pygame.mixer.music.load('Sound/intro.mp3')
pygame.mixer.music.play()
pygame.display.set_caption('Imagens/Space Dark')
menu_selecao = 1
temp = 0
# FUNCAO PRINCIPAL DO MENU, CHAMARA TODOS OS PROCESSOS
def selecao():
    # Cabeçalho do menu
    screem_menu.blit(ImagemDoUniverso, [0,0])
    fonte = pygame.font.SysFont("Agency FB", 100, False, False)
    Space_Dark = fonte.render("Space Dark", True, (0, 100, 0))
    screem_menu.blit(Space_Dark, ((LARGURA/2)-450, (ALTURA/2)-100))
    screem_menu.blit(ImagemDoJogador, [(LARGURA/2)-300, (ALTURA/2)])
    # VARIAVEIS DEFINIDAS COMO GLOBAIS PARA O USO DOS NIVEIS DO JOGO
    global NOVOINIMIGORATE
    global VELOMININIMIGO
    global VELOMAXINIMIGO
    global menu_selecao
    global temp
    global DIFICULDADE
    # FUNCOES DE SELECAO DO MENU PRINCIPAL
    def rdu():
        global menu_selecao
        if menu_selecao == 1:
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            iniciar = fonte.render("> INICIAR", True, (0, 100, 0))
            screem_menu.blit(iniciar, ((LARGURA/2)+215, (ALTURA/2)+35))
        if menu_selecao != 1:
            fonte = pygame.font.SysFont("Agency FB", 20, False, False)
            iniciar = fonte.render("INICIAR", True, (0, 0, 0))
            screem_menu.blit(iniciar, ((LARGURA/2)+215, (ALTURA/2)+35))
        if menu_selecao == 2:
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            configuracoes = fonte.render("> CONFIGURAÇÕES", True, (0, 100, 0))
            screem_menu.blit(configuracoes, ((LARGURA/2)+215, (ALTURA/2)+75))
        if menu_selecao != 2:
            fonte = pygame.font.SysFont("Agency FB", 20, False, False)
            configuracoes = fonte.render("CONFIGURAÇÕES", True, (0, 0, 0))
            screem_menu.blit(configuracoes, ((LARGURA/2)+215, (ALTURA/2)+75))
        if menu_selecao == 3:
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            creditos = fonte.render("> CRÉDITOS", True, (0, 100, 0))
            screem_menu.blit(creditos, ((LARGURA/2)+215, (ALTURA/2)+105))
        if menu_selecao != 3:
            fonte = pygame.font.SysFont("Agency FB", 20, False, False)
            creditos = fonte.render("CRÉDITOS", True, (0, 0, 0))
            screem_menu.blit(creditos, ((LARGURA/2)+215, (ALTURA/2)+105))
        if menu_selecao != 4:
            fonte = pygame.font.SysFont("Agency FB", 20, False, False)
            sair = fonte.render("RANK", True, (0, 0, 0))
            screem_menu.blit(sair, ((LARGURA/2)+215, (ALTURA/2)+135))
        if menu_selecao == 4:
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            sair = fonte.render("> RANK", True, (0, 100, 0))
            screem_menu.blit(sair, ((LARGURA/2)+215, (ALTURA/2)+135))
        if menu_selecao != 5:
            fonte = pygame.font.SysFont("Agency FB", 20, False, False)
            sair = fonte.render("SAIR", True, (0, 0, 0))
            screem_menu.blit(sair, ((LARGURA/2)+215, (ALTURA/2)+165))
        if menu_selecao == 5:
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            sair = fonte.render("> SAIR", True, (0, 100, 0))
            screem_menu.blit(sair, ((LARGURA/2)+215, (ALTURA/2)+165))
    def comecajogo():
        global menu_selecao
        if menu_selecao == 11:
            screem_menu.blit(ImagemDoUniverso, [0,0])
            jogo(screem)
    def config():
        global menu_selecao
        if menu_selecao == 200:
            fonte30 = pygame.font.SysFont("Agency FB", 30, False, False)
            som = fonte30.render("> SOM:", True, (0, 100, 0))
            screem_menu.blit(som, ((LARGURA/2)+200, (ALTURA/2)+35))
            ligado = fonte30.render("LIGADO/", True, (0, 100, 0))
            screem_menu.blit(ligado, ((LARGURA/2)+275, (ALTURA/2)+35))
        if menu_selecao == 210:
            fonte20 = pygame.font.SysFont("Agency FB", 20, False, False)
            fonte30 = pygame.font.SysFont("Agency FB", 30, False, False)
            iniciar = fonte30.render("> SOM:", True, (0, 100, 0))
            screem_menu.blit(iniciar, ((LARGURA/2)+200, (ALTURA/2)+35))
            desligado = fonte30.render("DESLIGADO", True, (0, 100, 0))
            screem_menu.blit(desligado, ((LARGURA/2)+370, (ALTURA/2)+35))
            ligado = fonte20.render("LIGADO/", True, (0, 0, 0))
            screem_menu.blit(ligado, ((LARGURA/2)+275, (ALTURA/2)+35))
        if menu_selecao != 200 and menu_selecao != 210:
            fonte20 = pygame.font.SysFont("Agency FB", 20, False, False)
            iniciar = fonte20.render("SOM:", True, (0, 0, 0))
            screem_menu.blit(iniciar, ((LARGURA/2)+215, (ALTURA/2)+35))
            ligado = fonte20.render("LIGADO/", True, (0, 0, 0))
            screem_menu.blit(ligado, ((LARGURA/2)+275, (ALTURA/2)+35))
        if menu_selecao == 201:
            fonte30 = pygame.font.SysFont("Agency FB", 30, False, False)
            nivel = fonte30.render("> NÍVEL", True, (0, 100, 0))
            screem_menu.blit(nivel, ((LARGURA/2)+215, (ALTURA/2)+80))
        if menu_selecao != 201:
            fonte20 = pygame.font.SysFont("Agency FB", 20, False, False)
            nivela = fonte20.render("NÍVEL", True, (0, 0, 0))
            screem_menu.blit(nivela, ((LARGURA/2)+215, (ALTURA/2)+80))
        if menu_selecao == 202:
            fonte30 = pygame.font.SysFont("Agency FB", 30, False, False)
            creditos = fonte30.render("> VOLTAR", True, (0, 100, 0))
            screem_menu.blit(creditos, ((LARGURA/2)+215, (ALTURA/2)+125))
        if menu_selecao != 202:
            fonte20 = pygame.font.SysFont("Agency FB", 20, False, False)
            voltar = fonte20.render("VOLTAR", True, (0, 0, 0))
            screem_menu.blit(voltar, ((LARGURA/2)+215, (ALTURA/2)+125))
        if menu_selecao != 210:
            fonte20 = pygame.font.SysFont("Agency FB", 20, False, False)
            desligado = fonte20.render("DESLIGADO", True, (0, 0, 0))
            screem_menu.blit(desligado, ((LARGURA/2)+370, (ALTURA/2)+35))
    def MostrarRank():
        RANK = open("Rank/lista.txt", 'r')
        texto = RANK.readlines()
        alturafinal = 125
        Pontos = []
        for linha in texto:
            Pontos.append(int(linha))
        for x in range(len(Pontos)-1, -1, -1):
            string = "#%d, Pontuacao: [%d]"%(x+1, Pontos[x])
            fonte20 = pygame.font.SysFont("Agency FB", 20, False, False)
            Mensagem = fonte20.render(string, True, (0, 0, 0))
            screem_menu.blit(Mensagem, ((LARGURA/2)+200, (ALTURA/2)+alturafinal))
            count = +1
            alturafinal -= 30
    def creditosmenu():
        global menu_selecao
        if menu_selecao == 13:
            menu_selecao = 300
        if menu_selecao == 300:
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            creditos = fonte.render("Produzido Por: ", True, (0, 0, 0))
            screem_menu.blit(creditos, ((LARGURA/2)+65, (ALTURA/2)))
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            creditos = fonte.render("Vinicius Cornelius ", True, (0, 100, 0))
            screem_menu.blit(creditos, ((LARGURA/2)+65, (ALTURA/2)+40))
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            creditos = fonte.render("Mateus Arthur ", True, (0, 100, 0))
            screem_menu.blit(creditos, ((LARGURA/2)+65, (ALTURA/2)+70))
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            creditos = fonte.render("Voltar ", True, (0, 100, 0))
            screem_menu.blit(creditos, ((LARGURA/2)+215, (ALTURA/2)+130))
    def sairmenu():
        global menu_selecao
        if menu_selecao == 15:
            exit()
    def nivel():
        global menu_selecao
        fonte = pygame.font.SysFont("Agency FB", 30, False, False)
        nivel = fonte.render("NÍVEL: ", True, (0, 100, 0))
        screem_menu.blit(nivel, ((LARGURA/2)+215, (ALTURA/2)))

        if menu_selecao == 222:
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            nivel1 = fonte.render("> FÁCIL", True, (0, 100, 0))
            screem_menu.blit(nivel1, ((LARGURA/2)+215, (ALTURA/2)+40))
        if menu_selecao != 222:
            fonte = pygame.font.SysFont("Agency FB", 20, False, False)
            nivel1 = fonte.render("FÁCIL", True, (0, 0, 0))
            screem_menu.blit(nivel1, ((LARGURA/2)+215, (ALTURA/2)+40))
        if menu_selecao == 223:
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            nivel2 = fonte.render("> MÉDIO", True, (0, 100, 0))
            screem_menu.blit(nivel2, ((LARGURA/2)+215, (ALTURA/2)+70))
        if menu_selecao != 223:
            fonte = pygame.font.SysFont("Agency FB", 20, False, False)
            nivel2 = fonte.render("MÉDIO", True, (0, 0, 0))
            screem_menu.blit(nivel2, ((LARGURA/2)+215, (ALTURA/2)+70))
        if menu_selecao == 224:
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            nivel3 = fonte.render("> DIFÍCIL", True, (0, 100, 0))
            screem_menu.blit(nivel3, ((LARGURA/2)+215, (ALTURA/2)+100))
        if menu_selecao != 224:
            fonte = pygame.font.SysFont("Agency FB", 20, False, False)
            nivel3 = fonte.render("DIFÍCIL", True, (0, 0, 0))
            screem_menu.blit(nivel3, ((LARGURA/2)+215, (ALTURA/2)+100))
        if menu_selecao == 225:
            fonte = pygame.font.SysFont("Agency FB", 30, False, False)
            voltar = fonte.render("> VOLTAR", True, (0, 100, 0))
            screem_menu.blit(voltar, ((LARGURA/2)+215, (ALTURA/2)+150))
        if menu_selecao != 225:
            fonte = pygame.font.SysFont("Agency FB", 20, False, False)
            voltar = fonte.render("VOLTAR", True, (0, 0, 0))
            screem_menu.blit(voltar, ((LARGURA/2)+215, (ALTURA/2)+150))

    # Condições para que a função do menu seja selecionada
    if 6 > menu_selecao > 0:
        rdu()
    elif menu_selecao == 11:
        comecajogo()
    elif 204 > menu_selecao > 199 or menu_selecao == 210:
        config()
    elif menu_selecao == 14:
        MostrarRank()
    elif menu_selecao == 13 or menu_selecao == 300:
        creditosmenu()
    elif menu_selecao == 15:
        sairmenu()
    elif menu_selecao < 0:
        exit()
    elif temp == 20 or 226 > menu_selecao > 221:
        nivel()

    # paremetros para que Menu de seleção não saia fora do looping
    if menu_selecao == 0:
        menu_selecao = 5
    if menu_selecao == 6:
        menu_selecao = 1
    if menu_selecao == 310:
        menu_selecao = 3
    if menu_selecao == 301:
        menu_selecao = 300
    if menu_selecao == 299:
        menu_selecao = 300
    if menu_selecao == 12:
        menu_selecao = 200
    if menu_selecao == 220:
        menu_selecao = 200
    if menu_selecao == 199:
        menu_selecao = 202
    if menu_selecao == 203:
        menu_selecao = 200
    if menu_selecao == 212:
        menu_selecao = 2
    if menu_selecao == 209:
        menu_selecao = 202
    if menu_selecao == 213:
        menu_selecao = 210
    if temp == 20:
        menu_selecao = 222
        temp = 0
    if menu_selecao == 211:
        temp += 10
        menu_selecao = 201
    if menu_selecao == 221:
        menu_selecao = 225
    if menu_selecao == 226:
        menu_selecao = 222
    if menu_selecao == 235:
        menu_selecao = 2
    if menu_selecao == 24:
        menu_selecao = 4
    # Condicoes para que o nivel seja selecionado atraves do menu_selecao
    if menu_selecao == 232:
        VELOMININIMIGO = 1
        VELOMAXINIMIGO = 5
        NOVOINIMIGORATE = 40
        DIFICULDADE = 1
        menu_selecao = 2
    if menu_selecao == 233:
        VELOMININIMIGO = 4
        VELOMAXINIMIGO = 8
        NOVOINIMIGORATE = 20
        DIFICULDADE = 2
        menu_selecao = 2
    if menu_selecao == 234:
        VELOMININIMIGO = 7
        VELOMAXINIMIGO = 11
        NOVOINIMIGORATE = 10
        DIFICULDADE = 3
        menu_selecao = 2

    # Condições para pausar e despausar a musica do menu
    if menu_selecao == 210:
            pygame.mixer.music.pause()
    if menu_selecao == 200:
            pygame.mixer.music.unpause()

# looping de seleção de menu
while (True):
    selecao()
    screem.blit(screem_menu, (0,0))
    pygame.display.update()
    pygame.display.flip()
    for e in pygame.event.get():
        if (e.type == QUIT):
                exit()
        if (e.type == KEYDOWN):
            if (e.key == K_DOWN):
                menu_selecao = menu_selecao+1
            if (e.key == K_UP):
                menu_selecao = menu_selecao-1
            if (e.key == K_RETURN):
                menu_selecao = menu_selecao+10
            if (e.key == K_ESCAPE):
                menu_selecao = menu_selecao-10
