from Settings import Const as c

def termial_state(board, lx, ly):
    player = board[ly][lx]
    if player == 0:
        return [False, None]

    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for dx, dy in directions:
        count = 1
        bx, by = lx, ly
        nx, ny = lx, ly
        for step in range(1, c.WIN_CONDITION):
            tx, ty = lx + step * dx, ly + step * dy
            print(f"Checking ({tx}, {ty}) in direction ({dx}, {dy})")
            if not(0 <= tx < c.GAME_SIZE and 0 <= ty < c.GAME_SIZE):
                break
            else:
                if board[ty][tx] == player:
                    count += 1
                    nx, ny = tx, ty
                else: break

        for step in range(1, c.WIN_CONDITION):
            tx, ty = lx - step * dx, ly - step * dy
            print(f"Checking ({tx}, {ty}) in direction (-{dx}, -{dy})")
            if not(0 <= tx < c.GAME_SIZE and 0 <= ty < c.GAME_SIZE):
                break
            else:
                if board[ty][tx] == player:
                    count += 1
                    bx, by = tx, ty
                else: break

        if count >= c.WIN_CONDITION:
            return [True, (bx, by, nx, ny)]

    return [False, None]
