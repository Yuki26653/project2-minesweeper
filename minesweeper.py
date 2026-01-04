# import relative module
import numpy as np
import random
from typing import List, Tuple, Set, Union, Any

# Variables (defaults, may be overridden by input)
num_mines = 5  # cannot exceed row_num * col_num
row_num = 9
col_num = 9
HIDDEN = "#"
FLAG = "X"


def ask_int(prompt: str, default: int) -> int:
    """Ask for an integer input; allow empty input to use default."""
    while True:
        s = input(f"{prompt} (default {default}): ").strip()
        if s == "":
            return default
        try:
            value = int(s)
            return value
        except ValueError:
            print("Please enter an integer (or press Enter for default).")


def print_help() -> None:
    print(
        """
Welcome to Minesweeper!

Commands:
  o <row> <col>    Open a cell
  f <row> <col>    Flag / unflag a cell
  quit             Exit the game

Examples:
  o 3 4
  f 2 6
"""
    )


def insert_mines(empty_board: np.ndarray, num_mines: int) -> np.ndarray:
    # insert mines in random position denoted by a value 1
    rows = list(range(1, row_num + 1))
    columns = list(range(1, col_num + 1))
    count = 0

    while count < num_mines:
        row = random.choice(rows)
        column = random.choice(columns)
        if empty_board[row][column] == 0:
            empty_board[row][column] = 1
            count += 1
    return empty_board


def display(board: List[List[Any]]) -> None:
    rows = len(board)
    cols = len(board[0])
    cell_w = 3

    def cell_str(x: Any) -> str:
        s = " " if x == 0 else str(x)
        s = s[:1]
        return f" {s} "

    print("    " + " ".join(f"{c:^{cell_w}}" for c in range(cols)))
    border = "   +" + "+".join("-" * cell_w for _ in range(cols)) + "+"
    print(border)

    for r, row in enumerate(board):
        cells = "|".join(cell_str(x) for x in row)
        print(f"{r:2} |{cells}|")
        print(border)

    print()


def compute_adjacent(logic_mined_board: np.ndarray) -> np.ndarray:
    ext_num_sheet = np.zeros([row_num + 2, col_num + 2])

    for r in range(1, row_num + 1):
        for c in range(1, col_num + 1):
            if logic_mined_board[r, c] == 1:
                ext_num_sheet[r, c] = -1
            else:
                section = logic_mined_board[r - 1 : r + 2, c - 1 : c + 2]
                ext_num_sheet[r, c] = np.sum(section)

    return ext_num_sheet[1 : row_num + 1, 1 : col_num + 1]


def open_grid(
    r: int,
    c: int,
    num_sheet: np.ndarray,
    view_board: List[List[Union[str, int]]],
) -> Union[str, List[List[Union[str, int]]]]:

    rows, cols = num_sheet.shape

    if num_sheet[r, c] == -1:
        return "GAME OVER!!!!!!! \n Boooooom!!!!!! \n\n"

    if view_board[r][c] == FLAG:
        return f"Falgged, unable to open \n {view_board}"

    if num_sheet[r, c] != 0:
        view_board[r][c] = int(num_sheet[r, c])
        return view_board

    queue: List[Tuple[int, int]] = [(r, c)]
    visited: Set[Tuple[int, int]] = set()

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    while queue:
        cr, cc = queue.pop(0)

        if (cr, cc) in visited:
            continue
        visited.add((cr, cc))

        if num_sheet[cr, cc] == -1:
            continue

        view_board[cr][cc] = int(num_sheet[cr, cc])

        if num_sheet[cr, cc] != 0:
            continue

        for dr, dc in directions:
            nr, nc = cr + dr, cc + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if view_board[nr][nc] != HIDDEN and view_board[nr][nc] != FLAG:
                continue
            queue.append((nr, nc))

    return view_board


def flag_grid(
    r: int,
    c: int,
    num_sheet: np.ndarray,
    view_board: List[List[Union[str, int]]],
) -> Union[str, List[List[Union[str, int]]]]:
    if type(view_board[r][c]) == int:
        return "Unable to Flag"
    else:
        view_board[r][c] = FLAG if view_board[r][c] == HIDDEN else HIDDEN
        return view_board


def win_board(num_sheet: np.ndarray) -> List[List[Union[str, int]]]:
    rows, cols = num_sheet.shape
    win_condition = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            if num_sheet[r, c] == -1:
                win_condition[r][c] = FLAG
            else:
                win_condition[r][c] = int(num_sheet[r, c])

    return win_condition


def main() -> None:
    global num_mines, row_num, col_num

    # --- Ask game settings ---
    while True:
        row_num = ask_int("Enter number of rows", 9)
        col_num = ask_int("Enter number of cols", 9)

        if row_num <= 0 or col_num <= 0:
            print("Rows and cols must be positive.")
            continue

        max_mines = row_num * col_num - 1
        default_mines = 5 if max_mines >= 5 else max_mines
        num_mines = ask_int(f"Enter number of mines (1 ~ {max_mines})", default_mines)

        if num_mines <= 0:
            print("Number of mines must be positive.")
            continue
        if num_mines >= row_num * col_num:
            print("Too many mines: must be less than rows*cols.")
            continue

        break

    ext_empty_board = np.zeros([row_num + 2, col_num + 2])
    logic_mined_board = insert_mines(ext_empty_board, num_mines)
    view_board = [[HIDDEN for _ in range(col_num)] for _ in range(row_num)]
    num_sheet = compute_adjacent(logic_mined_board)
    win_condition = win_board(num_sheet)

    cmd_dict = {
        "o": open_grid,
        "f": flag_grid,
        "quit": "quit",
    }

    win = False
    while not win:
        print_help()
        display(view_board)

        user_input = input("Please input in the format: command row column: ").strip().lower()
        print()

        if user_input == "quit":
            print("Game exited... \n")
            break

        parts = user_input.split()
        if len(parts) != 3:
            print("Invalid input, format: command row column")
            continue

        cmd = parts[0]
        try:
            r = int(parts[1])
            c = int(parts[2])
        except ValueError:
            print("Row and column must be integers.")
            continue

        # bounds check (important)
        if not (0 <= r < row_num and 0 <= c < col_num):
            print(f"Row must be 0~{row_num-1}, col must be 0~{col_num-1}.")
            continue

        operation = cmd_dict.get(cmd)
        if operation is None:
            print("Unknown command")
            continue

        output = operation(r, c, num_sheet, view_board)
        if isinstance(output, str):
            print(output)
            break
        else:
            view_board = output

        if view_board == win_condition:
            print("You won!!!!!!!!!!!!!!! \n")
            win = True


if __name__ == "__main__":
    main()
