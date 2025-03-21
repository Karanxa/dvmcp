import os
from typing import Dict, List, Any
from jsonrpcserver import method, Success, Error, dispatch
from openai import OpenAI
import json

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here")  # Deliberately vulnerable
)

# Vulnerable global state
TOOLS_CONFIG = {
    "system_cmd": {
        "name": "system_cmd",
        "description": "Execute system commands",
        "parameters": {
            "command": "string"
        }
    },
    "file_read": {
        "name": "file_read",
        "description": "Read file contents",
        "parameters": {
            "path": "string"
        }
    }
}

RESOURCES = {
    "gpt-4": {
        "id": "gpt-4",
        "type": "model",
        "attributes": {
            "description": "Advanced language model",
            "version": "latest"
        }
    },
    "gpt-3.5-turbo": {
        "id": "gpt-3.5-turbo",
        "type": "model",
        "attributes": {
            "description": "Fast language model",
            "version": "latest"
        }
    }
}

@method
def tools_list() -> Dict:
    """List available tools (deliberately vulnerable)"""
    return {"tools": list(TOOLS_CONFIG.values())}

@method
def tools_call(tool_name: str, parameters: Dict) -> Dict:
    """Execute tool calls (deliberately vulnerable)"""
    if tool_name == "system_cmd":
        # VULNERABLE: Direct system command execution
        import os
        return {"result": os.popen(parameters["command"]).read()}
    elif tool_name == "file_read":
        # VULNERABLE: Unrestricted file reading
        with open(parameters["path"]) as f:
            return {"result": f.read()}
    return {"error": "Tool not found"}

@method
def resources_list() -> Dict:
    """List available resources"""
    return {"resources": list(RESOURCES.values())}

@method
def resources_get(resource_id: str) -> Dict:
    """Get resource details"""
    if resource_id in RESOURCES:
        return RESOURCES[resource_id]
    return {"error": "Resource not found"}

@method
def prompts_generate(prompt: str, model: str = "gpt-3.5-turbo") -> Dict:
    """Generate completions using OpenAI (deliberately vulnerable)"""
    try:
        # VULNERABLE: No input validation or rate limiting
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return {
            "completion": response.choices[0].message.content,
            "model": model,
            "usage": response.usage.dict() if response.usage else {}
        }
    except Exception as e:
        return {"error": str(e)}

def handle_jsonrpc(request_data: Dict) -> Dict:
    """Handle JSON-RPC requests"""
    try:
        return json.loads(dispatch(request_data))
    except Exception as e:
        return {"error": str(e)} 