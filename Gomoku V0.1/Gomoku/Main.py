import random
import pygame
import tkinter as tk
from Settings import Const as c
from Tools import Drawer as d
from Tools import GLT as glt

#get specs
root = tk.Tk()
root.title("Gomoku Launcher")
root.geometry("200x250")

# --- Board size ---
tk.Label(root, text="Select Board Size:").pack(pady=10)
c.GAME_SIZE = tk.IntVar(value=15)
size_options = list(range(3, 21))
tk.OptionMenu(root, c.GAME_SIZE, *size_options).pack(pady=5)

# --- Win condition ---
tk.Label(root, text="Win Condition:").pack(pady=10)
c.WIN_CONDITION = tk.IntVar(value=5)

win_menu = tk.OptionMenu(root, c.WIN_CONDITION, *range(3, c.GAME_SIZE.get() + 1))
win_menu.pack(pady=5)

# --- update win options when board size changes ---
def update_win_options(*args):
    menu = win_menu["menu"]
    menu.delete(0, "end")

    for i in range(3, c.GAME_SIZE.get() + 1):
        menu.add_command(
            label=i,
            command=lambda v=i: c.WIN_CONDITION.set(v)
        )

    # keep win condition valid
    if c.WIN_CONDITION.get() > c.GAME_SIZE.get():
        c.WIN_CONDITION.set(c.GAME_SIZE.get())

c.GAME_SIZE.trace_add("write", update_win_options)

# --- launch ---
tk.Button(root, text="Launch", command=root.destroy).pack(pady=20)
root.mainloop()
print("Board size:", c.GAME_SIZE.get())
print("Win condition:", c.WIN_CONDITION.get())
c.GAME_SIZE = c.GAME_SIZE.get()
c.WIN_CONDITION = c.WIN_CONDITION.get()
c.BLOCK_SIZE = c.SCREEN_SIZE // c.GAME_SIZE





# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((c.SCREEN_SIZE+c.GUI_SPACING, c.SCREEN_SIZE))
pygame.display.set_caption("Gomoku")
clock = pygame.time.Clock()

def init_board():
    global board, turn, grid_x, grid_y
    board = [[0 for _ in range(c.GAME_SIZE)] for _ in range(c.GAME_SIZE)]
    turn = random.choice([1, 2])
    grid_x, grid_y = 0,0

#restart GUI function
def restart_gui(mx=-1,my=-1):
    if c.SCREEN_SIZE +10 <= mx <= c.SCREEN_SIZE + c.GUI_SPACING -10:
        if c.SCREEN_SIZE -60 <= my <= c.SCREEN_SIZE -10:
            #restart button
            init_board()
            return True
        if c.SCREEN_SIZE -120 <= my <= c.SCREEN_SIZE -70:
            #quit button
            pygame.quit()
            exit()
        return False

# --- Main loop ---
init_board()
while True:
    #reset screen
    screen.fill((97, 56, 4))
    for event in pygame.event.get():
        #quit events
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE:
                init_board()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // c.BLOCK_SIZE
            grid_y = mouse_y // c.BLOCK_SIZE
            print(f"Clicked on grid: ({grid_x}, {grid_y})")
            print(f"{c.GAME_SIZE=}, {c.SCREEN_SIZE=}, {c.BLOCK_SIZE=}")
            if (0 <= grid_x < c.GAME_SIZE and 0 <= grid_y < c.GAME_SIZE):
                 #update board & turn
                if board[grid_y][grid_x] == 0:
                    board[grid_y][grid_x] = turn
                    turn = 2 if turn == 1 else 1
                    #check for win
                    result = glt.termial_state(board,grid_x,grid_y)
                    if result[0]:
                        print(f"Player {board[grid_y][grid_x]} wins!")
                        print("Winning coordinates:", result[1])
                        d.draw_board(screen, c.GAME_SIZE, board)
                        d.highlight_winner(screen, result[1])
                        d.draw_gui(screen, turn)

                        #restart logic
                        w = True
                        while w:
                            pygame.display.update()
                            for ev in pygame.event.get():
                                if ev.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                if ev.type == pygame.KEYDOWN:
                                    if ev.key == pygame.K_ESCAPE:
                                        pygame.quit()
                                        exit()
                                    if ev.key == pygame.K_SPACE:
                                        init_board()
                                        w = False
                                        break
                                if ev.type == pygame.MOUSEBUTTONDOWN:
                                    mx, my = pygame.mouse.get_pos()
                                    if restart_gui(mx, my):
                                        w = False
                                        break
            
            else:
                #check if click on the GUI area
                if restart_gui(mouse_x, mouse_y):
                    continue

           
    
    #draw board and pieces
    d.draw_board(screen, c.GAME_SIZE, board)
    d.draw_gui(screen, turn)
    pygame.display.update()
    clock.tick(60)
