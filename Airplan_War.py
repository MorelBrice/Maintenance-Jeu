import pygame
import button
import constantes

pygame.init()

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
game_paused = True
menu_state = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 90)
font2_electric_boogaloo = pygame.font.SysFont("arialblack", 92)

High_font = pygame.font.SysFont("arialblack", 70)
High_font2_electric_boogaloo = pygame.font.SysFont("arialblack", 70)

#define colours
TEXT_COL = (255, 255, 255)
TEXT_COL2 = (0,0,0)

#load button images
resume_img = pygame.image.load("resources/image/button_resume.png").convert_alpha()
quit_img = pygame.image.load("resources/image/button_quit.png").convert_alpha()

wallpaper = pygame.image.load('resources/image/menu_wallpaper.jpg')	
background = pygame.transform.scale(wallpaper, (SCREEN_WIDTH * 1.5, SCREEN_HEIGHT))

#create button instances
resume_button = button.Button(304, 275, resume_img, 1)
quit_button = button.Button(336, 375, quit_img, 1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#game loop
run = True

background_song = pygame.mixer.Sound('resources/sound/On_The_Moon.mp3')
background_song.set_volume(constantes.SOUND_VOLUME)
run_once_start = 0
run_once_stop = 0

while run:

    if run_once_stop == 0:
        pygame.mixer.pause()
        run_once_stop = 1

    # screen.fill((52, 78, 91))
    screen.fill(0)
    screen.blit(background, (0, 0))

    if run_once_start == 0:
        background_song.play()
        run_once_start = 1

    draw_text("Airplane War", font2_electric_boogaloo, TEXT_COL2, SCREEN_WIDTH // 3.85, SCREEN_HEIGHT // 3.6)
    draw_text("Airplane War", font, TEXT_COL, SCREEN_WIDTH // 3.7, SCREEN_HEIGHT // 3.7)


    high = open("highscore.txt", "r")
    highscore = high.read()

    draw_text("Highscore : " + highscore, High_font2_electric_boogaloo, TEXT_COL2, SCREEN_WIDTH // 3.85, SCREEN_HEIGHT // 1.19)
    draw_text("Highscore : " + highscore, High_font, TEXT_COL, SCREEN_WIDTH // 3.7, SCREEN_HEIGHT // 1.2)

    high.close()

    #check menu state
    if menu_state == "main":
        #draw pause screen buttons
        if resume_button.draw(screen):
            exec(open("stage.py").read())
        if quit_button.draw(screen):
            run = False


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()