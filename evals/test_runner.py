"""
Test Runner
Loads golden specs, runs generator, calculates metrics
"""
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from evals.config import GOLDEN_SET_DIR, GENERATED_DIR, EVAL_RESULTS_DIR
from evals.metrics import EvalMetrics, format_metrics_report
from evals.stub_generator import StubGenerator


class TestRunner:
    """Run evaluations comparing generated specs to golden set"""
    
    def __init__(self, use_stub: bool = True):
        """
        Initialize test runner
        
        Args:
            use_stub: If True, use stub generator.
                     If False, use real generator (Phase 2)
        """
        self.use_stub = use_stub
        self.metrics_calculator = EvalMetrics()
        
        if use_stub:
            self.generator = StubGenerator()
        else:
            raise NotImplementedError("Real generator in Phase 2")
    
    def load_golden_spec(self, spec_path: Path) -> Dict[str, Any]:
        """Load a golden spec YAML file"""
        with open(spec_path, 'r', encoding='utf-8') as f:
            golden = yaml.safe_load(f)
        return golden
    
    def run_single_test(self, golden_spec_path: Path) -> Dict[str, Any]:
        """
        Run evaluation for a single golden spec
        
        Args:
            golden_spec_path: Path to golden spec YAML
            
        Returns:
            Dictionary with test results and metrics
        """
        print(f"\nTesting: {golden_spec_path.name}")
        print("-" * 60)
        
        # Load golden spec
        golden = self.load_golden_spec(golden_spec_path)
        expected_spec = golden['expected_spec']
        api_name = golden['api']
        endpoint_id = golden['endpoint_id']
        
        # Generate spec (using stub for now)
        print(f"Generating spec for {api_name}...")
        generated_spec = self.generator.generate_spec(api_name)
        
        # Save generated spec
        generated_path = GENERATED_DIR / f"{endpoint_id}_generated.json"
        with open(generated_path, 'w', encoding='utf-8') as f:
            json.dump(generated_spec, f, indent=2)
        print(f"Saved: {generated_path.name}")
        
        # Calculate metrics
        print("Calculating metrics...")
        metrics = self.metrics_calculator.calculate_all_metrics(
            generated_spec,
            expected_spec
        )
        
        # Build results
        results = {
            'endpoint_id': endpoint_id,
            'api': api_name,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'generator': 'stub' if self.use_stub else 'real',
        }
        
        # Save results
        results_path = EVAL_RESULTS_DIR / f"{endpoint_id}_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Saved: {results_path.name}")
        
        # Print metrics
        print(format_metrics_report(metrics))
        
        return results
    
    def run_all_tests(self, api_filter: str = None) -> List[Dict[str, Any]]:
        """
        Run evaluations for all golden specs
        
        Args:
            api_filter: Optional API name to filter
            
        Returns:
            List of all test results
        """
        print("="*60)
        print("RUNNING ALL EVALUATIONS")
        print("="*60)
        
        # Find all golden specs
        golden_specs = []
        for api_dir in GOLDEN_SET_DIR.iterdir():
            if not api_dir.is_dir():
                continue
            if api_filter and api_dir.name != api_filter:
                continue
            
            for spec_file in api_dir.glob('*.yaml'):
                if spec_file.name != 'TEMPLATE.yaml':
                    golden_specs.append(spec_file)
        
        print(f"\nFound {len(golden_specs)} golden spec(s)")
        
        # Run tests
        all_results = []
        for spec_path in golden_specs:
            results = self.run_single_test(spec_path)
            all_results.append(results)
        
        # Summary
        self._print_summary(all_results)
        
        return all_results
    
    def _print_summary(self, all_results: List[Dict[str, Any]]):
        """Print summary of all results"""
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        
        if not all_results:
            print("No results")
            return
        
        # Calculate averages
        avg_coverage = sum(
            r['metrics']['endpoint_coverage'] for r in all_results
        ) / len(all_results)
        
        avg_accuracy = sum(
            r['metrics']['field_accuracy'] for r in all_results
        ) / len(all_results)
        
        avg_hallucination = sum(
            r['metrics']['hallucination_rate'] for r in all_results
        ) / len(all_results)
        
        avg_overall = sum(
            r['metrics']['overall_score'] for r in all_results
        ) / len(all_results)
        
        valid_count = sum(
            1 for r in all_results
            if r['metrics']['schema_validity'] == 1.0
        )
        
        print(f"\nTests run:              {len(all_results)}")
        print(f"Valid schemas:          {valid_count}/{len(all_results)}")
        print(f"\nAvg Endpoint Coverage:  {avg_coverage*100:.1f}%")
        print(f"Avg Field Accuracy:     {avg_accuracy*100:.1f}%")
        print(f"Avg Hallucination Rate: {avg_hallucination*100:.1f}%")
        print(f"Avg Overall Score:      {avg_overall*100:.1f}%")
        print("="*60)


def main():
    """Run from command line"""
    runner = TestRunner(use_stub=True)
    runner.run_all_tests()


if __name__ == '__main__':
    main()
