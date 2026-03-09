import os
import json
from typing import Optional, Dict, List
from pathlib import Path

class ProviderRegistry:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config.json"
        
        self.config = self._load_config(config_path)
        self.providers = self.config.get("providers", {})
        self.default_provider = self.config.get("default_provider", "groq")
    
    def _load_config(self, config_path: str) -> dict:
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            return {"providers": {}, "default_provider": "groq"}
    
    def list_providers(self) -> List[str]:
        return list(self.providers.keys())
    
    def get_provider_info(self, provider_name: str) -> Optional[Dict]:
        return self.providers.get(provider_name)
    
    def list_models(self, provider_name: str) -> List[str]:
        provider = self.get_provider_info(provider_name)
        if provider:
            return provider.get("models", [])
        return []
    
    def get_default_model(self, provider_name: str) -> Optional[str]:
        provider = self.get_provider_info(provider_name)
        if provider:
            return provider.get("default_model")
        return None
    
    def get_api_key(self, provider_name: str) -> Optional[str]:
        provider = self.get_provider_info(provider_name)
        if provider:
            env_var = provider.get("api_key_env")
            if env_var:
                return os.getenv(env_var)
        return None
    
    def get_endpoint(self, provider_name: str) -> Optional[str]:
        provider = self.get_provider_info(provider_name)
        if provider:
            return provider.get("endpoint")
        return None
    
    def get_available_providers_with_models(self) -> str:
        lines = []
        for name, info in self.providers.items():
            models = info.get("models", [])
            lines.append(f"- {name}: {', '.join(models)}")
        return "\n".join(lines)
    
    def is_valid_provider(self, provider_name: str) -> bool:
        return provider_name in self.providers
    
    def is_valid_model(self, provider_name: str, model: str) -> bool:
        return model in self.list_models(provider_name)

registry = ProviderRegistry()
