import pygame
import math
import random

pygame.init()

# -------------------- SETTINGS --------------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cone Shooter")

clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# -------------------- PLAYER (CONE) --------------------
cone_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
angle = 0
rotation_speed = 15
cone_length = 50

# -------------------- BULLETS --------------------
bullets = []
bullet_speed = 30
bullet_radius = 4

fire_cooldown = 0
fire_rate = 6   # lower = faster shooting

# -------------------- BALLS (ENEMIES) --------------------
balls = []
ball_speed = 2
ball_radius = 12
spawn_timer = 0
spawn_delay = 40

# -------------------- FUNCTIONS --------------------
def spawn_ball():
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        pos = pygame.Vector2(random.randint(0, WIDTH), -ball_radius)
    elif side == "bottom":
        pos = pygame.Vector2(random.randint(0, WIDTH), HEIGHT + ball_radius)
    elif side == "left":
        pos = pygame.Vector2(-ball_radius, random.randint(0, HEIGHT))
    else:
        pos = pygame.Vector2(WIDTH + ball_radius, random.randint(0, HEIGHT))

    direction = (cone_pos - pos).normalize()
    balls.append({"pos": pos, "dir": direction})

def draw_cone():
    rad = math.radians(angle)
    tip = cone_pos + pygame.Vector2(math.cos(rad), -math.sin(rad)) * cone_length
    left = cone_pos + pygame.Vector2(math.cos(rad + 2.5), -math.sin(rad + 2.5)) * 30
    right = cone_pos + pygame.Vector2(math.cos(rad - 2.5), -math.sin(rad - 2.5)) * 30
    pygame.draw.polygon(screen, GREEN, [tip, left, right])

# -------------------- GAME LOOP --------------------
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------- INPUT --------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        angle += rotation_speed
    if keys[pygame.K_RIGHT]:
        angle -= rotation_speed

    # -------- CONTINUOUS FIRE --------
    if keys[pygame.K_SPACE]:
        if fire_cooldown == 0:
            rad = math.radians(angle)
            direction = pygame.Vector2(math.cos(rad), -math.sin(rad))
            bullets.append({
                "pos": cone_pos.copy(),
                "dir": direction
            })
            fire_cooldown = fire_rate

    if fire_cooldown > 0:
        fire_cooldown -= 1

    # -------- SPAWN BALLS --------
    spawn_timer += 1
    if spawn_timer >= spawn_delay:
        spawn_ball()
        spawn_timer = 0

    # -------- UPDATE BULLETS --------
    for bullet in bullets[:]:
        bullet["pos"] += bullet["dir"] * bullet_speed
        if not screen.get_rect().collidepoint(bullet["pos"]):
            bullets.remove(bullet)

    # -------- UPDATE BALLS --------
    for ball in balls:
        ball["pos"] += ball["dir"] * ball_speed

    # -------- COLLISION --------
    for bullet in bullets[:]:
        for ball in balls[:]:
            if bullet["pos"].distance_to(ball["pos"]) < bullet_radius + ball_radius:
                bullets.remove(bullet)
                balls.remove(ball)
                break

    # -------- DRAW --------
    draw_cone()

    for bullet in bullets:
        pygame.draw.circle(screen, YELLOW, bullet["pos"], bullet_radius)

    for ball in balls:
        pygame.draw.circle(screen, RED, ball["pos"], ball_radius)

    pygame.display.flip()

pygame.quit()
