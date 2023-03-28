# -*- coding: utf-8 -*-

from email.headerregistry import Group
import random
import pygame
from pygame.locals import *
from sys import exit
import constantes
import time

# Initialize the game
pygame.init()
screen = pygame.display.set_mode((constantes.SCREEN_WIDTH, constantes.SCREEN_HEIGHT))
pygame.display. set_caption('Airplane Wars') 

# Load the background map
background = pygame.image.load('resources/image/background.png')
gameover = pygame.image.load('resources/image/gameover.png')

# Load the picture of the plane
plane_img = pygame.image.load('resources/image/shoot.png')
# Select the position of the plane in the big picture, generate subsurface, and then initialize the position of the plane.


# Définir les paramètres liés à la surface utilisés par l'objet avion ennemi
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemies1 = pygame.sprite.Group()
enemy_frequency = constantes.NB_MIN_ENEMIES

clock = pygame.time.Clock()
running = True

shot_fired = False

            
# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs,init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = constantes.ENNEMY_SPEED
        self.down_index = constantes.DOWN_INDEX_INIT
    
    def move (self):
        self.rect.top += self.speed

# Bullets
class Bullet (pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = constantes.BULLET_SPEED

    def move(self):
        self.rect.top -= self.speed

# Players
class Player (pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = [] # List of pictures of player object wizard

        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
            
        self.rect = player_rect[0] # Initialize the rectangle where the picture is located
        self.rect.topleft = init_pos # Initialize the upper left corner coordinates of the rectangle
        self.speed = constantes.PLAYER_SPEED # Initialize the player speed, here is a definite value.
        self.bullets = pygame.sprite.Group() # Collection of bullets fired by the player's aircraft
        self.img_index = constantes.IMG_INDEX_INIT # Player Wizard Image Index
            
    def shoot (self, bullet_img):
        bullet = Bullet (bullet_img, self.rect.midtop)
        self.bullets.add (bullet)

    def moveUp (self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= constantes.SCREEN_HEIGHT - self.rect.height:
            self.rect.top = constantes.SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft (self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight (self):
        if self.rect.left >= constantes.SCREEN_WIDTH - self.rect.width:
            self.rect.left = constantes.SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

# Définir les paramètres liés au joueur
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126)) # Zone d'image du sprite du joueur
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126)) # Zone d'image du sprite d'explosion du joueur
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [constantes.PLAYER_X_POS, constantes.PLAYER_Y_POS]
player = Player(plane_img, player_rect, player_pos)

enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
enemy1_down_sound.set_volume(constantes.SOUND_VOLUME)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

# Stockez des avions détruits pour le rendu d'animations de sprites d'épaves
enemies_down = pygame.sprite.Group()


background_song = pygame.mixer.Sound('resources/sound/Unreal_Super_Hero_3.mp3')
background_song.set_volume(constantes.SOUND_VOLUME - 0.1)


bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
bullet_sound.set_volume(constantes.SOUND_VOLUME)

# Définir les paramètres liés à la surface utilisés par l'objet puce (bullets)
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)
shoot_frequency = constantes.SHOOTING_FREQUENCY

score = 0
run_once_stop = 0
run_once_start = 0

def dessiner_fond():
    """Redessine le fond.
    """    
    screen.fill(0)
    screen.blit(background, (0, 0))

def gerer_puce(player:Player):
    """Gère les déplacements d'une puce et la supprime si elle sort hors de la fenètre.

    Args:
        player (Player): Le joueur actuel.
    """    
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

def dessiner_avion(player:Player):
    """Dessine l'avion du joueur.

    Args:
        player (Player): Le joueur actuel.
    """    
    screen.blit(player.image[player.img_index], player.rect)
    player.bullets.draw(screen)

def apparition_ennemis(enemy_frequency:int, enemy1_img:pygame.Surface, enemy1_down_imgs:list, enemies1:Group)->int:
    """Gère l'apparition des avions ennemis.

    Args:
        enemy_frequency (int): Le nombre d'ennemis présents simultanément sur le jeu.
        enemy1_img (pygame.Surface): L'image d'un ennemi.
        enemy1_down_imgs (list):La liste des images pour l'annimation de destruction.
        enemies1 (Group): Le groupe contenant les ennemis.

    Returns:
        int: La fréquence des ennemis présents simultanément sur le jeu modifiée.
    """    
    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, constantes.SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img,
            enemy1_down_imgs,
            enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    return enemy_frequency

def temperer_apparition(enemy_frequency:int)->int:
    """Tempère le nombre d'ennemis présents simultanément sur le jeu.

    Args:
        enemy_frequency (int): La fréquence des ennemis présents simultanément sur le jeu.

    Returns:
        int: La nouvelle fréquence de présence des ennemis.
    """    
    if enemy_frequency >= constantes.NB_MAX_ENEMIES:
        enemy_frequency = constantes.NB_MIN_ENEMIES
    return enemy_frequency

