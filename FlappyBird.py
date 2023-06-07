# Importando a biblioteca da criação de jogos
import pygame 
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
        return pygame.mask.from_surface(self.imagem_passaro)
            
        
        
class Cano:
    
    # Definindo constantes de distancias de um cano para o outro
    DISTANCIA = 200
    VELOCIDADE = 5
    
    # Definindo a função init, passando só a posição X pois ela será gerada somente dentro dos canos, em qual posição 
    # do eixo X ele vai estar 
    def __init__(self, x):
        self.x = x 
        self.altura = 0 
        self.posicao_topo = 0
        self.posicao_base = 0
        # flipando no eixo Y
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()
        
    # DEFININDO ALTURA DO CANO     
    def definir_altura(self):
        # Gerando numero aleatorio em um intervalo entre 50 e 450
        self.altura = random.randrange(50, 450)
        # lembrar que para subir, subtrai, para descer, soma
        self.posicao_topo = self.altura - self.CANO_TOPO.get_height()
        self.posicao_base = self.altura + self.DISTANCIA
    
    # Função para mover os canos
    def mover(self, x):
        # mover os canos de forma negativa tirando valor de x
        self.x -= self.VELOCIDADE
    
    # Função para desenhar o cano
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.posicao_topo))
        tela.blit(self.CANO_BASE, (self.x, self.posicao_base))
        
    # Verificando se o cano e o passaro colidem 
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)
        
        # Deve-se pegar a distancia do topo do cano, para mask do passaro
        # criando o metodo para verificar a colisão 
        distancia_topo = (self.x - passaro.x, self.posicao_topo - round(passaro.y)) 
        distancia_base = (self.x - passaro.x, self.posicao_base - round(passaro.y)) 
        
        # calculando a colição 
        # Overlap verificará se tem pontos em comum entre os pixels, VERDADEIRO OU FALSO
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        
        # Verificando se o passaro colidiu 
        if base_ponto or topo_ponto:
            return True
        else:
            return False
    
class Chao:
    # Definindo constantes
    VELOCIDADE = 5 
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO


    # Definindo o init só com valor do eixo y
    # será passado para o chão
    def __init__(self, y):
        self.y = y 
        # x do primeiro chão
        self.x1 = 0
        # x do segundo chão
        self.x2 = self.LARGURA
        
    # Criando a função para mover o chão 
    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        # Movendo o chão 1 após o chão 2 passar
        if self.x1 + self.LARGURA < 0:
            # a lógica irá pegar o primeiro chão e andar apenas a largura que falta
            # caso não seja 0 especificamente
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0: 
            self.x2 = self.x1 + self.LARGURA

    # Função para desenhar o chão 
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))
        


# Criando uma função para desenhar a tela do jogo 
def desenhar_tela(tela, passaros, canos, chao, pontos):
    # Desenhar o fundo da tela, passando a imagem e a tupla com a posição inicial
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    
    # Desenhar o pássaro através de uma lista para os pássaros da IA estarem otimizados
    for passaro in passaros:
        passaro.desenhar(tela)
    
    # Desenhar o cano através de uma lista de canos para que tenha mais de um na tela
    for cano in canos: 
        cano.desenhar(tela)
        
    # Colocando o texto na tela passando um parametro para o texto não ficar pixelado e a cor
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    # desenhando o texto no canto da tela passando a largura menos 10 e a posição
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10 ))
    # desenhando o chão 
    chao.desenhar(tela)    
    # realizando update na tela
    pygame.display.update()
    

# Criando a função principal do jogo 
def main():
    # Criando os passaros através de uma instancia da classe Passaro
    passaros = [Passaro(230, 350)]
    # Criando o chão 
    chao = Chao(730)
    # Criando os canos, passando só o x, pois o y é gerado aleatoriamente
    canos = [Cano(700)]
    # Criando a tela passando uma tupla com largura e altura
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    # Definindo pontuação 
    pontos = 0
    # Criando um relogio para atualizar a animação do tempo
    relogio = pygame.time.Clock()
    
    
    # Criando o loop para o jogo continuar rodando
    rodando = True
    while rodando:
        # Andando o tempo do relogio passando os frames por segundo 
        relogio.tick(30)
        
        # Criar a forma de interação do usuário com o game, o evento através de uma lista
        for evento in pygame.event.get():
            # Se clicar no x, o pygame irá fechar
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            # Mandando o passaro pular APERTANDO UMA TECLA NO TECLADO
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros: 
                        passaro.pular()
        
        # Movendo os itens do game 
        for passaro in passaros: 
            passaro.mover()
        chao.mover()
        
        # Movimentando o cano com cuidado para não colidir os canos
        # Cria-se uma variavel auxiliar
        adicionar_cano = False
        remover_canos = []   
        
        for cano in canos: 
            # Verificar se o cano bateu com o passaro com enumerate, 
            # irá verificar a posição do passaro dentro da lista para utilizar a função pop 
            for i, passaro in enumerate(passaros):
                # Verificando se o passaro colidiu com o ano e removendo, caso sim
                if cano.colidir(passaro):
                    passaros.pop(i)
                # Verificando se o passaro passou do cano e se o x do passaro for maior do que o x do cano, 
                # a variavel passou será modificado na posição do x cano 
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            # Verificando se o cano já saiu da tela pegando sua posição e vendo se é menor do que 0 
            if cano.x + cano.CANO_TOPO.get_width() < 0:
               # Adiciona uma lista de canos no for do cano, depois que acabar o for, irá adicionar quem tem que adicionar
               # Excluir quem tem que excluir
               remover_canos.append(cano)      
        
        if adicionar_cano:
            pontos += 1
            # Caso ele passe o cano, adiciona um cano na posição do fundo
            cano.append(Cano(600))
        
        # Removendo os canos que passaram 
        for cano in remover_canos:
            canos.remove(cano)
            
        # Tratando caso o passaro colida com o ceu ou com o chão
        for i, passaro in enumerate(passaros):
            # Se a posição y do passaro e o tamanho dele forem maiores que o chão ou caso seja menor que 0
            if (passaro.y + passaro.imagem_passaro.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
        
        desenhar_tela(tela, passaros, canos, chao, pontos)
        
    
# Rodando a função main, pegando o arquivo python utilizando o name para rodar o arquivo, caso ele seja executado 
# de forma direta, caso não, ele não irá rodar 
if __name__ == '__main__':
    main()