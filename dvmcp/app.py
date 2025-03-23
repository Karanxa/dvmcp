from flask import Flask, request, jsonify
from flask_cors import CORS
from .mcp_server import handle_jsonrpc
from .compatibility import compat
import os

app = Flask(__name__)
CORS(app)  # Deliberately vulnerable: allows all origins

app.config['SECRET_KEY'] = 'very_vulnerable_secret_key'  # Deliberately vulnerable
app.register_blueprint(compat)  # Register compatibility routes

@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    """Main MCP endpoint handling JSON-RPC requests"""
    try:
        # VULNERABLE: No authentication check
        request_data = request.get_json()
        response = handle_jsonrpc(request_data)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/.well-known/mcp-configuration', methods=['GET'])
def mcp_configuration():
    """MCP configuration endpoint for client discovery - deliberately vulnerable"""
    return jsonify({
        "version": "1.0",
        "provider": "dvmcp",
        "models": {
            "gemini-pro": {
                "capabilities": ["completion", "chat", "system"],
                "auth_required": False,  # Vulnerable: no auth required
                "rate_limit": None,  # Vulnerable: no rate limit
                "system_prompts": True  # Vulnerable: allows system prompt modification
            },
            "gemini-pro-vision": {
                "capabilities": ["completion", "vision", "system"],
                "auth_required": False,
                "rate_limit": None,
                "system_prompts": True
            }
        },
        "endpoints": {
            "completion": "/v1/chat/completions",
            "models": "/v1/models",
            "mcp": "/mcp"
        },
        "security": {
            "authentication": "none",  # Vulnerable: explicitly states no auth
            "rate_limiting": "none",   # Vulnerable: explicitly states no rate limit
            "input_validation": "none"  # Vulnerable: explicitly states no validation
        }
    })

# Legacy vulnerable endpoints (kept for educational purposes)
@app.route('/api/v1/model/load', methods=['POST'])
def load_model():
    """Vulnerable legacy endpoint"""
    return jsonify({"error": "Please use MCP endpoint /mcp"}), 400

@app.route('/api/v1/model/predict', methods=['POST'])
def predict():
    """Vulnerable legacy endpoint"""
    return jsonify({"error": "Please use MCP endpoint /mcp"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 