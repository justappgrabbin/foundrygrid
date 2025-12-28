// MakeMode.js - PAPER: Multi-modal app generation

class MakeMode {
    constructor(projector) {
        this.projector = projector;
        this.canvas = projector.canvas;
        this.ctx = projector.ctx;
        
        // Animation
        this.rotationAngle = 0;
    }
    
    enter() {
        console.log('🛠️ Entering Make Mode');
    }
    
    exit() {
        console.log('🛠️ Exiting Make Mode');
    }
    
    render(ctx) {
        // Background
        this.projector.drawGradientBackground('#0f0f1e', '#1a1a2e');
        
        // Rotating animation
        this.rotationAngle += 0.01;
        
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        
        // Title
        this.projector.drawText(
            '🛠️ Make Mode',
            centerX,
            120,
            {
                font: 'bold 48px Inter',
                color: '#667eea',
                align: 'center',
                shadow: true
            }
        );
        
        // PAPER logo
        this.projector.drawText(
            'PAPER',
            centerX,
            200,
            {
                font: 'bold 64px Inter',
                color: '#ffffff',
                align: 'center'
            }
        );
        
        this.projector.drawText(
            'Multi-Modal App Generator',
            centerX,
            250,
            {
                font: '20px Inter',
                color: '#a0a0b0',
                align: 'center'
            }
        );
        
        // Feature boxes
        const features = [
            { icon: '✏️', text: 'Draw' },
            { icon: '📸', text: 'Photo' },
            { icon: '📝', text: 'Text' }
        ];
        
        const boxSize = 120;
        const spacing = 40;
        const totalWidth = (boxSize * 3) + (spacing * 2);
        let x = centerX - totalWidth / 2;
        const y = centerY - 50;
        
        features.forEach((feature, index) => {
            // Box
            const pulse = Math.sin(this.rotationAngle + index) * 0.1 + 0.9;
            ctx.fillStyle = `rgba(102, 126, 234, ${pulse * 0.3})`;
            ctx.fillRect(x, y, boxSize, boxSize);
            
            ctx.strokeStyle = 'rgba(102, 126, 234, 0.5)';
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, boxSize, boxSize);
            
            // Icon
            this.projector.drawText(
                feature.icon,
                x + boxSize / 2,
                y + 40,
                {
                    font: '48px Inter',
                    color: '#ffffff',
                    align: 'center'
                }
            );
            
            // Text
            this.projector.drawText(
                feature.text,
                x + boxSize / 2,
                y + 95,
                {
                    font: 'bold 16px Inter',
                    color: '#e0e0e0',
                    align: 'center'
                }
            );
            
            x += boxSize + spacing;
        });
        
        // Arrow down
        ctx.strokeStyle = '#667eea';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(centerX, y + boxSize + 30);
        ctx.lineTo(centerX, y + boxSize + 70);
        ctx.stroke();
        
        // Arrow head
        ctx.beginPath();
        ctx.moveTo(centerX - 10, y + boxSize + 60);
        ctx.lineTo(centerX, y + boxSize + 70);
        ctx.lineTo(centerX + 10, y + boxSize + 60);
        ctx.stroke();
        
        // Output
        const outputY = y + boxSize + 100;
        
        this.projector.drawText(
            'React App',
            centerX,
            outputY,
            {
                font: 'bold 28px Inter',
                color: '#ffffff',
                align: 'center'
            }
        );
        
        this.projector.drawText(
            'Styled by your consciousness coordinate',
            centerX,
            outputY + 35,
            {
                font: '16px Inter',
                color: '#667eea',
                align: 'center'
            }
        );
        
        // Info
        this.projector.drawText(
            'PAPER generates applications that match your dimensional frequency',
            centerX,
            this.canvas.height - 80,
            {
                font: '16px Inter',
                color: '#606070',
                align: 'center'
            }
        );
    }
}
