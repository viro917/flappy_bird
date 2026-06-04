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

pipes_oben = py.image.load("pipes_oben.png").convert()
pipes_oben.set_colorkey((163, 73, 164))

pipes_unten = py.image.load("pipes_unten.png").convert()
pipes_unten.set_colorkey((163, 73, 164))


WHITE = (255, 255, 255)
BLUE = (135, 206, 235)

clock = py.time.Clock()
FPS = 60
font = py.font.SysFont(None, 40)

bird_x = 80
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -8


pipe_width = 120
pipe_gap = 180
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
    shrink = 12
    return py.Rect(
        bird_x - 25 + shrink,
        bird_y - 25 + shrink,
        50 - shrink * 2,
        50 - shrink * 2
    )


def create_pipe():
    h = random.randint(80, HEIGHT - pipe_gap - 80)
    top = py.Rect(WIDTH, 0, pipe_width, h)
    bottom = py.Rect(WIDTH, h + pipe_gap, pipe_width, HEIGHT - (h + pipe_gap))
    return top, bottom

def reset():
    global pipes, bird_y, bird_velocity, score, powerups, power_active, pipe_speed

    pipes = []
    for i in range(3):
        p = create_pipe()
        p[0].x += i * 300
        p[1].x += i * 300
        pipes.append(p)

    powerups = []
    power_active = None
    pipe_speed = base_speed

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
            25
        )

        in_pipe = False

        for top, bottom in pipes:
            if rect.colliderect(top) or rect.colliderect(bottom):
                in_pipe = True
                break

        if not in_pipe:
            typ = random.choice(["FAST", "SLOW"])
            return rect, typ


def draw_game():
    screen.fill(BLUE)

    screen.blit(vogel, (bird_x - 25, int(bird_y) - 25))

    for top, bottom in pipes:
        top_img = py.transform.scale(pipes_oben, (pipe_width, top.height))
        bottom_img = py.transform.scale(pipes_unten, (pipe_width, bottom.height))

        screen.blit(top_img, (top.x, top.y))
        screen.blit(bottom_img, (bottom.x, bottom.y))

    for p, t in powerups:
        color = (255, 0, 0) if t == "FAST" else (0, 255, 255)
        py.draw.rect(screen, color, p)

    txt = font.render(f"Score: {score}", True, WHITE)
    screen.blit(txt, (10, 10))

    py.display.update()

def draw_start():
    screen.fill(BLUE)

    screen.blit(font.render("FLAPPY BIRD", True, WHITE), (110, 180))
    screen.blit(font.render("SPACE starten", True, WHITE), (100, 240))
    screen.blit(font.render(f"Highscore: {highscore}", True, WHITE), (100, 300))

    py.display.update()

def draw_gameover():
    screen.fill(BLUE)

    screen.blit(font.render("GAME OVER", True, WHITE), (120, 180))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (130, 240))
    screen.blit(font.render(f"Highscore: {highscore}", True, WHITE), (100, 300))
    screen.blit(font.render("SPACE Restart", True, WHITE), (90, 360))

    py.display.update()


def check_collision():
    b = bird_rect()

    if bird_y <= 0 or bird_y >= HEIGHT:
        return True

    for top, bottom in pipes:
        if b.colliderect(top) or b.colliderect(bottom):
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


    if power_active == "FAST":
        pipe_speed = 7
    elif power_active == "SLOW":
        pipe_speed = 2
    else:
        pipe_speed = base_speed

    if power_active and py.time.get_ticks() - power_timer > 5000:
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

        if p.x < -50:
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