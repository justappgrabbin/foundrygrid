// projector.js - The Canvas Projection Engine
// Single page, dynamic content via canvas rendering

class Projector {
    constructor() {
        // Canvas setup
        this.canvas = document.getElementById('projector');
        this.ctx = this.canvas.getContext('2d');
        
        // API endpoint
        this.API_URL = 'http://localhost:5000';
        
        // State
        this.currentMode = 'chat';
        this.modes = {};
        this.userState = null;
        this.isTransitioning = false;
        
        // Performance
        this.lastFrameTime = 0;
        this.fps = 60;
        this.frameInterval = 1000 / this.fps;
        
        // Initialize
        this.resize();
        this.initializeModes();
        this.setupEventListeners();
        this.loadCurrentPosition();
        
        // Start render loop
        this.animate(0);
        
        console.log('🎬 Projector initialized');
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        
        // Update all modes about resize
        Object.values(this.modes).forEach(mode => {
            if (mode.onResize) mode.onResize(this.canvas.width, this.canvas.height);
        });
    }
    
    initializeModes() {
        // Register all mode classes
        this.modes = {
            chat: new ChatMode(this),
            play: new PlayMode(this),
            view: new ViewMode(this),
            make: new MakeMode(this),
            meet: new MeetMode(this),
            learn: new LearnMode(this)
        };
        
        // Enter initial mode
        this.modes[this.currentMode].enter();
    }
    
    setupEventListeners() {
        // Window resize
        window.addEventListener('resize', () => this.resize());
        
        // Mode selector buttons
        const buttons = document.querySelectorAll('.mode-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const newMode = btn.dataset.mode;
                if (newMode !== this.currentMode) {
                    this.switchMode(newMode);
                    
                    // Update UI
                    buttons.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                }
            });
        });
        
        // Keyboard shortcuts
        window.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + number to switch modes
            if (e.metaKey || e.ctrlKey) {
                const modeKeys = ['1', '2', '3', '4', '5', '6'];
                const modeNames = ['chat', 'play', 'view', 'make', 'meet', 'learn'];
                const index = modeKeys.indexOf(e.key);
                
                if (index !== -1) {
                    e.preventDefault();
                    const newMode = modeNames[index];
                    this.switchMode(newMode);
                    
                    // Update UI
                    buttons.forEach(b => b.classList.remove('active'));
                    buttons[index].classList.add('active');
                }
            }
        });
    }
    
    switchMode(modeName) {
        if (this.isTransitioning) return;
        if (!this.modes[modeName]) {
            console.error(`Mode ${modeName} not found`);
            return;
        }
        
        this.isTransitioning = true;
        
        // Show transition effect
        this.showTransitionEffect();
        
        // Exit current mode
        if (this.modes[this.currentMode]) {
            this.modes[this.currentMode].exit();
        }
        
        // Switch
        this.currentMode = modeName;
        
        // Enter new mode
        setTimeout(() => {
            this.modes[this.currentMode].enter();
            this.isTransitioning = false;
        }, 300);
        
        console.log(`🎬 Switched to ${modeName} mode`);
    }
    
    showTransitionEffect() {
        const effect = document.createElement('div');
        effect.className = 'mode-transition';
        document.getElementById('ui-overlay').appendChild(effect);
        
        setTimeout(() => effect.remove(), 600);
    }
    
    animate(timestamp) {
        // Request next frame
        requestAnimationFrame((t) => this.animate(t));
        
        // Throttle to target FPS
        const elapsed = timestamp - this.lastFrameTime;
        if (elapsed < this.frameInterval) return;
        
        this.lastFrameTime = timestamp - (elapsed % this.frameInterval);
        
        // Clear canvas
        this.ctx.fillStyle = '#0a0a0a';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Render current mode
        if (this.modes[this.currentMode] && !this.isTransitioning) {
            this.modes[this.currentMode].render(this.ctx);
        }
    }
    
    async loadCurrentPosition() {
        try {
            const response = await fetch(`${this.API_URL}/position`);
            const data = await response.json();
            
            // Create minimal state from position
            this.updateCoordinateBar({
                coordinate_string: data.coordinate,
                gate: data.gate.number,
                dimension_name: data.dimension.name,
                coherence: 0.5 // Default until we have real analysis
            });
            
        } catch (error) {
            console.error('Failed to load position:', error);
        }
    }
    
    updateUserState(state) {
        this.userState = state;
        this.updateCoordinateBar(state);
        
        // Notify all modes
        Object.values(this.modes).forEach(mode => {
            if (mode.onStateUpdate) {
                mode.onStateUpdate(state);
            }
        });
    }
    
    updateCoordinateBar(state) {
        document.getElementById('coordinate').textContent = state.coordinate_string || '-.-.-.-.-';
        document.getElementById('gate').textContent = state.gate || '-';
        document.getElementById('dimension').textContent = state.dimension_name || '-';
        
        const coherence = state.coherence || 0;
        document.getElementById('coherence').textContent = `${(coherence * 100).toFixed(0)}%`;
    }
    
    showLoading(show = true) {
        document.getElementById('loading').style.display = show ? 'block' : 'none';
    }
    
    // Utility: Draw text with shadow
    drawText(text, x, y, options = {}) {
        const {
            font = '16px Inter',
            color = '#ffffff',
            align = 'left',
            baseline = 'top',
            shadow = false
        } = options;
        
        this.ctx.font = font;
        this.ctx.fillStyle = color;
        this.ctx.textAlign = align;
        this.ctx.textBaseline = baseline;
        
        if (shadow) {
            this.ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
            this.ctx.shadowBlur = 10;
            this.ctx.shadowOffsetX = 2;
            this.ctx.shadowOffsetY = 2;
        }
        
        this.ctx.fillText(text, x, y);
        
        if (shadow) {
            this.ctx.shadowColor = 'transparent';
            this.ctx.shadowBlur = 0;
        }
    }
    
    // Utility: Draw gradient background
    drawGradientBackground(color1, color2) {
        const gradient = this.ctx.createLinearGradient(0, 0, 0, this.canvas.height);
        gradient.addColorStop(0, color1);
        gradient.addColorStop(1, color2);
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }
}

// Initialize on load
let projector;
window.addEventListener('DOMContentLoaded', () => {
    projector = new Projector();
    
    // Expose globally for debugging
    window.projector = projector;
});
