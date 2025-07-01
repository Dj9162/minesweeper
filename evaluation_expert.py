import time, json
from game_structure.api import MinesweeperGameAPI
from agent.llm_agent import LLMGameAgent
from agent.llm_groq import llm_groq_strategy

def run_games(num_games=30, seed_base=3000):
    width, height, mines = 30, 16, 99
    results = []

    print(f"\nRunning {num_games} EXPERT games")

    for i in range(num_games):
        seed = seed_base + i
        api = MinesweeperGameAPI(width, height, mines, seed=seed)
        agent = LLMGameAgent(api, llm_groq_strategy, verbose=False)

        start = time.time()
        result = agent.play_game()
        end = time.time()

        score = result["final_score"]
        results.append({
            "win": score["win"],
            "steps": score["steps"],
            "safe_revealed": score["safe_revealed"],
            "duration": end - start
        })

    return results

def summarize(results):
    win_rate = sum(1 for r in results if r["win"]) / len(results)
    avg_steps = sum(r["steps"] for r in results) / len(results)
    avg_time = sum(r["duration"] for r in results) / len(results)
    return {
        "games_played": len(results),
        "win_rate": round(win_rate * 100, 2),
        "avg_steps": round(avg_steps, 2),
        "avg_runtime_sec": round(avg_time, 2)
    }

def main():
    results = run_games()
    summary = summarize(results)
    print("\nIntermediate Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    with open("results_expert.json", "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()
