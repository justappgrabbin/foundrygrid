/**
 * TINYLLAMA WEBLLM PROVIDER
 * Baked-in local AI that runs in browser (no downloads!)
 * Uses WebLLM to run TinyLlama directly in the browser
 * 
 * This is the DEFAULT provider - always available, always free
 * Users can upgrade to Claude/GPT/Gemini if they want
 */

class TinyLlamaWebProvider {
  constructor() {
    this.engine = null;
    this.ready = false;
    this.loadingProgress = 0;
    this.modelId = 'TinyLlama-1.1B-Chat-v1.0-q4f16_1';
    
    console.log('🦙 TinyLlama WebLLM Provider initializing...');
  }
  
  async initialize(onProgress = null) {
    /**
     * Load TinyLlama into browser memory
     * This happens automatically - no user downloads required!
     */
    
    try {
      // Import WebLLM from CDN
      const { CreateWebWorkerMLCEngine } = await import(
        'https://esm.run/@mlc-ai/web-llm'
      );
      
      // Create engine with progress callback
      this.engine = await CreateWebWorkerMLCEngine(
        this.modelId,
        {
          initProgressCallback: (progress) => {
            this.loadingProgress = progress.progress;
            if (onProgress) {
              onProgress(progress);
            }
            console.log(`🦙 Loading: ${(progress.progress * 100).toFixed(1)}%`);
          }
        }
      );
      
      this.ready = true;
      console.log('✓ TinyLlama ready! Running locally in your browser.');
      
      return true;
      
    } catch (error) {
      console.error('Failed to initialize TinyLlama:', error);
      this.ready = false;
      return false;
    }
  }
  
  async generate(prompt, options = {}) {
    /**
     * Generate response using TinyLlama
     * 
     * @param {string} prompt - User prompt
     * @param {Object} options
     * @param {number} options.maxTokens - Max tokens (default: 512)
     * @param {number} options.temperature - 0-2 (default: 1.0)
     * @returns {Object} { text, usage }
     */
    
    if (!this.ready) {
      throw new Error('TinyLlama not ready. Call initialize() first.');
    }
    
    const maxTokens = options.maxTokens || 512;
    const temperature = options.temperature || 1.0;
    
    const startTime = Date.now();
    
    try {
      // Generate response
      const response = await this.engine.chat.completions.create({
        messages: [{ role: 'user', content: prompt }],
        temperature: temperature,
        max_gen_len: maxTokens
      });
      
      const text = response.choices[0].message.content;
      const responseTime = Date.now() - startTime;
      
      return {
        text: text,
        model: this.modelId,
        usage: {
          prompt_tokens: 0, // WebLLM doesn't report this
          completion_tokens: 0,
          total_tokens: 0
        },
        provider: 'tinyllama-web',
        providerName: 'TinyLlama (Browser)',
        cost: 0, // Always free!
        responseTime: responseTime,
        stopReason: 'complete'
      };
      
    } catch (error) {
      console.error('TinyLlama generation error:', error);
      throw error;
    }
  }
  
  async generateStream(prompt, options = {}, onChunk = null) {
    /**
     * Stream generation for real-time output
     */
    
    if (!this.ready) {
      throw new Error('TinyLlama not ready. Call initialize() first.');
    }
    
    const chunks = [];
    const completion = await this.engine.chat.completions.create({
      messages: [{ role: 'user', content: prompt }],
      temperature: options.temperature || 1.0,
      max_gen_len: options.maxTokens || 512,
      stream: true
    });
    
    for await (const chunk of completion) {
      const delta = chunk.choices[0]?.delta?.content || '';
      if (delta && onChunk) {
        onChunk(delta);
      }
      chunks.push(delta);
    }
    
    return {
      text: chunks.join(''),
      model: this.modelId,
      provider: 'tinyllama-web',
      cost: 0
    };
  }
  
  unload() {
    /**
     * Unload model from memory (if user wants to free RAM)
     */
    if (this.engine) {
      this.engine.unload();
      this.ready = false;
      console.log('🦙 TinyLlama unloaded from memory');
    }
  }
  
