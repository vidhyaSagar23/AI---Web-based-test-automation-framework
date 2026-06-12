import os
from pathlib import Path
from datetime import datetime
from openpyxl import load_workbook
from agent.config_loader import ConfigLoader
from agent.memory_manager import MemoryManager
from agent.ai_client import AIClient
from agent.commands.generate_tests import GenerateTestsCommand


class UpdateTestsCommand(GenerateTestsCommand):
    def execute(self, excel_path: str, test_ids: str = None, force: bool = False) -> bool:
        try:
            excel_file = Path(excel_path)
            if not excel_file.exists():
                print(f"❌ Excel file not found: {excel_path}")
                return False

            print(f"\n[UPDATE] Processing: {excel_path}")

            excel_mtime = os.path.getmtime(excel_file)
            excel_modified = datetime.fromtimestamp(excel_mtime)

            print(f"Excel file modified: {excel_modified.strftime('%Y-%m-%d %H:%M:%S')}\n")

            print("[1/3] Reading test cases...")
            if not self._read_excel(excel_file):
                return False

            if test_ids:
                specified_ids = [t.strip() for t in test_ids.split(",")]
                self.test_cases = [
                    tc for tc in self.test_cases
                    if tc.get("testcaseid") in specified_ids
                ]
                print(f"  ✓ Filtering {len(self.test_cases)} specified test cases")

            print("[2/3] Updating test cases...")
            self._group_by_page()
            self._generate_page_objects(force=True)
            self._generate_tests()

            print("[3/3] Saving state...")
            self.memory.save()

            self._print_update_summary()
            return True

        except Exception as e:
            print(f"❌ Update failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _print_update_summary(self):
        print(f"\n{'='*60}")
        print(f"✅ UPDATE COMPLETE")
        print(f"{'='*60}")
        print(f"\nUpdated Pages: {len(self.pages_needed)}")
        print(f"Updated Tests: {len(self.test_cases)}")
        print(f"\nRun tests: python agent/agent.py --action run")
        print(f"\n{'='*60}\n")
