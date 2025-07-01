from game_structure.api import MinesweeperGameAPI


class LLMGameAgent:
    def __init__(self, api: MinesweeperGameAPI, llm_fn, verbose: bool = True):
        self.api = api
        self.llm_fn = llm_fn
        self.verbose = verbose
        self.steps = []

    def play_game(self) -> dict:
        while not self.api.is_terminal():
            board_text = self.api.get_visible_board()
            action, x, y = self.llm_fn(board_text)

            if self.verbose:
                print(f"\nLLM chose: {action} ({x}, {y})")

            result = self.api.step(action, x, y)
            self.steps.append((action, x, y))

            if self.verbose:
                print(result["board"])

        return {
            "final_score": self.api.get_score(),
            "steps_taken": len(self.steps),
            "steps": self.steps,
        }
