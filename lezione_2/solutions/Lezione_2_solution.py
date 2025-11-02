Lezione 2 – Movimento
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
 
# --- Elementi del livello ---
blocchi = [pygame.Rect(900, SCREEN_HEIGHT - 100, 50, 50)]
monete = [pygame.Rect(1000, SCREEN_HEIGHT - 200, 20, 20)]
nemici = [pygame.Rect(1600, SCREEN_HEIGHT - 100, 40, 40)]
 
# --- Boss e proiettili ---
boss = pygame.Rect(SCREEN_WIDTH + 200, SCREEN_HEIGHT - 150, 80, 80)
proiettili = []
boss_attivo = False  # Falso finché non raggiungiamo il punteggio richiesto
tempo_ultimo_proiettile = 0
tempo_ricarica = 1500  # ms
 
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
        # Scorrimento degli oggetti verso sinistra
        for blocco in blocchi:
            blocco.x -= 4
        for moneta in monete:
            moneta.x -= 4
        for nemico in nemici:
            nemico.x -= 4
 
        # Raccolta monete
        for moneta in monete[:]:
            if giocatore.colliderect(moneta):
                monete.remove(moneta)
                punteggio += 10
 
        # Collisione con i nemici
        for nemico in nemici[:]:
            if giocatore.colliderect(nemico):
                # Se lo colpisce dall’alto → lo elimina
                if giocatore.bottom - vel_y <= nemico.top + TOLLERANZA:
                    vel_y = SALTO_FORZA // 2
                    puo_saltare = True
                    nemici.remove(nemico)
                    punteggio += 10
                else:
                    vite -= 1
                    reset_giocatore()
 
        # Quando il punteggio raggiunge la soglia → attiva la sezione Boss
        if punteggio >= PUNTEGGIO_PER_BOSS:
            boss_attivo = True
            reset_giocatore()
            boss.x = SCREEN_WIDTH + 200  # entra da destra
 
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
            # Se lo colpisce dall’alto → scompare
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
 
    # Disegna elementi
    if not boss_attivo:
        for blocco in blocchi:
            pygame.draw.rect(screen, MARRONE, blocco)
        for moneta in monete:
            pygame.draw.circle(screen, GIALLO, moneta.center, moneta.width // 2)
        for nemico in nemici:
            pygame.draw.rect(screen, ROSSO, nemico)
    else:
        pygame.draw.rect(screen, VIOLA, boss)
        for p in proiettili:
            pygame.draw.rect(screen, (255, 140, 0), p)
 
    # HUD (vite, punti, sezione)
    testo_vite = font.render(f"Vite: {vite}", True, NERO)
    testo_punti = font.render(f"Punti: {punteggio}", True, NERO)
    testo_stato = font.render("Boss: SI" if boss_attivo else "Boss: NO", True, NERO)
    screen.blit(testo_vite, (10, 10))
    screen.blit(testo_punti, (10, 50))
    screen.blit(testo_stato, (10, 90))
 
    pygame.display.flip()