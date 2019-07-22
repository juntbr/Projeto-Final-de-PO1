import pygame
import random
from tkinter import *
from tkinter import messagebox
WIDTH = 860
HEIGHT = 600
FPS = 60

# cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# cria o jogo e cria a janela
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TankaoBrabo")
clock = pygame.time.Clock()
##carregando as imagens usadas durante o jogo
background_image = pygame.image.load("backgroundColor3.png").convert()
animal = pygame.image.load("animais/1.png").convert()
lista = [0]*8
lista[0] = pygame.image.load("animais/1.png").convert()
lista[1] = pygame.image.load("animais/6.png").convert()
lista[2] = pygame.image.load("animais/6.png").convert()

class Tank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./tankao.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = 50
        self.rect.bottom = 70
        self.speedy = 0

    def update(self):
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.y += self.speedy   
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0     
    def shoot(self):
        tiro = Tiro(self.rect.centerx, self.rect.top)
        all_sprites.add(tiro)
        tiros.add(tiro)
class Monstro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(lista[1], (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 790
        self.rect.y = random.randrange(1, 560)
        self.speedx = random.randrange(-8, -1)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = 790
            self.rect.y = random.randrange(1, 560)

font_name = pygame.font.match_font('arial')
##função pra escrever o texto na tela
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y+20
        self.rect.centerx = 100
        self.speedx = -10

    def update(self):
        self.rect.x -= self.speedx
        # kill se o tiro sair da tela
        if self.rect.right > WIDTH:
            self.kill()

score = 0
all_sprites = pygame.sprite.Group()
monstros = pygame.sprite.Group()
tiros = pygame.sprite.Group()
tank = Tank()
all_sprites.add(tank)
def subirNivel():
    for i in range(10):
        m = Monstro()
        all_sprites.add(m)
        monstros.add(m)
for i in range(8):
    m = Monstro()
    all_sprites.add(m)
    monstros.add(m)
def jogoRodando(score):
	running = True
	while running:
	    # keep loop running at the right speed
	    clock.tick(FPS)
		
	    for event in pygame.event.get():
	        
	        if event.type == pygame.QUIT:
	            running = False
	        elif event.type == pygame.KEYDOWN:
	            if event.key == pygame.K_SPACE:
	                tank.shoot()

	    # update
	    all_sprites.update()
		
	    # verificar se o tiro atingiu o monstro
	    hits = pygame.sprite.groupcollide(monstros, tiros, True, True)
	    for hit in hits:
	        if score==1000:
	            subirNivel()
	        if score==10000:
	            subirNivel()
	        if score==5000:
	            subirNivel()
	        score += 50
	        m = Monstro()
	        all_sprites.add(m)
	        monstros.add(m)
	    # verificar se um monstro atingiu o tank
	    hits = pygame.sprite.spritecollide(tank, monstros, False)
	    if hits:
	        Tk().wm_withdraw() #to hide the main window
	        messagebox.showinfo('Parece que você morreu! :( ','Aceita que dói menos')
	        running = False

	    # Render
	    screen.blit(background_image, [0, 0])
	    all_sprites.draw(screen)
	    draw_text(screen, str(score), 18, WIDTH / 2, 10)
	    pygame.display.flip()

	pygame.quit()
	pygame.quit()
jogoRodando(score)