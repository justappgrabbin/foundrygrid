// ViewMode.js - PhotoGAN generation + Content recommendations

class ViewMode {
    constructor(projector) {
        this.projector = projector;
        this.canvas = projector.canvas;
        this.ctx = projector.ctx;
        
        // Generated content
        this.generatedImage = null;
        this.recommendations = [];
        
        // Animation
        this.pulsePhase = 0;
    }
    
    enter() {
        console.log('🎨 Entering View Mode');
        this.generatePlaceholderContent();
    }
    
    exit() {
        console.log('🎨 Exiting View Mode');
    }
    
    generatePlaceholderContent() {
        // Placeholder recommendations based on coordinate
        if (this.projector.userState) {
            const dimension = this.projector.userState.dimension_name;
            
            this.recommendations = this.getRecommendationsForDimension(dimension);
        }
    }
    
    getRecommendationsForDimension(dimension) {
        const recommendations = {
            'Being': [
                { type: 'video', title: 'Slow Cinema: Norwegian Train Journey', match: 'Observational, grounded pace' },
                { type: 'music', title: 'Ambient Nature Sounds', match: 'Smell sensory tone alignment' },
                { type: 'game', title: 'Journey (Indie Exploration)', match: 'Being dimension resonance' }
            ],
            'Movement': [
                { type: 'video', title: 'Action Sports Compilation', match: 'High energy, dynamic creation' },
                { type: 'music', title: 'Epic Cinematic Soundtracks', match: 'Power and momentum' },
                { type: 'game', title: 'Fast-Paced Strategy Games', match: 'Movement expression' }
            ],
            'Evolution': [
                { type: 'video', title: 'Cosmos: Pattern Recognition', match: 'Memory and understanding focus' },
                { type: 'music', title: 'Progressive Compositions', match: 'Evolving structures' },
                { type: 'game', title: 'Puzzle Games with Learning', match: 'Pattern processing' }
            ],
            'Design': [
                { type: 'video', title: 'How It\'s Made: Engineering', match: 'Structure and systems' },
                { type: 'music', title: 'Minimalist Classical', match: 'Methodical design' },
                { type: 'game', title: 'City Building Simulators', match: 'Planning and organization' }
            ],
            'Space': [
                { type: 'video', title: 'Abstract Art Documentaries', match: 'Visionary exploration' },
                { type: 'music', title: 'Experimental Electronic', match: 'Conceptual freedom' },
                { type: 'game', title: 'Sandbox Creative Games', match: 'Unlimited possibility' }
            ]
        };
        
        return recommendations[dimension] || recommendations['Being'];
    }
    
    render(ctx) {
        // Background
        this.projector.drawGradientBackground('#0f0f1e', '#1a1a2e');
        
        // Pulse animation
        this.pulsePhase += 0.02;
        const pulse = Math.sin(this.pulsePhase) * 0.1 + 0.9;
        
        // Title
        this.projector.drawText(
            '🎨 View Mode',
            this.canvas.width / 2,
            100,
            {
                font: 'bold 48px Inter',
                color: '#667eea',
                align: 'center',
                shadow: true
            }
        );
        
        // Two columns: Generated | Recommended
        const midX = this.canvas.width / 2;
        const leftX = midX / 2;
        const rightX = midX + midX / 2;
        
        // Left: PhotoGAN Generated
        this.renderPhotoGAN(ctx, leftX);
        
        // Right: Content Recommendations
        this.renderRecommendations(ctx, rightX);
        
        // Center divider
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(midX, 180);
        ctx.lineTo(midX, this.canvas.height - 150);
        ctx.stroke();
        ctx.setLineDash([]);
    }
    
    renderPhotoGAN(ctx, centerX) {
        // Section title
        this.projector.drawText(
            'Your Consciousness Art',
            centerX,
            200,
            {
                font: 'bold 24px Inter',
                color: '#ffffff',
                align: 'center'
            }
        );
        
        // PhotoGAN placeholder
        const size = 250;
        const x = centerX - size / 2;
        const y = 280;
        
        // Gradient square
        const gradient = ctx.createRadialGradient(
            centerX, y + size / 2, 0,
            centerX, y + size / 2, size / 2
        );
        gradient.addColorStop(0, '#667eea');
        gradient.addColorStop(1, '#764ba2');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(x, y, size, size);
        
        // Border
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, size, size);
        
        // Placeholder text
        this.projector.drawText(
            'PhotoGAN',
            centerX,
            y + size / 2 - 10,
            {
                font: 'bold 28px Inter',
                color: '#ffffff',
                align: 'center',
                baseline: 'middle'
            }
        );
        
        this.projector.drawText(
            'Image Generation',
            centerX,
            y + size / 2 + 20,
            {
                font: '16px Inter',
                color: 'rgba(255, 255, 255, 0.8)',
                align: 'center',
                baseline: 'middle'
            }
        );
        
        // Generate button
        if (this.projector.userState) {
            this.projector.drawText(
                `Coordinate: ${this.projector.userState.coordinate_string}`,
                centerX,
                y + size + 30,
                {
                    font: '14px Courier New',
                    color: '#667eea',
                    align: 'center'
                }
            );
        }
    }
    
    renderRecommendations(ctx, centerX) {
        // Section title
        this.projector.drawText(
            'Curated For You',
            centerX,
            200,
            {
                font: 'bold 24px Inter',
                color: '#ffffff',
                align: 'center'
            }
        );
        
        if (this.recommendations.length === 0) {
            this.projector.drawText(
                'Analyze text to get recommendations',
                centerX,
                this.canvas.height / 2,
                {
                    font: '16px Inter',
                    color: '#606070',
                    align: 'center'
                }
            );
            return;
        }
        
        // Render recommendation cards
        let y = 280;
        const cardWidth = 350;
        
        this.recommendations.forEach((rec, index) => {
            const x = centerX - cardWidth / 2;
            
            // Card background
            ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
            ctx.fillRect(x, y, cardWidth, 80);
            
            // Border
            ctx.strokeStyle = 'rgba(102, 126, 234, 0.3)';
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, cardWidth, 80);
            
            // Icon
            const icons = { video: '📹', music: '🎵', game: '🎮' };
            this.projector.drawText(
                icons[rec.type],
                x + 20,
                y + 25,
                {
                    font: '32px Inter',
                    color: '#ffffff',
                    align: 'left'
                }
            );
            
            // Title
            this.projector.drawText(
                rec.title,
                x + 70,
                y + 20,
                {
                    font: 'bold 16px Inter',
                    color: '#ffffff',
                    align: 'left'
                }
            );
            
            // Match reason
            this.projector.drawText(
                `✓ ${rec.match}`,
                x + 70,
                y + 45,
                {
                    font: '13px Inter',
                    color: '#667eea',
                    align: 'left'
                }
            );
            
            y += 100;
        });
    }
    
    onStateUpdate(state) {
        this.generatePlaceholderContent();
    }
}
