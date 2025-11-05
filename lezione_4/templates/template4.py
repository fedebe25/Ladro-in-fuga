import pygame
import sys
import random

# --- Inizializzazione ---
pygame.init()

# Dimensioni schermo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ladro in fuga - Lezione 3: Ostacoli in movimento")

# Clock
clock = pygame.time.Clock()
FPS = 60

# --- Costanti di gioco ---
GRAVITA = 0.8
SALTO_FORZA = -15
TOLLERANZA = 10
PUNTEGGIO_PER_BOSS = 50  # Punteggio minimo per entrare nella sezione Boss

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

# --- Ostacoli e monete ---
obstacles = [
   {"x": 800, "y": SCREEN_HEIGHT - 100},
   {"x": 1200, "y": SCREEN_HEIGHT - 100},
   {"x": 1600, "y": SCREEN_HEIGHT - 100},
]
coins = [
   {"x": 900, "y": SCREEN_HEIGHT - 200},
   {"x": 1300, "y": SCREEN_HEIGHT - 180},
   {"x": 1700, "y": SCREEN_HEIGHT - 220},
]

# --- Boss e proiettili ---
boss = pygame.Rect(SCREEN_WIDTH + 200, SCREEN_HEIGHT - 150, 80, 80)
proiettili = []
boss_attivo = False
tempo_ultimo_proiettile = 0
tempo_ricarica = 1500  # ms

# --- TODO aggiungere gestione dei nemici sparanti ---

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

# --- TODO creare funzione spawn_nemico() ---

# --- Ciclo principale ---
running = True
while running:
   clock.tick(FPS)
   ora = pygame.time.get_ticks()  # necessario per spawn e gestione proiettili nemici

   # --- Gestione eventi ---
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

   # --- Sezione normale (senza boss) ---
   if not boss_attivo:
       # Scorrimento ostacoli e monete
       for obs in obstacles:
           obs["x"] -= 5
       for coin in coins:
           coin["x"] -= 5

       # Riaggiungi ostacoli che escono dallo schermo (loop infinito)
       for obs in obstacles:
           if obs["x"] < -50:
               obs["x"] = random.randint(800, 1200)
       # Riaggiungi monete
       for coin in coins:
           if coin["x"] < -20:
               coin["x"] = random.randint(900, 1500)
               coin["y"] = random.randint(SCREEN_HEIGHT - 250, SCREEN_HEIGHT - 150)

       # Collisioni con ostacoli
       for obs in obstacles:
           obs_rect = pygame.Rect(obs["x"], obs["y"], 50, 50)
           if giocatore.colliderect(obs_rect):
               # Se colpisce dall’alto → atterra sopra
               if giocatore.bottom - vel_y <= obs_rect.top + TOLLERANZA:
                   giocatore.bottom = obs_rect.top
                   vel_y = 0
                   puo_saltare = True
               else:
                   # Se colpisce di lato → perde vita
                   vite -= 1
                   reset_giocatore()

       # Collisione con monete
       for coin in coins[:]:
           coin_rect = pygame.Rect(coin["x"], coin["y"], 20, 20)
           if giocatore.colliderect(coin_rect):
               coins.remove(coin)
               punteggio += 10

       # --- TODO spawn nemici sparanti con intervallo controllato ---

       # --- TODO movimento nemici sparanti e generazione proiettili ---

       # --- TODO movimento e collisione proiettili nemici ---

       # Attiva sezione Boss
       if punteggio >= PUNTEGGIO_PER_BOSS:
           boss_attivo = True
           reset_giocatore()
           boss.x = SCREEN_WIDTH + 200

   # --- Sezione Boss ---
   else:
       boss.x -= 3  # Il boss entra lentamente nella scena

       # Il boss spara proiettili a intervalli regolari
       ora = pygame.time.get_ticks()
       if ora - tempo_ultimo_proiettile > tempo_ricarica:
           proiettile = pygame.Rect(boss.left, boss.centery - 5, 15, 10)
           proiettili.append(proiettile)
           tempo_ultimo_proiettile = ora

       # Movimento proiettili
       for p in proiettili[:]:
           p.x -= 7
           if p.right < 0:
               proiettili.remove(p)
           elif giocatore.colliderect(p):
               proiettili.remove(p)
               vite -= 1
               reset_giocatore()

       # Collisione del giocatore col boss
       if giocatore.colliderect(boss):
           if giocatore.bottom - vel_y <= boss.top + TOLLERANZA:
               vel_y = SALTO_FORZA // 2
               boss.x = -9999
               punteggio += 50
           else:
               vite -= 1
               reset_giocatore()

   # --- Disegno ---
   screen.fill(CELESTE)
   pygame.draw.rect(screen, MARRONE, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
   pygame.draw.rect(screen, VERDE, giocatore)

   # Disegna ostacoli e monete
   for obs in obstacles:
       pygame.draw.rect(screen, ROSSO, (obs["x"], obs["y"], 50, 50))
   for coin in coins:
       pygame.draw.circle(screen, GIALLO, (int(coin["x"]), int(coin["y"])), 10)

   # --- TODO disegnare nemici sparanti e i loro proiettili ---

   # Boss e proiettili
   if boss_attivo:
       pygame.draw.rect(screen, VIOLA, boss)
       for p in proiettili:
           pygame.draw.rect(screen, (255, 140, 0), p)

   # HUD
   testo_vite = font.render(f"Vite: {vite}", True, NERO)
   testo_punti = font.render(f"Punti: {punteggio}", True, NERO)
   testo_stato = font.render("Boss: SI" if boss_attivo else "Boss: NO", True, NERO)
   screen.blit(testo_vite, (10, 10))
   screen.blit(testo_punti, (10, 50))
   screen.blit(testo_stato, (10, 90))

   pygame.display.flip()
