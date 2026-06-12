#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.config_loader import ConfigLoader
from agent.memory_manager import MemoryManager
from agent.ai_client import AIClient
from agent.commands.scaffold import ScaffoldCommand
from agent.commands.generate_tests import GenerateTestsCommand
from agent.commands.update_tests import UpdateTestsCommand
from agent.commands.harvest_locators import HarvestLocatorsCommand


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered UI Test Automation Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent/agent.py --action scaffold
  python agent/agent.py --action generate --excel testcases/my_tests.xlsx
  python agent/agent.py --action update --excel testcases/my_tests.xlsx --test-id TC001,TC002
  python agent/agent.py --action harvest --url https://example.com --page LoginPage
  python agent/agent.py --action clear-memory
        """,
    )

    parser.add_argument(
        "--action",
        required=True,
        choices=["scaffold", "generate", "update", "harvest", "run", "debug", "clear-memory"],
        help="Action to execute",
    )
    parser.add_argument("--excel", help="Path to Excel test case file")
    parser.add_argument("--url", help="URL to harvest locators from")
    parser.add_argument("--page", help="Page name for locator harvesting")
    parser.add_argument(
        "--test-id", help="Comma-separated test IDs to update (for --action update)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force regeneration even if files exist",
    )

    args = parser.parse_args()

    try:
        config = ConfigLoader()
        memory = MemoryManager()
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        sys.exit(1)

    if args.action == "scaffold":
        scaffold = ScaffoldCommand(config, memory)
        success = scaffold.execute()

    elif args.action == "generate":
        if not args.excel:
            print("❌ --excel argument required for generate action")
            sys.exit(1)
        try:
            ai = AIClient(config)
            gen = GenerateTestsCommand(config, memory, ai)
            success = gen.execute(args.excel, args.force)
        except Exception as e:
            print(f"❌ {e}")
            sys.exit(1)

    elif args.action == "update":
        if not args.excel:
            print("❌ --excel argument required for update action")
            sys.exit(1)
        try:
            ai = AIClient(config)
            update = UpdateTestsCommand(config, memory, ai)
            success = update.execute(args.excel, args.test_id, args.force)
        except Exception as e:
            print(f"❌ {e}")
            sys.exit(1)

    elif args.action == "harvest":
        if not args.url:
            print("❌ --url argument required for harvest action")
            sys.exit(1)
        harvest = HarvestLocatorsCommand(config, memory)
        success = harvest.execute(args.url, args.page)

    elif args.action == "clear-memory":
        memory.clear()
        print("✅ Memory cleared")
        success = True

    else:
        parser.print_help()
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
