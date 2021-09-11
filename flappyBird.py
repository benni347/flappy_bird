#!/usr/bin/env python3

"""https://github.com/benni347 In here I will recode the flappy bird game."""

# Here are the imports needed for the project
import pygame
import sys
import random


def draw_floor():
    """In here I will define the floor of the game."""
    screen.blit(floor_base, (floor_x_pos, 900))
    screen.blit(floor_base, (floor_x_pos + 576, 900))


def create_pipe():
    """I will use this to create the pipe."""
    random_pipe_pos = random.randint(350, 800)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    """I will use this function to define the movment of the pipe."""
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    """I will use this function to draw the pipes."""
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    """In here I will check for collision with the bird_rect."""
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        die_sound.play()
        return False
    return True


def rotate_bird(bird):
    """In this function I will define the rotation of the bird."""
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    """I will use this function to animate the bird."""
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    """In this function I will define the score_display."""
    if game_state == "main_game":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f"High score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    """I will check if the new score is higher than the old high score and change the high score."""
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100, size=32, channels=2, buffer=2048)
pygame.init()
# Set the window title of pygame.
pygame.display.set_caption("Flappy bird")

# vars
clock = pygame.time.Clock()
game_active = True
score = 0
high_score = 0
game_font = pygame.font.Font("04B_19.ttf", 40)

screen = pygame.display.set_mode((576, 1024))
bg_day = pygame.transform.scale2x(pygame.image.load("sprites/background-day.png").convert())

floor_base = pygame.transform.scale2x(pygame.image.load("sprites/base.png").convert())
floor_x_pos = 0

# bird = pygame.image.load("sprites/bluebird-midflap.png").convert_alpha()
# bird = pygame.transform.scale2x(bird)
# bird_rect = bird.get_rect(center=(100, 512))

bird_downflap = pygame.transform.scale2x(pygame.image.load("sprites/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("sprites/bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("sprites/bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird = bird_frames[bird_index]
bird_rect = bird.get_rect(center=(100, 512))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
gravity = 0.25
bird_movement = 0

pipe_surface = pygame.transform.scale2x(pygame.image.load("sprites/pipe-green.png"))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

game_over_surface = pygame.transform.scale2x(pygame.image.load("sprites/message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound("audio/wing.wav")
die_sound = pygame.mixer.Sound("audio/hit.wav")
score_sound = pygame.mixer.Sound("audio/point.wav")
score_sound_countdown = 110
while True:
    for event in pygame.event.get():
        # This is for closing the game with the x.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # This will check for arrow up.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_active:
                bird_movement = 0
                bird_movement -= 12
                flap_sound.play()
            # To restart the game
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0
        # This will extend the create_pipe tulpe.
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg_day, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
