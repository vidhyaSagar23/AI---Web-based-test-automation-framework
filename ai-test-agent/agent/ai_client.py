import requests
import json
from typing import Optional, Dict
from agent.config_loader import ConfigLoader


class AIClient:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.ai_config = config.get_ai_config()
        self.model = self.ai_config["model"]
        self.base_url = self.ai_config["base_url"]
        self.api_key = self.ai_config["api_key"]
        self.provider = self.ai_config["provider"]

    def call(self, prompt: str, max_tokens: int = 4096) -> Optional[str]:
        try:
            if "localhost" in self.base_url or self.provider == "deepseek":
                return self._call_ollama(prompt, max_tokens)
            else:
                return self._call_api(prompt, max_tokens)
        except Exception as e:
            print(f"[AI ERROR] {e}")
            return None

    def _call_ollama(self, prompt: str, max_tokens: int) -> Optional[str]:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "num_ctx": 8192,
        }
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        return response.json().get("response", "")

    def _call_api(self, prompt: str, max_tokens: int) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }
        response = requests.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def generate_page_object(self, page_name: str,
                           locators: Dict,
                           framework: str) -> str:
        prompt = f"""Generate a page object class for {page_name} in {framework}.

Use these locators (in YAML format):
{json.dumps(locators, indent=2)}

Requirements:
- Use POM pattern
- Methods for each action (e.g., login(), click_button())
- Read locators from {page_name}/locators.yaml
- Include error handling
- Add docstrings

Return ONLY the code, no explanations."""

        return self.call(prompt, max_tokens=4096) or ""

    def generate_test_from_steps(self, test_case: Dict,
                                framework: str,
                                page_objects: Dict) -> str:
        steps_text = "\n".join([f"- {s}" for s in test_case.get("steps", [])])

        prompt = f"""Generate a test case in {framework}.

Test Case: {test_case.get('test_name')}
Feature: {test_case.get('feature')}
Steps:
{steps_text}

Expected: {test_case.get('expected_result')}

Available Page Objects: {', '.join(page_objects.keys())}

Requirements:
- Use POM (page objects provided)
- Add logging before each step
- Assert expected result
- Include screenshot on failure
- Add @Test annotation
- Handle waits properly

Return ONLY the code."""

        return self.call(prompt, max_tokens=4096) or ""
