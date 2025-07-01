from agent.llm_agent import LLMGameAgent
from game_structure.api import MinesweeperGameAPI
from agent.llm_groq import llm_groq_strategy

api = MinesweeperGameAPI(5, 5, 3, seed=12)
agent = LLMGameAgent(api, llm_groq_strategy)
result = agent.play_game()

print("\nFinal Score:", result["final_score"])
