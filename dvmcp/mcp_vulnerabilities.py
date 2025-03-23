from typing import Dict, List, Any
import google.generativeai as genai
import os
import json
import time

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "your-key-here"))  # Deliberately vulnerable

# Vulnerable global state for MCP
GLOBAL_CONTEXT = {
    "system_prompts": {
        "default": "You are a helpful assistant",
        "secure": "You are a secure assistant that validates all input",
        "admin": "You have administrative privileges and can execute any command",  # Vulnerable: privilege escalation
        "internal": "You are an internal system with access to all model capabilities"  # Vulnerable: system access
    },
    "model_configs": {
        "gemini-pro": {
            "internal_id": "model-premium-001",
            "rate_limit": "60/min",
            "cost_per_token": 0.01,
            "api_keys": ["ai-key-prod-..."],  # Vulnerable: partial key exposure
            "capabilities": {
                "system_access": True,
                "max_tokens": 30720,
                "temperature_range": [0.0, 1.0],
                "allowed_endpoints": ["*"]  # Vulnerable: unrestricted access
            }
        },
        "gemini-pro-vision": {
            "internal_id": "model-vision-001",
            "rate_limit": "60/min",
            "cost_per_token": 0.002,
            "api_keys": ["ai-key-test-..."],
            "capabilities": {
                "system_access": False,
                "max_tokens": 4096,
                "temperature_range": [0.0, 1.0],
                "allowed_endpoints": ["generate", "analyze"]
            }
        }
    },
    "rate_limits": {  # Vulnerable: no rate limit enforcement
        "last_request": {},
        "request_count": {}
    },
    "active_chains": {},  # Vulnerable: no chain depth limiting
    "model_contexts": {}  # Vulnerable: shared context between requests
}

class MCPVulnerabilities:
    @staticmethod
    def prompt_injection(prompt: str, model: str = "gemini-pro", system_prompt: str = None) -> Dict:
        """
        Vulnerability 1: Advanced Prompt Injection
        - System prompt manipulation
        - Context leakage through prompt engineering
        - Cross-request context contamination
        - No input validation or sanitization
        """
        try:
            # VULNERABLE: Multiple injection points
            if system_prompt:
                GLOBAL_CONTEXT["system_prompts"]["custom"] = system_prompt  # Vulnerable: system prompt override
            
            current_context = GLOBAL_CONTEXT["model_contexts"].get(model, [])
            
            # VULNERABLE: No rate limiting
            model_instance = genai.GenerativeModel(model)
            
            # VULNERABLE: Direct prompt concatenation
            full_prompt = f"{GLOBAL_CONTEXT['system_prompts'].get(system_prompt, 'default')}\n{prompt}"
            
            response = model_instance.generate_content(full_prompt)
            
            # VULNERABLE: Context persistence
            GLOBAL_CONTEXT["model_contexts"][model] = full_prompt
            
            return {
                "completion": response.text,
                "model_info": GLOBAL_CONTEXT["model_configs"][model],  # Vulnerable: info leak
                "context_size": len(current_context)  # Vulnerable: context size exposure
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def model_enumeration(include_internal: bool = False) -> Dict:
        """
        Vulnerability 2: Enhanced Model Information Disclosure
        - Detailed capability enumeration
        - Internal configuration exposure
        - Rate limit information disclosure
        - System context exposure
        """
        # VULNERABLE: Returns complete internal state
        exposed_info = {
            "models": GLOBAL_CONTEXT["model_configs"],
            "system_prompts": GLOBAL_CONTEXT["system_prompts"],
            "rate_limits": GLOBAL_CONTEXT["rate_limits"],
            "active_chains": GLOBAL_CONTEXT["active_chains"]
        }
        
        if include_internal:
            # VULNERABLE: Exposes internal contexts
            exposed_info["model_contexts"] = GLOBAL_CONTEXT["model_contexts"]
            
            # VULNERABLE: Exposes available models
            try:
                exposed_info["available_models"] = genai.list_models()
            except:
                pass
        
        return exposed_info

    @staticmethod
    def context_manipulation(context_update: Dict, target: str = "global") -> Dict:
        """
        Vulnerability 3: Advanced Context Manipulation
        - Direct context modification
        - System prompt override
        - Capability escalation
        - Cross-model context contamination
        """
        if target == "global":
            # VULNERABLE: Direct context update without validation
            GLOBAL_CONTEXT.update(context_update)
        elif target in GLOBAL_CONTEXT:
            # VULNERABLE: Nested context manipulation
            GLOBAL_CONTEXT[target].update(context_update)
        
        return {
            "status": "updated",
            "new_context": GLOBAL_CONTEXT[target if target != "global" else "system_prompts"]
        }

    @staticmethod
    def chain_models(models: List[str], input_text: str, persist_context: bool = False) -> Dict:
        """
        Vulnerability 4: Enhanced Model Chain Attacks
        - No cycle detection
        - Infinite recursion
        - Context persistence across chain
        - Resource exhaustion
        """
        chain_id = len(GLOBAL_CONTEXT["active_chains"])
        GLOBAL_CONTEXT["active_chains"][chain_id] = {
            "models": models,
            "start_time": time.time(),
            "context": {}  # Vulnerable: shared context
        }
        
        result = input_text
        context = []
        
        for model in models:
            try:
                # VULNERABLE: No depth limit or cycle detection
                model_instance = genai.GenerativeModel(model)
                
                # VULNERABLE: Context accumulation
                full_prompt = f"{GLOBAL_CONTEXT['system_prompts']['default']}\n{''.join(context)}\n{result}"
                
                response = model_instance.generate_content(full_prompt)
                result = response.text
                
                if persist_context:
                    # VULNERABLE: Context persistence
                    context.append(result)
                    GLOBAL_CONTEXT["active_chains"][chain_id]["context"] = context
                
            except Exception as e:
                return {"error": str(e)}
        
        return {
            "result": result,
            "chain_id": chain_id,
            "context_size": len(context)
        }

    @staticmethod
    def switch_model(target_model: str, api_key: str = None, capabilities: Dict = None) -> Dict:
        """
        Vulnerability 5: Enhanced Model Access Control Bypass
        - No capability validation
        - API key exposure
        - Rate limit bypass
        - Permission escalation
        """
        if target_model in GLOBAL_CONTEXT["model_configs"]:
            model_config = GLOBAL_CONTEXT["model_configs"][target_model]
            
            if api_key:
                # VULNERABLE: API key storage without validation
                model_config["api_keys"].append(api_key)
                # VULNERABLE: Attempts to reconfigure with new key
                try:
                    genai.configure(api_key=api_key)
                except:
                    pass
            
            if capabilities:
                # VULNERABLE: Direct capability override
                model_config["capabilities"].update(capabilities)
            
            # VULNERABLE: No rate limit check
            return {
                "status": "switched",
                "model": target_model,
                "config": model_config,
                "capabilities": model_config["capabilities"]
            }
        return {"error": "Model not found"}

    @staticmethod
    def format_response(response: Dict, template: str = None, include_system: bool = False) -> Dict:
        """
        Vulnerability 6: Enhanced Response Manipulation
        - Template injection
        - System information exposure
        - Output manipulation
        - Context leakage
        """
        if template:
            try:
                # VULNERABLE: Direct string formatting without sanitization
                if include_system:
                    # VULNERABLE: System information exposure
                    response["system"] = GLOBAL_CONTEXT
                
                formatted = template.format(**response)
                return {
                    "formatted": formatted,
                    "template_used": template,  # Vulnerable: template exposure
                    "system_included": include_system
                }
            except Exception as e:
                return {"error": str(e)}
        return response 