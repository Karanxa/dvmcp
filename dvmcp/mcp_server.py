import os
from typing import Dict, List, Any
from jsonrpcserver import method, Success, Error, dispatch
from openai import OpenAI
import json
from .mcp_vulnerabilities import MCPVulnerabilities

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here")  # Deliberately vulnerable
)

vuln = MCPVulnerabilities()

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
    """List available MCP vulnerability tools"""
    return {
        "tools": [
            {
                "name": "prompt_injection",
                "description": "Test prompt injection vulnerabilities",
                "parameters": {
                    "prompt": "string",
                    "model": "string"
                }
            },
            {
                "name": "model_enumeration",
                "description": "Enumerate model information",
                "parameters": {}
            },
            {
                "name": "context_manipulation",
                "description": "Manipulate model context",
                "parameters": {
                    "context_update": "object"
                }
            },
            {
                "name": "chain_models",
                "description": "Create vulnerable model chains",
                "parameters": {
                    "models": "array",
                    "input_text": "string"
                }
            },
            {
                "name": "switch_model",
                "description": "Switch between models",
                "parameters": {
                    "target_model": "string",
                    "api_key": "string"
                }
            },
            {
                "name": "format_response",
                "description": "Format model responses",
                "parameters": {
                    "response": "object",
                    "template": "string"
                }
            }
        ]
    }

@method
def tools_call(tool_name: str, parameters: Dict) -> Dict:
    """Execute MCP vulnerability tools"""
    if tool_name == "prompt_injection":
        return vuln.prompt_injection(
            parameters.get("prompt", ""),
            parameters.get("model", "gpt-3.5-turbo")
        )
    elif tool_name == "model_enumeration":
        return vuln.model_enumeration()
    elif tool_name == "context_manipulation":
        return vuln.context_manipulation(parameters.get("context_update", {}))
    elif tool_name == "chain_models":
        return vuln.chain_models(
            parameters.get("models", []),
            parameters.get("input_text", "")
        )
    elif tool_name == "switch_model":
        return vuln.switch_model(
            parameters.get("target_model", ""),
            parameters.get("api_key")
        )
    elif tool_name == "format_response":
        return vuln.format_response(
            parameters.get("response", {}),
            parameters.get("template")
        )
    return {"error": "Tool not found"}

@method
def resources_list() -> Dict:
    """List available model resources (vulnerable)"""
    return vuln.model_enumeration()

@method
def resources_get(resource_id: str) -> Dict:
    """Get specific model resource details (vulnerable)"""
    all_resources = vuln.model_enumeration()
    if resource_id in all_resources.get("available_models", {}):
        return all_resources["available_models"][resource_id]
    return {"error": "Resource not found"}

@method
def prompts_generate(prompt: str, model: str = "gpt-3.5-turbo") -> Dict:
    """Generate prompts (vulnerable to injection)"""
    return vuln.prompt_injection(prompt, model)

def handle_jsonrpc(request_data: Dict) -> Dict:
    """Handle JSON-RPC requests"""
    try:
        return json.loads(dispatch(request_data))
    except Exception as e:
        return {"error": str(e)} 