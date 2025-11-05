#Lezione 2 – Movimento
# Obiettivo: capire come il gioco passa da una sezione "normale" alla sezione del Boss finale
 
import pygame
import sys
import random
 
# --- Inizializzazione ---
pygame.init()
 
# Dimensioni schermo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ladro in fuga - Lezione 3: Boss Finale")
 
# Clock
clock = pygame.time.Clock()
FPS = 60
 
#TODO aggiungere le costanti di gioco
 
#TODO aggiungere in RGB i colori principali del gioco

#TODO aggiungere le informazioni del giocatore (velocità, vita, ecc..)
 
#TODO aggiungere gli elementi del livello
blocchi = [pygame.Rect(900, SCREEN_HEIGHT - 100, 50, 50)]
monete = [pygame.Rect(1000, SCREEN_HEIGHT - 200, 20, 20)]
nemici = [pygame.Rect(1600, SCREEN_HEIGHT - 100, 40, 40)]
 
#TODO Boss e proiettili
 
#TODO aggiungere font
 
#TODO funzione reset
def reset_giocatore():

# --- Ciclo principale ---
running = True
while running:
    clock.tick(FPS)
 
    # --- Gestione eventi ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    #TODO inpunt salto
    
 
    #TODO gravità
 
    #TODO collisione col suolo
  
    # --- Sezione normale (senza boss) ---
    if not boss_attivo:
        # Scorrimento degli oggetti verso sinistra
        for blocco in blocchi:
            blocco.x -= 4
        for moneta in monete:
            moneta.x -= 4
        for nemico in nemici:
            nemico.x -= 4
 
        #TODO raccolta delle monete
 
        #TODO collisione con i nemici
 
    #TODO sezione del boss
 
    # --- Disegno ---
    screen.fill(CELESTE)
    pygame.draw.rect(screen, MARRONE, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
    pygame.draw.rect(screen, VERDE, giocatore)
    
    #TODO disegna elementi
 
    #TODO HUD (vite, punti, sezione)

 
    pygame.display.flip()
