import pygame
import sys
import random
import os
pygame.init()
# --- Impostazioni schermo ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ladro in fuga")
# --- Clock e FPS ---
clock = pygame.time.Clock()
FPS = 60
# --- Costanti ---
GRAVITA = 0.8
SALTO_FORZA = -15
TOLLERANZA = 10
PUNTEGGIO_PER_BOSS = 50
TEMPO_VITTORIA = 30000 # 30 secondi (in millisecondi)
TEMPO_INVINCIBILE = 1000  # 1 secondo di invincibilità dopo danno
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
# --- Caricamento immagini ---
IMAGES_PATH = "images"
ladro_normale_img = pygame.image.load(os.path.join(IMAGES_PATH, "ladro3.png")).convert_alpha()
ladro_salto_img = pygame.image.load(os.path.join(IMAGES_PATH, "ladro2.png")).convert_alpha()
ladro_normale_img = pygame.transform.scale(ladro_normale_img, (48, 64))
ladro_salto_img = pygame.transform.scale(ladro_salto_img, (48, 64))
coin_frames = []
for i in range(1, 6):
    coin_img = pygame.image.load(os.path.join(IMAGES_PATH, f"coin{i}.png")).convert_alpha()
    coin_frames.append(pygame.transform.scale(coin_img, (32, 32)))
police_img = pygame.image.load(os.path.join(IMAGES_PATH, "police1.png")).convert_alpha()
police_img = pygame.transform.scale(police_img, (48, 48))
heart_img = pygame.image.load(os.path.join(IMAGES_PATH, "heart.png")).convert_alpha()
heart_img = pygame.transform.scale(heart_img, (32, 32))
# --- Stato del gioco ---
stato = "menu" # "menu" o "gioco"
# --- Variabili per menu ---
tempo_menu_inizio = 0
# --- Giocatore ---
ALTEZZA_GIOCATORE = 64
LARGHEZZA_GIOCATORE = 48
giocatore = pygame.Rect(100, SCREEN_HEIGHT - 50 - ALTEZZA_GIOCATORE, LARGHEZZA_GIOCATORE, ALTEZZA_GIOCATORE)
vel_y = 0
puo_saltare = False
vite = 3
punteggio = 0
tempo_danno = 0
# --- Ostacoli e monete ---
obstacles = [{"x": 800, "y": SCREEN_HEIGHT - 100}, {"x": 1200, "y": SCREEN_HEIGHT - 100}]
LARGHEZZA_MONETA = 32
ALTEZZA_MONETA = 32
coins = [
    {"x": 900, "y": SCREEN_HEIGHT - 200, "frame_index": 0},
    {"x": 1300, "y": SCREEN_HEIGHT - 180, "frame_index": 0}
]
# --- Nemici sparanti ---
LARGHEZZA_NEMICO = 48
ALTEZZA_NEMICO = 48
nemici_sparanti = []
proiettili_nemico = []
tempo_ultimo_spawn_nemico = 0
intervallo_spawn_nemico = 3000 # massimo un nemico ogni 3 secondi
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
    giocatore.y = SCREEN_HEIGHT - 50 - ALTEZZA_GIOCATORE
    vel_y = 0
    puo_saltare = False
# --- Funzione reset gioco ---
def reset_gioco():
    global vite, punteggio, obstacles, coins, nemici_sparanti, proiettili_nemico, proiettili, boss_attivo, tempo_ultimo_spawn_nemico, tempo_ultimo_proiettile, tempo_danno
    vite = 3
    punteggio = 0
    obstacles = [{"x": 800, "y": SCREEN_HEIGHT - 100}, {"x": 1200, "y": SCREEN_HEIGHT - 100}]
    coins = [
        {"x": 900, "y": SCREEN_HEIGHT - 200, "frame_index": 0},
        {"x": 1300, "y": SCREEN_HEIGHT - 180, "frame_index": 0}
    ]
    nemici_sparanti = []
    proiettili_nemico = []
    proiettili = []
    boss_attivo = False
    tempo_ultimo_spawn_nemico = 0
    tempo_ultimo_proiettile = 0
    tempo_danno = 0
    reset_giocatore()
reset_gioco()
# --- Funzione spawn nemico ---
def spawn_nemico():
    x = SCREEN_WIDTH + 50
    y = SCREEN_HEIGHT - 50 - ALTEZZA_NEMICO
    nemico = {"rect": pygame.Rect(x, y, LARGHEZZA_NEMICO, ALTEZZA_NEMICO), "spawn_time": pygame.time.get_ticks(), "proiettile_sparato": False}
    nemici_sparanti.append(nemico)
