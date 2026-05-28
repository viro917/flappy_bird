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
pipes_oben = py.transform.scale(pipes_oben, (50, 50))

pipes_unten = py.image.load("pipes_unten.png").convert()
pipes_unten.set_colorkey((163, 73, 164))
pipes_unten = py.transform.scale(pipes_unten, (50, 50))

WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

clock = py.time.Clock()
FPS = 60


font = py.font.SysFont(None, 40)

bird_x = 80
bird_y = HEIGHT // 2
bird_radius = 20
bird_velocity = 0
gravity = 0.5
jump_strength = -8


pipe_width = 70
pipe_gap = 180
pipe_velocity = 4
pipes = []


score = 0


def create_pipe():
    height = random.randint(100, 400)
    top_pipe = py.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = py.Rect(
        WIDTH,
        height + pipe_gap,
        pipe_width,
        HEIGHT - height - pipe_gap
    )
    return top_pipe, bottom_pipe



for i in range(3):
    pipes.append(create_pipe())
    pipes[i][0].x += i * 300
    pipes[i][1].x += i * 300


def draw():
    screen.fill(BLUE)


    screen.blit(vogel, (bird_x, int(bird_y)))


    for top, bottom in pipes:
        screen.blit(pipes_oben, top)
        screen.blit(pipes_unten, bottom)


    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    py.display.update()


def check_collision():
    bird_rect = py.Rect(
        bird_x - bird_radius,
        bird_y - bird_radius,
        bird_radius * 2,
        bird_radius * 2
    )

    if bird_y <= 0 or bird_y >= HEIGHT:
        return True


    for top, bottom in pipes:
        if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
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
                bird_velocity = jump_strength

    bird_velocity += gravity
    bird_y += bird_velocity


    for top, bottom in pipes:
        top.x -= pipe_velocity
        bottom.x -= pipe_velocity


    if pipes[0][0].x < -pipe_width:
        pipes.pop(0)
        last_pipe_x = pipes[-1][0].x
        new_top, new_bottom = create_pipe()
        new_top.x = last_pipe_x + 300
        new_bottom.x = last_pipe_x + 300
        pipes.append((new_top, new_bottom))
        score += 1

    if check_collision():
        running = False

    draw()


screen.fill(BLUE)
game_over = font.render("GAME OVER", True, WHITE)
final_score = font.render(f"Score: {score}", True, WHITE)

screen.blit(game_over, (WIDTH // 2 - 110, HEIGHT // 2 - 40))
screen.blit(final_score, (WIDTH // 2 - 80, HEIGHT // 2 + 10))

py.display.update()

py.time.wait(3000)

py.quit()