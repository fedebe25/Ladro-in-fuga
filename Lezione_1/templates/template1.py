# Lezione 1 – Template
# TODO: completare il codice seguendo le istruzioni della lezione

import pygame

# Inizializzazione Pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Ladro in fuga - Lezione 1")
clock = pygame.time.Clock()

# Ladro placeholder
player_x = 100
player_y = 250
player_width = 50
player_height = 50

running = True
while running:
    # Eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   

    #TODO:  Disegna sfondo
    
    #TODO: Disegna ladro (placeholder rettangolo rosso)

    # Aggiorna display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
