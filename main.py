import pygame
import sys
import random


pygame.init()
clock = pygame.time.Clock()

tennis_sound = pygame.mixer.music.load('./assets/audio/music.mp3')
score_sound = pygame.mixer.Sound('./assets/audio/goal.wav')
slap_sound = pygame.mixer.Sound('./assets/audio/slap.wav')
pygame.mixer.music.play(-1)

screen_width = 1280
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tennis Game")

ball = pygame.Rect(int(screen_width/2) - 15, int(screen_height/2) - 15, 30, 30)
player = pygame.Rect(screen_width - 20, int(screen_height/2) - 70, 10, 140)
enemy = pygame.Rect(10, int(screen_height/2) - 70, 10, 140)

bg = pygame.image.load('./assets/images/bg.jpg')


def ball_restart():
    global ball_speed_y, ball_speed_x, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (int(screen_width / 2), int(screen_height / 2))

    if current_time - score_time < 700:
        number_three = font.render("3", 1, (200, 200, 200))
        screen.blit(number_three, (int(screen_width / 2) - 10, int(screen_height / 20) + 20))
    if 700 < current_time - score_time < 1400:
        number_two = font.render("2", 1, (200, 200, 200))
        screen.blit(number_two, (int(screen_width / 2) - 10, int(screen_height / 20) + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = font.render("1", 1, (200, 200, 200))
        screen.blit(number_one, (int(screen_width / 2) - 10, int(screen_height / 20) + 20))

    if current_time - score_time < 2100:
        ball_speed_y, ball_speed_x = 0, 0
    else:
        ball_speed_y = 15 * random.choice((1, -1))
        ball_speed_x = 15 * random.choice((1, -1))
        score_time = None


ball_speed_x = 15 * random.choice((1, -1))
ball_speed_y = 15 * random.choice((1, -1))
player_speed = 0
enemy_speed = random.randint(0, 30)

player_score = 0
enemy_score = 0
font = pygame.font.SysFont('comicsans', 30, True)

score_time = True

run = True
while run:
    enemy_speed = random.randint(0, 30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 10
            if event.key == pygame.K_UP:
                player_speed -= 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 10
            if event.key == pygame.K_UP:
                player_speed += 10

    # ball_animation
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        enemy_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) or ball.colliderect(enemy):
        pygame.mixer.Sound.play(slap_sound)
        ball_speed_x *= -1

    # player_animaton
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

    # enemy_animation
    if enemy.top < ball.y:
        enemy.top += enemy_speed
    if enemy.bottom > ball.y:
        enemy.bottom -= enemy_speed
    if enemy.top <= 0:
        enemy.top = 0
    if enemy.bottom >= screen_height:
        enemy.bottom = screen_height

    screen.blit(bg, (0, 0))
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (255, 0, 0), enemy)
    pygame.draw.ellipse(screen, (255, 255, 255), ball)
    pygame.draw.aaline(screen, (95, 99, 104), (int(screen_width/2), 0), (int(screen_width/2), screen_height))

    if score_time:
        ball_restart()

    if player_score == 10 or enemy_score == 10:
        player_score = 0
        enemy_score = 0

    player_text = font.render(f"{player_score}", 1, (200, 200, 200))
    screen.blit(player_text, (650, 10))

    enemy_text = font.render(f"{enemy_score}", 1, (200, 200, 200))
    screen.blit(enemy_text, (618, 10))

    pygame.display.update()
    clock.tick(60)
