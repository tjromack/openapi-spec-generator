"""
Evaluation Metrics
Core metrics for measuring spec generation quality
"""
from typing import Dict, Any


class EvalMetrics:
    """Calculate evaluation metrics for generated OpenAPI specs"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_all_metrics(
        self,
        generated_spec: Dict[str, Any],
        expected_spec: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Calculate all metrics comparing generated vs expected spec
        
        Args:
            generated_spec: The AI-generated OpenAPI spec
            expected_spec: The hand-verified golden spec
            
        Returns:
            Dictionary of metric names to scores (0.0 to 1.0)
        """
        metrics = {}
        
        # 1. Endpoint Coverage: Did we find all the endpoints?
        metrics['endpoint_coverage'] = self._endpoint_coverage(
            generated_spec, expected_spec
        )
        
        # 2. Field Accuracy: Are the fields/parameters correct?
        metrics['field_accuracy'] = self._field_accuracy(
            generated_spec, expected_spec
        )
        
        # 3. Hallucination Rate: Did we make up endpoints/fields?
        metrics['hallucination_rate'] = self._hallucination_rate(
            generated_spec, expected_spec
        )
        
        # 4. Schema Validity: Is it valid OpenAPI 3.0?
        metrics['schema_validity'] = self._schema_validity(generated_spec)
        
        # 5. Overall Score: Weighted average
        metrics['overall_score'] = self._overall_score(metrics)
        
        return metrics
    
    def _endpoint_coverage(
        self,
        generated: Dict[str, Any],
        expected: Dict[str, Any]
    ) -> float:
        """
        What percentage of expected endpoints did we find?
        
        Returns: 0.0 to 1.0 (1.0 = found all endpoints)
        """
        expected_paths = set(expected.get('paths', {}).keys())
        generated_paths = set(generated.get('paths', {}).keys())
        
        if not expected_paths:
            return 1.0
        
        found = len(expected_paths.intersection(generated_paths))
        total = len(expected_paths)
        
        return found / total if total > 0 else 0.0
    
    def _field_accuracy(
        self,
        generated: Dict[str, Any],
        expected: Dict[str, Any]
    ) -> float:
        """
        What percentage of fields/parameters are correct?
        
        Simplified version: just checks response field names
        
        Returns: 0.0 to 1.0 (1.0 = all fields correct)
        """
        total_fields = 0
        correct_fields = 0
        
        expected_paths = expected.get('paths', {})
        generated_paths = generated.get('paths', {})
        
        # Only check paths that exist in both
        common_paths = set(expected_paths.keys()).intersection(
            set(generated_paths.keys())
        )
        
        for path in common_paths:
            expected_path = expected_paths[path]
            generated_path = generated_paths[path]
            
            # Check each HTTP method (get, post, etc.)
            for method in expected_path.keys():
                if method not in generated_path:
                    continue
                
                expected_method = expected_path[method]
                generated_method = generated_path[method]
                
                # Check response fields (simplified)
                exp_responses = expected_method.get('responses', {})
                gen_responses = generated_method.get('responses', {})
                
                for status_code in ['200', '201']:
                    if status_code not in exp_responses:
                        continue
                    
                    exp_content = exp_responses[status_code].get('content', {})
                    gen_content = gen_responses.get(status_code, {}).get('content', {})
                    
                    exp_schema = exp_content.get('application/json', {}).get('schema', {})
                    gen_schema = gen_content.get('application/json', {}).get('schema', {})
                    
                    # Get properties (handle arrays vs objects)
                    exp_props = self._get_properties(exp_schema)
                    gen_props = self._get_properties(gen_schema)
                    
                    if exp_props:
                        total_fields += len(exp_props)
                        correct_fields += len(exp_props.intersection(gen_props))
        
        return correct_fields / total_fields if total_fields > 0 else 0.0
    
    def _get_properties(self, schema: Dict[str, Any]) -> set:
        """Extract property names from schema (handles arrays)"""
        if schema.get('type') == 'array':
            items = schema.get('items', {})
            return set(items.get('properties', {}).keys())
        else:
            return set(schema.get('properties', {}).keys())
    
    def _hallucination_rate(
        self,
        generated: Dict[str, Any],
        expected: Dict[str, Any]
    ) -> float:
        """
        What percentage of generated content is hallucinated?
        
        Returns: 0.0 to 1.0 (0.0 = no hallucinations)
        """
        expected_paths = set(expected.get('paths', {}).keys())
        generated_paths = set(generated.get('paths', {}).keys())
        
        if not generated_paths:
            return 0.0
        
        # Hallucinated paths = paths in generated but not in expected
        hallucinated_paths = generated_paths - expected_paths
        
        hallucination_rate = len(hallucinated_paths) / len(generated_paths)
        
        return hallucination_rate
    
    def _schema_validity(self, generated: Dict[str, Any]) -> float:
        """
        Is this a valid OpenAPI 3.0 spec?
        
        Returns: 1.0 if valid, 0.0 if invalid
        """
        try:
            from openapi_spec_validator import validate_spec
            validate_spec(generated)
            return 1.0
        except Exception:
            return 0.0
    
    def _overall_score(self, metrics: Dict[str, float]) -> float:
        """
        Calculate weighted overall score
        
        Weights:
        - Endpoint coverage: 30%
        - Field accuracy: 30%
        - Hallucination rate: 25% (inverted - lower is better)
        - Schema validity: 15%
        """
        coverage = metrics.get('endpoint_coverage', 0.0)
        accuracy = metrics.get('field_accuracy', 0.0)
        hallucination = metrics.get('hallucination_rate', 1.0)
        validity = metrics.get('schema_validity', 0.0)
        
        # Invert hallucination rate (lower is better)
        hallucination_score = 1.0 - hallucination
        
        overall = (
            coverage * 0.30 +
            accuracy * 0.30 +
            hallucination_score * 0.25 +
            validity * 0.15
        )
        
        return overall


def format_metrics_report(metrics: Dict[str, float]) -> str:
    """Format metrics as a readable report"""
    lines = []
    lines.append("="*60)
    lines.append("EVALUATION METRICS")
    lines.append("="*60)
    lines.append("")
    lines.append(f"Endpoint Coverage:    {metrics.get('endpoint_coverage', 0)*100:.1f}%")
    lines.append(f"Field Accuracy:       {metrics.get('field_accuracy', 0)*100:.1f}%")
    lines.append(f"Hallucination Rate:   {metrics.get('hallucination_rate', 0)*100:.1f}%")
    lines.append(f"Schema Validity:      {'✓ Valid' if metrics.get('schema_validity', 0) == 1.0 else '✗ Invalid'}")
    lines.append("")
    lines.append(f"Overall Score:        {metrics.get('overall_score', 0)*100:.1f}%")
    lines.append("="*60)
    
    return "\n".join(lines)
