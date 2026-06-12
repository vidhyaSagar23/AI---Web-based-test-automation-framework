# AI-Powered UI Test Automation Agent

A distributable AI agent framework that auto-generates complete test frameworks (Playwright, Selenium) from Excel test cases.

## Quick Start

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Edit `config/config.json` with your settings

3. Scaffold a new framework:
   ```
   python agent/agent.py --action scaffold
   ```

4. Generate tests from Excel:
   ```
   python agent/agent.py --action generate --excel testcases/my_tests.xlsx
   ```

5. Run the test suite:
   ```
   python agent/agent.py --action run
   ```

## Commands

| Action | Description |
|--------|-------------|
| `scaffold` | Generate empty framework structure |
| `generate` | Create page objects + tests from Excel |
| `update` | Incrementally update changed tests |
| `harvest` | Extract locators from browser |
| `run` | Execute generated test suite |
| `clear-memory` | Reset agent memory |
