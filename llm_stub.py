import random

def llm_stub_strategy(board_str: str):
    lines = board_str.strip().split("\n")
    candidates = [
        (x, y)
        for y, row in enumerate(lines)
        for x, ch in enumerate(row)
        if ch == "."
    ]
    if not candidates:
        return ("terminate", None, None)

    x, y = random.choice(candidates)
    return ("reveal", x, y)
