import pygame
import random

pygame.init()


WIDTH = 900
HEIGHT = 600
ROWS = 10
COLS = 10
CELL_SIZE = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BattleShip")

def shoot(board, row, col):
    if board[row][col] == "S":
        board[row][col] = "X"  # Hit
        return "hit"
    elif board[row][col] == "~":
        board[row][col] = "O"  # Miss
        return "miss"
    return "Already shot here"  # Already shot here

def ai_shot(board):
    global ai_targets

    # 🎯 TARGET MODE
    while ai_targets:
        row, col = ai_targets.pop(0)

        if board[row][col] in ["X", "O"]:
            continue  # skip already used cells

        result = shoot(board, row, col)

        if result == "hit":
            neighbors = [
                (row-1, col),
                (row+1, col),
                (row, col-1),
                (row, col+1)
            ]

            for r, c in neighbors:
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if board[r][c] not in ["X", "O"] and (r, c) not in ai_targets:
                        ai_targets.append((r, c))

        return result

    # 🔍 HUNT MODE
    while True:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)

        if board[row][col] not in ["X", "O"]:
            result = shoot(board, row, col)

            if result == "hit":
                neighbors = [
                    (row-1, col),
                    (row+1, col),
                    (row, col-1),
                    (row, col+1)
                ]

                for r, c in neighbors:
                    if 0 <= r < ROWS and 0 <= c < COLS:
                        if (r, c) not in ai_targets:
                            ai_targets.append((r, c))

            return result
        


def check_win(board):
    for row in board:
        if "S" in row:
            return False
    return True

def place_ships(board, size):
    placed = False
    while not placed:
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        direction = random.choice(['H', 'V'])

        if direction == 'H' and col + size <= 10: 
            if all (board[row][col+i] == "~" for i in range(size)):
                for i in range(size):
                    board[row][col+i] = "S"
                placed = True

        elif direction == 'V' and row + size <= 10:
            if all (board[row+i][col] == "~" for i in range(size)):
                for i in range(size):
                    board[row+i][col] = "S"
                placed = True





def draw_grid(offset_x, board, show_ships=False):
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(
                offset_x + col * CELL_SIZE, 
                row * CELL_SIZE, 
                CELL_SIZE, 
                CELL_SIZE
            )

            cell = board[row][col]

            color = (0, 0, 255)
            if cell == "S" and show_ships:
                color = (0, 255, 0)  # Green for ships
            elif cell == "X":
                color = (255, 0, 0)  # Red for hits
            elif cell == "O":
                color = (255, 255, 0)  # Yellow for misse
            
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)


player_board = [["~"] * COLS for _ in range(ROWS)]
opponent_board = [["~"] * COLS for _ in range(ROWS)]

ships = [5, 4, 3, 3, 2]

for size in ships:
    place_ships(player_board, size)
    place_ships(opponent_board, size)






# Main game loop
running = True
player_turn = True
ai_targets = []  # List to store AI's target coordinates
ai_hits = []  # List to store AI's successful hits
font = pygame.font.SysFont(None, 36)


while running:
    screen.fill((0, 0, 0))

    draw_grid(50, player_board, True)  # Player's grid
    draw_grid(450, opponent_board, False)  # Opponent's grid
    turn_text = "Player's Turn" if player_turn else "AI's Turn"
    text_surface = font.render(turn_text, True, (255, 255, 255))
    screen.blit(text_surface, (350, 500))


    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if 450 <= mouse_x < 450 + COLS * CELL_SIZE and 0 <=  mouse_y < ROWS * CELL_SIZE:
                col = (mouse_x - 450) // CELL_SIZE
                row = mouse_y // CELL_SIZE

                result = shoot(opponent_board, row, col)
                print(f"Player shot at ({row}, {col}): {result}")

                if result != "Already shot here":
                    player_turn = False # Player's turn ends after a valid shot
                    
                    if check_win(opponent_board):
                        print("Player wins!")
                        running = False
        
        if not player_turn and running:
            pygame.time.delay(500)  # Delay for AI's turn

            ai_result = ai_shot(player_board)
            print(f"AI shot: {ai_result}")

            if check_win(player_board):
                print("AI wins!")
                running = False
            player_turn = True  # AI's turn ends after shooting


        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()

