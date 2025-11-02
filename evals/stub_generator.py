"""
Stub Generator
A placeholder generator for testing the eval harness
Returns intentionally imperfect specs to verify metrics work
"""
from typing import Dict, Any


class StubGenerator:
    """
    Stub generator for testing eval framework
    
    Intentionally produces imperfect specs:
    - Some correct endpoints
    - Some missing endpoints  
    - Some hallucinated endpoints
    - Some incorrect fields
    """
    
    def generate_spec(self, api_name: str) -> Dict[str, Any]:
        """Generate a stub OpenAPI spec for testing"""
        if api_name == 'jsonplaceholder':
            return self._jsonplaceholder_stub()
        else:
            return self._generic_stub(api_name)
    
    def _jsonplaceholder_stub(self) -> Dict[str, Any]:
        """
        Stub spec for JSONPlaceholder
        
        Intentional issues for testing:
        - Only has /posts (missing /posts/{id}, /users, etc.)
        - Has hallucinated /fake-endpoint
        - Missing 'userId' field in post schema
        """
        return {
            'openapi': '3.0.0',
            'info': {
                'title': 'JSONPlaceholder API',
                'version': '1.0.0'
            },
            'servers': [{'url': 'https://jsonplaceholder.typicode.com'}],
            'paths': {
                '/posts': {
                    'get': {
                        'summary': 'Get all posts',
                        'responses': {
                            '200': {
                                'description': 'Success',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'id': {'type': 'integer'},
                                                    'title': {'type': 'string'},
                                                    'body': {'type': 'string'},
                                                    # Missing: userId
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                # Hallucinated endpoint:
                '/fake-endpoint': {
                    'get': {
                        'summary': 'This does not exist',
                        'responses': {
                            '200': {'description': 'Fake'}
                        }
                    }
                }
            }
        }
    
    def _generic_stub(self, api_name: str) -> Dict[str, Any]:
        """Generic stub for other APIs"""
        return {
            'openapi': '3.0.0',
            'info': {
                'title': f'{api_name} API',
                'version': '1.0.0'
            },
            'paths': {}
        }
