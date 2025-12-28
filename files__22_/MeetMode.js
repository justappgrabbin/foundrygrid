// MeetMode.js - PAPER MATE: Consciousness compatibility matching

class MeetMode {
    constructor(projector) {
        this.projector = projector;
        this.canvas = projector.canvas;
        this.ctx = projector.ctx;
        
        // Mock matches for demonstration
        this.matches = [];
        this.heartbeatPhase = 0;
    }
    
    enter() {
        console.log('💕 Entering Meet Mode');
        this.generateMockMatches();
    }
    
    exit() {
        console.log('💕 Exiting Meet Mode');
    }
    
    generateMockMatches() {
        if (!this.projector.userState) {
            this.matches = [];
            return;
        }
        
        const userGate = this.projector.userState.gate;
        
        // Generate complementary matches
        this.matches = [
            {
                name: 'Sarah Chen',
                gate: 35,
                gateName: 'Progress',
                dimension: 'Movement',
                score: 0.94,
                reason: 'Your Being foundation provides stability for their Movement drive. Polarity creates creative tension.'
            },
            {
                name: 'Marcus Webb',
                gate: 14,
                gateName: 'Power Skills',
                dimension: 'Being',
                score: 0.87,
                reason: 'Both Sacral-defined. Their Power Skills complement your Fixed Rhythms. Strong material manifestation potential.'
            },
            {
                name: 'Aisha Patel',
                gate: 43,
                gateName: 'Breakthrough',
                dimension: 'Evolution',
                score: 0.82,
                reason: 'Evolution + Being = strategic embodiment. Their insights grounded by your patience. Excellent research partnership.'
            }
        ];
    }
    
    render(ctx) {
        // Background
        this.projector.drawGradientBackground('#0f0f1e', '#1a1a2e');
        
        // Heartbeat animation
        this.heartbeatPhase += 0.05;
        const heartbeat = Math.abs(Math.sin(this.heartbeatPhase)) * 0.2 + 0.8;
        
        const centerX = this.canvas.width / 2;
        
        // Title
        this.projector.drawText(
            '💕 Meet Mode',
            centerX,
            100,
            {
                font: 'bold 48px Inter',
                color: '#667eea',
                align: 'center',
                shadow: true
            }
        );
        
        // Subtitle
        this.projector.drawText(
            'PAPER MATE • Consciousness Compatibility',
            centerX,
            160,
            {
                font: '20px Inter',
                color: '#a0a0b0',
                align: 'center'
            }
        );
        
        if (this.matches.length === 0) {
            this.projector.drawText(
                'Analyze your consciousness to find matches',
                centerX,
                this.canvas.height / 2,
                {
                    font: '18px Inter',
                    color: '#606070',
                    align: 'center'
                }
            );
            return;
        }
        
        // Render match cards
        let y = 240;
        const cardWidth = 700;
        const cardHeight = 120;
        
        this.matches.forEach((match, index) => {
            const x = centerX - cardWidth / 2;
            
            // Card background with pulse
            const pulse = index === 0 ? heartbeat : 1.0;
            ctx.fillStyle = `rgba(0, 0, 0, ${0.6 * pulse})`;
            ctx.fillRect(x, y, cardWidth, cardHeight);
            
            // Border with glow for top match
            if (index === 0) {
                ctx.shadowColor = 'rgba(102, 126, 234, 0.5)';
                ctx.shadowBlur = 20;
            }
            ctx.strokeStyle = 'rgba(102, 126, 234, 0.6)';
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, cardWidth, cardHeight);
            ctx.shadowBlur = 0;
            
            // Match score (circular)
            const scoreRadius = 35;
            const scoreX = x + 50;
            const scoreY = y + cardHeight / 2;
            
            // Score circle background
            ctx.fillStyle = 'rgba(102, 126, 234, 0.2)';
            ctx.beginPath();
            ctx.arc(scoreX, scoreY, scoreRadius, 0, Math.PI * 2);
            ctx.fill();
            
            // Score arc
            ctx.strokeStyle = '#667eea';
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.arc(scoreX, scoreY, scoreRadius, -Math.PI / 2, 
                   -Math.PI / 2 + (Math.PI * 2 * match.score), false);
            ctx.stroke();
            
            // Score percentage
            this.projector.drawText(
                `${(match.score * 100).toFixed(0)}%`,
                scoreX,
                scoreY,
                {
                    font: 'bold 18px Inter',
                    color: '#ffffff',
                    align: 'center',
                    baseline: 'middle'
                }
            );
            
            // Name
            this.projector.drawText(
                match.name,
                x + 110,
                y + 20,
                {
                    font: 'bold 22px Inter',
                    color: '#ffffff',
                    align: 'left'
                }
            );
            
            // Gate info
            this.projector.drawText(
                `Gate ${match.gate} - ${match.gateName} | ${match.dimension} Dimension`,
                x + 110,
                y + 50,
                {
                    font: '14px Inter',
                    color: '#a0a0b0',
                    align: 'left'
                }
            );
            
            // Compatibility reason
            ctx.fillStyle = '#667eea';
            ctx.font = '13px Inter';
            ctx.textAlign = 'left';
            
            // Wrap text
            const maxWidth = cardWidth - 130;
            const words = match.reason.split(' ');
            let line = '';
            let lineY = y + 75;
            
            for (let word of words) {
                const testLine = line + word + ' ';
                const metrics = ctx.measureText(testLine);
                
                if (metrics.width > maxWidth && line.length > 0) {
                    ctx.fillText(line, x + 110, lineY);
                    line = word + ' ';
                    lineY += 18;
                } else {
                    line = testLine;
                }
            }
            ctx.fillText(line, x + 110, lineY);
            
            y += cardHeight + 20;
        });
        
        // Footer info
        this.projector.drawText(
            'Compatibility based on polarity, dimensional balance, and energetic flow',
            centerX,
            this.canvas.height - 80,
            {
                font: '14px Inter',
                color: '#606070',
                align: 'center'
            }
        );
    }
    
    onStateUpdate(state) {
        this.generateMockMatches();
    }
}
