import openai
import os
import re
import json
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

class LLMClient:
    def __init__(self, model="mistralai/mixtral-8x7b-instruct"):
        self.model = model

    def query(self, prompt: str, temperature=0.4, max_tokens=800) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            st.error(f"API Error: {e}")
            return None
