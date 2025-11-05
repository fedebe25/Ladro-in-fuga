# Ladro in Fuga

## Descrizione

**Ladro in Fuga** è un **endless runner 2D** sviluppato con **Pygame**, pensato come **serie di 7 lezioni** per ripassare i principi fondamentali dello sviluppo videoludico: setup, fisica, collisioni, animazioni e gestione degli stati.

Il protagonista è un ladro che deve scappare **saltando ostacoli rossi**, **raccogliendo monete gialle** e **schivando i proiettili dei poliziotti**.
Il giocatore ha **3 vite** e vince se sopravvive **30 secondi**; perde se le vite scendono a zero.

Ogni lezione è autonoma e mostra un passo avanti nello sviluppo, da codice base a struttura modulare e orientata agli oggetti.


## Caratteristiche Principali (Versione Finale)

* **Controlli**

  * `SPAZIO` per saltare e iniziare il gioco
  * Click del mouse o `SPAZIO` nei menu

* **Fisica e Collisioni**

  * Gravità e salto realistico
  * Danno solo laterale (il salto sopra gli ostacoli è consentito)
  * Invincibilità temporanea di 1 secondo dopo aver subito danno

* **Elementi di Gioco**

  * Ostacoli, monete e nemici rigenerati proceduralmente
  * Proiettili dei nemici con durata limitata
  * HUD con cuori e punteggio

* **Stati di Gioco**

  * Menu principale
  * Partita attiva
  * Schermate di vittoria e sconfitta (auto-ritorno al menu)

* **Grafica e Animazioni**

  * Sprite del ladro (normale e in salto)
  * Monete animate (5 frame)
  * Poliziotti e cuori per le vite

* **Bilanciamento e Logica**

  * Massimo 2 nemici contemporanei (spawn ogni 3 secondi)
  * Rigenerazione continua delle monete dopo la raccolta

---

## Requisiti

* **Python 3.8+**
* **Pygame**

  ```bash
  pip install pygame
  ```

---

## Installazione e Avvio

1. **Clona la repository**

   ```bash
   git clone https://github.com/fedebe25/Ladro-in-fuga.git
   cd Ladro-in-fuga
   ```

2. **Assicurati che la cartella `lezione_7/images/` contenga i file:**

   * `ladro2.png` – Ladro in salto (custom)
   * `ladro3.png` – Ladro normale (custom)
   * `coin1.png`–`coin5.png` – Monete animate
   * `police1.png` – Nemico
   * `heart.png` – Cuoricino vita

3. **Esegui il gioco completo**

   ```bash
   python main.py
   ```

   * Usa `SPAZIO` per saltare e iniziare il gioco
   * Evita ostacoli e proiettili, raccogli monete e sopravvivi 30 secondi

4. **Per eseguire una singola lezione**

   ```bash
   cd lezione_X
   python main.py
   ```

---

## Struttura del Progetto

```
Ladro-in-fuga/
├── main.py              # Versione completa e assemblata
├── lezione_1/           # Setup base
├── lezione_2/           # Fisica e movimento
├── lezione_3/           # Ostacoli dinamici
├── lezione_4/           # Nemici sparanti
├── lezione_5/           # Vittoria e sconfitta
├── lezione_6/           # Menu e stati di gioco
├── lezione_7/           # Grafica, animazioni e rifiniture
│   └── images/          # Sprite e asset grafici
│       ├── ladro2.png
│       ├── ladro3.png
│       ├── coin1-5.png
│       ├── police1.png
│       └── heart.png
└── README.md            # Questo file
```


## Lezioni e Contenuti

### Lezione 1 — Federico Betti

Setup base: finestra 800×400, clock 60 FPS, rettangolo rosso giocatore, loop eventi e disegno.
**Focus:** struttura base Pygame e gestione eventi.

### Lezione 2 — Leonardo Paneni

Fisica e movimento: salto (SPAZIO), gravità, collisioni con suolo e oggetti.
HUD vite/punti e logiche di base.
**Focus:** input, fisica e collisioni.

### Lezione 3 — Tricca

Ostacoli dinamici: generazione casuale e monete.
**Focus:** generazione procedurale e bilanciamento.

### Lezione 4 — Leonardo Paneni

Nemici e proiettili: spawn limitato e gestione durata proiettili.
**Focus:** temporizzazioni e liste dinamiche.

### Lezione 5 — Leonardo Paneni

Condizioni di vittoria (30 secondi) e sconfitta (vite a zero).
**Focus:** fine partita e HUD.

### Lezione 6 — Tricca

Menu e stati di gioco: passaggio tra menu, gioco e schermate finali.
**Focus:** gestione stati e UX di base.

### Lezione 7 — Federico Betti

Grafica, animazioni e polish finale: sprite, monete animate, invincibilità post-danno e fix bug.
**Focus:** integrazione asset e rifinitura.

---

## Contributori

| Nome                | Ruolo                                            | Lezioni |
| ------------------- | ------------------------------------------------ | ------- |
| **Federico Betti**  | Coordinatore, autore sprite ladro, polish finale | 1, 7    |
| **Leonardo Paneni** | Fisica, nemici, vittoria/sconfitta               | 2, 4, 5 |
| **Tricca**          | Ostacoli e gestione stati/menu                   | 3, 6    |



Sviluppato per il ripasso di Pygame.
Ultimo aggiornamento: 5 Novembre 2025.
