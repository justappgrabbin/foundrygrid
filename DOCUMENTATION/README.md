# 🤖 AI Provider Engine + Self-Building System

**Universal AI backend selector with TRUE self-building capability**

Transform your Universal Builder from template-based to AI-powered generative building using Claude, GPT, Gemini, or Ollama.

---

## 🎯 What This Does

### **Problem Solved**
Your existing Universal Builder could only create apps from 9 predefined templates. This system adds **AI-powered code generation** so you can build ANYTHING from natural language descriptions.

### **Key Features**
- ✅ **Multi-Provider Support**: Claude, GPT, Gemini, Ollama, + custom
- ✅ **Automatic Fallback**: Tries providers in sequence if one fails
- ✅ **Cost Tracking**: Monitor usage and spending across all providers
- ✅ **API Key Management**: Secure storage with localStorage persistence
- ✅ **True Code Generation**: Creates new apps that don't exist in templates
- ✅ **Consciousness Integration**: Personalizes apps based on Human Design charts
- ✅ **Self-Improvement**: Learns from successful builds

---

## 📦 Files Included

### **Core Engine**
1. **`ai-provider-engine.js`** - Universal AI provider selector (JavaScript)
2. **`ai_provider_engine.py`** - Python backend version
3. **`ai-enabled-builder.js`** - Integration with Universal Builder

### **User Interfaces**
4. **`ai-provider-selector.html`** - Provider configuration & testing UI
5. **`ai-self-builder-demo.html`** - Complete self-building demo

---

## 🚀 Quick Start

### **Option 1: Web Interface (Easiest)**

1. **Open `ai-self-builder-demo.html` in browser**

2. **Configure AI Provider:**
   ```
   - Select provider (Claude, GPT, Gemini, or Ollama)
   - Enter API key (if required)
   - Click "Save API Key"
   ```

3. **Build Something:**
   ```
   Describe what you want → Click "Build App with AI" → Get working code
   ```

### **Option 2: JavaScript Integration**

```javascript
// Initialize
const builder = new AIEnabledBuilder();

await builder.initialize({
  preferredProvider: 'claude',
  apiKeys: {
    claude: 'sk-ant-...',
    openai: 'sk-...'
  },
  fallbackChain: ['claude', 'openai', 'ollama']
});

// Build from description
const result = await builder.buildFromDescription(
  "Create a consciousness tracker with gate activation visualization",
  {
    appType: 'app',
    framework: 'vanilla',
    userChart: { type: 'Manifestor', profile: '4/6' }
  }
);

console.log(result.html); // Working HTML/JS code
```

### **Option 3: Python Backend**

```python
from ai_provider_engine import AIProviderEngine

# Initialize
engine = AIProviderEngine()
engine.set_api_key('claude', 'sk-ant-...')
engine.set_active_provider('claude')

# Generate
result = engine.generate(
    "Write a React component for consciousness tracking",
    max_tokens=4000,
    use_fallback=True
)

print(result.text)  # Generated code
print(f"Cost: ${result.cost:.4f}")
```

---

## 🔧 Provider Configuration

### **Claude (Anthropic)**
```javascript
builder.aiEngine.setAPIKey('claude', 'sk-ant-api03-...');
builder.aiEngine.setActiveProvider('claude', 'claude-sonnet-4-20250514');
```
- **Best for**: Complex code generation, consciousness integration
- **Cost**: $0.003/1K tokens (Sonnet 4)
- **Get key**: https://console.anthropic.com/

### **GPT (OpenAI)**
```javascript
builder.aiEngine.setAPIKey('openai', 'sk-...');
builder.aiEngine.setActiveProvider('openai', 'gpt-4-turbo-preview');
```
- **Best for**: Quick iterations, standard apps
- **Cost**: $0.01/1K tokens (GPT-4 Turbo)
- **Get key**: https://platform.openai.com/api-keys

### **Gemini (Google)**
```javascript
builder.aiEngine.setAPIKey('gemini', 'AIza...');
builder.aiEngine.setActiveProvider('gemini', 'gemini-pro');
```
- **Best for**: Budget-friendly generation
- **Cost**: $0.00025/1K tokens
- **Get key**: https://makersuite.google.com/app/apikey

### **Ollama (Local)**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.1

