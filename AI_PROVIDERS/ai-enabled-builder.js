/**
 * UNIVERSAL BUILDER + AI PROVIDER INTEGRATION
 * Connects AI backends to enable TRUE self-building capability
 * 
 * This module transforms Universal Builder from template-based
 * to AI-powered generative building.
 */

class AIEnabledBuilder {
  constructor() {
    // Initialize AI Provider Engine
    this.aiEngine = new AIProviderEngine();
    
    // Initialize Universal Builder (if available)
    this.universalBuilder = typeof UniversalBuilder !== 'undefined' 
      ? new UniversalBuilder({ overseer: { enforceProtocol: () => ({ valid: true }) } })
      : null;
    
    this.buildHistory = [];
    this.learningDatabase = new Map();
    
    console.log('🏗️ AI-Enabled Builder initialized');
  }
  
  // ============================================
  // SETUP & CONFIGURATION
  // ============================================
  
  async initialize(config = {}) {
    /**
     * Initialize with AI provider configuration
     * 
     * @param {Object} config
     * @param {string} config.preferredProvider - 'claude' | 'openai' | 'gemini' | 'ollama'
     * @param {Object} config.apiKeys - { claude: 'sk-...', openai: 'sk-...' }
     * @param {Array} config.fallbackChain - ['claude', 'openai', 'ollama']
     */
    
    // Set API keys
    if (config.apiKeys) {
      for (const [provider, key] of Object.entries(config.apiKeys)) {
        this.aiEngine.setAPIKey(provider, key);
      }
    }
    
    // Auto-detect providers
    await this.aiEngine.autoDetectProvider();
    
    // Set preferred provider if specified
    if (config.preferredProvider) {
      this.aiEngine.setActiveProvider(config.preferredProvider);
    }
    
    // Set fallback chain
    if (config.fallbackChain) {
      this.aiEngine.setFallbackChain(config.fallbackChain);
    } else {
      // Default fallback chain
      this.aiEngine.setFallbackChain(['claude', 'openai', 'gemini', 'ollama']);
    }
    
    console.log('✓ AI-Enabled Builder ready');
  }
  
  // ============================================
  // AI-POWERED APP GENERATION
  // ============================================
  
  async buildFromDescription(description, options = {}) {
    /**
     * Build app from natural language description using AI
     * 
     * @param {string} description - What the user wants to build
     * @param {Object} options
     * @param {string} options.appType - 'game' | 'app' | 'tool' | 'visualization'
     * @param {string} options.framework - 'react' | 'vanilla' | 'p5' | 'canvas'
     * @param {Object} options.userChart - Human Design chart data for personalization
     * @param {boolean} options.iterative - Build in multiple passes for complexity
     * @returns {Object} Generated app
     */
    
    console.log(`→ Building app from description using AI...`);
    
    // Construct prompt for AI
    const prompt = this._buildPrompt(description, options);
    
    try {
      // Generate code using AI
      const result = await this.aiEngine.generate(prompt, {
        maxTokens: options.iterative ? 8000 : 4000,
        temperature: 0.7,
        useFallback: true
      });
      
      // Extract code from AI response
      const code = this._extractCode(result.text);
      
      // Validate code
      const validation = this._validateGeneratedCode(code, options);
      
      if (!validation.valid) {
        console.warn('Generated code failed validation:', validation.errors);
        
        // Try again with corrections
        if (options.autoFix !== false) {
          return await this._fixAndRegenerate(description, options, validation.errors);
        }
      }
      
      // Store in build history
      const build = {
        id: `ai-build-${Date.now()}`,
        description: description,
        code: code,
        framework: options.framework || 'vanilla',
        aiProvider: result.providerName,
        aiModel: result.model,
        cost: result.cost,
        timestamp: Date.now(),
        validation: validation
      };
      
      this.buildHistory.push(build);
      
      // Learn from this build
      this._learnFromBuild(description, code, validation);
      
      console.log(`✓ App built successfully with ${result.providerName}`);
      
      return {
        app: build,
        html: code,
        metadata: {
          provider: result.providerName,
          model: result.model,
          cost: result.cost,
          tokens: result.usage.total_tokens
        }
      };
      
    } catch (error) {
      console.error('Failed to build app:', error);
      throw error;
    }
  }
  