  getStatus() {
    return {
      ready: this.ready,
      loadingProgress: this.loadingProgress,
      model: this.modelId,
      memoryUsage: this.ready ? 'Active (~1.5GB)' : 'Not loaded'
    };
  }
}

// ==================================================================
// INTEGRATION WITH AI PROVIDER ENGINE
// ==================================================================

/**
 * Add TinyLlama as the DEFAULT provider in AIProviderEngine
 * This gets registered automatically - users don't need to do anything
 */

// Extend AIProviderEngine to include TinyLlama
if (typeof AIProviderEngine !== 'undefined') {
  
  // Store original init
  const originalRegisterBuiltIn = AIProviderEngine.prototype._registerBuiltInProviders;
  
  // Override to add TinyLlama
  AIProviderEngine.prototype._registerBuiltInProviders = function() {
    // Call original
    originalRegisterBuiltIn.call(this);
    
    // Add TinyLlama as first option
    this.registerProvider({
      id: 'tinyllama-web',
      name: 'TinyLlama (Browser) - FREE',
      type: 'local',
      endpoint: 'browser://webllm',
      models: [
        { 
          id: 'TinyLlama-1.1B-Chat-v1.0-q4f16_1', 
          name: 'TinyLlama 1.1B (Browser)', 
          cost: 0 
        }
      ],
      defaultModel: 'TinyLlama-1.1B-Chat-v1.0-q4f16_1',
      headers: () => ({}),
      formatRequest: () => ({}),
      parseResponse: (data) => data, // Handled by provider
      requiresKey: false,
      keyName: null,
      
      // Custom fields
      webLLMProvider: new TinyLlamaWebProvider(),
      needsInit: true,
      isDefault: true
    });
    
    console.log('✓ TinyLlama registered as DEFAULT provider');
  };
  
  // Override generate to handle TinyLlama specially
  const originalGenerate = AIProviderEngine.prototype._generateWithProvider;
  
  AIProviderEngine.prototype._generateWithProvider = async function(
    providerId,
    prompt,
    maxTokens = 4000,
    temperature = 1.0,
    model = null
  ) {
    const provider = this.providers.get(providerId);
    
    // If it's TinyLlama, use the WebLLM provider
    if (providerId === 'tinyllama-web') {
      const webLLM = provider.webLLMProvider;
      
      // Auto-initialize if needed
      if (!webLLM.ready && provider.needsInit) {
        console.log('🦙 First use - initializing TinyLlama...');
        await webLLM.initialize((progress) => {
          console.log(`Loading: ${(progress.progress * 100).toFixed(1)}%`);
        });
        provider.needsInit = false;
      }
      
      // Generate
      return await webLLM.generate(prompt, { maxTokens, temperature });
    }
    
    // Otherwise use original logic
    return originalGenerate.call(this, providerId, prompt, maxTokens, temperature, model);
  };
  
  // Override test provider for TinyLlama
  const originalTestProvider = AIProviderEngine.prototype.testProvider;
  
  AIProviderEngine.prototype.testProvider = async function(providerId) {
    if (providerId === 'tinyllama-web') {
      // TinyLlama is always available in browser
      return typeof window !== 'undefined';
    }
    return originalTestProvider.call(this, providerId);
  };
}

// ==================================================================
// STANDALONE USAGE (if not using AIProviderEngine)
// ==================================================================

async function useTinyLlama() {
  const llama = new TinyLlamaWebProvider();
  
  // Initialize (first time only - takes ~30 seconds)
  await llama.initialize((progress) => {
    console.log(`Loading model: ${(progress.progress * 100).toFixed(1)}%`);
  });
  
  // Generate
  const result = await llama.generate(
    "Write a haiku about consciousness",
    { maxTokens: 100, temperature: 0.7 }
  );
  
  console.log(result.text);
}

// Export
if (typeof window !== 'undefined') {
  window.TinyLlamaWebProvider = TinyLlamaWebProvider;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = TinyLlamaWebProvider;
}