# Run server
ollama serve
```
```javascript
builder.aiEngine.setActiveProvider('ollama', 'llama3.1:latest');
```
- **Best for**: Privacy, unlimited usage, no cost
- **Cost**: FREE (runs locally)
- **Setup**: https://ollama.com/

### **Custom Providers**
```javascript
builder.aiEngine.registerProvider({
  id: 'my-llm',
  name: 'My Custom LLM',
  type: 'custom',
  endpoint: 'https://api.my-llm.com/generate',
  models: [{ id: 'model-v1', name: 'Custom Model', cost: 0 }],
  defaultModel: 'model-v1',
  headers: (apiKey) => ({ 'Authorization': `Bearer ${apiKey}` }),
  formatRequest: (prompt, model, options) => ({
    prompt: prompt,
    max_tokens: options.maxTokens
  }),
  parseResponse: (data) => ({
    text: data.output,
    model: model,
    usage: { total_tokens: 0 },
    stopReason: 'complete'
  }),
  requiresKey: true,
  keyName: 'MY_LLM_API_KEY'
});
```

---

## 💡 Usage Examples

### **Example 1: Consciousness Tracker**
```javascript
const result = await builder.buildFromDescription(
  `Create an interactive tracker for the 64 Human Design gates.
  
  Features:
  - Visual grid showing all 64 gates
  - Click to activate/deactivate gates
  - Statistics showing most-used gates
  - Beautiful neon color scheme
  - Smooth animations on state changes
  - Save state to localStorage`,
  
  { appType: 'app', framework: 'vanilla' }
);

// Result contains working HTML file
document.body.innerHTML = result.html;
```

### **Example 2: Personalized for User**
```javascript
const userChart = {
  type: 'Generator',
  profile: '2/4',
  authority: 'sacral',
  activeGates: [1, 13, 25, 46]
};

const result = await builder.buildForConsciousnessPattern(
  userChart,
  'meditation timer'
);

// App will be designed specifically for Generator energy
```

### **Example 3: React Component**
```javascript
const component = await builder.buildReactComponent(
  `A chart visualization component that displays:
  - User's bodygraph with defined centers highlighted
  - Active gates shown with colors
  - Hoverable tooltips showing gate descriptions
  - Responsive layout`,
  
  userChart
);

// Result is production-ready React component
```

### **Example 4: Improve Existing Code**
```javascript
const improved = await builder.improveExistingCode(
  existingCode,
  [
    'Add dark mode toggle',
    'Make mobile-responsive',
    'Add localStorage persistence'
  ]
);
```

---

## 🔐 Security Notes

### **API Key Storage**
- Keys stored in browser localStorage (client-side only)
- Never sent to any server except the AI provider
- Clear with: `builder.aiEngine.clearAPIKey('claude')`

### **For Production**
1. **Use environment variables** for API keys
2. **Implement backend proxy** to hide keys from client
3. **Add rate limiting** to prevent abuse
4. **Monitor costs** with usage tracking

---

## 📊 Cost Tracking

### **View Statistics**
```javascript
const stats = builder.getStats();

console.log(stats.builds.total);        // Number of builds
console.log(stats.builds.totalCost);    // Total cost across all providers
console.log(stats.ai.claude.avgResponseTime); // Performance metrics
```

### **Export History**
```javascript
const history = builder.exportBuildHistory();
// Contains all builds with metadata (excluding full code)
```

---

## 🧪 Testing

### **Test Provider Availability**
```javascript
const available = await builder.aiEngine.autoDetectProvider();
// Returns: ['claude', 'ollama'] (example)
```

### **Test Generation**
```javascript
try {
  const result = await builder.aiEngine.generate(
    "Write a haiku about consciousness",
    { maxTokens: 100, temperature: 0.7 }
  );
  console.log(result.text);
} catch (error) {
  console.error('Provider failed:', error.message);
}
```

---

## 🛠️ Advanced Features

### **Fallback Chain**
```javascript
// Automatically try providers in sequence
builder.aiEngine.setFallbackChain(['claude', 'openai', 'gemini', 'ollama']);

