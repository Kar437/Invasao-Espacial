# Importa as bibliotecas necessárias
import pygame
from pygame.sprite import Sprite, Group, GroupSingle
from random import randint, random

print('Invasão Espacial, versão: 1.6.2')

''' Controla os sons do jogo '''
pygame.mixer.init()
pygame.mixer.music.load('sons/Star Wars.mp3')  # Musica de fundo
som_tiro = pygame.mixer.Sound('sons/laser.wav')  # Som do tiro

pygame.mixer_music.play(-1)  # Toca a musica

''' Variáveis de controle de power-up '''
powerUp_tiro_ativo = False
powerUp_tiro_timer = 0

powerUp_velocidade_ativo = False
powerUp_velocidade_timer = 0

powerUp_escudo_ativo = False
powerUp_escudo_timer = 0

''' Variáveis de controle do jogo '''
q = 0           # Contador de inimigos
nivel = 0       # Nivel do jogo
pontos = 0      # Pontuação do jogador
loop = True     # Variável que controla o loop principal do jogo
recorde = 0     # Variável que armazena a maior pontuação do jogador

''' Cores utilizadas no jogo '''
preto = (0, 0, 0)
picton_blue = (57, 183, 255)
cinza = (128, 128, 128)
esverdeado = (106, 120, 107)

# Configurações principais da tela do jogo
tamanho_tela = 800, 600
superficie = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption('Invasão Espacial')

# Carrega a imagem do fundo do jogo
fundo = pygame.transform.scale(pygame.image.load('Game-images/space.jpg'), tamanho_tela)

botão = pygame.image.load('Game-images/botão.png')

# Cria as fontes utilizadas no jogo
pygame.font.init()
fonte = pygame.font.SysFont(None, 30)
fonte_titulo = pygame.font.SysFont(None, 50)


''' ~~~~~~~~POWER-UPs~~~~~~~~'''


