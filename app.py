from flask import Flask, request, jsonify
import jwt
import json
import os
import pickle
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_vulnerable_secret_key'  # Deliberately vulnerable
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Vulnerable model storage (deliberately unsafe)
MODEL_STORE = {}

@app.route('/api/v1/model/load', methods=['POST'])
def load_model():
    """
    Vulnerability 1: Unsafe Deserialization
    This endpoint accepts serialized model data and loads it without proper validation
    """
    if 'model' not in request.files:
        return jsonify({'error': 'No model file provided'}), 400
    
    model_file = request.files['model']
    model_name = request.form.get('name', 'default_model')
    
    # VULNERABLE: Unsafe pickle loading
    model_data = pickle.loads(model_file.read())
    MODEL_STORE[model_name] = model_data
    
    return jsonify({'message': f'Model {model_name} loaded successfully'})

@app.route('/api/v1/model/predict', methods=['POST'])
def predict():
    """
    Vulnerability 2: Injection in Model Input
    This endpoint doesn't properly sanitize or validate model inputs
    """
    data = request.get_json()
    model_name = data.get('model_name', 'default_model')
    
    if model_name not in MODEL_STORE:
        return jsonify({'error': 'Model not found'}), 404
    
    # VULNERABLE: No input validation
    model = MODEL_STORE[model_name]
    result = model.predict(data.get('input', []))
    
    return jsonify({'prediction': result.tolist()})

@app.route('/api/v1/admin/token', methods=['POST'])
def get_admin_token():
    """
    Vulnerability 3: Weak Authentication
    This endpoint uses a predictable token generation method
    """
    username = request.form.get('username')
    password = request.form.get('password')
    
    # VULNERABLE: Hardcoded credentials
    if username == 'admin' and password == 'admin123':
        token = jwt.encode(
            {'username': username, 'role': 'admin'},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/v1/model/metadata', methods=['GET'])
def get_model_metadata():
    """
    Vulnerability 4: Information Disclosure
    This endpoint leaks sensitive information about models
    """
    # VULNERABLE: Exposes internal model details
    metadata = {
        name: {
            'type': str(type(model)),
            'memory_address': hex(id(model)),
            'attributes': dir(model)
        }
        for name, model in MODEL_STORE.items()
    }
    return jsonify(metadata)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 