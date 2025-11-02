# Lezione 3 – Movimento degli ostacoli
# Obiettivo: creare ostacoli che scorrono verso sinistra e che il giocatore deve saltare
import pygame
import sys
import random
pygame.init()
# --- Impostazioni schermo ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ladro in fuga - Lezione 3: Ostacoli in movimento")
# --- Clock e FPS ---
clock = pygame.time.Clock()
FPS = 60
# --- Costanti ---
GRAVITA = 0.8
SALTO_FORZA = -15
TOLLERANZA = 10
PUNTEGGIO_PER_BOSS = 50
# --- Colori ---
CELESTE = (135, 206, 235)
MARRONE = (139, 69, 19)
GIALLO = (255, 215, 0)
VERDE = (0, 200, 0)
ROSSO = (255, 0, 0)
VIOLA = (128, 0, 128)
NERO = (0, 0, 0)
# --- Giocatore ---
giocatore = pygame.Rect(100, SCREEN_HEIGHT - 150, 40, 50)
vel_y = 0
puo_saltare = False
vite = 3
punteggio = 0
# --- TODO 1: Crea una lista di ostacoli che si muovono verso sinistra ---
# Ogni ostacolo è un dizionario: {"x": posizione iniziale, "y": altezza sul terreno}
# Esempio:
# obstacles = [{"x":800, "y":SCREEN_HEIGHT - 100}, {"x":1200, "y":SCREEN_HEIGHT - 100}]
# --- TODO 2: Crea una lista di monete che scorrono verso sinistra ---
# coins = [{"x":900, "y":SCREEN_HEIGHT - 200}, {"x":1300, "y":SCREEN_HEIGHT - 180}]
# --- Boss (uguale alla lezione 2) ---
boss = pygame.Rect(SCREEN_WIDTH + 200, SCREEN_HEIGHT - 150, 80, 80)
proiettili = []
boss_attivo = False
tempo_ultimo_proiettile = 0
tempo_ricarica = 1500
# --- Font ---
font = pygame.font.SysFont(None, 36)
# --- Funzione reset ---
def reset_giocatore():
   global vel_y, puo_saltare
   giocatore.x = 100
   giocatore.y = SCREEN_HEIGHT - 150
   vel_y = 0
   puo_saltare = False
reset_giocatore()
# --- Ciclo principale ---
running = True
while running:
   clock.tick(FPS)
   # --- Eventi ---
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
   # --- Input salto ---
   keys = pygame.key.get_pressed()
   if keys[pygame.K_SPACE] and puo_saltare:
       vel_y = SALTO_FORZA
       puo_saltare = False
   # --- Gravità ---
   vel_y += GRAVITA
   giocatore.y += vel_y
   # --- Collisione col suolo ---
   if giocatore.bottom >= SCREEN_HEIGHT - 50:
       giocatore.bottom = SCREEN_HEIGHT - 50
       vel_y = 0
       puo_saltare = True
   # --- Sezione normale ---
   if not boss_attivo:
       # TODO 3: Fai scorrere ostacoli e monete verso sinistra
       # for obs in obstacles:
       #     obs["x"] -= 5
       # for coin in coins:
       #     coin["x"] -= 5
       # --- TODO 4: Gestisci collisioni con gli ostacoli ---
       # for obs in obstacles:
       #     obs_rect = pygame.Rect(obs["x"], obs["y"], 50, 50)
       #
       #     if giocatore.colliderect(obs_rect):
       #         # Se il giocatore arriva dall'alto (salta sopra)
       #         if giocatore.bottom - vel_y <= obs_rect.top + TOLLERANZA:
       #             giocatore.bottom = obs_rect.top
       #             vel_y = 0
       #             puo_saltare = True
       #         else:
       #             # Se colpisce di lato → perde una vita
       #             vite -= 1
       #             reset_giocatore()
       # --- TODO 5: Gestisci collisioni con le monete ---
       # for coin in coins[:]:
       #     coin_rect = pygame.Rect(coin["x"], coin["y"], 20, 20)
       #     if giocatore.colliderect(coin_rect):
       #         coins.remove(coin)
       #         punteggio += 10
       # --- TODO 6: Attiva la sezione Boss se il punteggio è abbastanza alto ---
       # if punteggio >= PUNTEGGIO_PER_BOSS:
       #     boss_attivo = True
       #     reset_giocatore()
       #     boss.x = SCREEN_WIDTH + 200
   else:
       # TODO 7: Mantieni la logica del boss (dalla lezione 2)
       pass
   # --- Disegno ---
   screen.fill(CELESTE)
   pygame.draw.rect(screen, MARRONE, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
   pygame.draw.rect(screen, VERDE, giocatore)
   # --- TODO 8: Disegna ostacoli e monete ---
   # for obs in obstacles:
   #     pygame.draw.rect(screen, ROSSO, (obs["x"], obs["y"], 50, 50))
   # for coin in coins:
   #     pygame.draw.circle(screen, GIALLO, (int(coin["x"]), int(coin["y"])), 10)
   # --- HUD ---
   testo_vite = font.render(f"Vite: {vite}", True, NERO)
   testo_punti = font.render(f"Punti: {punteggio}", True, NERO)
   testo_stato = font.render("Boss: SI" if boss_attivo else "Boss: NO", True, NERO)
   screen.blit(testo_vite, (10, 10))
   screen.blit(testo_punti, (10, 50))
   screen.blit(testo_stato, (10, 90))
   pygame.display.flip()