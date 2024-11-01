import pygame
import sys

def toh(screen):
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tower of Hanoi")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (100, 149, 237)
    GREEN = (50, 205, 50)
    RED = (255, 69, 0)
    LIGHT_GREY = (200, 200, 200)
    DARK_GREY = (70, 70, 70)
    GOLD = (255, 215, 0)

    font = pygame.font.Font(None, 36)

    difficulty_levels = {"Easy": 3, "Medium": 4, "Hard": 5}
    moves = 0
    disks = 3
    stacks = [[], [], []]
    dragging = False
    dragged_disk = None
    dragged_disk_start_stack = None
    disk_width = 120

    def draw_button(text, x, y, color, action=None):
        button_rect = pygame.Rect(x, y, 150, 50)
        hover = button_rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, DARK_GREY if hover else color, button_rect, border_radius=10)
        
        text_surf = font.render(text, True, WHITE)
        screen.blit(text_surf, (button_rect.x + (button_rect.width - text_surf.get_width()) // 2,
                                button_rect.y + (button_rect.height - text_surf.get_height()) // 2))
        
        if hover and pygame.mouse.get_pressed()[0] and action:
            action()

    def start_game(level):
        nonlocal disks, stacks, moves
        disks = difficulty_levels[level]
        moves = 0
        stacks[:] = [list(range(disks, 0, -1)), [], []]

    buttons = [
        {"text": "Easy", "x": 50, "y": 500, "color": BLUE, "action": lambda: start_game("Easy")},
        {"text": "Medium", "x": 250, "y": 500, "color": GREEN, "action": lambda: start_game("Medium")},
        {"text": "Hard", "x": 450, "y": 500, "color": RED, "action": lambda: start_game("Hard")},
        {"text": "Quit", "x": 650, "y": 500, "color": DARK_GREY, "action": lambda: sys.exit()}
    ]

    def draw_game():
        screen.fill(LIGHT_GREY)
        pygame.draw.rect(screen, (210, 180, 140), (0, 450, WIDTH, 150))  # ground color

        for i in range(3):
            pygame.draw.rect(screen, GOLD, (150 + i * 250 - 5, 200, 10, 250))

        for i, stack in enumerate(stacks):
            for j, disk in enumerate(stack):
                if dragging and dragged_disk == disk and dragged_disk_start_stack == i:
                    continue
                pygame.draw.rect(screen, BLUE,
                                (150 + i * 250 - disk_width * disk // disks // 2,
                                450 - (j + 1) * 20, disk_width * disk // disks, 20),
                                border_radius=5)

        if dragging and dragged_disk is not None:
            pygame.draw.rect(screen, BLUE,
                            (pygame.mouse.get_pos()[0] - disk_width * dragged_disk // disks // 2,
                            pygame.mouse.get_pos()[1] - 10, disk_width * dragged_disk // disks, 20),
                            border_radius=5)

        move_text = font.render(f"Moves: {moves}", True, BLACK)
        screen.blit(move_text, (10, 10))

    def is_valid_move(from_stack, to_stack):
        if not stacks[from_stack]:
            return False
        if not stacks[to_stack] or stacks[from_stack][-1] < stacks[to_stack][-1]:
            return True
        return False

    def move_disk(from_stack, to_stack):
        nonlocal moves
        if is_valid_move(from_stack, to_stack):
            disk = stacks[from_stack].pop()
            stacks[to_stack].append(disk)
            moves += 1

    def check_win():
        return len(stacks[2]) == disks

    def display_win():
        win_text = font.render("Congratulations! You Won!", True, GREEN)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not dragging:
                    for i, stack in enumerate(stacks):
                        if stack and pygame.Rect(150 + i * 250 - disk_width * stack[-1] // disks // 2, 450 - len(stack) * 20, disk_width * stack[-1] // disks, 20).collidepoint(pygame.mouse.get_pos()):
                            dragging = True
                            dragged_disk = stack[-1]
                            dragged_disk_start_stack = i
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    closest_stack = min(range(3), key=lambda i: abs(150 + i * 250 - pygame.mouse.get_pos()[0]))
                    if is_valid_move(dragged_disk_start_stack, closest_stack):
                        move_disk(dragged_disk_start_stack, closest_stack)
                        if check_win():
                            display_win()
                    else:
                        stacks[dragged_disk_start_stack].append(dragged_disk)

                    dragging = False
                    dragged_disk = None
                    dragged_disk_start_stack = None

        draw_game()
        for button in buttons:
            draw_button(button["text"], button["x"], button["y"], button["color"], button["action"])

        pygame.display.flip()
