/**
 * AI PROVIDER ENGINE
 * Universal backend selector for Claude, GPT, Gemini, Ollama, + Custom
 * 
 * Features:
 * - Auto-detection of available providers
 * - Fallback chain (try Claude -> GPT -> Gemini -> Ollama)
 * - User-configurable API keys
 * - Custom provider registration
 * - Type-safe responses
 * - Cost tracking per provider
 */

class AIProviderEngine {
  constructor() {
    this.providers = new Map();
    this.activeProvider = null;
    this.fallbackChain = [];
    this.costs = new Map();
    this.requestHistory = [];
    
    // Initialize built-in providers
    this.registerBuiltInProviders();
    
    console.log('🤖 AI Provider Engine initialized');
  }
  
  // ============================================
  // PROVIDER REGISTRATION
  // ============================================
  
  registerBuiltInProviders() {
    // Claude (Anthropic)
    this.registerProvider({
      id: 'claude',
      name: 'Claude (Anthropic)',
      type: 'commercial',
      endpoint: 'https://api.anthropic.com/v1/messages',
      models: [
        { id: 'claude-sonnet-4-20250514', name: 'Claude Sonnet 4', cost: 0.003 },
        { id: 'claude-opus-4-20250514', name: 'Claude Opus 4', cost: 0.015 },
        { id: 'claude-sonnet-3-5-20241022', name: 'Claude Sonnet 3.5', cost: 0.003 },
      ],
      defaultModel: 'claude-sonnet-4-20250514',
      headers: (apiKey) => ({
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      }),
      formatRequest: (prompt, model, options = {}) => ({
        model: model,
        max_tokens: options.maxTokens || 4000,
        messages: [{ role: 'user', content: prompt }],
        temperature: options.temperature || 1.0
      }),
      parseResponse: (data) => ({
        text: data.content[0].text,
        model: data.model,
        usage: data.usage,
        stopReason: data.stop_reason
      }),
      requiresKey: true,
      keyName: 'ANTHROPIC_API_KEY'
    });
    
    // GPT (OpenAI)
    this.registerProvider({
      id: 'openai',
      name: 'GPT (OpenAI)',
      type: 'commercial',
      endpoint: 'https://api.openai.com/v1/chat/completions',
      models: [
        { id: 'gpt-4-turbo-preview', name: 'GPT-4 Turbo', cost: 0.01 },
        { id: 'gpt-4', name: 'GPT-4', cost: 0.03 },
        { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', cost: 0.0005 },
      ],
      defaultModel: 'gpt-4-turbo-preview',
      headers: (apiKey) => ({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      }),
      formatRequest: (prompt, model, options = {}) => ({
        model: model,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: options.maxTokens || 4000,
        temperature: options.temperature || 1.0
      }),
      parseResponse: (data) => ({
        text: data.choices[0].message.content,
        model: data.model,
        usage: data.usage,
        stopReason: data.choices[0].finish_reason
      }),
      requiresKey: true,
      keyName: 'OPENAI_API_KEY'
    });
    
    // Gemini (Google)
    this.registerProvider({
      id: 'gemini',
      name: 'Gemini (Google)',
      type: 'commercial',
      endpoint: 'https://generativelanguage.googleapis.com/v1/models',
      models: [
        { id: 'gemini-pro', name: 'Gemini Pro', cost: 0.00025 },
        { id: 'gemini-pro-vision', name: 'Gemini Pro Vision', cost: 0.00025 },
      ],
      defaultModel: 'gemini-pro',
      headers: (apiKey) => ({
        'Content-Type': 'application/json'
      }),
      formatRequest: (prompt, model, options = {}) => ({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: {
          maxOutputTokens: options.maxTokens || 4000,
          temperature: options.temperature || 1.0
        }
      }),
      parseResponse: (data) => ({
        text: data.candidates[0].content.parts[0].text,
        model: 'gemini-pro',
        usage: data.usageMetadata,
        stopReason: data.candidates[0].finishReason
      }),
      requiresKey: true,
      keyName: 'GOOGLE_API_KEY',
      customEndpoint: (model, apiKey) => 
        `https://generativelanguage.googleapis.com/v1/models/${model}:generateContent?key=${apiKey}`
    });
    
    // Ollama (Local)
    this.registerProvider({
      id: 'ollama',
      name: 'Ollama (Local)',
      type: 'local',
      endpoint: 'http://localhost:11434/api/generate',
      models: [
        { id: 'llama3.1:latest', name: 'Llama 3.1 (8B)', cost: 0 },
        { id: 'llama3.1:70b', name: 'Llama 3.1 (70B)', cost: 0 },
        { id: 'mistral:latest', name: 'Mistral 7B', cost: 0 },
        { id: 'mixtral:latest', name: 'Mixtral 8x7B', cost: 0 },
        { id: 'phi3:latest', name: 'Phi-3', cost: 0 },
        { id: 'tinyllama:latest', name: 'TinyLlama', cost: 0 },
      ],
      defaultModel: 'llama3.1:latest',
      headers: () => ({
        'Content-Type': 'application/json'
      }),
      formatRequest: (prompt, model, options = {}) => ({
        model: model,
        prompt: prompt,
        stream: false,
        options: {
          temperature: options.temperature || 1.0,
          num_predict: options.maxTokens || 4000
        }
      }),
      parseResponse: (data) => ({
        text: data.response,
        model: data.model,
        usage: {
          prompt_tokens: data.prompt_eval_count,
          completion_tokens: data.eval_count,
          total_tokens: (data.prompt_eval_count || 0) + (data.eval_count || 0)
        },
        stopReason: data.done ? 'complete' : 'length'
      }),
      requiresKey: false,
      keyName: null
    });
  }
  
  registerProvider(config) {
    /**
     * Register a provider (built-in or custom)
     * 
     * @param {Object} config - Provider configuration
     * @param {string} config.id - Unique provider ID
     * @param {string} config.name - Display name
     * @param {string} config.type - 'commercial' | 'local' | 'custom'
     * @param {string} config.endpoint - API endpoint
     * @param {Array} config.models - Available models
     * @param {Function} config.headers - Header generator
     * @param {Function} config.formatRequest - Request formatter
     * @param {Function} config.parseResponse - Response parser
     * @param {boolean} config.requiresKey - Needs API key?
     * @param {string} config.keyName - Environment variable name for key
     */
    
    if (this.providers.has(config.id)) {
      console.warn(`⚠️ Provider ${config.id} already registered, overwriting`);
    }
    
    this.providers.set(config.id, config);
    console.log(`✓ Registered provider: ${config.name}`);
    
    // Initialize cost tracking
    if (!this.costs.has(config.id)) {
      this.costs.set(config.id, {
        totalRequests: 0,
        totalTokens: 0,
        totalCost: 0,
        avgResponseTime: 0
      });
    }
  }
  
  // ============================================
  // API KEY MANAGEMENT
  // ============================================
  
  setAPIKey(providerId, apiKey) {
    /**
     * Set API key for a provider
     * Stores in localStorage for persistence
     */
    const provider = this.providers.get(providerId);
    if (!provider) {
      throw new Error(`Unknown provider: ${providerId}`);
    }
    
    // Store in memory
    provider.apiKey = apiKey;
    
    // Persist to localStorage
    try {
      localStorage.setItem(`ai_provider_key_${providerId}`, apiKey);
      console.log(`✓ API key set for ${provider.name}`);
    } catch (e) {
      console.warn('Could not persist API key to localStorage:', e);
    }
  }
  
  getAPIKey(providerId) {
    /**
     * Get API key for provider (from memory or localStorage)
     */
    const provider = this.providers.get(providerId);
    if (!provider) return null;
    
    // Check memory first
    if (provider.apiKey) return provider.apiKey;
    
    // Try localStorage
    try {
      const stored = localStorage.getItem(`ai_provider_key_${providerId}`);
      if (stored) {
        provider.apiKey = stored;
        return stored;
      }
    } catch (e) {
      console.warn('Could not read from localStorage:', e);
    }
    
    // Try environment variable (if in Node.js context)
    if (typeof process !== 'undefined' && process.env) {
      const envKey = process.env[provider.keyName];
      if (envKey) return envKey;
    }
    
    return null;
  }
  
  clearAPIKey(providerId) {
    /**
     * Remove API key
     */
    const provider = this.providers.get(providerId);
    if (!provider) return;
    
    delete provider.apiKey;
    
    try {
      localStorage.removeItem(`ai_provider_key_${providerId}`);
      console.log(`✓ API key cleared for ${provider.name}`);
    } catch (e) {
      console.warn('Could not clear from localStorage:', e);
    }
  }
  
  // ============================================
  // PROVIDER SELECTION
  // ============================================
  
  async autoDetectProvider() {
    /**
     * Auto-detect which providers are available
     * Tests API keys and local endpoints
     */
    
    const available = [];
    
    for (const [id, provider] of this.providers) {
      const isAvailable = await this.testProvider(id);
      if (isAvailable) {
        available.push(id);
      }
    }
    
    console.log(`✓ Available providers: ${available.join(', ')}`);
    
    // Set active provider to first available
    if (available.length > 0) {
      this.setActiveProvider(available[0]);
    }
    
    return available;
  }
  
  async testProvider(providerId) {
    /**
     * Test if provider is available and working
     */
    const provider = this.providers.get(providerId);
    if (!provider) return false;
    
    // Check if requires API key
    if (provider.requiresKey) {
      const apiKey = this.getAPIKey(providerId);
      if (!apiKey) {
        console.log(`⚠️ ${provider.name}: No API key`);
        return false;
      }
    }
    
    // For local providers, test endpoint
    if (provider.type === 'local') {
      try {
        const response = await fetch(provider.endpoint.replace('/api/generate', '/api/tags'), {
          method: 'GET'
        });
        return response.ok;
      } catch (e) {
        console.log(`⚠️ ${provider.name}: Not running locally`);
        return false;
      }
    }
    
    // For commercial, assume available if has key
    return true;
  }
  
  setActiveProvider(providerId, modelId = null) {
    /**
     * Set the active provider
     */
    const provider = this.providers.get(providerId);
    if (!provider) {
      throw new Error(`Unknown provider: ${providerId}`);
    }
    
    this.activeProvider = {
      id: providerId,
      config: provider,
      model: modelId || provider.defaultModel
    };
    
    console.log(`✓ Active provider: ${provider.name} (${this.activeProvider.model})`);
  }
  
  setFallbackChain(providerIds) {
    /**
     * Set fallback chain for redundancy
     * Example: ['claude', 'openai', 'gemini', 'ollama']
     */
    this.fallbackChain = providerIds;
    console.log(`✓ Fallback chain: ${providerIds.join(' → ')}`);
  }
  
  // ============================================
  // GENERATION
  // ============================================
  
  async generate(prompt, options = {}) {
    /**
     * Generate AI response using active provider
     * 
     * @param {string} prompt - User prompt
     * @param {Object} options
     * @param {number} options.maxTokens - Max output tokens
     * @param {number} options.temperature - 0-2, creativity
     * @param {string} options.model - Override model
     * @param {boolean} options.useFallback - Try fallback on failure
     * @returns {Object} { text, model, usage, provider, cost }
     */
    
    if (!this.activeProvider) {
      throw new Error('No active provider. Call setActiveProvider() first.');
    }
    
    const startTime = Date.now();
    
    try {
      const result = await this._generateWithProvider(
        this.activeProvider.id,
        prompt,
        options
      );
      
      result.responseTime = Date.now() - startTime;
      this._trackUsage(this.activeProvider.id, result);
      
      return result;
      
    } catch (error) {
      console.error(`Error with ${this.activeProvider.config.name}:`, error.message);
      
      // Try fallback chain if enabled
      if (options.useFallback && this.fallbackChain.length > 0) {
        console.log('→ Trying fallback providers...');
        
        for (const fallbackId of this.fallbackChain) {
          if (fallbackId === this.activeProvider.id) continue; // Skip current
          
          try {
            const result = await this._generateWithProvider(
              fallbackId,
              prompt,
              options
            );
            
            result.responseTime = Date.now() - startTime;
            result.usedFallback = true;
            this._trackUsage(fallbackId, result);
            
            console.log(`✓ Fallback successful: ${this.providers.get(fallbackId).name}`);
            return result;
            
          } catch (fallbackError) {
            console.error(`Fallback ${fallbackId} failed:`, fallbackError.message);
            continue;
          }
        }
      }
      
      throw new Error(`All providers failed. Last error: ${error.message}`);
    }
  }
  
  async _generateWithProvider(providerId, prompt, options = {}) {
    /**
     * Internal: Generate with specific provider
     */
    const provider = this.providers.get(providerId);
    if (!provider) {
      throw new Error(`Unknown provider: ${providerId}`);
    }
    
    const model = options.model || provider.defaultModel;
    const apiKey = this.getAPIKey(providerId);
    
    if (provider.requiresKey && !apiKey) {
      throw new Error(`${provider.name} requires API key`);
    }
    
    // Format request
    const requestBody = provider.formatRequest(prompt, model, options);
    
    // Determine endpoint
    let endpoint = provider.endpoint;
    if (provider.customEndpoint) {
      endpoint = provider.customEndpoint(model, apiKey);
    }
    
    // Make request
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: provider.headers(apiKey),
      body: JSON.stringify(requestBody)
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error (${response.status}): ${errorText}`);
    }
    
    const data = await response.json();
    
    // Parse response
    const parsed = provider.parseResponse(data);
    
    // Calculate cost
    const modelConfig = provider.models.find(m => m.id === model);
    const cost = modelConfig ? 
      (parsed.usage?.total_tokens || 0) / 1000 * modelConfig.cost : 
      0;
    
    return {
      text: parsed.text,
      model: parsed.model,
      usage: parsed.usage,
      provider: providerId,
      providerName: provider.name,
      cost: cost,
      stopReason: parsed.stopReason
    };
  }
  
  // ============================================
  // USAGE TRACKING
  // ============================================
  
  _trackUsage(providerId, result) {
    /**
     * Track usage statistics
     */
    const stats = this.costs.get(providerId);
    if (!stats) return;
    
    stats.totalRequests++;
    stats.totalTokens += result.usage?.total_tokens || 0;
    stats.totalCost += result.cost || 0;
    
    // Update average response time
    const prevAvg = stats.avgResponseTime;
    const n = stats.totalRequests;
    stats.avgResponseTime = (prevAvg * (n - 1) + result.responseTime) / n;
    
    // Store in history
    this.requestHistory.push({
      timestamp: new Date().toISOString(),
      provider: providerId,
      model: result.model,
      tokens: result.usage?.total_tokens || 0,
      cost: result.cost || 0,
      responseTime: result.responseTime
    });
    
    // Keep only last 100 requests
    if (this.requestHistory.length > 100) {
      this.requestHistory.shift();
    }
  }
  
  getStats(providerId = null) {
    /**
     * Get usage statistics
     */
    if (providerId) {
      return this.costs.get(providerId);
    }
    
    // Return all stats
    const allStats = {};
    for (const [id, stats] of this.costs) {
      allStats[id] = {
        ...stats,
        name: this.providers.get(id).name
      };
    }
    return allStats;
  }
  
  // ============================================
  // UI HELPERS
  // ============================================
  
  getProviderList() {
    /**
     * Get list of all providers for UI
     */
    const list = [];
    for (const [id, provider] of this.providers) {
      const apiKey = this.getAPIKey(id);
      list.push({
        id: id,
        name: provider.name,
        type: provider.type,
        models: provider.models,
        defaultModel: provider.defaultModel,
        requiresKey: provider.requiresKey,
        hasKey: !!apiKey,
        isActive: this.activeProvider?.id === id
      });
    }
    return list;
  }
  
  exportConfig() {
    /**
     * Export configuration (without API keys)
     */
    return {
      activeProvider: this.activeProvider?.id,
      activeModel: this.activeProvider?.model,
      fallbackChain: this.fallbackChain,
      customProviders: Array.from(this.providers.values())
        .filter(p => p.type === 'custom')
        .map(p => ({
          id: p.id,
          name: p.name,
          endpoint: p.endpoint,
          models: p.models
        }))
    };
  }
  
  importConfig(config) {
    /**
     * Import configuration
     */
    if (config.activeProvider) {
      this.setActiveProvider(config.activeProvider, config.activeModel);
    }
    if (config.fallbackChain) {
      this.setFallbackChain(config.fallbackChain);
    }
    if (config.customProviders) {
      for (const provider of config.customProviders) {
        if (!this.providers.has(provider.id)) {
          // Would need full config to register
          console.warn(`Cannot import custom provider ${provider.id} - needs full config`);
        }
      }
    }
  }
}

// Make available globally
if (typeof window !== 'undefined') {
  window.AIProviderEngine = AIProviderEngine;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AIProviderEngine;
}
