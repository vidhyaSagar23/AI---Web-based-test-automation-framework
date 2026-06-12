import yaml
from pathlib import Path
from agent.config_loader import ConfigLoader
from agent.memory_manager import MemoryManager


class HarvestLocatorsCommand:
    def __init__(self, config: ConfigLoader, memory: MemoryManager):
        self.config = config
        self.memory = memory
        self.output_dir = Path(config.get("output_dir", "framework_output"))
        self.driver = None

    def execute(self, url: str, page_name: str = None) -> bool:
        try:
            print(f"\n[HARVEST] Opening: {url}\n")

            if not page_name:
                page_name = url.split("/")[-1] or "HomePage"

            print(f"Page Name: {page_name}")
            print("Instructions:")
            print("  1. Browser will open to the URL")
            print("  2. Inspect elements using DevTools (F12)")
            print("  3. When done, close the browser")
            print("  4. Locators will be saved to locators.yaml")
            print("")

            print("[1/2] Opening browser...")
            self._open_browser(url)

            print(f"\n[2/2] Waiting for manual locator collection...")
            print("(Close the browser when done)")

            while True:
                try:
                    self.driver.current_url
                except:
                    break

            print("✓ Browser closed")

            locators_data = {
                "# Format": "element_name:",
                "# ": "  xpath: //xpath/here",
                "# ": "  id: element_id",
            }

            page_folder = self.output_dir / "pages" / page_name.lower()
            page_folder.mkdir(parents=True, exist_ok=True)
            locators_file = page_folder / "locators.yaml"

            with open(locators_file, "w") as f:
                yaml.dump(locators_data, f)

            print(f"✓ Locators template saved: {locators_file}")
            print("\n" + "=" * 60)
            print("✅ HARVEST COMPLETE")
            print("=" * 60)
            print(f"\nNext: Edit {locators_file} and add your locators")
            print("\n" + "=" * 60 + "\n")

            return True

        except Exception as e:
            print(f"❌ Harvest failed: {e}")
            return False

    def _open_browser(self, url: str):
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        print(f"✓ Browser opened: {url}")
