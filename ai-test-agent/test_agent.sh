#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     TESTING AI TEST AUTOMATION AGENT (Prompts 1-4.5)           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# TEST 1: Project Structure
echo "TEST 1: Project Structure"
echo "=========================="
echo ""

files=(
  "agent/__init__.py"
  "agent/agent.py"
  "agent/config_loader.py"
  "agent/ai_client.py"
  "agent/memory_manager.py"
  "agent/commands/__init__.py"
  "config/config.json"
  ".gitignore"
  "requirements.txt"
)

missing=0
for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ $file"
  else
    echo "✗ MISSING: $file"
    missing=$((missing+1))
  fi
done

if [ $missing -eq 0 ]; then
  echo ""
  echo "✅ TEST 1 PASSED: All files present"
  TEST1_PASS=true
else
  echo ""
  echo "❌ TEST 1 FAILED: $missing files missing"
  TEST1_PASS=false
fi

echo ""
echo "---"
echo ""

# TEST 2: Config Loader
echo "TEST 2: Config Loader"
echo "===================="
echo ""

python3 << 'PYEOF'
import sys

try:
    from agent.config_loader import ConfigLoader
    
    config = ConfigLoader("config/config.json")
    print("✓ Config file loaded")
    
    fw = config.get_framework_type()
    print(f"✓ Framework type: {fw}")
    
    db = config.get_database_type()
    print(f"✓ Database type: {db}")
    
    tf = config.get_test_framework()
    print(f"✓ Test framework: {tf}")
    
    ai = config.get_ai_config()
    print(f"✓ AI Provider: {ai['provider']}")
    print(f"✓ AI Model: {ai['model']}")
    
    if config.validate():
        print("✓ All required fields present")
    else:
        print("✗ Validation failed")
        sys.exit(1)
    
    exec = config.get_execution_config()
    print(f"✓ Parallel threads: {exec['threads']}")
    print(f"✓ Retry count: {exec['retry_count']}")
    
    print("")
    print("✅ TEST 2 PASSED: Config working correctly")
    
