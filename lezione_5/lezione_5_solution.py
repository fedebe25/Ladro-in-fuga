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
 
# --- Boss (anche se non serve ancora, resta nel codice per struttura futura) ---
boss = pygame.Rect(SCREEN_WIDTH + 200, SCREEN_HEIGHT - 150, 80, 80)
proiettili = []
boss_attivo = False
tempo_ultimo_proiettile = 0
tempo_ricarica = 1500
 
# --- Font ---
font = pygame.font.SysFont(None, 36)
font_grande = pygame.font.SysFont(None, 80)
 
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
 
while running:
    clock.tick(FPS)
    ora = pygame.time.get_ticks()
    tempo_passato = ora - tempo_inizio
 
    # --- Eventi ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    # --- Controlla condizioni di fine gioco ---
    if vite <= 0 and not sconfitta:
        sconfitta = True
        nemici_sparanti.clear()
        proiettili_nemico.clear()
        obstacles.clear()
        coins.clear()
        proiettili.clear()
        boss_attivo = False
 
    if tempo_passato >= TEMPO_VITTORIA and not vittoria and not sconfitta:
        vittoria = True
        nemici_sparanti.clear()
        proiettili_nemico.clear()
        obstacles.clear()
        coins.clear()
        proiettili.clear()
        boss_attivo = False
 
    # --- Se il gioco non è finito ---
    if not vittoria and not sconfitta:
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
 
        # --- Sezione normale (niente boss ancora) ---
        if not boss_attivo:
            # Scorrimento ostacoli e monete
            for obs in obstacles:
                obs["x"] -= 5
            for coin in coins:
                coin["x"] -= 5
 
            # Rigenerazione ostacoli e monete
            for obs in obstacles[:]:
                if obs["x"] < -50:
                    obstacles.remove(obs)
                    obstacles.append({"x": SCREEN_WIDTH + random.randint(200, 400), "y": SCREEN_HEIGHT - 100})
 
            for coin in coins[:]:
                if coin["x"] < -20:
                    coins.remove(coin)
                    coins.append({"x": SCREEN_WIDTH + random.randint(300, 600), "y": SCREEN_HEIGHT - random.randint(150, 250)})
 
            # Collisione con ostacoli
            for obs in obstacles:
                obs_rect = pygame.Rect(obs["x"], obs["y"], 50, 50)
                if giocatore.colliderect(obs_rect):
                    if giocatore.bottom - vel_y <= obs_rect.top + TOLLERANZA:
                        giocatore.bottom = obs_rect.top
                        vel_y = 0
                        puo_saltare = True
                    else:
                        vite -= 1
                        reset_giocatore()
 
            # Raccolta monete
            for coin in coins[:]:
                coin_rect = pygame.Rect(coin["x"], coin["y"], 20, 20)
                if giocatore.colliderect(coin_rect):
                    coins.remove(coin)
                    punteggio += 10
 
            # Spawn nemici
            if len(nemici_sparanti) < 2 and ora - tempo_ultimo_spawn_nemico > intervallo_spawn_nemico:
                spawn_nemico()
                tempo_ultimo_spawn_nemico = ora
 
            # Movimento nemici e proiettili
            for nemico in nemici_sparanti[:]:
                nemico["rect"].x -= 4
                if not nemico["proiettile_sparato"]:
                    p = pygame.Rect(nemico["rect"].left, nemico["rect"].centery - 5, 15, 10)
                    proiettili_nemico.append({"rect": p, "spawn_time": ora})
                    nemico["proiettile_sparato"] = True
                if ora - nemico["spawn_time"] > 2500:
                    nemici_sparanti.remove(nemico)
 
            # Movimento proiettili nemici
            for p in proiettili_nemico[:]:
                p["rect"].x -= 7
                if ora - p["spawn_time"] > 3000 or p["rect"].right < 0:
                    proiettili_nemico.remove(p)
                    continue
                if giocatore.colliderect(p["rect"]):
                    vite -= 1
                    reset_giocatore()
                    proiettili_nemico.remove(p)
 
    # --- Disegno ---
    screen.fill(CELESTE)
    pygame.draw.rect(screen, MARRONE, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
    pygame.draw.rect(screen, VERDE, giocatore)
 
    # Ostacoli e monete
    for obs in obstacles:
        pygame.draw.rect(screen, ROSSO, (obs["x"], obs["y"], 50, 50))
    for coin in coins:
        pygame.draw.circle(screen, GIALLO, (int(coin["x"]), int(coin["y"])), 10)
 
    # Nemici e proiettili nemici
    for nemico in nemici_sparanti:
        pygame.draw.rect(screen, ROSSO, nemico["rect"])
    for p in proiettili_nemico:
        pygame.draw.rect(screen, ARANCIONE, p["rect"])
 
    # --- HUD ---
    testo_vite = font.render(f"Vite: {vite}", True, NERO)
    testo_punti = font.render(f"Punti: {punteggio}", True, NERO)
    screen.blit(testo_vite, (10, 10))
    screen.blit(testo_punti, (10, 50))
 
    # --- Fase vittoria ---
    if vittoria:
        rett_vittoria = pygame.Rect(100, 150, 600, 300)
        pygame.draw.rect(screen, BIANCO, rett_vittoria, border_radius=20)
        testo_vittoria = font_grande.render("HAI VINTO!", True, NERO)
        screen.blit(testo_vittoria, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 40))
 
    # --- Fase sconfitta ---
    if sconfitta:
        rett_sconfitta = pygame.Rect(100, 150, 600, 300)
        pygame.draw.rect(screen, BIANCO, rett_sconfitta, border_radius=20)
        testo_sconfitta = font_grande.render("HAI PERSO!", True, NERO)
        screen.blit(testo_sconfitta, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 40))
 
    pygame.display.flip()
