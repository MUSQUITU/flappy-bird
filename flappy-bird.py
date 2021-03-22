# biblioteca responsavel por renderizar o jogo
import pygame
# biblioteca utilizada para gerar numeros aleatorios
import random
# biblioteca das constantes do pygame
from pygame.locals import *

# dimensoes da tela
SCREEN_WIDTH = 400   # largura
SCREEN_HEIGHT = 800  # altura
# velocidade do passaro, velocidade do corpo
SPEED = 10
# queda do passaro
GRAVIDADE = 1
# velocidade do jogo
GAME_SPEED = 10
# dimensoes do chao
GROUND_WIDTH = 2 * SCREEN_HEIGHT  # duplicado pelo tamanho da tela p estender
GROUND_HEIGHT = 100

# Dimensoes dos canos
PIPE_WIDTH = 80  # largura
PIPE_HEIGHT = 500  # altura

# espaco entre os canos
PIPE_GAP = 200


class Passaro(pygame.sprite.Sprite):
    # class das funcoes do passaro

    def __init__(self):
        # construtor do pygame
        pygame.sprite.Sprite.__init__(self)
        # imagens para o movimento do passaro
        # toda imagem tem que haver um 'image' e um 'rect'
        self.images = [
            pygame.image.load('bluebird-upflap.png').convert_alpha(),
            pygame.image.load(
                'bluebird-midflap.png').convert_alpha(),
            pygame.image.load(
                'bluebird-downflap.png').convert_alpha()]

        # velocidade do passaro
        self.speed = SPEED

        # variavel para fazer a troca de imagens
        self.current_image = 0

        # a imagem inicial com as asas p cima
        # convert_alfa pra converter a transparecia
        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()
        # mascara para detectar a colisao
        # usando apenas os pixels definidos, descartando os transparentes
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        # posicionamento do passaro na tela
        self.rect[0] = SCREEN_WIDTH / 2  # posicao x
        self.rect[1] = SCREEN_HEIGHT / 2  # posicao y

    def update(self):
        # atualizacao das imagens pro movimento das assas
        # current_image comeca com 0 conta ate 2, quando chega em 3 o %3 da zero e comeca de novo
        # a contagem fica 0, 1 e 2
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        # forca contraria
        # cada frame o passaro cai no valor da gravidade
        self.speed += GRAVIDADE

        # atualizacao da altura
        # o passaro vai p cima
        self.rect[1] += self.speed

    # pulo do passaro
    def bump(self):
        self.speed = -SPEED


class Pipe(pygame.sprite.Sprite):
    # classe com as funcoes do cano
    # inverted = invertido, xpos = posicao em x, ysize = tamanho em y
    def __init__(self, invereted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        # adcionando imagem e escalando no tamanho
        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        # inversao da imagem dos canos
        if invereted:
            # flip(imagem, x, y)
            # pega a altura do cano menos a altura desejada
            # 'esconde' o cano
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            # quando n ta invertido depende da altura da tela menos o tamanho desejado
            self.rect[1] = SCREEN_HEIGHT - ysize

         # mascara para detectar a colisao
        self.mask = pygame.mask.from_surface(self.image)

    # atualizacao pega a imagem e joga pra tras
    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):
    # clase pra definir a base do jogo

    def __init__(self, xpos):  # xpos = posicao x
        pygame.sprite.Sprite.__init__(self)

        # adcionando imagem e escalando no tamanho
        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        # mascara para detectar a colisao
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        # posicionar a base na parte de baixo da tela
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    # atualizacao pega a imagem e joga pra tras
    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    # funcao pra verificar se o sprite ta fora da tela
    # se o tamanho de x for menor que a largura do objeto
    # rect [2] = largura da tela
    return sprite.rect[0] < -(sprite.rect[2])


def get_random_pipes(xpos):             # funcao pra espanar os canos aleatoriamente
    size = random.randint(100, 300)     # randomica entre os tamanhos 100 e 300
    # posicao do cano NAO INVERTIDO / Pipe(inverted, xpos, size)
    pipe = Pipe(False, xpos, size)
    # Posicao do cano invertido
    # Pipe(invertido, posicao x, tamnanho da tela menos o tamanho do cano nao invertido menos o espaco entre os canos)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)  # retona uma tupla com os dois canos


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# adicionando e escalando a imagem de background
BACKGROUND = pygame.image.load('background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))


passaro_grupo = pygame.sprite.Group()
passaro = Passaro()
passaro_grupo.add(passaro)

ground_group = pygame.sprite.Group()
for i in range(2):  # estendendo a base
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)


pipe_group = pygame.sprite.Group()
for i in range(2):
    # 700 = espaco p primeiro cano
    pipes = get_random_pipes(SCREEN_WIDTH * i + 700)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

# controle do fps da batida das assas do passaro
clock = pygame.time.Clock()

while True:
    clock.tick(30)  # 30 fps
    # interacao para fechar o jogo
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    # evento pro pulo do passaro
    # ao clicar na tecla up, o passaro pula
    if event.type == KEYDOWN:
        if event.key == K_UP:
            passaro.bump()

    # posicao do background na tela
    screen.blit(BACKGROUND, (0, 0))

    # testa o primeiro ground se ta fora da tela
    if is_off_screen(ground_group.sprites()[0]):
        # se tiver fora da tela remove o sprite
        ground_group.remove(ground_group.sprites()[0])
        # depois add um novo ground
        new_ground = Ground(GROUND_WIDTH)
        ground_group.add(new_ground)

    # testar os canos p ver se esta fora da tela
    if is_off_screen(pipe_group.sprites()[0]):
        # se tiver fora da tela remove os canos
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        # gera um cano mais a frente
        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    # atualizacao dos grupos
    passaro_grupo.update()
    ground_group.update()
    pipe_group.update()

    # draw - Essa funcao funciona para renderizar em qualquer formato de superficie.
    # desenha na supercie, no caso na tela = screen
    passaro_grupo.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)
    pygame.display.update()
    # colisao
    # caso o passaro colide com o chao ele para o jogo ou com o cano
    if (pygame.sprite.groupcollide(passaro_grupo, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(passaro_grupo, pipe_group, False, False, pygame.sprite.collide_mask)):
       # Game over
        input()
        break

    # Ele permite que apenas uma parte da tela seja atualizada,
    # em vez de toda a area. Se nenhum argumento for passado,
    # ele atualiza toda a area de superficie como pygame.display.flip ()
