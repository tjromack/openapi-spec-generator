import importlib.metadata

packages = ['openai', 'anthropic', 'pydantic', 'braintrust', 'requests', 'beautifulsoup4', 'pytest', 'black', 'ruff']

print('Package Versions:')
print('=' * 50)
for package in packages:
    try:
        version = importlib.metadata.version(package)
        print(f'✓ {package}: {version}')
    except Exception as e:
        print(f'✗ {package}: Not installed')
print('=' * 50)