// If Claude fails, tries OpenAI, then Gemini, then Ollama
const result = await builder.generate(prompt, { useFallback: true });
```

### **Iterative Building**
```javascript
// Build complex apps in multiple passes
const result = await builder.buildFromDescription(
  description,
  { iterative: true, maxTokens: 8000 }
);
```

### **Consciousness Integration**
```javascript
// Apps automatically adapt to user's HD chart
const result = await builder.buildFromDescription(
  "Create a decision-making tool",
  {
    userChart: {
      type: 'Projector',
      authority: 'emotional'
    }
  }
);
// Result: Tool designed for emotional wave decision-making
```

---

## 🔄 Integration with Existing Systems

### **With Universal Builder**
```javascript
// Use AI for complex cases, templates for simple ones
async function smartBuild(description) {
  const analysis = universalBuilder.analyzeUpload({name: 'desc.txt'}, description);
  
  if (analysis.confidence > 0.8) {
    // Use template (fast, free)
    return universalBuilder.buildFromDescription(description);
  } else {
    // Use AI (slower, costs money, but handles anything)
    return aiBuilder.buildFromDescription(description);
  }
}
```

### **With Foundry Core**
```javascript
// Generate glyphs for AI-built apps
const app = await builder.buildFromDescription(description);

const glyph = await foundry.createGlyph(
  app.html,
  { userId: 'user-123', tool: 'ai-builder/1.0.0' }
);

console.log(`App glyph: ${glyph.id}`);
```

---

## 🎨 Customization

### **Add Custom Prompts**
```javascript
// Modify prompt engineering
AIEnabledBuilder.prototype._buildPrompt = function(description, options) {
  return `
    BUILD INSTRUCTION:
    ${description}
    
    STYLE REQUIREMENTS:
    - Cyberpunk aesthetic
    - Neon colors (#00ff88, #ffaa00, #ff00ff)
    - Monospace fonts
    - Dark background
    
    TECHNICAL:
    - Framework: ${options.framework}
    - Single file
    - Production ready
  `;
};
```

### **Custom Validators**
```javascript
builder._validateGeneratedCode = function(code, options) {
  const errors = [];
  
  // Your custom validation logic
  if (!code.includes('consciousness')) {
    errors.push('Must reference consciousness');
  }
  
  return { valid: errors.length === 0, errors };
};
```

---

## 🐛 Troubleshooting

### **"No active provider" error**
```javascript
await builder.aiEngine.autoDetectProvider();
builder.aiEngine.setActiveProvider('claude'); // or openai, gemini, ollama
```

### **"API error (401)" - Invalid key**
```javascript
// Re-enter API key
builder.aiEngine.setAPIKey('claude', 'your-correct-key');
```

### **Ollama not connecting**
```bash
# Make sure Ollama is running
ollama serve

# Check models
ollama list

# Pull model if needed
ollama pull llama3.1
```

### **Generated code has errors**
```javascript
// Enable auto-fix
const result = await builder.buildFromDescription(
  description,
  { autoFix: true }  // Will attempt to regenerate if validation fails
);
```

---

## 📈 Performance Optimization

### **Reduce Costs**
1. **Use Ollama for development** (free, local)
2. **Use Gemini for production** (cheapest commercial)
3. **Cache common generations** (implement caching layer)
4. **Lower temperature** for deterministic outputs (0.3-0.5)

### **Improve Speed**
1. **Use faster models** (GPT-3.5 Turbo, gemini-pro)
2. **Reduce max_tokens** (1000-2000 for simple apps)
3. **Run Ollama locally** (no network latency)

---

## 🔮 Future Enhancements

Potential additions:
- **Multi-turn conversations** for complex apps
- **Code review & refinement** loops
- **A/B testing** of generated variations
- **User feedback integration** for learning
- **Template extraction** from successful builds
- **Collaborative building** with multiple AIs

---

## 📝 License

MIT License - Use freely in your projects

---

## 🤝 Contributing

To add a new provider:

```javascript
builder.aiEngine.registerProvider({
  id: 'new-provider',
  name: 'New Provider',
  type: 'commercial',
  endpoint: 'https://api.provider.com/v1/generate',
  models: [
    { id: 'model-1', name: 'Model 1', cost: 0.001 }
  ],
  defaultModel: 'model-1',
  headers: (apiKey) => ({ /* headers */ }),
  formatRequest: (prompt, model, options) => ({ /* request */ }),
  parseResponse: (data) => ({ /* response */ }),
  requiresKey: true,
  keyName: 'PROVIDER_API_KEY'
});
```

---

## 📧 Support

- **Issues**: Check troubleshooting section above
- **Questions**: Review code comments for detailed explanations
- **Custom integrations**: Modify `ai-enabled-builder.js`

---

**Built with 🤖 by the YOU-N-I-VERSE consciousness research team**

*Transform your builder from template-based to truly generative*
