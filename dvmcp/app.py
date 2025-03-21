from flask import Flask, request, jsonify
from .mcp_server import handle_jsonrpc
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_vulnerable_secret_key'  # Deliberately vulnerable

@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    """Main MCP endpoint handling JSON-RPC requests"""
    try:
        request_data = request.get_json()
        response = handle_jsonrpc(request_data)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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