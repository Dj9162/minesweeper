from game_structure.api import MinesweeperGameAPI
from agent.llm_agent import LLMGameAgent
from llm_stub import llm_stub_strategy

api = MinesweeperGameAPI(5, 5, 3, seed=42)
agent = LLMGameAgent(api, llm_stub_strategy)
result = agent.play_game()

print("\nFinal Result:")
print(result)
