import numpy as np
import minesweeper as ms


def setup_module():
    # Make tests stable (your functions use global row_num/col_num)
    ms.row_num = 9
    ms.col_num = 9


def test_compute_adjacent_mine_and_numbers():
    # extended board because your compute_adjacent expects padding
    logic = np.zeros((ms.row_num + 2, ms.col_num + 2))
    logic[1, 1] = 1  # mine at top-left cell in real board

    num_sheet = ms.compute_adjacent(logic)

    # mine becomes -1
    assert num_sheet[0, 0] == -1

    # adjacent cells should see 1 mine
    assert num_sheet[0, 1] == 1
    assert num_sheet[1, 0] == 1
    assert num_sheet[1, 1] == 1


def test_flag_grid_toggle():
    num_sheet = np.zeros((ms.row_num, ms.col_num))
    view_board = [[ms.HIDDEN for _ in range(ms.col_num)] for _ in range(ms.row_num)]

    out = ms.flag_grid(2, 3, num_sheet, view_board)
    assert out[2][3] == ms.FLAG

    out = ms.flag_grid(2, 3, num_sheet, view_board)
    assert out[2][3] == ms.HIDDEN


def test_open_grid_reveal_number_cell():
    num_sheet = np.zeros((ms.row_num, ms.col_num))
    num_sheet[4, 4] = 2
    view_board = [[ms.HIDDEN for _ in range(ms.col_num)] for _ in range(ms.row_num)]

    out = ms.open_grid(4, 4, num_sheet, view_board)
    assert out[4][4] == 2


def test_open_grid_game_over_on_mine():
    num_sheet = np.zeros((ms.row_num, ms.col_num))
    num_sheet[0, 0] = -1
    view_board = [[ms.HIDDEN for _ in range(ms.col_num)] for _ in range(ms.row_num)]

    out = ms.open_grid(0, 0, num_sheet, view_board)
    assert isinstance(out, str)
    assert "GAME OVER" in out


def test_open_grid_zero_expands_some_cells():
    num_sheet = np.zeros((ms.row_num, ms.col_num))  # all zeros
    view_board = [[ms.HIDDEN for _ in range(ms.col_num)] for _ in range(ms.row_num)]

    out = ms.open_grid(0, 0, num_sheet, view_board)

    revealed = sum(
        1 for r in range(ms.row_num) for c in range(ms.col_num)
        if out[r][c] != ms.HIDDEN
    )
    assert revealed > 1
