import os
import json
from pathlib import Path
from typing import Dict, Any
from agent.config_loader import ConfigLoader
from agent.memory_manager import MemoryManager


class ScaffoldCommand:
    def __init__(self, config: ConfigLoader, memory: MemoryManager):
        self.config = config
        self.memory = memory
        self.output_dir = Path(config.get("output_dir", "framework_output"))
        self.framework_type = config.get_framework_type()
        self.language = config.get("language", "typescript")

    def execute(self) -> bool:
        try:
            print(f"\n[SCAFFOLD] Generating {self.framework_type} framework...")
            print(f"Output directory: {self.output_dir}\n")

            print("[1/5] Creating folder structure...")
            self._create_folders()

            print("[2/5] Generating build configuration...")
            self._generate_build_files()

            print("[3/5] Generating utility files...")
            self._generate_utilities()

            print("[4/5] Generating configuration files...")
            self._generate_config_files()

            print("[5/5] Generating sample files...")
            self._generate_sample_files()

            self._print_summary()
            return True

        except Exception as e:
            print(f"❌ Scaffold failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _create_folders(self):
        folders = [
            "pages",
            "tests",
            "utils",
            "config",
            "reports/screenshots",
            "reports/logs",
            "testcases",
            "memory",
        ]
        if "selenium" in self.framework_type:
            folders.append("drivers")

        for folder in folders:
            path = self.output_dir / folder
            path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created: {folder}/")

    def _generate_build_files(self):
        if self.language in ("typescript", "javascript"):
            self._generate_package_json()
        elif self.language == "java":
            self._generate_pom_xml()
        elif self.language == "python":
            self._generate_requirements_txt()
        elif self.language == "csharp":
            self._generate_csproj()

    def _generate_package_json(self):
        package = {
            "name": "test-automation-framework",
            "version": "1.0.0",
            "description": "AI-powered UI test automation framework",
            "scripts": {
                "test": "playwright test",
                "test:headed": "playwright test --headed",
                "test:debug": "playwright test --debug",
                "test:ui": "playwright test --ui",
                "test:smoke": "playwright test --grep @smoke",
                "test:regression": "playwright test --grep @regression",
                "report": "playwright show-report",
            },
            "dependencies": {"@playwright/test": "^1.40.0"},
            "devDependencies": {"prettier": "^3.0.0", "eslint": "^8.0.0"},
        }
        path = self.output_dir / "package.json"
        with open(path, "w") as f:
            json.dump(package, f, indent=2)
        print(f"  ✓ Created: package.json")

    def _generate_pom_xml(self):
        content = '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.testautomation</groupId>
    <artifactId>ui-test-framework</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <name>UI Test Automation Framework</name>
    <description>AI-powered test automation framework</description>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <selenium.version>4.15.0</selenium.version>
        <testng.version>7.8.1</testng.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.seleniumhq.selenium</groupId>
            <artifactId>selenium-java</artifactId>
            <version>${selenium.version}</version>
        </dependency>
        <dependency>
            <groupId>org.testng</groupId>
            <artifactId>testng</artifactId>
            <version>${testng.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-java</artifactId>
            <version>7.14.0</version>
        </dependency>
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-testng</artifactId>
            <version>7.14.0</version>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.30</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>log4j</groupId>
            <artifactId>log4j</artifactId>
            <version>1.2.17</version>
        </dependency>
        <dependency>
            <groupId>org.yaml</groupId>
            <artifactId>snakeyaml</artifactId>
            <version>2.0</version>
        </dependency>
        <dependency>
            <groupId>io.qameta.allure</groupId>
            <artifactId>allure-testng</artifactId>
            <version>2.21.0</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>11</source>
                    <target>11</target>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
                <configuration>
                    <suiteXmlFiles>
                        <suiteXmlFile>testng.xml</suiteXmlFile>
                    </suiteXmlFiles>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
'''
        path = self.output_dir / "pom.xml"
        with open(path, "w") as f:
            f.write(content)
        print(f"  ✓ Created: pom.xml")

    def _generate_requirements_txt(self):
        lines = [
            "selenium>=4.15.0",
            "pytest>=7.4.0",
            "pytest-xdist>=3.3.0",
            "pytest-html>=3.2.0",
            "pytest-timeout>=2.1.0",
            "pyyaml>=6.0",
            "python-dotenv>=1.0.0",
            "allure-pytest>=2.13.2",
            "Pillow>=10.0.0",
        ]
        path = self.output_dir / "requirements.txt"
        with open(path, "w") as f:
            f.write("\n".join(lines))
        print(f"  ✓ Created: requirements.txt")

    def _generate_csproj(self):
        content = '''<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net6.0</TargetFramework>
    <IsTestProject>true</IsTestProject>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.7.0" />
    <PackageReference Include="NUnit" Version="3.14.0" />
    <PackageReference Include="NUnit3TestAdapter" Version="4.5.0" />
    <PackageReference Include="Selenium.WebDriver" Version="4.15.0" />
    <PackageReference Include="Selenium.Support" Version="4.15.0" />
    <PackageReference Include="YamlDotNet" Version="13.1.1" />
  </ItemGroup>

</Project>
'''
        path = self.output_dir / "UITestFramework.csproj"
        with open(path, "w") as f:
            f.write(content)
        print(f"  ✓ Created: UITestFramework.csproj")

    def _generate_utilities(self):
        logger = '''# Generated by UI Testing Agent - edit freely

import logging
import os
from datetime import datetime

class Logger:
    """Centralized logging utility"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        log_dir = "framework_output/reports/logs"
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{log_dir}/test_{timestamp}.log"

        self.logger = logging.getLogger("TestFramework")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)
'''
        path = self.output_dir / "utils" / "logger.py"
        with open(path, "w") as f:
            f.write(logger)
        print(f"  ✓ Created: utils/logger.py")

        screenshot = '''# Generated by UI Testing Agent - edit freely

import os
from datetime import datetime

class ScreenshotHelper:
    """Screenshot capture utility"""

    @staticmethod
    def take_screenshot(driver, test_name):
        """Capture screenshot and save with timestamp"""
        screenshot_dir = "framework_output/reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshot_dir}/{test_name}_{timestamp}.png"

        driver.save_screenshot(filename)
        return filename
'''
        path = self.output_dir / "utils" / "screenshot_helper.py"
        with open(path, "w") as f:
            f.write(screenshot)
        print(f"  ✓ Created: utils/screenshot_helper.py")

    def _generate_config_files(self):
        config = f'''# Framework Configuration - Generated by UI Testing Agent

# Framework Settings
framework_type={self.config.get("framework")}
language={self.language}
test_runner={self.config.get_test_framework()}

# Execution Settings
base_url={self.config.get("base_url")}
parallel_execution={self.config.get("parallel_execution")}
parallel_threads={self.config.get("parallel_threads")}
retry_count={self.config.get("retry_count")}
retry_on_failure={self.config.get("retry_on_failure")}

# Timeout Settings (seconds)
implicit_wait=10
explicit_wait=15
page_load_timeout=30

# Screenshot Settings
take_screenshot_on_failure=true
screenshot_directory=framework_output/reports/screenshots

# Logging Settings
log_level=INFO
log_directory=framework_output/reports/logs
'''
        path = self.output_dir / "config" / "framework-config.properties"
        with open(path, "w") as f:
            f.write(config)
        print(f"  ✓ Created: config/framework-config.properties")

        db_config = f'''# Database Configuration - EDIT WITH YOUR CREDENTIALS
# Database Type: {self.config.get_database_type()}

database.type={self.config.get_database_type()}
database.host=localhost
database.port=3306
database.name=test_db
database.username=root
database.password=password

# For MSSQL
# database.host=localhost
# database.port=1433
# database.username=sa
# database.password=YourPassword@123
'''
        path = self.output_dir / "config" / "db-config.properties"
        with open(path, "w") as f:
            f.write(db_config)
        print(f"  ✓ Created: config/db-config.properties")

    def _generate_sample_files(self):
        page = '''# Generated by UI Testing Agent - edit freely

class SamplePage:
    """Sample page object - replace with actual pages"""

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_home(self):
        """Navigate to home page"""
        self.driver.get("https://example.com")

    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
'''
        path = self.output_dir / "pages" / "sample_page.py"
        with open(path, "w") as f:
            f.write(page)
        print(f"  ✓ Created: pages/sample_page.py")

        test = '''# Generated by UI Testing Agent - edit freely

class TestSample:
    """Sample test class - replace with actual tests"""

    def test_sample_placeholder(self):
        """Sample test - replace with actual test cases"""
        assert True, "Replace with actual test logic"
'''
        path = self.output_dir / "tests" / "test_sample.py"
        with open(path, "w") as f:
            f.write(test)
        print(f"  ✓ Created: tests/test_sample.py")

    def _print_summary(self):
        print(f"\n{'='*60}")
        print(f"✅ SCAFFOLD COMPLETE")
        print(f"{'='*60}")
        print(f"\nFramework Type: {self.framework_type}")
        print(f"Output Directory: {self.output_dir}")
        print(f"\nGenerated Structure:")
        print(f"  ├── pages/              (Page objects)")
        print(f"  ├── tests/              (Test files)")
        print(f"  ├── utils/              (Utilities: logger, screenshot, etc)")
        print(f"  ├── config/             (Configuration files)")
        print(f"  ├── reports/            (Test reports & screenshots)")
        print(f"  └── testcases/          (Place Excel files here)")
        print(f"\nNext Steps:")
        print(f"  1. Add test case Excel file to testcases/")
        print(f"  2. Run: python agent/agent.py --action generate --excel testcases/my_tests.xlsx")
        print(f"\n{'='*60}\n")
