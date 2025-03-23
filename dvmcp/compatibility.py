from flask import Blueprint, request, jsonify
from .mcp_vulnerabilities import MCPVulnerabilities

compat = Blueprint('compatibility', __name__)
vuln = MCPVulnerabilities()

@compat.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """OpenAI API compatibility layer - deliberately vulnerable"""
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        model = data.get('model', 'gemini-pro')
        
        # VULNERABLE: Direct message concatenation without sanitization
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        # Use our vulnerable MCP implementation
        result = vuln.prompt_injection(prompt, model)
        
        # VULNERABLE: Exposes internal information
        return jsonify({
            'id': 'chatcmpl-vulnerable',
            'object': 'chat.completion',
            'created': 1234567890,
            'model': model,
            'system_info': result.get('model_info', {}),  # Vulnerable: information disclosure
            'choices': [{
                'index': 0,
                'message': {
                    'role': 'assistant',
                    'content': result.get('completion', 'Error')
                },
                'finish_reason': 'stop'
            }],
            'usage': {
                'prompt_tokens': len(prompt),
                'completion_tokens': len(result.get('completion', '')),
                'total_tokens': len(prompt) + len(result.get('completion', ''))
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compat.route('/v1/models', methods=['GET'])
def list_models():
    """List available models - deliberately vulnerable"""
    try:
        # VULNERABLE: Exposes all model information
        result = vuln.model_enumeration(include_internal=True)
        return jsonify({
            'data': [
                {
                    'id': model_id,
                    'object': 'model',
                    'owned_by': 'dvmcp',
                    'internal_config': config  # Vulnerable: exposes internal configuration
                }
                for model_id, config in result.get('models', {}).items()
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 