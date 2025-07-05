# llm_client.py
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_API_TOKEN")

class LLMClient:
    def __init__(self, model="HuggingFaceH4/zephyr-7b-beta"):
        self.client = InferenceClient(model=model, token=HF_TOKEN)

    def query(self, prompt: str, temperature=0.4, max_tokens=800) -> str:
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {e}"
