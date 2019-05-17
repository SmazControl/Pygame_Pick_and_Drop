# Pick and Drop Multi Picture
# Supot Sawangpiriyakij 
# Desc. Click to Pick and Click again to Drop
# Base code from Kelvin Saltion
# https://updatedcode.wordpress.com/2016/04/24/pygame-drag-and-drop
# Importa as bibliotecas utilizadas
import sys, pygame
from pygame import mouse

# Define uma cor padrao em RGB
WHITE = (255, 255, 255)

def xrange(x,y):
    return iter(range(x,y))

# Cria uma classe para armazenar os atributos do nosso heroi
class Hero(object):
    # Deixei alguns valores por padrao apenas por comodidade
    def __init__(self, image_path = "C:/Users/Admin/Desktop/chew.png", scale = (100,160), position = [100, 200]):
        # Caminho para a imagem que ira representar o heroi
        self.image_path = image_path
        # Posicao inicial do heroi na tela
        self.position = position
        # Escala fixa do heroi
        self.scale = scale
        # Variavel utilizada para saber se o heroi esta selecionado ou nao
        self.held = False

        # Carrega a imagem do heroi
        self.image = pygame.image.load(self.image_path).convert_alpha()
        # Redimensiona a imagem para a escala definida
        self.image = pygame.transform.scale(self.image, self.scale)

class Mouse_Mode(object):
    def __init__(self, position = [0,0]):
        self.mode = False
        self.position = position

# Classe principal responsavel pela logica do jogo
class Game(object):

    def __init__(self,mouse_mode):
        # Inicializa a biblioteca pygame
        pygame.init()
        # Define a largura e altura da janela em pixels 600x400
        self.main_window = pygame.display.set_mode((600, 400))

        # Define um nome para a janela
        pygame.display.set_caption("Pick and Drop")

        # Utiliza uma lista para armazenar os herois do jogo
        self.heroes = []
        mouse_mode.position = mouse.get_pos()

        # Utilizado para controlar a velocidade de quadros (de atualizacoes da tela)
        self.clock = pygame.time.Clock()
        
    def is_mouse_same_position(self, mouse_mode):
        mouse_pos = mouse.get_pos()
        if mouse_pos == mouse_mode.position:
           return True
        else:
           return False

    # Funcao utilizada para criar e carregar a imagem de todos os herois
    def create_heroes(self):
        self.heroes.append(Hero("C:/Users/Admin/Desktop/chew.png", (100, 160), [100, 200]))
        self.heroes.append(Hero("C:/Users/Admin/Desktop/chew.png", (80, 128), [50, 100]))
        self.heroes.append(Hero("C:/Users/Admin/Desktop/chew.png", (50, 80), [400, 300]))
        self.heroes.append(Hero("C:/Users/Admin/Desktop/chew.png", (25, 40), [300, 250]))

    # Funcao utilizada para verificar se a posicao do mouse esta em cima
    # de um heroi (passado por parametro)
    def is_over(self, mouse_pos, hero):
        # Verifica a posicao no eixo X
        if mouse_pos[0] > hero.position[0] and mouse_pos[0] < hero.position[0] + hero.scale[0]:
            # Verifica a posicao no eixo Y
            if mouse_pos[1] > hero.position[1] and mouse_pos[1] < hero.position[1] + hero.scale[1]:
                return True
        return False

    # Funcao chamada quando o usuario clica com o mouse
    def mouse_button_down(self, mouse_mode):
        if mouse_mode.mode == False:
           # Obtem a posicao atual do mouse
           mouse_pos = mouse.get_pos()
           mouse_mode.position = mouse_pos
           mouse_mode.mode = True
           for i in xrange(0, len(self.heroes)):
               # Somente "ativa" a imagem_selecionada se o usuario clicou em cima da imagem
               if self.is_over(mouse_pos, self.heroes[i]):
                  self.heroes[i].held = True
        else:
           if self.is_mouse_same_position(mouse_mode)==False:
              mouse_mode.mode = False
              # 'Libera' todos os herois
              for i in xrange(0, len(self.heroes)):
                  self.heroes[i].held = False

    # Funcao responsavel por atualizar a posicao de todos os herois
    def update_position(self):
        # Obtem a posicao atual do mouse
        mouse_pos = mouse.get_pos()

        for i in xrange(0, len(self.heroes)):
            # Se a variavel imagem_selecionada estiver "ativa" (True), atualiza a posicao da imagem
            if self.heroes[i].held:
                # Define as posicoes X e Y da imagem, posiciona a imagem com o mouse centralizado
                self.heroes[i].position[0] = mouse_pos[0] - self.heroes[i].scale[0]/2
                self.heroes[i].position[1] = mouse_pos[1] - self.heroes[i].scale[1]/2

    # Funcao que roda o jogo
    def run(self, mouse_mode):
        # Chama a funcao para criar os herois
        self.create_heroes()

        # Loop principal do jogo
        while True:

            # Verifica se algum evento aconteceu
            for event in pygame.event.get():
                # Verifica se foi um evento de saida (pygame.QUIT), em caso afirmativo fecha a aplicacao
                if event.type == pygame.QUIT: 
                     sys.exit()
                # Se o usuario soltar o botao do mouse "ativa" a variavel imagem_selecionada
                elif event.type == pygame.MOUSEBUTTONDOWN:
                     self.mouse_button_down(mouse_mode)

            # Chama a funcao que atualiza a posicao dos herois
            self.update_position()

            # Preenche a tela com uma cor, neste caso preto (definido logo apos importar as bibliotecas)
            self.main_window.fill(WHITE)
            
            # Coloca a imagem de todos os herois na tela com base na posicao
            for i in xrange(0, len(self.heroes)):
                self.main_window.blit(self.heroes[i].image, self.heroes[i].position)
            
            # Atualiza a tela visivel ao usuario
            pygame.display.flip()

            # Limita a taxa de quadros (framerate) a 60 quadros por segundo (60fps)
            self.clock.tick(60)

if __name__ == "__main__":
    mouse_mode = Mouse_Mode()
    game = Game(mouse_mode)
    game.run(mouse_mode)
