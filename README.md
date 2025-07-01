# 🧠 Minesweeper + LLM Agent

This project implements a fully functional Minesweeper game environment and demonstrates how to control it with a large language model (LLM) using only the visible board state. The agent can run using local LLMs (e.g., Phi-3) or cloud-based models like Groq's `gemma2-9b-it`.

---

## 🚀 Quick Setup

```bash
git clone https://github.com/yourname/minesweeper-llm.git
cd minesweeper-llm
pip install -r requirements.txt
```

### 🔐 Groq API Key

If using Groq-hosted LLMs:

```bash
export GROQ_API_KEY=your-groq-api-key
```

---

## ▶️ Run the Agent

Play a single game using Groq (e.g., `gemma2-9b-it`):

```bash
python llm_groq_example.py
```

Play with a local model (e.g., `Phi-3`):

```bash
python llm_local_example.py
```

---

## 📊 Evaluation Harness (Phase 4)

You can evaluate LLM performance across difficulty levels:

```bash
python evaluation_beginner.py
python evaluation_intermediate.py
python evaluation_expert.py
```

Each will generate:
- `results_beginner.json`
- `results_intermediate.json`
- `results_expert.json`

Example:
```json
{
  "games_played": 30,
  "win_rate": 56.67,
  "avg_steps": 18.2,
  "avg_runtime_sec": 2.9
}
```

---

## ✅ Run Tests

```bash
pytest tests/
```

Test coverage includes:
- Game engine logic (reveal, flag, win/loss detection)
- API wrapper
- End-to-end LLM playthrough on a small board

---

## 🧱 Project Structure

| File                     | Purpose                                  |
|--------------------------|------------------------------------------|
| `engine.py`              | Pure Minesweeper game logic              |
| `api.py`                 | Game API interface                       |
| `llm_agent.py`           | Main agent loop                          |
| `llm_prompt.py`          | Prompt formatter for LLM input           |
| `llm_groq.py`            | Groq-hosted LLM strategy (OpenAI-compatible) |
| `llm_transformers.py`    | Local LLM support (Phi-3) via Transformers |
| `evaluation_*.py`        | Difficulty-specific evaluation scripts   |
| `tests/`                 | Unit and integration tests               |

---

## 🧠 Design Notes

### Architecture
- The engine handles Minesweeper game logic with reproducible seed-based generation.
- The agent operates in a loop, reading the visible board and choosing actions via LLM.
- Actions include: `reveal x y`, `flag x y`, `unflag x y`, and `terminate`.

### Prompt Strategy
LLMs are prompted with the current board and asked to think step-by-step before suggesting an action:
```
reveal 2 3
```

The response is parsed using regex and validated before applying.

---

## 🧠 LLM Options

| Model           | Source | Strength            |
|------------------|--------|---------------------|
| Phi-3            | Local  | Fast, compact       |
| Gemma2-9B (Groq) | Groq   | Good reasoning speed |
| LLaMA 3-70B      | Groq   | High reasoning power |

---

## 📁 Output Artifacts

| File                   | Description                            |
|------------------------|----------------------------------------|
| `results_beginner.json`     | Groq agent stats on 9x9 boards         |
| `results_intermediate.json` | Stats for 16x16 boards                |
| `results_expert.json`       | Stats for 30x16 boards with 99 mines  |
| `colab_notebook.ipynb`      | (Optional) Full demo in Google Colab  |

---

## 📌 Known Limitations

- LLM may hallucinate or misformat replies (fallbacks used)
- Win rate on high difficulty is low without RL/self-play
- Action parser relies on pattern-matching and can fail if format drifts

---

## 🎉 Deliverables Checklist

- ✅ Fully testable Minesweeper engine
- ✅ API exposing visible board and actions
- ✅ Groq/Local LLM agent that plays until win/loss
- ✅ Evaluation loop with win-rate summary
- ✅ README + tests + `.ipynb` for ease of use

---

## 📄 License

MIT © Dhanraj Kumar, 2025
