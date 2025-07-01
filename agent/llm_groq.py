import os
from openai import OpenAI
from llm_prompt import build_prompt
import re
os.environ["GROQ_API_KEY"] = "gsk_..."
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

def llm_groq_strategy(board_text: str):
    prompt = build_prompt(board_text)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a smart Minesweeper agent. Think out loud, then give an action."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=1024
    )

    reply = response.choices[0].message.content.strip()

    match = re.search(r"current action:\s*(reveal|flag|unflag)\s+(\d+)\s+(\d+)", reply.lower())
    if not match:
        return ("terminate", None, None)
    return match.group(1), int(match.group(2)), int(match.group(3))
