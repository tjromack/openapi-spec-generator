from dotenv import load_dotenv
import os

load_dotenv()

print('\n' + '='*60)
print('ENVIRONMENT VARIABLES CHECK')
print('='*60 + '\n')

keys = {
    'ANTHROPIC_API_KEY': {'required': True, 'prefix': 'sk-ant'},
    'BRAINTRUST_API_KEY': {'required': True, 'prefix': 'sk-'},  # Updated: Braintrust now uses sk- prefix
    'OPENWEATHER_API_KEY': {'required': True, 'prefix': None},
    'GITHUB_TOKEN': {'required': True, 'prefix': 'ghp_'},
    'OPENAI_API_KEY': {'required': False, 'prefix': 'sk-'},
    'SENDGRID_API_KEY': {'required': False, 'prefix': 'SG.'},
    'STRIPE_TEST_KEY': {'required': False, 'prefix': 'sk_test_'},
}

all_required_present = True

for name, config in keys.items():
    value = os.getenv(name)
    is_required = config['required']
    expected_prefix = config['prefix']
    
    if value:
        # Check prefix if specified
        prefix_match = True
        if expected_prefix and not value.startswith(expected_prefix):
            prefix_match = False
            
        if prefix_match:
            preview = value[:15] + '...' if len(value) > 15 else value
            status = '✓' if is_required else '✓ (optional)'
            print(f'{status} {name}: {preview}')
        else:
            print(f'⚠ {name}: Present but unexpected format')
            if is_required:
                all_required_present = False
    else:
        if is_required:
            print(f'✗ {name}: MISSING (required)')
            all_required_present = False
        else:
            print(f'○ {name}: Not set (optional)')

print('\n' + '='*60)
if all_required_present:
    print('✓ All required API keys are configured!')
    print('='*60)
    print('\nYou can now proceed with the project.')
else:
    print('✗ Some required API keys are missing!')
    print('='*60)
    print('\nPlease add the missing keys to your .env file.')
    exit(1)
