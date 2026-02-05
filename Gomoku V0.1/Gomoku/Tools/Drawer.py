import pygame
from Settings import Const as c

class Piece:
    def __init__(self, player, coord):
        self._player = player
        self._coord = coord

    def draw(self, screen):
        x, y = self._coord
        if self._player == 1:
            pygame.draw.circle(screen, (0, 0, 0),
                               (x*c.BLOCK_SIZE + c.BLOCK_SIZE//2,
                                y*c.BLOCK_SIZE + c.BLOCK_SIZE//2),
                               c.BLOCK_SIZE//2 - 5)
        else:
            pygame.draw.circle(screen, (255, 255, 255),
                               (x*c.BLOCK_SIZE + c.BLOCK_SIZE//2,
                                y*c.BLOCK_SIZE + c.BLOCK_SIZE//2),
                               c.BLOCK_SIZE//2 - 5)
            pygame.draw.circle(screen, (0, 0, 0),
                               (x*c.BLOCK_SIZE + c.BLOCK_SIZE//2,
                                y*c.BLOCK_SIZE + c.BLOCK_SIZE//2),
                               c.BLOCK_SIZE//2 - 5, 1)


def draw_board(screen, cells,board):
    block_size = c.SCREEN_SIZE // cells
    for x in range(0, c.SCREEN_SIZE + 1, block_size):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, c.SCREEN_SIZE), 1)
    for y in range(0, c.SCREEN_SIZE + 1, block_size):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (c.SCREEN_SIZE, y), 1)
    # draw pieces
    for y in range(cells):
        for x in range(cells):
            if board[y][x] != 0:
                Piece(board[y][x], (x, y)).draw(screen)

def highlight_winner(screen, win_coords):
    if win_coords is None:
        return
    x1, y1, x2, y2 = win_coords
    start_pos = (x1 * c.BLOCK_SIZE + c.BLOCK_SIZE // 2,
                 y1 * c.BLOCK_SIZE + c.BLOCK_SIZE // 2)
    end_pos = (x2 * c.BLOCK_SIZE + c.BLOCK_SIZE // 2,
               y2 * c.BLOCK_SIZE + c.BLOCK_SIZE // 2)
    pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 5)
def draw_gui(screen, turn,w=None):
    font = pygame.font.SysFont(None, 36)
    if w:
        text = font.render(f"Player {w} wins!", True, (255, 255, 255))
    else:
        text = font.render(f"Player {turn}'s turn", True, (255, 255, 255))
    screen.fill((50, 50, 50), (c.SCREEN_SIZE, 0, c.GUI_SPACING, c.SCREEN_SIZE))
    screen.blit(text, (c.SCREEN_SIZE + 10, 10))
    instructions = [
        "Press SPACE to restart",
        "Press ESC to quit"
    ]
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, (255, 255, 255))
        screen.blit(text, (c.SCREEN_SIZE + 10, 40 + i * 30))

    #button
    pygame.draw.rect(screen, (200, 0, 0), (c.SCREEN_SIZE + 10, c.SCREEN_SIZE - 60, c.GUI_SPACING - 20, 50))
    button_text = font.render("Restart", True, (255, 255, 255))
    screen.blit(button_text, (c.SCREEN_SIZE + (c.GUI_SPACING-20)//2 - button_text.get_width()//2, c.SCREEN_SIZE - 60 + 15))

    pygame.draw.rect(screen, (0, 0, 200), (c.SCREEN_SIZE + 10, c.SCREEN_SIZE - 120, c.GUI_SPACING - 20, 50))
    quit_text = font.render("Quit", True, (255, 255, 255))
    screen.blit(quit_text, (c.SCREEN_SIZE + (c.GUI_SPACING-20)//2 - quit_text.get_width()//2, c.SCREEN_SIZE - 120 + 15))