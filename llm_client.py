from __future__ import annotations
import json
import os
from typing import Any, Dict

import httpx
from openai import OpenAI

from prompt import SYSTEM_PROMPT, build_user_prompt
from persona_schema import PersonaBundle


class LLMClient:
    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
        if self.provider not in {"openai", "huggingface"}:
            raise ValueError("LLM_PROVIDER debe ser 'openai' o 'huggingface'")

        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.hf_model = os.getenv("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct")

        self._openai = None
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("Falta OPENAI_API_KEY")
            self._openai = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

        if self.provider == "huggingface":
            if not os.getenv("HF_API_TOKEN"):
                raise ValueError("Falta HF_API_TOKEN")

    def generate_personas(self, product_description: str, target_market: str, num_personas: int) -> PersonaBundle:
        user_prompt = build_user_prompt(product_description, target_market, num_personas)
        if self.provider == "openai":
            return self._generate_openai(user_prompt)
        return self._generate_hf(user_prompt)

    def _generate_openai(self, user_prompt: str) -> PersonaBundle:
        assert self._openai is not None
        result = self._openai.chat.completions.create(
            model=self.openai_model,
            messages=([
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]),
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        text = result.choices[0].message.content or "{}"
        data = json.loads(text)
        return PersonaBundle.model_validate(data)

    def _generate_hf(self, user_prompt: str) -> PersonaBundle:
        # Simple call to HF text generation inference API
        token = os.getenv("HF_API_TOKEN")
        model = self.hf_model
        headers = {"Authorization": f"Bearer {token}"}
        # Many instruct models respect system prefixes; we prepend system guidance
        prompt = f"[SYSTEM]\n{SYSTEM_PROMPT}\n[USER]\n{user_prompt}\n[ASSISTANT]"
        payload: Dict[str, Any] = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1200,
                "temperature": 0.7,
                "return_full_text": False,
            },
            "options": {"use_cache": True},
        }
        url = f"https://api-inference.huggingface.co/models/{model}"
        with httpx.Client(timeout=60) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            outputs = resp.json()
            if isinstance(outputs, list) and outputs and "generated_text" in outputs[0]:
                text = outputs[0]["generated_text"]
            else:
                text = json.dumps(outputs)
        data = json.loads(text)
        return PersonaBundle.model_validate(data)

