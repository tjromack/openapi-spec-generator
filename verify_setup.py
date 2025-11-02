"""
Multi-device setup verification script
Run this on BOTH devices to ensure parity
"""
import sys
import os
from pathlib import Path
import subprocess

def check_python_version():
    version = sys.version_info
    expected = (3, 13)
    if version.major == expected[0] and version.minor == expected[1]:
        print(f'✓ Python {version.major}.{version.minor}.{version.micro}')
        return True
    else:
        print(f'✗ Python version mismatch: {version.major}.{version.minor}')
        return False

def check_venv():
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        print(f'✓ Virtual environment active: {sys.prefix}')
        return True
    else:
        print('✗ Not in virtual environment')
        return False

def check_dependencies():
    required = ['openai', 'anthropic', 'braintrust', 'pydantic', 'requests']
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f'✓ {package}')
        except ImportError:
            print(f'✗ {package} not installed')
            missing.append(package)
    return len(missing) == 0

def check_env_file():
    env_path = Path('.env')
    if env_path.exists():
        print('✓ .env file exists')
        # Check for key variables
        from dotenv import load_dotenv
        load_dotenv()
        keys = ['ANTHROPIC_API_KEY', 'BRAINTRUST_API_KEY']
        all_present = True
        for key in keys:
            if os.getenv(key):
                print(f'  ✓ {key} set')
            else:
                print(f'  ✗ {key} missing')
                all_present = False
        return all_present
    else:
        print('✗ .env file not found')
        return False

def check_git_config():
    try:
        name = subprocess.check_output(['git', 'config', 'user.name']).decode().strip()
        email = subprocess.check_output(['git', 'config', 'user.email']).decode().strip()
        print(f'✓ Git configured: {name} <{email}>')
        return True
    except:
        print('✗ Git not configured')
        return False

def check_directory_structure():
    required_dirs = ['src', 'evals', 'data', 'docs']
    all_present = True
    for dir in required_dirs:
        if Path(dir).exists():
            print(f'✓ {dir}/ exists')
        else:
            print(f'✗ {dir}/ missing')
            all_present = False
    return all_present

def main():
    print('=' * 50)
    print('OpenAPI Spec Generator - Setup Verification')
    print('=' * 50)
    print()
    
    checks = [
        ('Python Version', check_python_version),
        ('Virtual Environment', check_venv),
        ('Dependencies', check_dependencies),
        ('Environment Variables', check_env_file),
        ('Git Configuration', check_git_config),
        ('Directory Structure', check_directory_structure),
    ]
    
    results = []
    for name, check_func in checks:
        print(f'\n{name}:')
        results.append(check_func())
    
    print('\n' + '=' * 50)
    if all(results):
        print('✓ ALL CHECKS PASSED - Setup is complete!')
        print('=' * 50)
        return 0
    else:
        print('✗ SOME CHECKS FAILED - Review errors above')
        print('=' * 50)
        return 1

if __name__ == '__main__':
    sys.exit(main())
