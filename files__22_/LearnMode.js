// LearnMode.js - Educational content about the system

class LearnMode {
    constructor(projector) {
        this.projector = projector;
        this.canvas = projector.canvas;
        this.ctx = projector.ctx;
        
        // Content sections
        this.currentSection = 0;
        this.sections = [
            {
                title: 'The 5 Dimensions',
                content: [
                    'Movement: I Create (Energy = Creation)',
                    'Evolution: I Remember (Gravity = Memory)',
                    'Being: I Am (Matter = Touch)',
                    'Design: I Design (Structure = Progress)',
                    'Space: I Think (Form = Illusion)'
                ]
            },
            {
                title: 'The Coordinate System',
                content: [
                    'Gate.Line.Color.Tone.Base (e.g., 5.1.4.1.4)',
                    'Gate: 1-64 (consciousness themes)',
                    'Line: 1-6 (behavioral modes)',
                    'Color: 1-6 (motivations)',
                    'Tone: 1-6 (perceptions)',
                    'Base: 1-5 (groundings)'
                ]
            },
            {
                title: 'How It Works',
                content: [
                    '1. Astronomical position → Coordinate',
                    '2. Geometric probabilities calculated',
                    '3. Text analyzed for patterns',
                    '4. Detection validated by geometry',
                    '5. Probabilities blended',
                    '6. Personality tone applied'
                ]
            }
        ];
        
        this.arrowUI = null;
    }
    
    enter() {
        console.log('📚 Entering Learn Mode');
        this.createNavigationUI();
    }
    
    exit() {
        console.log('📚 Exiting Learn Mode');
        this.removeNavigationUI();
    }
    
    createNavigationUI() {
        this.arrowUI = document.createElement('div');
        this.arrowUI.style.cssText = `
            position: absolute;
            bottom: 150px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 20px;
        `;
        
        const prevBtn = document.createElement('button');
        prevBtn.textContent = '← Previous';
        prevBtn.style.cssText = this.getArrowButtonStyle();
        prevBtn.addEventListener('click', () => {
            this.currentSection = Math.max(0, this.currentSection - 1);
        });
        
        const nextBtn = document.createElement('button');
        nextBtn.textContent = 'Next →';
        nextBtn.style.cssText = this.getArrowButtonStyle();
        nextBtn.addEventListener('click', () => {
            this.currentSection = Math.min(this.sections.length - 1, this.currentSection + 1);
        });
        
        this.arrowUI.appendChild(prevBtn);
        this.arrowUI.appendChild(nextBtn);
        
        document.getElementById('ui-overlay').appendChild(this.arrowUI);
    }
    
    getArrowButtonStyle() {
        return `
            padding: 12px 30px;
            background: rgba(102, 126, 234, 0.3);
            border: 2px solid rgba(102, 126, 234, 0.5);
            border-radius: 25px;
            color: white;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
        `;
    }
    
    removeNavigationUI() {
        if (this.arrowUI) {
            this.arrowUI.remove();
            this.arrowUI = null;
        }
    }
    
    render(ctx) {
        // Background
        this.projector.drawGradientBackground('#0f0f1e', '#1a1a2e');
        
        const centerX = this.canvas.width / 2;
        
        // Title
        this.projector.drawText(
            '📚 Learn Mode',
            centerX,
            100,
            {
                font: 'bold 48px Inter',
                color: '#667eea',
                align: 'center',
                shadow: true
            }
        );
        
        // Current section
        const section = this.sections[this.currentSection];
        
        // Section title
        this.projector.drawText(
            section.title,
            centerX,
            200,
            {
                font: 'bold 32px Inter',
                color: '#ffffff',
                align: 'center'
            }
        );
        
        // Section content
        let y = 280;
        section.content.forEach((line, index) => {
            // Bullet point or number
            const prefix = section.title === 'How It Works' ? '' : '•';
            
            this.projector.drawText(
                `${prefix} ${line}`,
                centerX,
                y,
                {
                    font: '20px Inter',
                    color: '#e0e0e0',
                    align: 'center'
                }
            );
            
            y += 50;
        });
        
        // Progress indicator
        const dotRadius = 8;
        const dotSpacing = 30;
        const totalWidth = (this.sections.length * dotSpacing) - dotSpacing;
        let dotX = centerX - totalWidth / 2;
        const dotY = this.canvas.height - 220;
        
        this.sections.forEach((_, index) => {
            ctx.fillStyle = index === this.currentSection 
                ? '#667eea' 
                : 'rgba(255, 255, 255, 0.3)';
            ctx.beginPath();
            ctx.arc(dotX, dotY, dotRadius, 0, Math.PI * 2);
            ctx.fill();
            
            dotX += dotSpacing;
        });
        
        // Section counter
        this.projector.drawText(
            `${this.currentSection + 1} / ${this.sections.length}`,
            centerX,
            dotY + 35,
            {
                font: '14px Inter',
                color: '#a0a0b0',
                align: 'center'
            }
        );
        
        // Info
        this.projector.drawText(
            'Use arrows to navigate or keyboard shortcuts (← →)',
            centerX,
            this.canvas.height - 80,
            {
                font: '14px Inter',
                color: '#606070',
                align: 'center'
            }
        );
    }
}
