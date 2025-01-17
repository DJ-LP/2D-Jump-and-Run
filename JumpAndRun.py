import pygame
import sys

# Pygame initialisieren
pygame.init()

# Fenstergröße und FPS
WIDTH, HEIGHT = 800, 400
FPS = 60

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

# Spielbildschirm
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Jump and Run mit Levelwechsel")

# Spieler-Einstellungen
player_size = (50, 50)
player_color = BLUE
player_speed = 5
player_jump_power = 15
gravity = 1

# Boden-Einstellungen
ground_height = 50
ground_color = GREEN
ground_rect = pygame.Rect(0, HEIGHT - ground_height, WIDTH, ground_height)

# ------------------ ÄNDERUNG: Level-Daten hinzufügen ------------------
# Levels definieren: Plattformen und Zielposition für jedes Level
levels = [
    {
        "platforms": [
            pygame.Rect(300, HEIGHT - 150, 100, 20),
            pygame.Rect(500, HEIGHT - 200, 150, 20)
        ],
        "goal": pygame.Rect(550, HEIGHT - ground_height - 200, 50, 50)
    },
    {
        "platforms": [
            pygame.Rect(200, HEIGHT - 100, 120, 20),
            pygame.Rect(400, HEIGHT - 150, 150, 20),
            pygame.Rect(600, HEIGHT - 250, 100, 20)
        ],
       "goal": pygame.Rect(650, HEIGHT - ground_height - 250, 50, 50)
    },
    {
        "platforms": [
            pygame.Rect(0, HEIGHT - 150, 120, 20),
            pygame.Rect(400, HEIGHT - 350, 150, 20),
            pygame.Rect(700, HEIGHT - 250, 100, 20)
        ],
        "goal": pygame.Rect(450, HEIGHT - ground_height - 350, 50, 50)
    },
    {
        "platforms": [
            pygame.Rect(300, HEIGHT - 150, 10, 20),
            pygame.Rect(500, HEIGHT - 200, 10, 20)
        ],
        "goal": pygame.Rect(550, HEIGHT - ground_height - 200, 50, 50)
    },
    {
        "platforms": [
            pygame.Rect(400, HEIGHT - 150, 30, 20),
            pygame.Rect(550, HEIGHT - 300, 30, 20)
        ],
       "goal": pygame.Rect(650, HEIGHT - ground_height - 300, 50, 50)
    },
    {
        "platforms": [
            pygame.Rect(0, HEIGHT - 150, 120, 20),
            pygame.Rect(400, HEIGHT - 250, 150, 20),
            pygame.Rect(700, HEIGHT - 300, 100, 20)
        ],
        "goal": pygame.Rect(450, HEIGHT - ground_height - 350, 50, 50)
    }
]

# Spielerbewegung
player_rect = pygame.Rect(100, HEIGHT - player_size[1] - ground_height, *player_size)
player_velocity_y = 0
is_jumping = False

# ------------------ ÄNDERUNG: Level-Status-Variablen ------------------
# Level-Status
current_level = 0
game_won = False

# Spiel-Schleife
clock = pygame.time.Clock()

# ------------------ ÄNDERUNG: Spieler-Reset-Funktion ------------------
def reset_player():
    """Setzt den Spieler auf die Startposition zurück."""
    global player_rect, player_velocity_y, is_jumping
    player_rect.x = 100
    player_rect.y = HEIGHT - player_size[1] - ground_height
    player_velocity_y = 0
    is_jumping = False

def handle_input():
    """Verarbeitet die Eingaben."""
    global is_jumping, player_velocity_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player_rect.x < -20:
            player_rect.x += 800
        else:
            player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        if player_rect.x > 780:
            player_rect.x -= 800
        else:
            player_rect.x += player_speed
    if keys[pygame.K_SPACE] and not is_jumping:
        player_velocity_y = -player_jump_power
        is_jumping = True

def apply_gravity():
    """Wendet Schwerkraft an und überprüft Kollision mit Boden."""
    global is_jumping, player_velocity_y
    player_velocity_y += gravity
    player_rect.y += player_velocity_y

    # Boden-Kollision
    if player_rect.colliderect(ground_rect):
        player_rect.y = ground_rect.top - player_rect.height
        player_velocity_y = 0
        is_jumping = False

    # Plattform-Kollision
    for platform in levels[current_level]["platforms"]:  # ÄNDERUNG: Plattformen pro Level
        if player_rect.colliderect(platform) and player_velocity_y > 0:
            player_rect.y = platform.top - player_rect.height
            player_velocity_y = 0
            is_jumping = False

def check_goal():
    """Überprüft, ob der Spieler das Ziel erreicht hat."""
    return player_rect.colliderect(levels[current_level]["goal"])  # ÄNDERUNG: Ziel pro Level

# ------------------ ÄNDERUNG: Level-Wechsel-Funktion ------------------
def load_next_level():
    """Lädt das nächste Level oder beendet das Spiel, wenn es keine weiteren Levels gibt."""
    global current_level, game_won
    if current_level + 1 < len(levels):  # Prüfen, ob weitere Levels existieren
        current_level += 1  # Zum nächsten Level wechseln
        reset_player()  # Spieler zurücksetzen
    else:
        game_won = True  # Alle Levels geschafft

while True:
    screen.fill(WHITE)
   
    # Ereignisverarbeitung
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
   
    if not game_won:
        # Eingaben verarbeiten und Schwerkraft anwenden
        handle_input()
        apply_gravity()

        # Überprüfen, ob das Ziel erreicht wurde
        if check_goal():
            load_next_level()  # ÄNDERUNG: Levelwechsel bei Zielerreichung

    # Spieler, Plattformen und Ziel zeichnen
    pygame.draw.rect(screen, player_color, player_rect)
    pygame.draw.rect(screen, ground_color, ground_rect)
    for platform in levels[current_level]["platforms"]:  # ÄNDERUNG: Plattformen pro Level zeichnen
        pygame.draw.rect(screen, RED, platform)
    pygame.draw.rect(screen, GOLD, levels[current_level]["goal"])  # ÄNDERUNG: Ziel pro Level zeichnen

    # Spielstatus anzeigen
    if game_won:
        font = pygame.font.SysFont(None, 55)
        text = font.render("Spiel beendet! Alle Level geschafft!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    else:
        pygame.display.flip()

    # Taktung
    clock.tick(FPS)