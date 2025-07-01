from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re
from agent.llm_prompt import build_prompt

class LocalLLM:
    def __init__(self, model_name="microsoft/Phi-3-mini-4k-instruct", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=50,
            do_sample=False,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt, "").strip()

def llm_transformers_strategy(board_text: str, llm: LocalLLM):
    prompt = build_prompt(board_text)
    reply = llm.generate(prompt)
    return parse_llm_response(reply)

def parse_llm_response(text: str):
    match = re.match(r"(reveal|flag|unflag|terminate)\s+(\d+)?\s*(\d+)?", text.strip().lower())
    if not match:
        return ("terminate", None, None)
    action = match.group(1)
    x = int(match.group(2)) if match.group(2) else None
    y = int(match.group(3)) if match.group(3) else None
    return (action, x, y)