  async buildReactComponent(componentSpec, chartData = null) {
    /**
     * Build a React component using AI
     * Specialized for consciousness-based interfaces
     */
    
    const prompt = `Create a React component based on the following specification:

${componentSpec}

${chartData ? `
Personalize the component for a user with the following consciousness data:
- Type: ${chartData.type}
- Profile: ${chartData.profile}
- Authority: ${chartData.authority}
- Centers: ${JSON.stringify(chartData.centers)}
` : ''}

Requirements:
- Single-file React component (JSX)
- Use Tailwind for styling
- Include useState/useEffect if needed
- Make it interactive and engaging
- Export as default

Return ONLY the code, wrapped in \`\`\`jsx code blocks.`;
    
    const result = await this.aiEngine.generate(prompt, {
      maxTokens: 6000,
      temperature: 0.8
    });
    
    return this._extractCode(result.text, 'jsx');
  }
  
  async buildHTMLArtifact(description, chartData = null) {
    /**
     * Build a complete HTML artifact (game, tool, visualization)
     */
    
    const prompt = `Create a complete, self-contained HTML file for:

${description}

${chartData ? `
Design it to resonate with a ${chartData.type} with ${chartData.profile} profile.
Their authority is ${chartData.authority}.
` : ''}

Requirements:
- Single HTML file (no external dependencies)
- Include inline CSS and JavaScript
- Make it beautiful and functional
- Use modern ES6+ JavaScript
- Add visual polish (animations, gradients, etc.)

Return ONLY the HTML code, wrapped in \`\`\`html code blocks.`;
    
    const result = await this.aiEngine.generate(prompt, {
      maxTokens: 8000,
      temperature: 0.9
    });
    
    return this._extractCode(result.text, 'html');
  }
  
  async improveExistingCode(code, improvements) {
    /**
     * Improve existing code using AI
     * 
     * @param {string} code - Existing code
     * @param {Array} improvements - List of requested improvements
     */
    
    const prompt = `Improve the following code:

\`\`\`
${code}
\`\`\`

Requested improvements:
${improvements.map((imp, i) => `${i + 1}. ${imp}`).join('\n')}

Return the improved code ONLY, maintaining all existing functionality while adding the improvements.`;
    
    const result = await this.aiEngine.generate(prompt, {
      maxTokens: 8000,
      temperature: 0.5
    });
    
    return this._extractCode(result.text);
  }
  
  async debugCode(code, errorMessage) {
    /**
     * Debug code using AI
     */
    
    const prompt = `Debug this code that's producing the following error:

Error: ${errorMessage}

Code:
\`\`\`
${code}
\`\`\`

Return the fixed code with the bug corrected.`;
    
    const result = await this.aiEngine.generate(prompt, {
      maxTokens: 8000,
      temperature: 0.3  // Lower temp for debugging
    });
    
    return this._extractCode(result.text);
  }
  
  // ============================================
  // CONSCIOUSNESS-AWARE GENERATION
  // ============================================
  
  async buildForConsciousnessPattern(pattern, appType) {
    /**
     * Build apps tailored to specific consciousness patterns
     * 
     * @param {Object} pattern - { type, profile, authority, gates, etc. }
     * @param {string} appType - What to build
     */
    
    const prompt = `Build a ${appType} specifically designed for someone with this consciousness pattern:

Type: ${pattern.type}
Profile: ${pattern.profile}
Authority: ${pattern.authority}
Defined Centers: ${pattern.definedCenters?.join(', ')}
Active Gates: ${pattern.activeGates?.join(', ')}

Design considerations:
- ${pattern.type === 'Manifestor' ? 'Enable initiating action without waiting' : ''}
- ${pattern.type === 'Generator' ? 'Create response-based interactions' : ''}
- ${pattern.type === 'Projector' ? 'Focus on recognition and guidance' : ''}
- ${pattern.type === 'Reflector' ? 'Emphasize environmental awareness' : ''}
- Authority: ${pattern.authority} (design decision-making flow accordingly)

Return a complete, working HTML file optimized for this consciousness pattern.`;
    
    const result = await this.aiEngine.generate(prompt, {
      maxTokens: 8000,
      temperature: 0.8
    });
    
    return this._extractCode(result.text, 'html');
  }
  
  // ============================================
  // PROMPT ENGINEERING
  // ============================================
  
  _buildPrompt(description, options) {
    /**
     * Build optimized prompt for code generation
     */
    
    const framework = options.framework || 'vanilla';
    const appType = options.appType || 'app';
    
    let prompt = `Create a ${appType} based on this description:

${description}

Technical requirements:
- Framework: ${framework}
- Single-file implementation
- Modern, clean code
- Responsive design
- Beautiful UI with gradients and animations`;
    
    if (framework === 'react') {
      prompt += `
- Use functional components with hooks
- Use Tailwind for styling (utility classes only)
- Export as default component`;
    } else if (framework === 'vanilla') {
      prompt += `
- Vanilla JavaScript (ES6+)
- Inline CSS in <style> tag
- Self-contained HTML file`;
    } else if (framework === 'p5') {
      prompt += `
- Use p5.js for graphics
- Include p5.js from CDN
- Implement setup() and draw()`;
    }
    
    if (options.userChart) {
      prompt += `

Personalization:
- Design for ${options.userChart.type} energy type
- Consider ${options.userChart.profile} profile characteristics
- Respect ${options.userChart.authority} decision-making`;
    }
    
    if (options.features) {
      prompt += `

Must include features:
${options.features.map((f, i) => `${i + 1}. ${f}`).join('\n')}`;
    }
    
    prompt += `

Return ONLY the code, wrapped in appropriate code blocks (\`\`\`html or \`\`\`jsx).
No explanations, just the working code.`;
    
    return prompt;
  }
  
