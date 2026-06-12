import requests
import json
from typing import Optional, Dict, Any
from agent.config_loader import ConfigLoader


class AIClient:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.ai_config = config.get_ai_config()
        self.provider = self.ai_config.get("provider", "deepseek").lower()
        self.model = self.ai_config.get("model", "deepseek-r1:7b")
        self.api_key = self.ai_config.get("api_key", "").strip()
        self.base_url = self.ai_config.get("base_url", "http://localhost:11434").strip()

        valid_providers = ["deepseek", "claude", "openai", "gemini", "groq"]
        if self.provider not in valid_providers:
            raise ValueError(
                f"Invalid AI provider: {self.provider}. "
                f"Must be one of: {', '.join(valid_providers)}"
            )

        if self.provider in ["claude", "openai", "gemini", "groq"] and not self.api_key:
            raise ValueError(
                f"API key required for {self.provider}. "
                f"Set ai_api_key in config.json"
            )

        print(f"[AI] Provider: {self.provider} | Model: {self.model}")

    def call(self, prompt: str, max_tokens: int = 4096) -> Optional[str]:
        try:
            if self.provider == "deepseek":
                return self._call_ollama(prompt, max_tokens)
            elif self.provider == "claude":
                return self._call_claude(prompt, max_tokens)
            elif self.provider == "openai":
                return self._call_openai(prompt, max_tokens)
            elif self.provider == "gemini":
                return self._call_gemini(prompt, max_tokens)
            elif self.provider == "groq":
                return self._call_groq(prompt, max_tokens)
        except Exception as e:
            print(f"[AI ERROR] {self.provider}: {e}")
            return None

    def _call_ollama(self, prompt: str, max_tokens: int) -> Optional[str]:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "num_ctx": 8192,
        }
        try:
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except requests.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}\n"
                "Make sure: ollama serve is running in another terminal"
            )

    def _call_claude(self, prompt: str, max_tokens: int) -> Optional[str]:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["content"][0]["text"].strip()

    def _call_openai(self, prompt: str, max_tokens: int) -> Optional[str]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    def _call_gemini(self, prompt: str, max_tokens: int) -> Optional[str]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.7,
            },
        }
        params = {"key": self.api_key}
        response = requests.post(
            url, headers=headers, json=payload, params=params, timeout=120
        )
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

    def _call_groq(self, prompt: str, max_tokens: int) -> Optional[str]:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    def generate_page_object(
        self, page_name: str, locators: Dict, framework: str
    ) -> str:
        prompt = f"""Generate a page object class for {page_name} in {framework}.

Use these locators (YAML):
{json.dumps(locators, indent=2)}

Requirements:
- Use POM pattern
- Methods for each action (e.g., login(), click_button())
- Read locators from {page_name}/locators.yaml
- Include error handling
- Add docstrings
- Production-ready code

Return ONLY the complete code, no explanations or markdown."""

        return self.call(prompt, max_tokens=4096) or ""

    def generate_test_from_steps(
        self, test_case: Dict, framework: str, page_objects: Dict
    ) -> str:
        steps_text = "\n".join([f"- {s}" for s in test_case.get("steps", [])])
        pages_available = ", ".join(page_objects.keys())

        prompt = f"""Generate a complete test case in {framework}.

Test ID: {test_case.get('test_id')}
Test Name: {test_case.get('test_name')}
Feature: {test_case.get('feature')}

Test Steps:
{steps_text}

Expected Result: {test_case.get('expected_result')}

Available Page Objects: {pages_available}

Requirements:
- Use POM (page objects provided)
- Add logging before each step
- Assert expected result
- Include screenshot on failure
- Add proper annotations (@Test for Java, def test_* for Python, etc)
- Handle waits and synchronization
- Production-ready code
- NO imports or file headers needed

Return ONLY the test method/function code, no extra text."""

        return self.call(prompt, max_tokens=4096) or ""
