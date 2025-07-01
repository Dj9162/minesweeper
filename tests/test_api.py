from game_structure.api import MinesweeperGameAPI


def test_api_initial_state():
    api = MinesweeperGameAPI(width=4, height=4, num_mines=2, seed=42)
    board = api.get_visible_board()
    assert isinstance(board, str)
    assert board.count('.') == 16


def test_api_valid_actions():
    api = MinesweeperGameAPI(3, 3, 1)
    actions = api.get_valid_actions()
    assert set(actions) == {"reveal", "flag", "unflag", "terminate"}


def test_api_reveal_action():
    api = MinesweeperGameAPI(4, 4, 2, seed=99)
    result = api.step("reveal", 1, 1)
    assert "board" in result
    assert "score" in result
    assert result["score"]["steps"] == 1
    assert result["score"]["safe_revealed"] >= 1


def test_api_flag_unflag():
    api = MinesweeperGameAPI(3, 3, 1)
    api.step("flag", 0, 0)
    board = api.get_visible_board()
    assert "F" in board

    api.step("unflag", 0, 0)
    board = api.get_visible_board()
    assert "F" not in board


def test_api_terminate():
    api = MinesweeperGameAPI(3, 3, 1)
    result = api.step("terminate")
    assert result["terminal"] is True
    assert result["score"]["terminated"] is True


def test_api_invalid_action_handling():
    api = MinesweeperGameAPI(3, 3, 1)
    result = api.step("explode", 0, 0)
    assert "error" in result
