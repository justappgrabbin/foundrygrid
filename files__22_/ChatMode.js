// ChatMode.js - Text analysis with personality responses

class ChatMode {
    constructor(projector) {
        this.projector = projector;
        this.canvas = projector.canvas;
        this.ctx = projector.ctx;
        
        // State
        this.messages = [];
        this.selectedTone = 'venom';
        this.inputContainer = null;
        this.toneSelector = null;
        
        // Scroll
        this.scrollOffset = 0;
        this.maxScroll = 0;
    }
    
    enter() {
        console.log('💬 Entering Chat Mode');
        this.createUI();
    }
    
    exit() {
        console.log('💬 Exiting Chat Mode');
        this.removeUI();
    }
    
    createUI() {
        // Input container
        this.inputContainer = document.createElement('div');
        this.inputContainer.style.cssText = `
            position: absolute;
            bottom: 120px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 800px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        `;
        
        // Tone selector
        this.toneSelector = document.createElement('div');
        this.toneSelector.style.cssText = `
            display: flex;
            gap: 8px;
            justify-content: center;
            flex-wrap: wrap;
        `;
        
        const tones = ['venom', 'prime', 'echo', 'dream', 'softcore'];
        const toneEmojis = {
            venom: '🔥',
            prime: '⚙️',
            echo: '🌊',
            dream: '✨',
            softcore: '🌱'
        };
        
        tones.forEach(tone => {
            const btn = document.createElement('button');
            btn.textContent = `${toneEmojis[tone]} ${tone}`;
            btn.className = tone === this.selectedTone ? 'tone-btn-active' : 'tone-btn-inactive';
            btn.style.cssText = `
                padding: 8px 16px;
                border-radius: 20px;
                border: none;
                cursor: pointer;
                font-size: 13px;
                font-weight: 500;
                text-transform: capitalize;
                transition: all 0.3s;
                ${tone === this.selectedTone 
                    ? 'background: linear-gradient(135deg, #667eea, #764ba2); color: white;'
                    : 'background: rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.6);'
                }
            `;
            
            btn.addEventListener('click', () => {
                this.selectedTone = tone;
                this.toneSelector.querySelectorAll('button').forEach(b => {
                    b.style.background = 'rgba(255, 255, 255, 0.1)';
                    b.style.color = 'rgba(255, 255, 255, 0.6)';
                });
                btn.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
                btn.style.color = 'white';
            });
            
            this.toneSelector.appendChild(btn);
        });
        
        // Textarea
        const textarea = document.createElement('textarea');
        textarea.placeholder = 'Write anything... your thoughts, feelings, questions...';
        textarea.style.cssText = `
            width: 100%;
            height: 100px;
            padding: 20px;
            background: rgba(26, 26, 46, 0.95);
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 15px;
            color: white;
            font-size: 16px;
            font-family: Inter, sans-serif;
            resize: none;
            backdrop-filter: blur(15px);
        `;
        
        textarea.addEventListener('focus', () => {
            textarea.style.borderColor = 'rgba(102, 126, 234, 0.8)';
        });
        
        textarea.addEventListener('blur', () => {
            textarea.style.borderColor = 'rgba(102, 126, 234, 0.3)';
        });
        
        // Analyze button
        const analyzeBtn = document.createElement('button');
        analyzeBtn.textContent = 'Analyze Consciousness';
        analyzeBtn.style.cssText = `
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            border-radius: 12px;
            color: white;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.3s;
            align-self: center;
        `;
        
        analyzeBtn.addEventListener('mouseenter', () => {
            analyzeBtn.style.transform = 'translateY(-2px)';
            analyzeBtn.style.boxShadow = '0 10px 30px rgba(102, 126, 234, 0.4)';
        });
        
        analyzeBtn.addEventListener('mouseleave', () => {
            analyzeBtn.style.transform = 'translateY(0)';
            analyzeBtn.style.boxShadow = 'none';
        });
        
        analyzeBtn.addEventListener('click', async () => {
            const text = textarea.value.trim();
            if (!text) return;
            
            this.projector.showLoading(true);
            
            try {
                const response = await fetch(`${this.projector.API_URL}/analyze`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        text: text,
                        tone: this.selectedTone,
                        include_technical: false
                    })
                });
                
                const data = await response.json();
                
                // Update state
                this.projector.updateUserState(data.state);
                
                // Add messages
                this.messages.push({
                    type: 'user',
                    text: text,
                    timestamp: Date.now()
                });
                
                this.messages.push({
                    type: 'assistant',
                    text: data.response,
                    timestamp: Date.now(),
                    coordinate: data.state.coordinate_string
                });
                
                // Clear input
                textarea.value = '';
                
                // Update scroll
                this.maxScroll = Math.max(0, this.messages.length * 120 - this.canvas.height + 400);
                this.scrollOffset = this.maxScroll;
                
            } catch (error) {
                console.error('Analysis failed:', error);
                this.messages.push({
                    type: 'error',
                    text: `Error: ${error.message}`,
                    timestamp: Date.now()
                });
            } finally {
                this.projector.showLoading(false);
            }
        });
        
        // Assemble UI
        this.inputContainer.appendChild(this.toneSelector);
        this.inputContainer.appendChild(textarea);
        this.inputContainer.appendChild(analyzeBtn);
        
        document.getElementById('ui-overlay').appendChild(this.inputContainer);
    }
    
    removeUI() {
        if (this.inputContainer) {
            this.inputContainer.remove();
            this.inputContainer = null;
        }
    }
    
    render(ctx) {
        // Background gradient
        this.projector.drawGradientBackground('#1a1a2e', '#0f0f1e');
        
        // Title
        this.projector.drawText('💬 Chat Mode', 
            this.canvas.width / 2, 
            200, 
            { 
                font: 'bold 36px Inter', 
                color: '#667eea', 
                align: 'center',
                shadow: true
            }
        );
        
        // Messages
        if (this.messages.length === 0) {
            this.projector.drawText(
                'Start a conversation to analyze your consciousness...',
                this.canvas.width / 2,
                this.canvas.height / 2 - 100,
                {
                    font: '20px Inter',
                    color: '#606070',
                    align: 'center'
                }
            );
        } else {
            this.renderMessages(ctx);
        }
        
        // Probability visualization (if we have state)
        if (this.projector.userState) {
            this.renderProbabilityBars(ctx);
        }
    }
    
    renderMessages(ctx) {
        const messageWidth = Math.min(700, this.canvas.width - 100);
        const x = (this.canvas.width - messageWidth) / 2;
        let y = 280 - this.scrollOffset;
        
        this.messages.forEach((msg, index) => {
            // Skip if off-screen
            if (y + 100 < 0 || y > this.canvas.height) {
                y += 120;
                return;
            }
            
            // Message bubble background
            ctx.fillStyle = msg.type === 'user' 
                ? 'rgba(102, 126, 234, 0.2)' 
                : 'rgba(0, 0, 0, 0.5)';
            ctx.fillRect(x, y, messageWidth, 100);
            
            // Border
            ctx.strokeStyle = msg.type === 'user' 
                ? 'rgba(102, 126, 234, 0.5)' 
                : 'rgba(255, 255, 255, 0.1)';
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, messageWidth, 100);
            
            // Message text (wrapped)
            ctx.fillStyle = '#e0e0e0';
            ctx.font = '16px Inter';
            ctx.textAlign = 'left';
            
            const words = msg.text.split(' ');
            let line = '';
            let lineY = y + 25;
            const maxWidth = messageWidth - 40;
            
            for (let word of words) {
                const testLine = line + word + ' ';
                const metrics = ctx.measureText(testLine);
                
                if (metrics.width > maxWidth && line.length > 0) {
                    ctx.fillText(line, x + 20, lineY);
                    line = word + ' ';
                    lineY += 22;
                    
                    if (lineY > y + 80) break; // Max 3 lines
                } else {
                    line = testLine;
                }
            }
            ctx.fillText(line, x + 20, lineY);
            
            y += 120;
        });
    }
    
    renderProbabilityBars(ctx) {
        const probs = this.projector.userState.blended_probabilities;
        const barWidth = 250;
        const barHeight = 25;
        const x = this.canvas.width - barWidth - 50;
        let y = 200;
        
        // Title
        ctx.fillStyle = '#a0a0b0';
        ctx.font = 'bold 14px Inter';
        ctx.textAlign = 'right';
        ctx.fillText('PROBABILITY DISTRIBUTION', x + barWidth, y - 10);
        
        // Sort by value
        const sorted = Object.entries(probs).sort((a, b) => b[1] - a[1]);
        
        sorted.forEach(([dimension, value]) => {
            // Label
            ctx.fillStyle = '#e0e0e0';
            ctx.font = '13px Inter';
            ctx.textAlign = 'left';
            ctx.fillText(dimension, x, y + 17);
            
            // Bar background
            ctx.fillStyle = '#2a2a3e';
            ctx.fillRect(x + 100, y, barWidth - 100, barHeight);
            
            // Bar fill
            const gradient = ctx.createLinearGradient(x + 100, 0, x + barWidth, 0);
            gradient.addColorStop(0, '#667eea');
            gradient.addColorStop(1, '#764ba2');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 100, y, (barWidth - 100) * value, barHeight);
            
            // Percentage
            ctx.fillStyle = '#667eea';
            ctx.font = 'bold 13px Inter';
            ctx.textAlign = 'right';
            ctx.fillText(`${(value * 100).toFixed(0)}%`, x + barWidth + 35, y + 17);
            
            y += 35;
        });
    }
    
    onStateUpdate(state) {
        // React to state updates
        console.log('Chat mode received state update:', state.coordinate_string);
    }
    
    onResize(width, height) {
        // Handle canvas resize
        this.maxScroll = Math.max(0, this.messages.length * 120 - height + 400);
    }
}
