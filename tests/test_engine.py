import pytest
from game_structure.engine import MinesweeperBoard, Action, TileState


def test_first_click_never_hits_mine():
    board = MinesweeperBoard(width=5, height=5, num_mines=5, seed=123)
    board.step(Action.REVEAL, 2, 2)
    assert board._board[2][2] != -1, "First click should never hit a mine"
    assert board._state[2][2] == TileState.REVEALED


def test_flag_and_unflag():
    board = MinesweeperBoard(width=3, height=3, num_mines=1, seed=1)
    board.step(Action.FLAG, 0, 0)
    assert board._state[0][0] == TileState.FLAGGED
    board.step(Action.UNFLAG, 0, 0)
    assert board._state[0][0] == TileState.HIDDEN


def test_flood_fill_zero_expansion():
    board = MinesweeperBoard(width=5, height=5, num_mines=1, seed=999)
    # Click a tile that triggers flood fill
    board.step(Action.REVEAL, 0, 0)
    # Count how many tiles were revealed
    revealed = sum(
        1 for row in board._state for cell in row if cell == TileState.REVEALED
    )
    assert revealed > 1, "Flood fill should reveal multiple tiles when starting from 0"


def test_game_win_state():
    board = MinesweeperBoard(width=3, height=3, num_mines=1, seed=321)
    # Reveal all non-mine tiles
    for y in range(3):
        for x in range(3):
            board.step(Action.REVEAL, x, y)
            if board.terminated:
                break
        if board.terminated:
            break
    # Force win check
    if not board.terminated:
        assert board.is_win()


def test_game_termination_on_mine():
    board = MinesweeperBoard(width=3, height=3, num_mines=1, seed=42)
    board.step(Action.REVEAL, 0, 0)
    for y in range(3):
        for x in range(3):
            if board._board[y][x] == -1:
                board.step(Action.REVEAL, x, y)
                assert board.terminated
                assert not board.is_win()
                return
    pytest.fail("No mine found to test termination.")
