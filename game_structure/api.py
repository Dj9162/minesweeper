from engine import MinesweeperBoard, Action
from typing import Optional, List


class MinesweeperGameAPI:

    def __init__(self, width: int, height: int, num_mines: int, seed: Optional[int] = None):
        """
        Initialize the game.

        :param width: Board width
        :param height: Board height
        :param num_mines: Number of mines
        :param seed: Random seed for reproducibility
        """
        self.board = MinesweeperBoard(width, height, num_mines, seed)

    def get_visible_board(self) -> str:
        """
        Returns a string rendering of the visible board.
        """
        return self.board.render()

    def get_valid_actions(self) -> List[str]:
        """
        Returns the list of valid actions.
        """
        return [action.value for action in Action]

    def step(self, action: str, x: Optional[int] = None, y: Optional[int] = None) -> dict:
        """
        Applies an action and returns the result.

        :param action: One of "reveal", "flag", "unflag", "terminate"
        :param x: X coordinate (if applicable)
        :param y: Y coordinate (if applicable)
        :return: dict with terminal status, score, and board
        """
        try:
            act = Action(action.lower())
        except ValueError:
            return {"error": f"Invalid action: {action}"}

        self.board.step(act, x, y)
        return {
            "board": self.get_visible_board(),
            "terminal": self.board.is_terminal(),
            "score": self.board.get_score()
        }

    def is_terminal(self) -> bool:
        return self.board.is_terminal()

    def get_score(self) -> dict:
        return self.board.get_score()