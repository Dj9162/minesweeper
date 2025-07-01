from agent.llm_agent import LLMGameAgent
from game_structure.api import MinesweeperGameAPI
from agent.llm_transformers import LocalLLM, llm_transformers_strategy

llm = LocalLLM("microsoft/Phi-3-mini-4k-instruct")
api = MinesweeperGameAPI(5, 5, 3, seed=42)
agent = LLMGameAgent(api, lambda board: llm_transformers_strategy(board, llm))
result = agent.play_game()

print("\nFinal Score:", result["final_score"])