def gerer_destruction_ennemis(enemies1:Group, player:Player, enemies_down:Group)->Group:
    """Gère la destruction des ennemis lorsqu'ils sont touchés par une puce.

    Args:
        enemies1 (Group): Les ennemis présents sur le jeu.
        player (Player): Le joueur actuel.
        enemies_down (Group): Les ennemis détruits.

    Returns:
        Group: Le groupe des ennemis détruits modifié.
    """    
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)
    return enemies_down

def dessiner_epave_ennemis(enemies_down:Group, enemy1_down_sound:pygame.mixer.Sound, score)->Group:
    """Dessine les ennemis détruits.

    Args:
        enemies_down (Group): Le groupe des ennemis détruits.
        enemy1_down_sound (pygame.mixer.Sound): Le son joué lors de la destruction d'un ennemis.

    Returns:
        Group: Le groupe mis à jour des ennemis détruits.
    """    
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
            score += 1
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1
    return enemies_down, score

def game_over(enemies1:Group, player:Player, joueur_down:Group)->Group:

    down = []

    boom = pygame.Rect(330, 624, 102, 126)

    joueur_down = pygame.sprite.spritecollideany(player, enemies1)
    if joueur_down != None:
        screen.blit(gameover, (0, 0))
        pygame.display.update()
        down.append(player)
        enemy1_down_sound.play()
        pygame.time.wait(1000)
        exec(open("Airplan_War.py").read())
    return down
    
def gerer_deplacements_ennemis(enemies1:Group)->Group:
    """Gère les déplacements des ennemis.

    Args:
        enemies1 (Group): Le groupe des ennemis présents sur le jeu.

    Returns:
        Group: Le groupe des ennemis présents actualisé.
    """    
    for enemy in enemies1:
        enemy.move()
        if enemy.rect.top > constantes.SCREEN_HEIGHT:
            enemies1.remove(enemy)
    enemies1.draw(screen)
    return enemies1

def gerer_deplacements_joueur(player:Player):
    """Gère les déplacements du joueur en fonction des touches directionnelles du clavier appuyées.

    Args:
        player (Player): Le joueur actuel.
    """    
    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_w] or key_pressed[K_UP]:
        player.moveUp()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        player.moveDown()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        player.moveLeft()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        player.moveRight()

def gerer_fermeture_jeu():
    """Arrête proprement le jeu lorsque l'utilisateur ferme la fenètre.
    """    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def tirer(player:Player, shoot_frequency:int):
    """Gère les tirs du joueur.

    Args:
        player (Player): Le joueur actuel.
    """ 
    key_pressed = pygame.key.get_pressed()

    for event in pygame.event.get() :
        if event.type == pygame.KEYUP:
            if key_pressed[K_SPACE]:
                bullet_sound.play()
                player.shoot(bullet_img)


def afficher_score(score):
    font = pygame.font.Font('freesansbold.ttf', 32)
 
    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('Score : ' + str(score), True, constantes.BLACK)
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    
    # set the center of the rectangular object.
    textRect.center = (constantes.SCREEN_WIDTH // 2, constantes.Y * 1.95)

    screen.blit(text, textRect)

    high = open("highscore.txt", "r")

    if int(high.read()) < int(score):
        high = open("highscore.txt", "w")
        high.write(str(score))
    # print(high.read())
    high.close()


while running:

    if run_once_stop == 0:
        pygame.mixer.pause()
        run_once_stop = 1

    # Contrôlez la fréquence d'images maximale du jeu
    clock.tick(45)

    # Draw the background
    dessiner_fond()

    if run_once_start == 0:
        background_song.play()
        run_once_start = 1

    # Contrôler la fréquence des tirs de balles et des balles de feu
    # shoot_frequency = gerer_freq_tirs(shoot_frequency)

    tirer(player, shoot_frequency)

    # Déplacer la puce, la supprimer si elle dépasse le cadre de la fenêtre
    gerer_puce(player)

    # Draw an airplane
    dessiner_avion(player)

    # Faire apparaître des avions ennemis :
    enemy_frequency = apparition_ennemis(enemy_frequency, enemy1_img, enemy1_down_imgs, enemies1)

    # Tempérer le nombre d'ennemis présents simultanéments sur le jeu
    enemy_frequency = temperer_apparition(enemy_frequency)
    
    # Ajoutez l'objet avion ennemi touché au groupe d'avions ennemis détruits, utilisé pour rendre l'animation de destruction
    enemies_down = gerer_destruction_ennemis(enemies1, player, enemies_down)

    # Dessinez l'animation de l'épave
    enemies_down, score = dessiner_epave_ennemis(enemies_down, enemy1_down_sound, score)

    afficher_score(score)

    # Déplacez l'avion ennemi, s'il dépasse la plage de la fenêtre, supprimez-le
    enemies1 = gerer_deplacements_ennemis(enemies1)

    # Update the screen
    pygame.display.update()

    joueur_down = game_over(enemies1, player, enemies_down)
    

    # Monitor keyboard events
    gerer_deplacements_joueur(player)

    # Process game exits
    gerer_fermeture_jeu()

