import pygame
import sys
import time
import random

def snake_game(screen):
    difficulty = 25
    screen_width, screen_height = 800, 600
    game_window = pygame.display.set_mode((screen_width, screen_height))

    check_errors = pygame.init()
    if check_errors[1] > 0:
        print(f'[!] Had {check_errors[1]} errors when initializing game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialized')

    pygame.display.set_caption('Snake Eater')

    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)

    background_image = pygame.image.load("snake/snake_bg.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    fps_controller = pygame.time.Clock()

    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    # Game Over function
    def game_over():
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (screen_width / 2, screen_height / 4)
        game_window.fill(black)
        game_window.blit(game_over_surface, game_over_rect)
        show_score(0, red, 'times', 40)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (screen_width / 10, 15)
        else:
            score_rect.midtop = (screen_width / 2, screen_height / 1.25)
        game_window.blit(score_surface, score_rect)

    def main_menu():
        while True:
            screen.blit(background_image, (0, 0))
            my_font = pygame.font.SysFont('times new roman', 60)
            start_surface = my_font.render('START', True, white)
            my_font1 = pygame.font.SysFont('times new roman', 80)
            start_surface1 = my_font1.render('Snake Game', True, white)
            start_rect = start_surface.get_rect(center=(screen_width // 2, screen_height / 2))
            start_rect1 = start_surface1.get_rect(center=(screen_width // 2, screen_height / 8))

            game_window.blit(start_surface, start_rect)
            game_window.blit(start_surface1, start_rect1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        main_game()

            pygame.display.update()

    def main_game():
        nonlocal snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        change_to = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        change_to = 'DOWN'
                    elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                        change_to = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        change_to = 'RIGHT'
                    elif event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            if change_to == 'UP':
                direction = 'UP'
            if change_to == 'DOWN':
                direction = 'DOWN'
            if change_to == 'LEFT':
                direction = 'LEFT'
            if change_to == 'RIGHT':
                direction = 'RIGHT'

            if direction == 'UP':
                snake_pos[1] -= 10
            if direction == 'DOWN':
                snake_pos[1] += 10
            if direction == 'LEFT':
                snake_pos[0] -= 10
            if direction == 'RIGHT':
                snake_pos[0] += 10

            snake_body.insert(0, list(snake_pos))
            if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
                score += 1
                food_spawn = False
            else:
                snake_body.pop()

            if not food_spawn:
                food_pos = [random.randrange(1, (screen_width // 10)) * 10, random.randrange(1, (screen_height // 10)) * 10]
            food_spawn = True

            game_window.fill(black)
            for pos in snake_body:
                pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

            pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

            if snake_pos[0] < 0 or snake_pos[0] > screen_width - 10:
                game_over()
            if snake_pos[1] < 0 or snake_pos[1] > screen_height - 10:
                game_over()
            for block in snake_body[1:]:
                if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                    game_over()

            show_score(1, white, 'consolas', 20)
            pygame.display.update()
            fps_controller.tick(difficulty)

    main_menu()

if __name__ == "__main__":
    snake_game(None)
