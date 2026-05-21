import pygame as py
import random
import sys


py.init()


WIDTH = 400
HEIGHT = 600
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Flappy Bird")


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
    pipes[i][0].x += i * 200
    pipes[i][1].x += i * 200


def draw():
    screen.fill(BLUE)


    py.draw.circle(screen, YELLOW, (bird_x, int(bird_y)), bird_radius)


    for top, bottom in pipes:
        py.draw.rect(screen, GREEN, top)
        py.draw.rect(screen, GREEN, bottom)


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
        new_pipe = create_pipe()
        new_pipe[0].x = WIDTH
        new_pipe[1].x = WIDTH
        pipes.append(new_pipe)
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