// PlayMode.js - GameGAN behavioral prediction + Loopbreaker gaming

class PlayMode {
    constructor(projector) {
        this.projector = projector;
        this.canvas = projector.canvas;
        this.ctx = projector.ctx;
        
        // Sub-modes
        this.currentSubMode = 'prediction'; // 'prediction' or 'loopbreaker'
        this.subModeUI = null;
        
        // Animation
        this.particles = [];
        this.time = 0;
    }
    
    enter() {
        console.log('🎮 Entering Play Mode');
        this.createUI();
        this.initializeParticles();
    }
    
    exit() {
        console.log('🎮 Exiting Play Mode');
        this.removeUI();
    }
    
    createUI() {
        this.subModeUI = document.createElement('div');
        this.subModeUI.style.cssText = `
            position: absolute;
            top: 200px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 20px;
        `;
        
        const predictionBtn = this.createSubModeButton(
            '🎯 GameGAN Prediction',
            'prediction'
        );
        
        const loopbreakerBtn = this.createSubModeButton(
            '🎲 Loopbreaker Game',
            'loopbreaker'
        );
        
        this.subModeUI.appendChild(predictionBtn);
        this.subModeUI.appendChild(loopbreakerBtn);
        
        document.getElementById('ui-overlay').appendChild(this.subModeUI);
    }
    
    createSubModeButton(text, mode) {
        const btn = document.createElement('button');
        btn.textContent = text;
        btn.style.cssText = `
            padding: 20px 40px;
            background: ${mode === this.currentSubMode 
                ? 'linear-gradient(135deg, #667eea, #764ba2)' 
                : 'rgba(255, 255, 255, 0.1)'};
            border: 2px solid ${mode === this.currentSubMode 
                ? 'transparent' 
                : 'rgba(255, 255, 255, 0.2)'};
            border-radius: 15px;
            color: white;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        `;
        
        btn.addEventListener('click', () => {
            this.currentSubMode = mode;
            this.removeUI();
            this.createUI();
        });
        
        return btn;
    }
    
    removeUI() {
        if (this.subModeUI) {
            this.subModeUI.remove();
            this.subModeUI = null;
        }
    }
    
    initializeParticles() {
        this.particles = [];
        for (let i = 0; i < 50; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                size: Math.random() * 3 + 1,
                alpha: Math.random() * 0.5 + 0.2
            });
        }
    }
    
    render(ctx) {
        // Animated background
        this.projector.drawGradientBackground('#0f0f1e', '#1a1a2e');
        
        // Update and draw particles
        this.time += 0.016;
        this.particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            
            if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;
            
            ctx.fillStyle = `rgba(102, 126, 234, ${p.alpha})`;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        
        // Title
        this.projector.drawText(
            '🎮 Play Mode',
            this.canvas.width / 2,
            150,
            {
                font: 'bold 48px Inter',
                color: '#667eea',
                align: 'center',
                shadow: true
            }
        );
        
        // Current sub-mode content
        if (this.currentSubMode === 'prediction') {
            this.renderPredictionMode(ctx);
        } else {
            this.renderLoopbreakerMode(ctx);
        }
        
        // Instructions
        this.projector.drawText(
            'GameGAN and Loopbreaker modules will render here',
            this.canvas.width / 2,
            this.canvas.height - 100,
            {
                font: '16px Inter',
                color: '#606070',
                align: 'center'
            }
        );
    }
    
    renderPredictionMode(ctx) {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2 + 50;
        
        // GameGAN placeholder
        this.projector.drawText(
            '🎯 GameGAN Behavioral Prediction',
            centerX,
            centerY - 100,
            {
                font: 'bold 28px Inter',
                color: '#ffffff',
                align: 'center'
            }
        );
        
        this.projector.drawText(
            '"If I do X, what is the probability of Y outcome?"',
            centerX,
            centerY - 50,
            {
                font: '18px Inter',
                color: '#a0a0b0',
                align: 'center'
            }
        );
        
        // Placeholder visualization
        ctx.strokeStyle = 'rgba(102, 126, 234, 0.5)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(centerX, centerY + 50, 80, 0, Math.PI * 2);
        ctx.stroke();
        
        this.projector.drawText(
            'Decision Simulation Engine',
            centerX,
            centerY + 50,
            {
                font: '16px Inter',
                color: '#667eea',
                align: 'center',
                baseline: 'middle'
            }
        );
    }
    
    renderLoopbreakerMode(ctx) {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2 + 50;
        
        // Loopbreaker placeholder
        this.projector.drawText(
            '🎲 Loopbreaker Multiplayer',
            centerX,
            centerY - 100,
            {
                font: 'bold 28px Inter',
                color: '#ffffff',
                align: 'center'
            }
        );
        
        this.projector.drawText(
            'Play as your consciousness type • Team dynamics • Real-time strategy',
            centerX,
            centerY - 50,
            {
                font: '18px Inter',
                color: '#a0a0b0',
                align: 'center'
            }
        );
        
        // Placeholder game board
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                const x = centerX - 120 + i * 80;
                const y = centerY + j * 80;
                
                ctx.fillStyle = (i + j) % 2 === 0 
                    ? 'rgba(102, 126, 234, 0.2)' 
                    : 'rgba(118, 75, 162, 0.2)';
                ctx.fillRect(x, y, 70, 70);
                
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
                ctx.lineWidth = 1;
                ctx.strokeRect(x, y, 70, 70);
            }
        }
    }
    
    onResize(width, height) {
        this.initializeParticles();
    }
}
