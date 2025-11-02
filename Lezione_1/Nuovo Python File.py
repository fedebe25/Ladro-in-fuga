import pygame
import sys

# -------------------------------
# Inizializzazione Pygame
# -------------------------------
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Ladro in fuga - Test animazioni")
clock = pygame.time.Clock()

# -------------------------------
# Caricamento immagini
# -------------------------------

# Sfondo secondario
location_img = pygame.image.load("images/location.png")

# Animazione ladro (3 frame)
ladro_frames = [
    pygame.image.load("images/ladro2.png"),
    pygame.image.load("images/ladro3.png")
]

# Animazione moneta (5 frame)
coin_frames = [
    pygame.image.load("images/coin1.png"),
    pygame.image.load("images/coin2.png"),
    pygame.image.load("images/coin3.png"),
    pygame.image.load("images/coin4.png"),
    pygame.image.load("images/coin5.png")
]

# Poliziotto statico
police_img = pygame.image.load("images/policeprove.png")

# Poliziotto aggiuntivo in primo piano (police1)
police1_img = pygame.image.load("images/police1.png")

# Oggetti statici
spazzatura_img = pygame.image.load("images/spazzatura.png")
idrante_img = pygame.image.load("images/idrante.png")
car_img = pygame.image.load("images/car.png")

# -------------------------------
# Posizioni iniziali
# -------------------------------
ladro_x, ladro_y = 100, 260
coin_x, coin_y = 400, 270
police_x, police_y = 600, 250
police1_x, police1_y = 650, 250
spazzatura_x, spazzatura_y = 600, 290
idrante_x, idrante_y = 700, 290
car_x, car_y = 500, 250

# -------------------------------
# Variabili per animazioni
# -------------------------------
ladro_frame = 0
coin_frame = 0
frame_timer = 0

ladro_anim_speed = 0.15
coin_anim_speed = 0.20

# -------------------------------
# Ciclo principale
# -------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    frame_timer += 1

    # Animazioni
    if frame_timer % int(10 / ladro_anim_speed) == 0:
        ladro_frame = (ladro_frame + 1) % len(ladro_frames)

    if frame_timer % int(10 / coin_anim_speed) == 0:
        coin_frame = (coin_frame + 1) % len(coin_frames)

    # -------------------------------
    # Disegno dello schermo
    # -------------------------------
    # Sfondo location (secondo piano)
    screen.blit(location_img, (0, 0))

    # Oggetti statici
    screen.blit(spazzatura_img, (spazzatura_x, spazzatura_y))
    screen.blit(idrante_img, (idrante_x, idrante_y))
    screen.blit(car_img, (car_x, car_y))
    screen.blit(police_img, (police_x, police_y))

    # Poliziotto in primo piano
    screen.blit(police1_img, (police1_x, police1_y))

    # Personaggi animati
    screen.blit(ladro_frames[ladro_frame], (ladro_x, ladro_y))
    screen.blit(coin_frames[coin_frame], (coin_x, coin_y))

    pygame.display.update()
    clock.tick(60)


