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

def draw_grid(offset_x):
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(
                offset_x + col * CELL_SIZE, 
                row * CELL_SIZE, 
                CELL_SIZE, 
                CELL_SIZE
            )
            pygame.draw.rect(screen, (0, 0, 255), rect, 1)

running = True
while running:
    screen.fill((0, 0, 0))

    draw_grid(50)  # Player's grid
    draw_grid(450)  # Opponent's grid

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()

