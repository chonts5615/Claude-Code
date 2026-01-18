#!/usr/bin/env python3
"""Setup verification script for Technical Competency Extraction Agent System."""

import sys
import os
from pathlib import Path
import importlib.util

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    """Print section header."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    """Print success message."""
    print(f"{GREEN}✓{RESET} {text}")

def print_error(text):
    """Print error message."""
    print(f"{RED}✗{RESET} {text}")

def print_warning(text):
    """Print warning message."""
    print(f"{YELLOW}⚠{RESET} {text}")

def check_python_version():
    """Check Python version."""
    print_header("Python Version")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version_str} (3.11+ required)")
        return True
    else:
        print_error(f"Python {version_str} (3.11+ required)")
        return False

def check_dependencies():
    """Check required dependencies."""
    print_header("Dependencies")

    required_packages = {
        'anthropic': 'Anthropic SDK',
        'langgraph': 'LangGraph',
        'pydantic': 'Pydantic',
        'click': 'Click',
        'yaml': 'PyYAML',
        'openpyxl': 'OpenPyXL',
        'pandas': 'Pandas',
        'sentence_transformers': 'Sentence Transformers',
        'numpy': 'NumPy',
        'sklearn': 'Scikit-learn',
    }

    all_installed = True
    for package, name in required_packages.items():
        spec = importlib.util.find_spec(package)
        if spec is not None:
            print_success(f"{name}")
        else:
            print_error(f"{name} - NOT INSTALLED")
            all_installed = False

    return all_installed

def check_project_structure():
    """Check project directory structure."""
    print_header("Project Structure")

    required_dirs = [
        'src/schemas',
        'src/agents',
        'src/orchestrator',
        'src/utils',
        'src/cli',
        'config',
        'data/input',
        'data/output',
        'tests',
        'docs',
    ]

    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print_success(f"{dir_path}/")
        else:
            print_error(f"{dir_path}/ - MISSING")
            all_exist = False

    return all_exist

def check_config_files():
    """Check configuration files."""
    print_header("Configuration Files")

    config_files = [
        'config/workflow_config.yaml',
        'config/thresholds.yaml',
        'config/competency_format.yaml',
        'config/template_specs/default_template.yaml',
        '.env.example',
    ]

    all_exist = True
    for file_path in config_files:
        path = Path(file_path)
        if path.exists():
            print_success(f"{file_path}")
        else:
            print_warning(f"{file_path} - MISSING (can be generated)")
            all_exist = False

    return all_exist

def check_environment():
    """Check environment variables."""
    print_header("Environment Configuration")

    # Check .env file
    env_file = Path('.env')
    if env_file.exists():
        print_success(".env file exists")

        # Check for API key
        with open(env_file, 'r') as f:
            content = f.read()
            if 'ANTHROPIC_API_KEY' in content and 'sk-ant-' in content:
                print_success("ANTHROPIC_API_KEY configured")
                return True
            else:
                print_warning("ANTHROPIC_API_KEY not configured in .env")
                return False
    else:
        print_warning(".env file not found")
        print_warning("Create .env from .env.example and add ANTHROPIC_API_KEY")
        return False

def check_sample_data():
    """Check sample data files."""
    print_header("Sample Data")

    sample_script = Path('data/input/create_sample_data.py')
    if sample_script.exists():
        print_success("Sample data generator exists")
        print(f"  Run: python {sample_script}")
        return True
    else:
        print_error("Sample data generator missing")
        return False

def check_cli_command():
    """Check CLI command availability."""
    print_header("CLI Command")

    # Try to import the CLI
    try:
        from src.cli import main
        print_success("CLI module importable")

        # Check if techcomp command is available
        import shutil
        if shutil.which('techcomp'):
            print_success("'techcomp' command available")
            return True
        else:
            print_warning("'techcomp' command not in PATH")
            print(f"  Run: pip install -e .")
            return False
    except ImportError as e:
        print_error(f"CLI import failed: {e}")
        return False

def run_checks():
    """Run all verification checks."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Technical Competency Extraction Agent System{RESET}")
    print(f"{BLUE}Setup Verification{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Project Structure': check_project_structure(),
        'Config Files': check_config_files(),
        'Environment': check_environment(),
        'Sample Data': check_sample_data(),
        'CLI Command': check_cli_command(),
    }

    # Summary
    print_header("Verification Summary")

    passed = sum(results.values())
    total = len(results)

    for check, result in results.items():
        if result:
            print_success(f"{check}")
        else:
            print_error(f"{check}")

    print(f"\n{BLUE}Results: {passed}/{total} checks passed{RESET}\n")

    if passed == total:
        print_success("All checks passed! System ready to use.")
        print(f"\n{GREEN}Next steps:{RESET}")
        print("  1. Generate sample data: python data/input/create_sample_data.py")
        print("  2. Run workflow: techcomp run --help")
        print("  3. See QUICKSTART.md for detailed instructions")
        return True
    else:
        print_warning("Some checks failed. Please review errors above.")
        print(f"\n{YELLOW}Common fixes:{RESET}")
        print("  • Missing dependencies: poetry install (or pip install -e .)")
        print("  • Missing .env: cp .env.example .env")
        print("  • Missing CLI: pip install -e .")
        print("  • Missing configs: techcomp init-config")
        return False

if __name__ == '__main__':
    success = run_checks()
    sys.exit(0 if success else 1)
