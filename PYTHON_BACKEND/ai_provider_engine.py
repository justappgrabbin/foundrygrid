"""
AI PROVIDER ENGINE - Python Backend
Universal AI provider selector with Claude, GPT, Gemini, Ollama support

Usage:
    engine = AIProviderEngine()
    engine.set_api_key('claude', 'sk-ant-...')
    engine.set_active_provider('claude')
    
    result = engine.generate("Write a haiku about consciousness")
    print(result['text'])
"""

import os
import json
import time
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class ProviderType(Enum):
    COMMERCIAL = "commercial"
    LOCAL = "local"
    CUSTOM = "custom"


@dataclass
class ModelConfig:
    id: str
    name: str
    cost: float  # Cost per 1K tokens


@dataclass
class ProviderConfig:
    id: str
    name: str
    type: ProviderType
    endpoint: str
    models: List[ModelConfig]
    default_model: str
    requires_key: bool
    key_name: Optional[str] = None
    
    
@dataclass
class GenerationResult:
    text: str
    model: str
    provider: str
    provider_name: str
    usage: Dict[str, int]
    cost: float
    response_time: float
    stop_reason: str
    used_fallback: bool = False


class AIProviderEngine:
    """Universal AI provider engine with multi-backend support"""
    
    def __init__(self):
        self.providers: Dict[str, ProviderConfig] = {}
        self.api_keys: Dict[str, str] = {}
        self.active_provider: Optional[Dict] = None
        self.fallback_chain: List[str] = []
        self.costs: Dict[str, Dict] = {}
        self.request_history: List[Dict] = []
        
        self._register_builtin_providers()
        
    def _register_builtin_providers(self):
        """Register Claude, GPT, Gemini, Ollama"""
        
        # Claude (Anthropic)
        self.register_provider(ProviderConfig(
            id='claude',
            name='Claude (Anthropic)',
            type=ProviderType.COMMERCIAL,
            endpoint='https://api.anthropic.com/v1/messages',
            models=[
                ModelConfig('claude-sonnet-4-20250514', 'Claude Sonnet 4', 0.003),
                ModelConfig('claude-opus-4-20250514', 'Claude Opus 4', 0.015),
                ModelConfig('claude-sonnet-3-5-20241022', 'Claude Sonnet 3.5', 0.003),
            ],
            default_model='claude-sonnet-4-20250514',
            requires_key=True,
            key_name='ANTHROPIC_API_KEY'
        ))
        
        # GPT (OpenAI)
        self.register_provider(ProviderConfig(
            id='openai',
            name='GPT (OpenAI)',
            type=ProviderType.COMMERCIAL,
            endpoint='https://api.openai.com/v1/chat/completions',
            models=[
                ModelConfig('gpt-4-turbo-preview', 'GPT-4 Turbo', 0.01),
                ModelConfig('gpt-4', 'GPT-4', 0.03),
                ModelConfig('gpt-3.5-turbo', 'GPT-3.5 Turbo', 0.0005),
            ],
            default_model='gpt-4-turbo-preview',
            requires_key=True,
            key_name='OPENAI_API_KEY'
        ))
        
        # Gemini (Google)
        self.register_provider(ProviderConfig(
            id='gemini',
            name='Gemini (Google)',
            type=ProviderType.COMMERCIAL,
            endpoint='https://generativelanguage.googleapis.com/v1/models',
            models=[
                ModelConfig('gemini-pro', 'Gemini Pro', 0.00025),
                ModelConfig('gemini-pro-vision', 'Gemini Pro Vision', 0.00025),
            ],
            default_model='gemini-pro',
            requires_key=True,
            key_name='GOOGLE_API_KEY'
        ))
        
        # Ollama (Local)
        self.register_provider(ProviderConfig(
            id='ollama',
            name='Ollama (Local)',
            type=ProviderType.LOCAL,
            endpoint='http://localhost:11434/api/generate',
            models=[
                ModelConfig('llama3.1:latest', 'Llama 3.1 (8B)', 0),
                ModelConfig('llama3.1:70b', 'Llama 3.1 (70B)', 0),
                ModelConfig('mistral:latest', 'Mistral 7B', 0),
                ModelConfig('mixtral:latest', 'Mixtral 8x7B', 0),
                ModelConfig('phi3:latest', 'Phi-3', 0),
                ModelConfig('tinyllama:latest', 'TinyLlama', 0),
            ],
            default_model='llama3.1:latest',
            requires_key=False,
            key_name=None
        ))
        
        print("✓ Registered 4 built-in providers (Claude, GPT, Gemini, Ollama)")
        
    def register_provider(self, config: ProviderConfig):
        """Register a new provider"""
        self.providers[config.id] = config
        
        # Initialize cost tracking
        if config.id not in self.costs:
            self.costs[config.id] = {
                'total_requests': 0,
                'total_tokens': 0,
                'total_cost': 0.0,
                'avg_response_time': 0.0
            }
            
    def set_api_key(self, provider_id: str, api_key: str):
        """Set API key for a provider"""
        if provider_id not in self.providers:
            raise ValueError(f"Unknown provider: {provider_id}")
        
        self.api_keys[provider_id] = api_key
        print(f"✓ API key set for {self.providers[provider_id].name}")
        
    def get_api_key(self, provider_id: str) -> Optional[str]:
        """Get API key (from memory or environment)"""
        # Check memory first
        if provider_id in self.api_keys:
            return self.api_keys[provider_id]
        
        # Try environment variable
        provider = self.providers.get(provider_id)
        if provider and provider.key_name:
            env_key = os.environ.get(provider.key_name)
            if env_key:
                self.api_keys[provider_id] = env_key
                return env_key
        
        return None
        
    def set_active_provider(self, provider_id: str, model_id: Optional[str] = None):
        """Set the active provider"""
        if provider_id not in self.providers:
            raise ValueError(f"Unknown provider: {provider_id}")
        
        provider = self.providers[provider_id]
        
        self.active_provider = {
            'id': provider_id,
            'config': provider,
            'model': model_id or provider.default_model
        }
        
        print(f"✓ Active provider: {provider.name} ({self.active_provider['model']})")
        
    def set_fallback_chain(self, provider_ids: List[str]):
        """Set fallback chain for redundancy"""
        self.fallback_chain = provider_ids
        print(f"✓ Fallback chain: {' → '.join(provider_ids)}")
        
    def test_provider(self, provider_id: str) -> bool:
        """Test if provider is available"""
        provider = self.providers.get(provider_id)
        if not provider:
            return False
        
        # Check API key requirement
        if provider.requires_key:
            api_key = self.get_api_key(provider_id)
            if not api_key:
                print(f"⚠️ {provider.name}: No API key")
                return False
        
        # For local providers, test endpoint
        if provider.type == ProviderType.LOCAL:
            try:
                response = requests.get(
                    provider.endpoint.replace('/api/generate', '/api/tags'),
                    timeout=2
                )
                return response.ok
            except:
                print(f"⚠️ {provider.name}: Not running locally")
                return False
        
        return True
        
    def auto_detect_provider(self) -> List[str]:
        """Auto-detect available providers"""
        available = []
        
        for provider_id in self.providers:
            if self.test_provider(provider_id):
                available.append(provider_id)
        
        print(f"✓ Available providers: {', '.join(available)}")
        
        # Set first available as active
        if available and not self.active_provider:
            self.set_active_provider(available[0])
        
        return available
        
    def generate(
        self,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 1.0,
        model: Optional[str] = None,
        use_fallback: bool = True
    ) -> GenerationResult:
        """Generate AI response using active provider"""
        
        if not self.active_provider:
            raise ValueError("No active provider. Call set_active_provider() first.")
        
        start_time = time.time()
        
        try:
            result = self._generate_with_provider(
                self.active_provider['id'],
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                model=model
            )
            
            result.response_time = time.time() - start_time
            self._track_usage(self.active_provider['id'], result)
            
            return result
            
        except Exception as error:
            print(f"Error with {self.active_provider['config'].name}: {error}")
            
            # Try fallback chain
            if use_fallback and self.fallback_chain:
                print("→ Trying fallback providers...")
                
                for fallback_id in self.fallback_chain:
                    if fallback_id == self.active_provider['id']:
                        continue
                    
                    try:
                        result = self._generate_with_provider(
                            fallback_id,
                            prompt,
                            max_tokens=max_tokens,
                            temperature=temperature,
                            model=model
                        )
                        
                        result.response_time = time.time() - start_time
                        result.used_fallback = True
                        self._track_usage(fallback_id, result)
                        
                        print(f"✓ Fallback successful: {self.providers[fallback_id].name}")
                        return result
                        
                    except Exception as fallback_error:
                        print(f"Fallback {fallback_id} failed: {fallback_error}")
                        continue
            
            raise Exception(f"All providers failed. Last error: {error}")
            
    def _generate_with_provider(
        self,
        provider_id: str,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 1.0,
        model: Optional[str] = None
    ) -> GenerationResult:
        """Internal: Generate with specific provider"""
        
        provider = self.providers[provider_id]
        model_id = model or provider.default_model
        api_key = self.get_api_key(provider_id)
        
        if provider.requires_key and not api_key:
            raise ValueError(f"{provider.name} requires API key")
        
        # Format request based on provider
        if provider_id == 'claude':
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            }
            body = {
                'model': model_id,
                'max_tokens': max_tokens,
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': temperature
            }
            
        elif provider_id == 'openai':
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            body = {
                'model': model_id,
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': max_tokens,
                'temperature': temperature
            }
            
        elif provider_id == 'gemini':
            headers = {'Content-Type': 'application/json'}
            endpoint = f"{provider.endpoint}/{model_id}:generateContent?key={api_key}"
            body = {
                'contents': [{'parts': [{'text': prompt}]}],
                'generationConfig': {
                    'maxOutputTokens': max_tokens,
                    'temperature': temperature
                }
            }
            
        elif provider_id == 'ollama':
            headers = {'Content-Type': 'application/json'}
            body = {
                'model': model_id,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': temperature,
                    'num_predict': max_tokens
                }
            }
            
        else:
            raise ValueError(f"Unsupported provider: {provider_id}")
        
        # Make request
        endpoint = provider.endpoint if provider_id != 'gemini' else endpoint
        response = requests.post(endpoint, headers=headers, json=body, timeout=60)
        
        if not response.ok:
            raise Exception(f"API error ({response.status_code}): {response.text}")
        
        data = response.json()
        
        # Parse response based on provider
        if provider_id == 'claude':
            text = data['content'][0]['text']
            usage = data['usage']
            stop_reason = data['stop_reason']
            
        elif provider_id == 'openai':
            text = data['choices'][0]['message']['content']
            usage = data['usage']
            stop_reason = data['choices'][0]['finish_reason']
            
        elif provider_id == 'gemini':
            text = data['candidates'][0]['content']['parts'][0]['text']
            usage = data.get('usageMetadata', {})
            stop_reason = data['candidates'][0]['finishReason']
            
        elif provider_id == 'ollama':
            text = data['response']
            usage = {
                'prompt_tokens': data.get('prompt_eval_count', 0),
                'completion_tokens': data.get('eval_count', 0),
                'total_tokens': (data.get('prompt_eval_count', 0) + 
                               data.get('eval_count', 0))
            }
            stop_reason = 'complete' if data.get('done') else 'length'
        
        # Calculate cost
        model_config = next((m for m in provider.models if m.id == model_id), None)
        cost = (usage.get('total_tokens', 0) / 1000 * model_config.cost) if model_config else 0
        
        return GenerationResult(
            text=text,
            model=model_id,
            provider=provider_id,
            provider_name=provider.name,
            usage=usage,
            cost=cost,
            response_time=0,  # Set by caller
            stop_reason=stop_reason
        )
        
    def _track_usage(self, provider_id: str, result: GenerationResult):
        """Track usage statistics"""
        stats = self.costs[provider_id]
        
        stats['total_requests'] += 1
        stats['total_tokens'] += result.usage.get('total_tokens', 0)
        stats['total_cost'] += result.cost
        
        # Update average response time
        n = stats['total_requests']
        prev_avg = stats['avg_response_time']
        stats['avg_response_time'] = (prev_avg * (n - 1) + result.response_time) / n
        
        # Store in history (keep last 100)
        self.request_history.append({
            'timestamp': time.time(),
            'provider': provider_id,
            'model': result.model,
            'tokens': result.usage.get('total_tokens', 0),
            'cost': result.cost,
            'response_time': result.response_time
        })
        
        if len(self.request_history) > 100:
            self.request_history.pop(0)
            
    def get_stats(self, provider_id: Optional[str] = None) -> Dict:
        """Get usage statistics"""
        if provider_id:
            return self.costs.get(provider_id, {})
        
        # Return all stats with provider names
        all_stats = {}
        for pid, stats in self.costs.items():
            all_stats[pid] = {
                **stats,
                'name': self.providers[pid].name
            }
        return all_stats
        
    def export_config(self) -> Dict:
        """Export configuration (without API keys)"""
        return {
            'active_provider': self.active_provider['id'] if self.active_provider else None,
            'active_model': self.active_provider['model'] if self.active_provider else None,
            'fallback_chain': self.fallback_chain
        }
        
    def import_config(self, config: Dict):
        """Import configuration"""
        if config.get('active_provider'):
            self.set_active_provider(
                config['active_provider'],
                config.get('active_model')
            )
        if config.get('fallback_chain'):
            self.set_fallback_chain(config['fallback_chain'])


# Example usage
if __name__ == '__main__':
    # Initialize engine
    engine = AIProviderEngine()
    
    # Auto-detect available providers
    available = engine.auto_detect_provider()
    
    # Or manually set provider
    # engine.set_api_key('claude', 'sk-ant-...')
    # engine.set_active_provider('claude')
    
    # Set fallback chain
    engine.set_fallback_chain(['claude', 'openai', 'gemini', 'ollama'])
    
    # Generate
    if available:
        result = engine.generate(
            "Write a haiku about consciousness and technology",
            max_tokens=500,
            temperature=0.7,
            use_fallback=True
        )
        
        print(f"\n✓ Generated by {result.provider_name} ({result.model})")
        print(f"\n{result.text}")
        print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"Usage: {result.usage.get('total_tokens', 0)} tokens")
        print(f"Cost: ${result.cost:.4f}")
        print(f"Time: {result.response_time:.2f}s")
        
        # Show stats
        print(f"\nAll stats:")
        for provider_id, stats in engine.get_stats().items():
            print(f"  {stats['name']}: {stats['total_requests']} req, ${stats['total_cost']:.4f}")
