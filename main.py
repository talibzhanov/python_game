import pygame
from random import randrange as rnd

win = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('my game')

clock = pygame.time.Clock()
FPS = 60

paddle_w = 250
paddle_h = 30
paddle_speed = 15
paddle = pygame.Rect(1200 // 2 - paddle_w // 2, 800 - paddle_h, paddle_w, paddle_h)

ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, 1200 - ball_rect), 800 // 2, ball_rect, ball_rect)
dx,dy = 1, -1

block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100,50) for i in range(10) for j in range(4)]
color_list = [(rnd(30,256), rnd(30,256), rnd(30,256)) for i in range(10) for j in range(4)]

def detect_collide(dx,dy,ball,rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = ball.left - rect.right
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = ball.top - rect.bottom
    if abs(delta_x - delta_y) < 10:
        dx,dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx,dy

run = True
while run:
    clock.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    win.fill((0,0,0))
    [pygame.draw.rect(win, color_list[color], block) for color,block in enumerate(block_list)]
    pygame.draw.rect(win, (255,255,255),  paddle)
    pygame.draw.circle(win,(255,255,255), ball.center, ball_radius)
    pygame.display.update()

    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.x > 0:
        paddle.x -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.x < 1200 - paddle_w:
        paddle.x += paddle_speed

    if ball.centerx < ball_radius or ball.centerx > 1200 - ball_radius:
        dx = -dx
    if ball.centery < ball_radius:
        dy = -dy
    if ball.colliderect(paddle) and dy > 0:
        dy = -dy

    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit = block_list.pop(hit_index)
        hit = color_list.pop(hit_index)
        FPS += 2
        dx,dy = detect_collide(dx,dy,ball,paddle)