# Cria o Power-up de tiro tripo
class PowerUp_tiro(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Game-images/power-up.tiro.png')
        self.rect = self.image.get_rect(center=(randint(20, 800), 0))
        self.velocidade = 1
        self.tipo = 'tiro'

    def update(self):
        self.rect.y += self.velocidade

        if self.rect.y > 600:
            self.kill()

# Cria o Power-up de velocidade
class PowerUp_velocidade(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Game-images/power-up_velocidade.png'), (108, 78))
        self.rect = self.image.get_rect(center=(randint(20, 800), 0))
        self.velocidade = 1
        self.tipo = 'velocidade'

    def update(self):
        self.rect.y += self.velocidade

        if self.rect.y > 600:
            self.kill()


# Cria o Power-up de escudo
class PowerUp_escudo(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Game-images/power-up_escudos.png'), (108, 78))
        self.rect = self.image.get_rect()
        self.velocidade = 1
        self.tipo = 'escudo'

    def update(self):
        self.rect.y += self.velocidade

        if self.rect.y > 600:
            self.kill()


''' ~~~~~~~~POWER-UPs~~~~~~~~'''


# Cria a tela inicial do jogo
class Tela_inicial():
    def __init__(self):
        self.rodando = True
        self.botão = Botao(esverdeado, 320, 255, 150, 50, 'Jogar')
        self.ajuda = Botao(esverdeado, 320, 355, 150, 50, 'Ajuda')
        self.sair = Botao(esverdeado, 320, 455, 150, 50, 'Sair')

    def executar(self):
        while self.rodando:
            tela = pygame.image.load('Game-images/tela.jpg')
            superficie.blit(tela, (0, 0))
            titulo = fonte_titulo.render("Invasão Espacial", True, 'white')
            superficie.blit(titulo, (tamanho_tela[0] // 2 - titulo.get_width() // 2, 25))
            self.botão.desenhar(superficie)
            self.ajuda.desenhar(superficie)
            self.sair.desenhar(superficie)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    quit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.botão.estar_sobre_pos(mouse_pos):
                        self.rodando = False
                    if self.ajuda.estar_sobre_pos(mouse_pos):
                        como_jogar = Como_jogar()
                        como_jogar.executar()
                    if self.sair.estar_sobre_pos(mouse_pos):
                        quit()


# Cria o menu de pausa do jogo
class Pausa():
    def __init__(self):
        self.continuar = Botao(esverdeado, 320, 355, 170, 50, 'Continuar')
        self.sair = Botao(esverdeado, 320, 455, 170, 50, 'Sair')
        self.rodando = False

    def executar(self):
        self.rodando = True
        while self.rodando:
            superficie.fill(preto)
            titulo = fonte_titulo.render('Jogo Pausado', True, 'white')
            superficie.blit(titulo, (tamanho_tela[0] // 2 - titulo.get_width() // 2, 25))

            self.sair.desenhar(superficie)
            self.continuar.desenhar(superficie)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.continuar.estar_sobre_pos(mouse_pos):
                        self.rodando = False
                    if self.sair.estar_sobre_pos(mouse_pos):
                        quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.rodando = False


# cria a janela de ajuda do Menu principal do jogo
class Como_jogar():
    def __init__(self):
        self.rodando = True
        self.voltar = Botao(esverdeado, 320, 500, 150, 50, 'Voltar')
        self.guia = Botao(esverdeado, 480, 500, 70, 50, '>')

    def executar(self):
        while self.rodando:
            superficie.fill(preto)

            titulo = fonte_titulo.render('Como jogar', True, 'white')
            texto1 = fonte.render('-Utilize as setas do teclado para movimentar a nave;', True, 'white')
            texto2 = fonte.render('-Utilize espaço para atirar;', True, 'white')
            texto3 = fonte.render('-Cada abate conta um (1) ponto;', True, 'white')
            texto4 = fonte.render('-Cada virus que deixar passar desconta um (1) ponto;', True, 'white')
            texto5 = fonte.render('-Quanto maior for sua pontuação, maior será a dificuldade;', True, 'white')
            texto6 = fonte.render('-Obejetivo: eliminar a maior quantidade de vírus possivel.', True, 'white')

            superficie.blit(titulo, (tamanho_tela[0] // 2 - titulo.get_width() // 2, 25))
            superficie.blit(texto1, (50, 100))
            superficie.blit(texto2, (50, 125))
            superficie.blit(texto3, (50, 150))
            superficie.blit(texto4, (50, 175))
            superficie.blit(texto5, (50, 200))
            superficie.blit(texto6, (50, 225))

            self.voltar.desenhar(superficie)
            self.guia.desenhar(superficie)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.voltar.estar_sobre_pos(mouse_pos):
                        self.rodando = False
                    if self.guia.estar_sobre_pos(mouse_pos):
                        guia = Guia_powerUp()
                        guia.executar()


class Guia_powerUp():
    def __init__(self):
        self.rodando = True
        self.voltar = Botao(esverdeado, 320, 500, 70, 50, '<')
        self.PU_tiro = pygame.transform.scale(pygame.image.load('Game-images/power-up.tiro.png'), (70, 70))
        self.PU_velocidade = pygame.transform.scale(pygame.image.load('Game-images/power-up_velocidade.png'), (70, 70))
        self.PU_escudo = pygame.transform.scale(pygame.image.load('Game-images/power-up_escudos.png'), (70, 70))

    def executar(self):
        while self.rodando:
            superficie.fill(preto)

            titulo = fonte_titulo.render('POWER-UPs', True, 'white')
            texto_tiro = fonte.render('Faz o jogador atirar três (3) projéteis simutaneamente. Dura 5 segundos.', True,
                                      'White')
            texto_velocidade = fonte.render('Aumenta a velocidade de movimento do jogador. Dura 5 segundos.', True,
                                            'white')
            texto_escudo = fonte.render('O jogador cria um escudo que o deixa invunerável. Dura 10 segundos. ', True,
                                        'White')

            superficie.blit(titulo, (tamanho_tela[0] // 2 - titulo.get_width() // 2, 25))
            superficie.blit(self.PU_tiro, (5, 125))
            superficie.blit(texto_tiro, (70, 160))
            superficie.blit(self.PU_velocidade, (7, 225))
            superficie.blit(texto_velocidade, (80, 255))
            superficie.blit(self.PU_escudo, (5, 325))
            superficie.blit(texto_escudo, (80, 355))

            self.voltar.desenhar(superficie)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.voltar.estar_sobre_pos(mouse_pos):
                        self.rodando = False


# Cria a tela de game-over
def mostrar_game_over():
    global recorde

    if pontos > recorde:
        recorde = pontos

    tela = pygame.image.load('Game-images/tela.jpg')
    superficie.blit(tela, (0, 0))

    perdeu = fonte_titulo.render('Game over!', True, 'white')
    pontuação = fonte.render(f'Pontuação: {pontos}', True, 'white')
    mostra_nivel = fonte.render(f'Nível: {nivel}', True, 'white')
    melhor_pontos = fonte.render(f'Melhor pontução: {recorde}', True, 'white')

    sair = Botao(esverdeado, 320, 470, 150, 50, 'Sair')
    voltar = Botao(esverdeado, 320, 270, 150, 50, 'Jogar')
    menu_ajuda = Botao(esverdeado, 320, 370, 150, 50, 'Ajuda')

    sair.desenhar(superficie)
    voltar.desenhar(superficie)
    menu_ajuda.desenhar(superficie)

    superficie.blit(perdeu, (tamanho_tela[0] // 2 - perdeu.get_width() // 2, 25))
    superficie.blit(pontuação, (tamanho_tela[0] // 2 - pontuação.get_width() // 2, 75))
    superficie.blit(mostra_nivel, (tamanho_tela[0] // 2 - pontuação.get_width() // 2, 100))
    superficie.blit(melhor_pontos, (tamanho_tela[0] // 2 - pontuação.get_width() // 2, 125))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if sair.estar_sobre_pos(mouse_pos):
                    return 'sair'
                elif voltar.estar_sobre_pos(mouse_pos):
                    return 'voltar'
                elif menu_ajuda.estar_sobre_pos(mouse_pos):
                    return 'Ajuda'

# classe que cria os botões
class Botao():
    def __init__(self, cor, x, y, largura, altura, texto=''):
        self.cor = cor
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.texto = texto

    # Método para desenhar os botões na tela
    def desenhar(self, superficie):
        superficie.blit(botão, (self.x, self.y))
        if self.texto != '':
            fonte_botao = pygame.font.SysFont(None, 70)
            texto = fonte_botao.render(self.texto, False, 'green')
            superficie.blit(texto, (self.x + (self.largura / 2 - texto.get_width() / 2),
                                    self.y + (self.altura / 2 - texto.get_height() / 2)))

    # Método para verificar se o mouse está sobre o botão
    def estar_sobre_pos(self, pos):
        if self.x < pos[0] < self.x + self.largura and self.y < pos[1] < self.y + self.altura:
            return True
        return False


# Cria instancia das classes acima
tela_inicial = Tela_inicial()
tela_inicial.executar()
ajuda = Como_jogar()
menu_pausa = Pausa()


# Cria o tiro disparado pelo jogador
class Tiro(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Game-images/laser.png')
        self.rect = self.image.get_rect(center=(x, y))

        self.rect.centerx = x
        self.rect.bottom = y

        self.velocidade = 5

    def update(self):
        self.rect.y -= self.velocidade

        global tirosQ

        if self.rect.y < 0:
            self.kill()


# Cria a nave controlada pelo jogador
class Jogador(Sprite):
    def __init__(self, tiros):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load('Game-images/space-invaders.png'),
                                            (80, 80))  # Carrega a imagem do personagem
        self.rect = self.image.get_rect()  # Obtendo o retângulo delimitador da imagem.

        self.rect.centerx = tamanho_tela[0] // 2
        self.rect.bottom = tamanho_tela[1] - 10

        self.velocidade = 3.5

        self.tiros = tiros

    def update(self):

        # Controla o movimento do jogador
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade + 0.5
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade + 0.5
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade

        if self.rect.x < 0:
            self.rect.x = 0

        if self.rect.x > 800 - 80:
            self.rect.x = 800 - 80

        if self.rect.y < 0:
            self.rect.y = 0

        if self.rect.y > 600 - 80:
            self.rect.y = 600 - 80

    # Método que faz o jogador atirar
    def atirar(self):
        global tirosQ
        if len(self.tiros) < 3:
            self.tiros.add(Tiro(self.rect.centerx, self.rect.top))
            som_tiro.play()

    # Método que faz o jogador atirar triplo (Quando powwer-up ativo)
    def atirar_triplo(self):
        if len(self.tiros) < 9:
            self.tiros.add(Tiro(self.rect.centerx - 50, self.rect.top))
            self.tiros.add(Tiro(self.rect.centerx, self.rect.top))
            self.tiros.add(Tiro(self.rect.centerx + 50, self.rect.top))
            som_tiro.play()


# Cria o vírus (Inimigo)
class Virus(Sprite):
    def __init__(self):
        super().__init__()
        self.velocidade = 1
        self.image = pygame.image.load('Game-images/inimigo_1.png')
        self.rect = self.image.get_rect(
            center=(randint(20, 800), 0)
        )
        # Ajusta a velocidade com base na pontuação
        if pontos < 80:
            self.velocidade = 1
        elif pontos > 80:
            self.velocidade = 1.5
        elif pontos > 100:
            self.velocidade = 2
        elif pontos > 120:
            self.velocidade = 2.5
        elif pontos > 160:
            self.velocidade = 3
        elif pontos > 200:
            self.velocidade = 3.5

        # Gera um power-up com certa probalidade
        if random() < 0.07:
            if len(grupo_powerUp) < 1 and powerUp_tiro_ativo == False:
                self.gerar_powerUp_tiro()

        if random() < 0.07:
            if len(grupo_powerUp) < 1 and powerUp_velocidade_ativo == False:
                self.gerar_powerUp_velocidade()

        if random() < 0.03:
            if len(grupo_powerUp) < 1 and powerUp_escudo_ativo == False:
                self.gerar_powerUp_escudo()

    # Método que gera o power-up de tiro
    def gerar_powerUp_tiro(self):
        powerup_tiro = PowerUp_tiro()
        grupo_powerUp.add(powerup_tiro)

    # Método que gera o power-up de velocidade
    def gerar_powerUp_velocidade(self):
        powerup_velocidade = PowerUp_velocidade()
        grupo_powerUp.add(powerup_velocidade)

    # Método que gera o power-up de escudo
    def gerar_powerUp_escudo(self):
        powerup_escudo = PowerUp_escudo()
        grupo_powerUp.add(powerup_escudo)

    def update(self):
        self.rect.y += self.velocidade

        if self.rect.y > 600:
            self.kill()
            global q
            global pontos
            q -= 1
            pontos -= 1


# Cria grupos de sprites
grupo_powerUp = Group()
grupo_tiro = Group()
grupo_inimigos = Group()
jogador = Jogador(grupo_tiro)
grupo_jogador = GroupSingle(jogador)

grupo_inimigos.add(Virus())

# Cria um relogio para o jogo
clock = pygame.time.Clock()

jogo_perdido = False

''' Loop principal do jogo '''
while loop:

    # Ajusta a quantidade de inimigos com base na pontuação
    if pontos < 21:
        if q < 3:
            grupo_inimigos.add(Virus())
            q += 1

    if pontos > 20:
        if q < 4:
            grupo_inimigos.add(Virus())
            q += 1
        nivel = 1

    if pontos > 40:
        if q < 5:
            grupo_inimigos.add(Virus())
            q += 1
        nivel = 2

    if pontos > 60:
        if q < 6:
            grupo_inimigos.add(Virus())
            q += 1
        nivel = 3

    if pontos > 80:
        nivel = 4

    if pontos > 100:
        nivel = 5

    if pontos > 120:
        nivel = 6

    if pontos > 140:
        nivel = 7
        if q < 7:
            grupo_inimigos.add(Virus())
            q += 1

    if pontos > 160:
        nivel = 8

    if pontos > 180:
        nivel = 9
        if q < 8:
            grupo_inimigos.add(Virus())
            q += 1

    if pontos > 200:
        nivel = 10

    clock.tick(120)  # controla o tempo de atualização da tela

    superficie.blit(fundo, (0, 0))

    ''' Eventos do jogo '''
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Fechamento da janela
            loop = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:  # Se espaço foi pressionado
                if powerUp_tiro_ativo:
                    jogador.atirar_triplo()
                else:
                    jogador.atirar()
            if evento.key == pygame.K_ESCAPE:
                menu_pausa.executar()

    # Desenha e atualiza os grupos de sprites
    grupo_jogador.draw(superficie)
    grupo_jogador.update()

    grupo_inimigos.draw(superficie)
    grupo_inimigos.update()

    grupo_tiro.draw(superficie)
    grupo_tiro.update()

    grupo_powerUp.draw(superficie)
    grupo_powerUp.update()

    # Verifica a colisão entre jogador e power-up
    for powerup in grupo_powerUp:
        if pygame.sprite.collide_rect(jogador, powerup):

            if powerup.tipo == 'tiro':
                powerup.kill()
                powerUp_tiro_ativo = True
                powerUp_tiro_timer = pygame.time.get_ticks()

            if powerup.tipo == 'velocidade':
                powerup.kill()
                powerUp_velocidade_ativo = True
                powerUp_velocidade_timer = pygame.time.get_ticks()
                jogador.velocidade = 8

            if powerup.tipo == 'escudo':
                powerup.kill()
                powerUp_escudo_ativo = True
                powerUp_escudo_timer = pygame.time.get_ticks()
                jogador.image = pygame.transform.scale(pygame.image.load('Game-images/space-invaders_l.png'),
                                                       (100, 100))

    # Desativa o power-up apos ceto tempo
    if powerUp_tiro_ativo and pygame.time.get_ticks() - powerUp_tiro_timer > 5000:
        powerUp_tiro_ativo = False

    if powerUp_velocidade_ativo and pygame.time.get_ticks() - powerUp_velocidade_timer > 5000:
        powerUp_velocidade_ativo = False
        jogador.velocidade = 3.5

    if powerUp_escudo_ativo and pygame.time.get_ticks() - powerUp_escudo_timer > 10000:
        powerUp_escudo_ativo = False
        jogador.image = pygame.transform.scale(pygame.image.load('Game-images/space-invaders.png'), (80, 80))

    # Verifica as colisões entre os tiros e os inimigos
    for tiro in grupo_tiro:
        inimigos_atingidos = pygame.sprite.spritecollide(tiro, grupo_inimigos, True)

        for inimigo in inimigos_atingidos:
            tiro.kill()
            q -= 1
            pontos += 1

    # Verifica se houve colisão entre o jogador e os inimigos
    colisoes = pygame.sprite.spritecollide(jogador, grupo_inimigos, False)

    # Se hover colisão, o jogador perde o jogo
    if colisoes and not powerUp_escudo_ativo:
        escolha_game_over = mostrar_game_over()

        if escolha_game_over == 'sair':
            loop = False
        elif escolha_game_over == 'voltar':
            pontos = 0
            q = 0
            nivel = 0
            grupo_inimigos.empty()
            grupo_tiro.empty()
            grupo_powerUp.empty()
            jogador.rect.centerx = tamanho_tela[0] // 2
            jogador.rect.bottom = tamanho_tela[1] - 10
            loop = True
        elif escolha_game_over == 'Ajuda':
            ajuda.executar()

    # Exibe na tela a pontuação e o nivel do jogador
    texto_pontos = fonte.render(f'Pontos: {pontos}', True, 'white')
    texto_nivel = fonte.render(f'Nivel: {nivel}', True, (255, 255, 255))

    superficie.blit(texto_pontos, (10, 10))
    superficie.blit(texto_nivel, (10, 40))

    pygame.display.update()

print('Obrigado por jogar Invasão Espacial.')