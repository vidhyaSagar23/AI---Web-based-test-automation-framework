# AI-Powered UI Test Automation Agent

An intelligent test automation framework that generates complete test
suites from Excel test cases using AI and browser locator harvesting.

## Features

✅ **Multi-Framework Support**
- Playwright (TypeScript, JavaScript, Python)
- Selenium (Java, Python, C#)

✅ **Multi-Provider AI**
- Local: DeepSeek (via Ollama) - FREE
- Cloud: Claude, ChatGPT, Gemini, Groq - PAID

✅ **Automatic Code Generation**
- Page objects from locators
- Test scripts from test cases
- Config files and utilities

✅ **Memory & Deduplication**
- Tracks created artifacts
- Prevents duplicate page objects
- Supports incremental updates

✅ **Full Test Utilities**
- Logging (console + file)
- Screenshots on failure
- Retry mechanism
- Parallel execution
- HTML/Allure reporting

## Installation

### Prerequisites
- Python 3.8+
- Ollama (for free AI, or use paid API key)

### Setup

1. **Download agent from Nexus** (or clone repository)
```bash
git clone <repo> ai-test-agent
cd ai-test-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up Ollama** (if using free DeepSeek)
```bash
# Install Ollama from https://ollama.ai
ollama pull deepseek-r1:7b
ollama serve  # Start in background terminal
```

4. **Configure the agent**
Edit `config/config.json`:

```json
{
  "framework": "playwright",
  "language": "typescript",
  "database": "mssql",
  "ai_provider": "deepseek",
  "ai_model": "deepseek-r1:7b",
  "ai_base_url": "http://localhost:11434",
  "ai_api_key": ""
}
```

## Configuration

### Framework & Language
```json
"framework": "playwright" or "selenium"
"language": "typescript", "javascript", "python", "java", "csharp"
```

### AI Provider

**FREE (Local)**
```json
"ai_provider": "deepseek",
"ai_model": "deepseek-r1:7b",
"ai_base_url": "http://localhost:11434",
"ai_api_key": ""
```

**PAID (Cloud)**
```json
"ai_provider": "claude",
"ai_model": "claude-opus-4-6",
"ai_api_key": "sk-ant-...",
"ai_base_url": "https://api.anthropic.com"
```

### Database
```json
"database": "mssql", "mysql", "postgres", "mongodb"
```

Edit `config/db-config.properties` with your credentials.

## Usage

### 1. Scaffold Framework
Generate empty framework structure:
```bash
python agent/agent.py --action scaffold
```

Output: Complete framework in `framework_output/` with configs, utils, and build files.

### 2. Create Excel Test Case File
Create `testcases/my_tests.xlsx`:

| TestCaseID | Feature | Page | Steps | ExpectedResult |
|------------|---------|------|-------|----------------|
| TC001 | Login | LoginPage | Enter username; Enter password; Click login | User lands on dashboard |
| TC002 | Login | LoginPage | Click login without credentials | Error message displays |

### 3. Generate Tests & Page Objects
```bash
python agent/agent.py --action generate --excel testcases/my_tests.xlsx
```

Output:
- `pages/loginpage/LoginPage.java`
- `pages/loginpage/locators.yaml`
- `tests/loginpage/test_tc001.java`
- `tests/loginpage/test_tc002.java`

### 4. Add Locators
Edit `pages/loginpage/locators.yaml`:
```yaml
username_input:
  id: "username"
  xpath: "//input[@id='username']"

password_input:
  id: "password"
  xpath: "//input[@id='password']"

login_button:
  xpath: "//button[contains(text(), 'Login')]"
```

### 5. Implement Page Objects
Edit `pages/loginpage/LoginPage.java`:
```java
public class LoginPage extends BasePage {
    public void enter_username(String username) {
        click(username_input);
        type_text(username_input, username);
    }

    public void enter_password(String password) {
        click(password_input);
        type_text(password_input, password);
    }

    public void click_login() {
        click(login_button);
    }
}
```

### 6. Implement Tests
Edit `tests/loginpage/test_tc001.java`:
```java
@Test
public void test_tc001_valid_login() {
    LoginPage login = new LoginPage(driver);
    login.enter_username("tomsmith");
    login.enter_password("SuperSecretPassword!");
    login.click_login();

    assertTrue(driver.getCurrentUrl().contains("dashboard"));
}
```

### 7. Update Tests (Incremental)
```bash
# Update only changed tests
python agent/agent.py --action update --excel testcases/my_tests.xlsx

# Update specific tests
python agent/agent.py --action update --excel testcases/my_tests.xlsx --test-id TC001,TC002
```

### 8. Run Tests
```bash
# Framework specific
cd framework_output
pytest  # Python
npm test  # JavaScript/TypeScript
mvn test  # Java
```

## Commands Reference

```bash
# Scaffold new framework
python agent/agent.py --action scaffold

# Generate tests from Excel
python agent/agent.py --action generate --excel testcases/my_tests.xlsx

# Update specific tests
python agent/agent.py --action update --excel testcases/my_tests.xlsx --test-id TC001

# Harvest locators from browser
python agent/agent.py --action harvest --url https://example.com --page LoginPage

# Clear memory (start fresh)
python agent/agent.py --action clear-memory

# Get help
python agent/agent.py --help
```

## Folder Structure

```
ai-test-agent/
├── agent/
│   ├── agent.py              <- Main CLI
│   ├── config_loader.py      <- Config management
│   ├── ai_client.py          <- AI provider wrapper
│   ├── memory_manager.py     <- State tracking
│   └── commands/
│       ├── scaffold.py       <- Framework generator
│       ├── generate_tests.py <- Test generator
│       ├── update_tests.py   <- Incremental update
│       └── harvest_locators.py <- Locator harvester
├── config/
│   ├── config.json           <- Main config (edit here)
│   ├── db-config.properties  <- Database config
│   └── framework_templates/  <- Language templates
├── testcases/                <- Drop Excel files here
├── framework_output/         <- Generated framework (do not commit)
└── README.md
```

## Supported Frameworks

### Playwright
- **TypeScript**: `npm test`
- **JavaScript**: `npm test`
- **Python**: `pytest`

### Selenium
- **Java**: `mvn test`
- **Python**: `pytest`
- **C#**: `dotnet test`

## AI Providers

| Provider | Cost | Speed | Best For |
|----------|------|-------|----------|
| DeepSeek (Ollama) | FREE | Fast | Local testing, dev teams |
| Claude | PAID | Very Fast | Complex test logic |
| ChatGPT | PAID | Fast | General automation |
| Gemini | PAID | Fast | Google ecosystem |
| Groq | FREE/PAID | Fastest | Performance testing |

## Troubleshooting

### Ollama not connecting
```bash
# Make sure Ollama is running
ollama serve

# Check if model is available
curl http://localhost:11434/api/tags
```

### Excel file not found
```bash
# Ensure file exists in testcases/ folder
ls testcases/my_tests.xlsx

# Use full path if needed
python agent/agent.py --action generate --excel /full/path/testcases/my_tests.xlsx
```

### AI API Key invalid
```bash
# Check config.json has valid API key for your provider
# Make sure key is not expired
# Verify provider name matches (claude, openai, gemini, groq)
```

## Best Practices

1. **Keep locators in YAML** - Easier to maintain across tests
2. **Use meaningful page/test names** - Makes reports readable
3. **One feature per Excel sheet** - Easier to organize
4. **Update incrementally** - Use `--action update` for changes
5. **Review generated code** - AI-generated code may need tweaks
6. **Run locally first** - Test on your machine before CI/CD
7. **Version control** - Track config.json, pages/, tests/ (ignore framework_output/)

## CI/CD Integration

### GitHub Actions
```yaml
name: Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: cd framework_output && pytest --html=report.html
      - uses: actions/upload-artifact@v2
        with:
          name: test-report
          path: framework_output/report.html
```

### Jenkins
```groovy
pipeline {
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Generate') {
            steps {
                sh 'python agent/agent.py --action generate --excel testcases/tests.xlsx'
            }
        }
        stage('Test') {
            steps {
                dir('framework_output') {
                    sh 'pytest --html=reports/index.html'
                }
            }
        }
    }
    post {
        always {
            publishHTML([
                reportDir: 'framework_output/reports',
                reportFiles: 'index.html',
                reportName: 'Test Report'
            ])
        }
    }
}
```

## License

MIT License - See LICENSE file

## Support

For issues or questions:
1. Check README troubleshooting section
2. Review config.json settings
3. Check logs in framework_output/reports/logs/
4. Open an issue on the repository

---

Happy testing!