# --- Ciclo principale ---
running = True
vittoria = False
sconfitta = False
while running:
    clock.tick(FPS)
    ora = pygame.time.get_ticks()
    # --- Eventi generali ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if stato == "menu":
                mouse_pos = pygame.mouse.get_pos()
                bottone_gioca = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 60)
                if bottone_gioca.collidepoint(mouse_pos):
                    stato = "gioco"
                    reset_gioco()
                    tempo_inizio = ora
                    vittoria = False
                    sconfitta = False
    # --- Input tastiera generale ---
    keys = pygame.key.get_pressed()
    if stato == "menu" and keys[pygame.K_SPACE]:
        stato = "gioco"
        reset_gioco()
        tempo_inizio = ora
        vittoria = False
        sconfitta = False
    # --- Gestione menu ---
    if stato == "menu":
        # Sfondo menu come il gioco
        screen.fill(CELESTE)
        pygame.draw.rect(screen, MARRONE, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        # Titolo centrato in alto
        testo_titolo = font_grande.render("Ladro in fuga", True, NERO)
        x_titolo = (SCREEN_WIDTH - testo_titolo.get_width()) // 2
        screen.blit(testo_titolo, (x_titolo, 100))
        # Rettangolo colorato con "GIOCA" centrato
        bottone_gioca = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 60)
        pygame.draw.rect(screen, VERDE, bottone_gioca, border_radius=10)
        testo_gioca = font.render("GIOCA", True, NERO)
        x_gioca = bottone_gioca.centerx - testo_gioca.get_width() // 2
        y_gioca = bottone_gioca.centery - testo_gioca.get_height() // 2
        screen.blit(testo_gioca, (x_gioca, y_gioca))
    # --- Gestione gioco ---
    elif stato == "gioco":
        tempo_passato = ora - tempo_inizio
        # --- Controlla condizioni di fine gioco ---
        if vite <= 0 and not sconfitta:
            sconfitta = True
            nemici_sparanti.clear()
            proiettili_nemico.clear()
            obstacles.clear()
            coins.clear()
            proiettili.clear()
            boss_attivo = False
            # Torna al menu dopo 2 secondi
            tempo_menu_inizio = ora
        if tempo_passato >= TEMPO_VITTORIA and not vittoria and not sconfitta:
            vittoria = True
            nemici_sparanti.clear()
            proiettili_nemico.clear()
            obstacles.clear()
            coins.clear()
            proiettili.clear()
            boss_attivo = False
            # Torna al menu dopo 2 secondi
            tempo_menu_inizio = ora
        # --- Se il gioco non è finito ---
        if not vittoria and not sconfitta:
            # --- Input salto ---
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
                    if coin["x"] < -32:
                        coins.remove(coin)
                        coins.append({"x": SCREEN_WIDTH + random.randint(300, 600), "y": SCREEN_HEIGHT - random.randint(150, 250), "frame_index": 0})
                # Collisione con ostacoli
                for obs in obstacles:
                    if ora - tempo_danno < TEMPO_INVINCIBILE:
                        continue  # Invincibile, salta collisione
                    obs_rect = pygame.Rect(obs["x"], obs["y"], 50, 50)
                    if giocatore.colliderect(obs_rect):
                        if giocatore.bottom - vel_y <= obs_rect.top + TOLLERANZA:
                            giocatore.bottom = obs_rect.top
                            vel_y = 0
                            puo_saltare = True
                        else:
                            vite -= 1
                            tempo_danno = ora
                            reset_giocatore()
                # Raccolta monete
                for coin in coins[:]:
                    coin_rect = pygame.Rect(coin["x"], coin["y"], LARGHEZZA_MONETA, ALTEZZA_MONETA)
                    if giocatore.colliderect(coin_rect):
                        coins.remove(coin)
                        punteggio += 10
                        coins.append({"x": SCREEN_WIDTH + random.randint(300, 600), "y": SCREEN_HEIGHT - random.randint(150, 250), "frame_index": 0})
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
                    if ora - tempo_danno < TEMPO_INVINCIBILE:
                        continue  # Invincibile, salta collisione
                    p["rect"].x -= 7
                    if ora - p["spawn_time"] > 3000 or p["rect"].right < 0:
                        proiettili_nemico.remove(p)
                        continue
                    if giocatore.colliderect(p["rect"]):
                        vite -= 1
                        tempo_danno = ora
                        reset_giocatore()
                        proiettili_nemico.remove(p)
        # --- Disegno gioco ---
        screen.fill(CELESTE)
        pygame.draw.rect(screen, MARRONE, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        # Disegna giocatore
        if vel_y < 0 and not puo_saltare: # Salto in corso
            screen.blit(ladro_salto_img, (giocatore.x, giocatore.y))
        else:
            screen.blit(ladro_normale_img, (giocatore.x, giocatore.y))
        # Ostacoli e monete
        for obs in obstacles:
            pygame.draw.rect(screen, ROSSO, (obs["x"], obs["y"], 50, 50))
        for coin in coins:
            frame_index = (ora // 200) % len(coin_frames) # Animazione rotazione ogni 200ms
            coin["frame_index"] = frame_index
            screen.blit(coin_frames[frame_index], (coin["x"], coin["y"]))
        # Nemici e proiettili nemici
        for nemico in nemici_sparanti:
            screen.blit(police_img, (nemico["rect"].x, nemico["rect"].y))
        for p in proiettili_nemico:
            pygame.draw.rect(screen, ARANCIONE, p["rect"])
        # --- HUD ---
        # Disegna cuoricini per le vite
        for i in range(vite):
            screen.blit(heart_img, (10 + i * 35, 10))
        testo_punti = font.render(f"Punti: {punteggio}", True, NERO)
        screen.blit(testo_punti, (10, 50))
        # --- Fase vittoria ---
        if vittoria:
            rett_vittoria = pygame.Rect(100, 150, 600, 300)
            pygame.draw.rect(screen, BIANCO, rett_vittoria, border_radius=20)
            testo_vittoria = font_grande.render("HAI VINTO!", True, NERO)
            screen.blit(testo_vittoria, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 40))
            # Controlla se passare al menu dopo 2 secondi
            if ora - tempo_menu_inizio > 2000:
                stato = "menu"
        # --- Fase sconfitta ---
        if sconfitta:
            rett_sconfitta = pygame.Rect(100, 150, 600, 300)
            pygame.draw.rect(screen, BIANCO, rett_sconfitta, border_radius=20)
            testo_sconfitta = font_grande.render("HAI PERSO!", True, NERO)
            screen.blit(testo_sconfitta, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 40))
            # Controlla se passare al menu dopo 2 secondi
            if ora - tempo_menu_inizio > 2000:
                stato = "menu"
    pygame.display.flip()