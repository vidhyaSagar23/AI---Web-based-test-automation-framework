import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


class ConfigLoader:
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        with open(self.config_path) as f:
            return json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    def get_framework_type(self) -> str:
        fw = self.get("framework", "playwright")
        lang = self.get("language", "typescript")
        return f"{fw}-{lang}"

    def get_test_framework(self) -> str:
        return self.get("test_framework", "playwright")

    def get_database_type(self) -> str:
        return self.get("database", "mssql")

    def get_ai_config(self) -> Dict[str, str]:
        return {
            "provider": self.get("ai_provider", "deepseek"),
            "model": self.get("ai_model", "deepseek-r1:7b"),
            "api_key": self.get("ai_api_key"),
            "base_url": self.get("ai_base_url", "http://localhost:11434"),
        }

    def get_execution_config(self) -> Dict[str, Any]:
        return {
            "parallel": self.get("parallel_execution", True),
            "threads": self.get("parallel_threads", 4),
            "retry_count": self.get("retry_count", 2),
            "retry_on_failure": self.get("retry_on_failure", True),
        }

    def validate(self) -> bool:
        """Validate required fields exist"""
        required = ["framework", "language", "database"]
        for field in required:
            if not self.get(field):
                print(f"ERROR: Missing required config: {field}")
                return False
    
         # API key is only required for paid providers
        provider = self.get("ai_provider", "deepseek")
        if provider in ["claude", "openai", "gemini", "groq"]:
            if not self.get("ai_api_key"):
                print(f"ERROR: API key required for {provider}")
                return False
    
    # Ollama (deepseek) doesn't need an API key
        if provider == "deepseek":
            if not self.get("ai_base_url"):
                print(f"ERROR: Missing ai_base_url for Ollama")
                return False
    
        return True