import pygame
import sys
import random

pygame.init()

# --- Impostazioni schermo ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ladro in fuga - Lezione 4 con vittoria e sconfitta")

# --- Clock e FPS ---
clock = pygame.time.Clock()
FPS = 60

# --- Costanti ---
GRAVITA = 0.8
SALTO_FORZA = -15
TOLLERANZA = 10
PUNTEGGIO_PER_BOSS = 50
TEMPO_VITTORIA = 30000  # 30 secondi (in millisecondi)

# --- Colori ---
CELESTE = (135, 206, 235)
MARRONE = (139, 69, 19)
GIALLO = (255, 215, 0)
VERDE = (0, 200, 0)
ROSSO = (255, 0, 0)
VIOLA = (128, 0, 128)
NERO = (0, 0, 0)
ARANCIONE = (255, 140, 0)
BIANCO = (255, 255, 255)

# TODO: Aggiungi una variabile per lo stato del gioco, ad esempio stato = "menu"

# --- Giocatore ---
giocatore = pygame.Rect(100, SCREEN_HEIGHT - 150, 40, 50)
vel_y = 0
puo_saltare = False
vite = 3
punteggio = 0

# --- Ostacoli e monete ---
obstacles = [{"x": 800, "y": SCREEN_HEIGHT - 100}, {"x": 1200, "y": SCREEN_HEIGHT - 100}]
coins = [{"x": 900, "y": SCREEN_HEIGHT - 200}, {"x": 1300, "y": SCREEN_HEIGHT - 180}]

# --- Nemici sparanti ---
nemici_sparanti = []
proiettili_nemico = []
tempo_ultimo_spawn_nemico = 0
intervallo_spawn_nemico = 3000  # massimo un nemico ogni 3 secondi

# --- Boss ---
boss = pygame.Rect(SCREEN_WIDTH + 200, SCREEN_HEIGHT - 150, 80, 80)
proiettili = []
boss_attivo = False
tempo_ultimo_proiettile = 0
tempo_ricarica = 1500

# --- Font ---
font = pygame.font.SysFont(None, 36)
font_grande = pygame.font.SysFont(None, 80)

# TODO: Aggiungi funzione reset_gioco() che resetta tutte le variabili principali

# --- Funzione reset giocatore ---
def reset_giocatore():
    global vel_y, puo_saltare
    giocatore.x = 100
    giocatore.y = SCREEN_HEIGHT - 150
    vel_y = 0
    puo_saltare = False

reset_giocatore()

# --- Funzione spawn nemico ---
def spawn_nemico():
    x = SCREEN_WIDTH + 50
    y = SCREEN_HEIGHT - 100
    nemico = {"rect": pygame.Rect(x, y, 40, 40), "spawn_time": pygame.time.get_ticks(), "proiettile_sparato": False}
    nemici_sparanti.append(nemico)

# --- Ciclo principale ---
tempo_inizio = pygame.time.get_ticks()
running = True
vittoria = False
sconfitta = False

# TODO: Aggiungi una variabile tempo_menu_inizio = 0 per gestire il ritorno al menu

while running:
    clock.tick(FPS)
    ora = pygame.time.get_ticks()
    tempo_passato = ora - tempo_inizio

    # --- Eventi ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # TODO: Gestisci il click del bottone "GIOCA" nel menu

    # TODO: Gestisci input tastiera (spazio per avviare gioco)

    # TODO: Disegna il menu con titolo e bottone "GIOCA"

    # TODO: Sposta logica di vittoria/sconfitta dentro if stato == "gioco"

    # TODO: Sezione principale del gioco con salti, gravità, collisioni, ostacoli, monete, nemici

    # TODO: Disegna gli elementi del gioco

    # TODO: Mostra schermata di vittoria o sconfitta e ritorna al menu dopo 2 secondi

    pygame.display.flip()
