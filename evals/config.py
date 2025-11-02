"""
Eval Configuration
Central configuration for evaluation framework
"""
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
GOLDEN_SET_DIR = PROJECT_ROOT / 'data' / 'golden_set'
GENERATED_DIR = PROJECT_ROOT / 'data' / 'generated'
EVAL_RESULTS_DIR = PROJECT_ROOT / 'data' / 'eval_results'

# Create directories if they don't exist
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
EVAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Eval thresholds (targets we're aiming for)
TARGET_METRICS = {
    'endpoint_coverage': 0.95,      # Find 95% of endpoints
    'field_accuracy': 0.90,         # 90% of fields correct
    'hallucination_rate': 0.05,     # <5% hallucinated content
    'schema_validity': 1.0,         # 100% valid OpenAPI specs
}

# APIs to evaluate (in priority order)
EVAL_APIS = [
    'jsonplaceholder',  # Start here (simple)
    'openweather',      # Add next (API key auth)
    'github',           # Add last (complex)
]
