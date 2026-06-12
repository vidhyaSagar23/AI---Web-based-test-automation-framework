import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set


class MemoryManager:
    def __init__(self, memory_file: str = ".agent_memory/memory.json"):
        self.memory_file = Path(memory_file)
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self.memory = self._load_memory()

    def _load_memory(self) -> Dict:
        if self.memory_file.exists():
            with open(self.memory_file) as f:
                return json.load(f)
        return {
            "pages_created": {},
            "tests_created": {},
            "locators_by_page": {},
            "test_cases_processed": [],
            "last_run": None,
        }

    def save(self):
        self.memory["last_run"] = datetime.now().isoformat()
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=2)

    def page_exists(self, page_name: str) -> bool:
        return page_name in self.memory["pages_created"]

    def register_page(self, page_name: str, file_path: str):
        self.memory["pages_created"][page_name] = {
            "path": file_path,
            "created_at": datetime.now().isoformat(),
        }

    def register_test(self, test_id: str, test_name: str, file_path: str):
        self.memory["tests_created"][test_id] = {
            "name": test_name,
            "path": file_path,
            "created_at": datetime.now().isoformat(),
        }

    def register_locators(self, page_name: str, locators: Dict):
        self.memory["locators_by_page"][page_name] = {
            "count": len(locators),
            "elements": list(locators.keys()),
            "updated_at": datetime.now().isoformat(),
        }

    def mark_test_processed(self, test_id: str):
        if test_id not in self.memory["test_cases_processed"]:
            self.memory["test_cases_processed"].append(test_id)

    def get_created_pages(self) -> Set[str]:
        return set(self.memory["pages_created"].keys())

    def get_created_tests(self) -> Dict:
        return self.memory["tests_created"]

    def clear(self):
        self.memory = {
            "pages_created": {},
            "tests_created": {},
            "locators_by_page": {},
            "test_cases_processed": [],
            "last_run": None,
        }
        self.save()
        print("[MEMORY] Cleared all tracked artifacts")
