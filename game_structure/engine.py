import random
from enum import Enum, auto
from typing import List, Optional, Tuple


class TileState(Enum):
    HIDDEN = auto()
    REVEALED = auto()
    FLAGGED = auto()


class Action(Enum):
    REVEAL = "reveal"
    FLAG = "flag"
    UNFLAG = "unflag"
    TERMINATE = "terminate"


class MinesweeperBoard:
    def __init__(self, width: int, height: int, num_mines: int, seed: Optional[int] = None):
        assert 0 < num_mines < width * height, "Invalid mine count"
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.seed = seed
        self.first_click = True
        self.steps = 0
        self.terminated = False
        self._rng = random.Random(seed)

        # Internal state
        self._board: List[List[int]] = [[0] * width for _ in range(height)]  # -1 = mine
        self._state: List[List[TileState]] = [[TileState.HIDDEN] * width for _ in range(height)]

    def step(self, action: Action, x: Optional[int] = None, y: Optional[int] = None):
        if self.terminated:
            return

        self.steps += 1

        if action == Action.TERMINATE:
            self.terminated = True
            return

        if x is None or y is None or not (0 <= x < self.width and 0 <= y < self.height):
            return

        if action == Action.REVEAL:
            if self.first_click:
                self._place_mines(exclude_x=x, exclude_y=y)
                self.first_click = False

            if self._state[y][x] == TileState.HIDDEN:
                if self._board[y][x] == -1:
                    self._state[y][x] = TileState.REVEALED
                    self.terminated = True
                else:
                    self._flood_fill(x, y)

        elif action == Action.FLAG:
            if self._state[y][x] == TileState.HIDDEN:
                self._state[y][x] = TileState.FLAGGED

        elif action == Action.UNFLAG:
            if self._state[y][x] == TileState.FLAGGED:
                self._state[y][x] = TileState.HIDDEN

    def _place_mines(self, exclude_x: int, exclude_y: int):
        coords = [(x, y) for y in range(self.height) for x in range(self.width)
                  if not (x == exclude_x and y == exclude_y)]
        self._rng.shuffle(coords)
        for x, y in coords[:self.num_mines]:
            self._board[y][x] = -1
            for nx, ny in self._neighbors(x, y):
                if self._board[ny][nx] != -1:
                    self._board[ny][nx] += 1

    def _neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        result = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    result.append((nx, ny))
        return result

    def _flood_fill(self, x: int, y: int):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if self._state[cy][cx] != TileState.HIDDEN:
                continue
            self._state[cy][cx] = TileState.REVEALED
            if self._board[cy][cx] == 0:
                stack.extend([
                    (nx, ny) for nx, ny in self._neighbors(cx, cy)
                    if self._state[ny][nx] == TileState.HIDDEN
                ])

    def render(self) -> str:
        def cell_str(x, y):
            state = self._state[y][x]
            if state == TileState.HIDDEN:
                return ". "
            elif state == TileState.FLAGGED:
                return "F "
            elif self._board[y][x] == -1:
                return "* "
            elif self._board[y][x] == 0:
                return "0 "
            else:
                return str(self._board[y][x])+ " "
        return "\n".join("".join(cell_str(x, y) for x in range(self.width))
                         for y in range(self.height))

    def is_win(self) -> bool:
        for y in range(self.height):
            for x in range(self.width):
                if self._state[y][x] != TileState.REVEALED and self._board[y][x] != -1:
                    return False
        return not self.terminated

    def get_visible_state(self) -> List[List[str]]:
        state = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = self._state[y][x]
                if cell == TileState.HIDDEN:
                    row.append(".")
                elif cell == TileState.FLAGGED:
                    row.append("F")
                elif self._board[y][x] == -1:
                    row.append("*")
                elif self._board[y][x] == 0:
                    row.append(" ")
                else:
                    row.append(str(self._board[y][x]) + " ")
            state.append(row)
        return state

    def is_terminal(self) -> bool:
        return self.terminated or self.is_win()

    def get_score(self) -> dict:
        return {
            "win": self.is_win(),
            "terminated": self.terminated,
            "steps": self.steps,
            "safe_revealed": sum(
                1 for y in range(self.height) for x in range(self.width)
                if self._state[y][x] == TileState.REVEALED and self._board[y][x] != -1
            ),
        }