except Exception as e:
    print(f"")
    print(f"❌ TEST 2 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
  TEST2_PASS=true
else
  TEST2_PASS=false
fi

echo ""
echo "---"
echo ""

# TEST 3: Memory Manager
echo "TEST 3: Memory Manager"
echo "====================="
echo ""

python3 << 'PYEOF'
import sys
import json
from pathlib import Path

try:
    from agent.memory_manager import MemoryManager
    
    mem = MemoryManager()
    print("✓ Memory manager initialized")
    
    mem.register_page("LoginPage", "pages/login/LoginPage.java")
    print("✓ Registered page: LoginPage")
    
    test_locators = {
        "username_input": "//input[@id='username']",
        "password_input": "//input[@id='password']",
        "login_button": "//button[text()='Login']"
    }
    mem.register_locators("LoginPage", test_locators)
    print(f"✓ Registered {len(test_locators)} locators for LoginPage")
    
    mem.register_test("TC001", "test_valid_login", "tests/login/test_valid_login.java")
    mem.register_test("TC002", "test_invalid_login", "tests/login/test_invalid_login.java")
    print("✓ Registered test: TC001")
    print("✓ Registered test: TC002")
    
    mem.mark_test_processed("TC001")
    mem.mark_test_processed("TC002")
    print("✓ Marked tests as processed")
    
    mem.save()
    print("✓ Memory saved to disk")
    
    if Path(".agent_memory/memory.json").exists():
        print("✓ Memory file exists: .agent_memory/memory.json")
    
    mem2 = MemoryManager()
    
    if "LoginPage" in mem2.get_created_pages():
        print("✓ LoginPage persisted correctly")
    else:
        print("✗ LoginPage not found in reloaded memory")
        sys.exit(1)
    
    if "TC001" in mem2.get_created_tests():
        print("✓ TC001 persisted correctly")
    else:
        print("✗ TC001 not found in reloaded memory")
        sys.exit(1)
    
    print("")
    print("Memory contents:")
    print(f"  Pages created: {mem2.get_created_pages()}")
    print(f"  Tests created: {list(mem2.get_created_tests().keys())}")
    
    print("")
    print("✅ TEST 3 PASSED: Memory manager working correctly")
    
except Exception as e:
    print(f"")
    print(f"❌ TEST 3 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
  TEST3_PASS=true
else
  TEST3_PASS=false
fi

echo ""
echo "---"
echo ""

# TEST 4: AI Client Providers
echo "TEST 4: AI Client - Provider Initialization"
echo "==========================================="
echo ""

python3 << 'PYEOF'
import sys
import requests

try:
    from agent.config_loader import ConfigLoader
    from agent.ai_client import AIClient
    
    config = ConfigLoader()
    
    print("[1] Testing Ollama (free, local)...")
    config.config["ai_provider"] = "deepseek"
    config.config["ai_model"] = "deepseek-r1:7b"
    config.config["ai_base_url"] = "http://localhost:11434"
    config.config["ai_api_key"] = ""
    
    try:
        ai_ollama = AIClient(config)
        print("✓ Ollama provider initialized")
    except Exception as e:
        print(f"✗ Ollama init failed: {e}")
        sys.exit(1)
    
    print("")
    print("[2] Testing Claude (paid)...")
    config.config["ai_provider"] = "claude"
    config.config["ai_model"] = "claude-opus-4-6"
    config.config["ai_api_key"] = "sk-ant-test-key"
    
    try:
        ai_claude = AIClient(config)
        print("✓ Claude provider initialized")
    except Exception as e:
        print(f"✗ Claude init failed: {e}")
        sys.exit(1)
    
    print("")
    print("[3] Testing OpenAI (paid)...")
    config.config["ai_provider"] = "openai"
    config.config["ai_model"] = "gpt-4o"
    config.config["ai_api_key"] = "sk-test-key"
    
    try:
        ai_openai = AIClient(config)
        print("✓ OpenAI provider initialized")
    except Exception as e:
        print(f"✗ OpenAI init failed: {e}")
        sys.exit(1)
    
    print("")
    print("[4] Testing Gemini (paid)...")
    config.config["ai_provider"] = "gemini"
    config.config["ai_model"] = "gemini-2.0-flash"
    config.config["ai_api_key"] = "AIza-test-key"
    
    try:
        ai_gemini = AIClient(config)
        print("✓ Gemini provider initialized")
    except Exception as e:
        print(f"✗ Gemini init failed: {e}")
        sys.exit(1)
    
    print("")
    print("[5] Testing Groq (paid/free)...")
    config.config["ai_provider"] = "groq"
    config.config["ai_model"] = "llama-3.3-70b-versatile"
    config.config["ai_api_key"] = "gsk-test-key"
    
    try:
        ai_groq = AIClient(config)
        print("✓ Groq provider initialized")
    except Exception as e:
        print(f"✗ Groq init failed: {e}")
        sys.exit(1)
    
    print("")
    print("[6] Checking Ollama server connectivity...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Ollama server is running")
            models = response.json().get("models", [])
            if models:
                model_names = [m['name'] for m in models]
                print(f"  Available models: {model_names}")
                if any('deepseek-r1:7b' in m for m in model_names):
                    print("  ✓ deepseek-r1:7b is available")
                else:
                    print("  ⚠ deepseek-r1:7b not found")
            else:
                print("  ⚠ No models found in Ollama")
        else:
            print(f"⚠ Ollama returned status {response.status_code}")
    except requests.ConnectionError:
        print("⚠ Ollama server not running at http://localhost:11434")
        print("  (This is OK for now - start with: ollama serve)")
    
    print("")
    print("✅ TEST 4 PASSED: All AI providers initialized correctly")
    
except Exception as e:
    print(f"")
    print(f"❌ TEST 4 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
  TEST4_PASS=true
else
  TEST4_PASS=false
fi

echo ""
echo "---"
echo ""

# TEST 5: Integration Test
echo "TEST 5: Full Integration Test"
echo "============================"
echo ""

python3 << 'PYEOF'
import sys

try:
    print("[1] Loading ConfigLoader...")
    from agent.config_loader import ConfigLoader
    config = ConfigLoader()
    print("✓ ConfigLoader loaded")
    
    print("")
    print("[2] Loading MemoryManager...")
    from agent.memory_manager import MemoryManager
    mem = MemoryManager()
    print("✓ MemoryManager loaded")
    
    print("")
    print("[3] Loading AIClient...")
    from agent.ai_client import AIClient
    ai = AIClient(config)
    print("✓ AIClient loaded")
    
    print("")
    print("[4] Simulating workflow...")
    
    print("  - Scaffold: Create framework structure (simulated)")
    mem.register_page("HomePage", "pages/home/HomePage.java")
    print("  ✓ HomePage registered")
    
    print("  - Generate: Read Excel and create tests (simulated)")
    mem.register_test("TC001", "test_home_loaded", "tests/home/test_home_loaded.java")
    print("  ✓ TC001 registered")
    
    print("  - Save memory")
    mem.save()
    print("  ✓ Memory saved")
    
    print("  - Reload and verify")
    mem_check = MemoryManager()
    if "HomePage" in mem_check.get_created_pages() and "TC001" in mem_check.get_created_tests():
        print("  ✓ Workflow state persisted")
    else:
        print("  ✗ Workflow state not persisted")
        sys.exit(1)
    
    print("")
    print("✅ TEST 5 PASSED: Full integration working correctly")
    print("")
    print("Summary:")
    print(f"  - Pages tracked: {mem_check.get_created_pages()}")
    print(f"  - Tests tracked: {list(mem_check.get_created_tests().keys())}")
    print(f"  - AI Provider: {config.get_ai_config()['provider']}")
    print(f"  - Framework: {config.get_framework_type()}")
    
except Exception as e:
    print(f"")
    print(f"❌ TEST 5 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
  TEST5_PASS=true
else
  TEST5_PASS=false
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   TEST SUMMARY                                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

if [ "$TEST1_PASS" = true ]; then
  echo "✅ TEST 1 PASSED: Project Structure"
else
  echo "❌ TEST 1 FAILED: Project Structure"
fi

if [ "$TEST2_PASS" = true ]; then
  echo "✅ TEST 2 PASSED: Config Loading"
else
  echo "❌ TEST 2 FAILED: Config Loading"
fi

if [ "$TEST3_PASS" = true ]; then
  echo "✅ TEST 3 PASSED: Memory Manager"
else
  echo "❌ TEST 3 FAILED: Memory Manager"
fi

if [ "$TEST4_PASS" = true ]; then
  echo "✅ TEST 4 PASSED: AI Client Providers"
else
  echo "❌ TEST 4 FAILED: AI Client Providers"
fi

if [ "$TEST5_PASS" = true ]; then
  echo "✅ TEST 5 PASSED: Integration Test"
else
  echo "❌ TEST 5 FAILED: Integration Test"
fi

echo ""

if [ "$TEST1_PASS" = true ] && [ "$TEST2_PASS" = true ] && [ "$TEST3_PASS" = true ] && [ "$TEST4_PASS" = true ] && [ "$TEST5_PASS" = true ]; then
  echo "╔════════════════════════════════════════════════════════════════╗"
  echo "║        🎉 ALL TESTS PASSED - READY FOR PROMPT SET 5! 🎉       ║"
  echo "╚════════════════════════════════════════════════════════════════╝"
  exit 0
else
  echo "❌ Some tests failed. Review errors above."
  exit 1
fi