  _extractCode(aiResponse, codeType = null) {
    /**
     * Extract code from AI response (handles markdown code blocks)
     */
    
    // Try to extract from code blocks
    const codeBlockRegex = /```(?:html|jsx|javascript|js|typescript|tsx)?\n([\s\S]*?)```/;
    const match = aiResponse.match(codeBlockRegex);
    
    if (match) {
      return match[1].trim();
    }
    
    // If no code blocks, return as-is (AI might have returned plain code)
    return aiResponse.trim();
  }
  
  _validateGeneratedCode(code, options) {
    /**
     * Validate AI-generated code
     */
    
    const errors = [];
    const warnings = [];
    
    // Basic checks
    if (!code || code.length < 50) {
      errors.push('Generated code is too short or empty');
    }
    
    if (options.framework === 'react') {
      if (!code.includes('export default')) {
        errors.push('React component missing export default');
      }
      if (!code.includes('function') && !code.includes('const')) {
        errors.push('React component missing function declaration');
      }
    } else if (options.framework === 'vanilla') {
      if (!code.includes('<html') && !code.includes('<!DOCTYPE')) {
        warnings.push('HTML file missing DOCTYPE or html tag');
      }
    }
    
    // Check for common issues
    if (code.includes('YOUR_API_KEY') || code.includes('INSERT_KEY_HERE')) {
      warnings.push('Code contains placeholder API key');
    }
    
    return {
      valid: errors.length === 0,
      errors: errors,
      warnings: warnings
    };
  }
  
  async _fixAndRegenerate(description, options, errors) {
    /**
     * Attempt to fix validation errors by regenerating
     */
    
    console.log('→ Attempting to fix errors and regenerate...');
    
    const fixPrompt = `The previous code had these errors:
${errors.join('\n')}

Please regenerate the code for:
${description}

Fix the errors and return working code.`;
    
    const result = await this.aiEngine.generate(fixPrompt, {
      maxTokens: 6000,
      temperature: 0.5  // Lower temp for fixing
    });
    
    const code = this._extractCode(result.text);
    
    return {
      app: {
        id: `ai-build-${Date.now()}`,
        description: description,
        code: code,
        aiProvider: result.providerName,
        wasFixed: true
      },
      html: code
    };
  }
  
  _learnFromBuild(description, code, validation) {
    /**
     * Learn from successful builds to improve future prompts
     */
    
    const keywords = this._extractKeywords(description);
    
    for (const keyword of keywords) {
      if (!this.learningDatabase.has(keyword)) {
        this.learningDatabase.set(keyword, {
          count: 0,
          successfulPatterns: [],
          commonIssues: []
        });
      }
      
      const entry = this.learningDatabase.get(keyword);
      entry.count++;
      
      if (validation.valid) {
        entry.successfulPatterns.push({
          description: description.substring(0, 100),
          codeLength: code.length
        });
      } else {
        entry.commonIssues.push(...validation.errors);
      }
    }
  }
  
  _extractKeywords(text) {
    /**
     * Extract keywords from description
     */
    const commonWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for']);
    return text
      .toLowerCase()
      .split(/\W+/)
      .filter(word => word.length > 3 && !commonWords.has(word))
      .slice(0, 10);
  }
  
  // ============================================
  // UTILITIES
  // ============================================
  
  getProviderList() {
    return this.aiEngine.getProviderList();
  }
  
  getStats() {
    return {
      ai: this.aiEngine.getStats(),
      builds: {
        total: this.buildHistory.length,
        successful: this.buildHistory.filter(b => b.validation?.valid).length,
        totalCost: this.buildHistory.reduce((sum, b) => sum + (b.cost || 0), 0)
      }
    };
  }
  
  exportBuildHistory() {
    return this.buildHistory.map(build => ({
      ...build,
      code: undefined  // Don't export full code in summary
    }));
  }
}

// Make available globally
if (typeof window !== 'undefined') {
  window.AIEnabledBuilder = AIEnabledBuilder;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AIEnabledBuilder;
}
