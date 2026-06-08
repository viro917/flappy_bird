import pygame as py
import random
import sys

py.init()

WIDTH = 400
HEIGHT = 600
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Flappy Bird")

vogel = py.image.load("vogel3.png").convert()
vogel.set_colorkey((163, 73, 164))
vogel = py.transform.scale(vogel, (50, 50))

pipes_oben = py.image.load("pipes_oben_neu.png").convert_alpha()
pipes_unten = py.image.load("pipes_unten_neu.png").convert_alpha()

speed_icon = py.image.load("speed_icon.png").convert_alpha()
slow_icon = py.image.load("slow_icon.png").convert_alpha()

grow_icon = py.image.load("grow_icon.png").convert_alpha()
shrink_icon = py.image.load("shrink_icon.png").convert_alpha()

speed_icon = py.transform.scale(speed_icon, (25, 25))
slow_icon = py.transform.scale(slow_icon, (25, 25))

grow_icon = py.transform.scale(grow_icon, (25, 25))
shrink_icon = py.transform.scale(shrink_icon, (25, 25))

WHITE = (255, 255, 255)
BLUE = (135, 206, 235)

clock = py.time.Clock()
FPS = 60
font = py.font.SysFont(None, 40)

bird_x = 80
bird_y = HEIGHT // 2
bird_velocity = 0
bird_size = 50
gravity = 0.5
jump_strength = -8

pipe_width = 100
pipe_gap = 200
base_speed = 4
pipe_speed = base_speed

pipes = []
score = 0

state = "START"

powerups = []
power_active = None
power_timer = 0


def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def save_highscore(s):
    with open("highscore.txt", "w") as f:
        f.write(str(s))


highscore = load_highscore()


def bird_rect():
    shrink = int(bird_size * 0.24)

    return py.Rect(
        bird_x - bird_size // 2 + shrink,
        bird_y - bird_size // 2 + shrink,
        bird_size - shrink * 2,
        bird_size - shrink * 2)


def create_pipe():
    h = random.randint(80, HEIGHT - pipe_gap - 80)

    top = py.Rect(WIDTH, 0, pipe_width, h)
    bottom = py.Rect(
        WIDTH,
        h + pipe_gap,
        pipe_width,
        HEIGHT - (h + pipe_gap))

    return top, bottom


def reset():
    global pipes
    global bird_y
    global bird_velocity
    global score
    global powerups
    global power_active
    global pipe_speed
    global bird_size

    pipes = []

    for i in range(3):
        p = create_pipe()
        p[0].x += i * 325
        p[1].x += i * 325
        pipes.append(p)

    powerups = []
    power_active = None
    pipe_speed = base_speed
    bird_size = 50

    bird_y = HEIGHT // 2
    bird_velocity = 0
    score = 0


reset()


def create_powerup():
    while True:

        rect = py.Rect(
            WIDTH + random.randint(0, 200),
            random.randint(50, HEIGHT - 75),
            25,
            25)

        in_pipe = False

        for top, bottom in pipes:
            if rect.colliderect(top) or rect.colliderect(bottom):
                in_pipe = True
                break

        if not in_pipe:
            typ = random.choice(["SPEED", "SLOW", "GROW", "SHRINK"])
            return rect, typ


def draw_game():
    screen.fill(BLUE)

    scaled_bird = py.transform.scale(
        vogel,
        (bird_size, bird_size))

    screen.blit(
        scaled_bird,
        (
            bird_x - bird_size // 2,
            int(bird_y) - bird_size // 2))

    for top, bottom in pipes:

        top_img = py.transform.scale(
            pipes_oben,
            (pipe_width, top.height)
        )

        bottom_img = py.transform.scale(
            pipes_unten,
            (pipe_width, bottom.height)
        )

        screen.blit(top_img, (top.x, top.y))
        screen.blit(bottom_img, (bottom.x, bottom.y))

    # Powerups zeichnen
    for p, t in powerups:

        if t == "SPEED":
            screen.blit(speed_icon, (p.x, p.y))

        elif t == "SLOW":
            screen.blit(slow_icon, (p.x, p.y))

        elif t == "GROW":
            screen.blit(grow_icon, (p.x, p.y))

        elif t == "SHRINK":
            screen.blit(shrink_icon, (p.x, p.y))

    txt = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(txt, (10, 10))

    if power_active:
        active_text = font.render(
            power_active,
            True,WHITE)

        screen.blit(active_text, (260, 10))

    py.display.update()


def draw_start():
    screen.fill(BLUE)

    screen.blit(
        font.render("FLAPPY BIRD", True, WHITE),
        (110, 180))

    screen.blit(
font.render("SPACE starten", True, WHITE),
        (90, 240))

    screen.blit(
        font.render(
            f"Highscore: {highscore}",
            True,
            WHITE),(90, 300))

    py.display.update()


def draw_gameover():
    screen.fill(BLUE)

    screen.blit(
        font.render("GAME OVER", True, WHITE),(110, 180))

    screen.blit(
        font.render(f"Score: {score}", True, WHITE),(120, 240))

    screen.blit(
        font.render(
            f"Highscore: {highscore}",
            True,
            WHITE),(90, 300))

    screen.blit(
        font.render("SPACE Restart", True, WHITE),(80, 360))

    py.display.update()


def check_collision():

    b = bird_rect()

    if bird_y <= 0 or bird_y >= HEIGHT:
        return True

    for top, bottom in pipes:

        if b.colliderect(top):
            return True

        if b.colliderect(bottom):
            return True

    return False


running = True

while running:

    clock.tick(FPS)

    for event in py.event.get():

        if event.type == py.QUIT:
            py.quit()
            sys.exit()

        if event.type == py.KEYDOWN:

            if event.key == py.K_SPACE:

                if state == "START":
                    state = "PLAY"

                elif state == "PLAY":
                    bird_velocity = jump_strength

                elif state == "GAMEOVER":
                    reset()
                    state = "PLAY"

    if state == "START":
        draw_start()
        continue

    if state == "GAMEOVER":
        draw_gameover()
        continue

    if power_active == "SPEED":
        pipe_speed = 7
        bird_size = 50

    elif power_active == "SLOW":
        pipe_speed = 2
        bird_size = 50

    elif power_active == "GROW":
        pipe_speed = base_speed
        bird_size = 75

    elif power_active == "SHRINK":
        pipe_speed = base_speed
        bird_size = 25

    else:
        pipe_speed = base_speed
        bird_size = 50

    if (
        power_active and
        py.time.get_ticks() - power_timer > 5000
    ):
        power_active = None

    bird_velocity += gravity
    bird_y += bird_velocity

    for top, bottom in pipes:

        top.x -= pipe_speed
        bottom.x -= pipe_speed

    if random.randint(1, 180) == 1:
        powerups.append(create_powerup())

    for p, t in powerups[:]:

        p.x -= pipe_speed

        if bird_rect().colliderect(p):

            power_active = t
            power_timer = py.time.get_ticks()

            powerups.remove((p, t))

        elif p.x < -50:

            powerups.remove((p, t))

    if pipes[0][0].x < -pipe_width:

        pipes.pop(0)

        last = pipes[-1][0].x

        new = create_pipe()

        new[0].x = last + 300
        new[1].x = last + 300

        pipes.append(new)

        score += 1

    if check_collision():

        if score > highscore:
            highscore = score
            save_highscore(highscore)

        state = "GAMEOVER"

    draw_game()

py.quit()