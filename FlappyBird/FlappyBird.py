# Importando a biblioteca da criação de jogos
from imgs import pygame 
# Biblioteca de integração para arquivos do pc
import os 
# Numeros aleatórios do python para os canos
import random

# Definindo as constantes do jogo 

TELA_LARGURA = 500
TELA_ALTURA = 800

# Utilizando o os para juntar as pastas, com nome do arquivo, chamando as pastas
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png'))),
]

# Selecionando uma fonte para o letreiro do score
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


# Criando os objetos do jogo, classes do Python 

class Passaro:
    # Definindo as constantes
    IMGS = IMAGENS_PASSARO
    # Animações da rotação, onde pode inclinar pra cima e pra baixo
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20 
    TEMPO_ANIMACAO = 5
    
    # Definindo os atributos do passaro
    def __init__(self, x, y ):
        self.x = x 
        self.y = y
        self.angulo = 0 
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem_passaro = 0
        self.imagem_passaro = self.IMGS[0]

    # Criando a função para o pulo do passaro
    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    # Função para mover o passaro e seus calculos 
    def mover(self):
        # Calcular o deslocamento
        self.tempo += 1
        # Formula do sorevetão
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
        
        # Restringir o deslocamento
        if deslocamento > 16:
            # definindo o deslocamento maximo
            deslocamento = 16
        elif deslocamento < 0:
            # Dando um ganho extra quando ele pular para facilitar o jogo
            deslocamento -= 2
            
        # para deslocar o passaro
        self.y += deslocamento
        
        
        # Animação do passaro (angulo)
        # se o passaro desloca pra cima, o bico estará para cima
        # ou para que ele não caia direto na posição inicial dele, um espaço é dado 
        # se a posição dele estiver abaixo da altura, ele ainda estará de bico para cima
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            # Caso contrário, ele pode cair diretamente
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO
        
    # função que se preocupa onde o passaro deve aparecer, como será a rotação, para facilitar
    def desenhar(self, tela):
        # Definindo imagem do passaro
        self.contagem_imagem_passaro += 1
        # lógica para verificar em qual imagem de passaro se encontra o jogo
        if self.contagem_imagem_passaro < self.TEMPO_ANIMACAO:
            self.imagem_passaro = self.IMGS[0]
        elif self.contagem_imagem_passaro < self.TEMPO_ANIMACAO * 2:
            self.imagem_passaro = self.IMGS[1]
        elif self.contagem_imagem_passaro < self.TEMPO_ANIMACAO * 3:          
            self.imagem_passaro = self.IMGS[2]
        elif self.contagem_imagem_passaro < self.TEMPO_ANIMACAO * 4:          
            self.imagem_passaro = self.IMGS[1]
        elif self.contagem_imagem_passaro >= self.TEMPO_ANIMACAO * 4 + 1:          
            self.imagem_passaro = self.IMGS[0]
            self.contagem_imagem_passaro = 0
        
        
        # se o passaro tiver caindo, não baterá asa
        if self.angulo >= -80:
            self.imagem_passaro = self.IMGS[1]
            self.contagem_imagem_passaro = self.TEMPO_ANIMACAO * 2
            
        
        # desenhar a imagem
        # Rotacionando a imagem do passaro, pega a imagem e os graus
        imagem_rotacionada = pygame.transform.rotate(self.imagem_passaro, self.angulo)
        # desenhando o objeto, ele pegará o retangulo que esta comportando a imagem para rotacionar o retangulo
        # sempre que quiser rotacionar, pode utilizar esse método abaixo
        posicao_centro_imagem = self.imagem_passaro.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center = posicao_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)
        
        
        # Criando a máscara para que o jogo não fique dando erro no pássaro, utilizando pixels para garantir isso
        def get_mask(self):
            # Na hora da colisão irá avaliar a mascara do passaro e a mascara do cano 
            # Se tiverem pixels em comum, bateram, se n, não bateram
            pygame.mask.from_surface(self.imagem_passaro)
            
        
class Cano:
    ...

class Chao:
    pass
