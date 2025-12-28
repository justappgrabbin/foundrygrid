// daily-sync.js - Frontend for Daily Sync interface

const API_URL = 'http://localhost:5000';

// DOM Elements
const userInput = document.getElementById('user-input');
const syncButton = document.getElementById('sync-button');
const loading = document.getElementById('loading');
const dailySync = document.getElementById('daily-sync');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    // Optionally auto-load on page load
    // generateSync();
});

function setupEventListeners() {
    syncButton.addEventListener('click', generateSync);
    
    // Allow Enter to submit
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
            generateSync();
        }
    });
}

async function generateSync() {
    const input = userInput.value.trim() || 'current state check';
    
    // Show loading
    loading.style.display = 'block';
    dailySync.style.display = 'none';
    
    try {
        const response = await fetch(`${API_URL}/daily-sync`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_input: input
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide loading
        loading.style.display = 'none';
        
        // Display sync
        displaySync(data.sync);
        
    } catch (error) {
        loading.style.display = 'none';
        alert(`Failed to generate sync: ${error.message}`);
        console.error('Sync generation failed:', error);
    }
}

function displaySync(sync) {
    // Greeting
    document.getElementById('greeting').textContent = `${sync.greeting}!`;
    
    // Vibe
    document.getElementById('vibe-emoji').textContent = sync.vibe.emoji;
    document.getElementById('vibe-name').textContent = sync.vibe.name;
    document.getElementById('vibe-description').textContent = sync.vibe.description;
    
    // Energy
    document.getElementById('energy-level').textContent = sync.energy.level.toUpperCase();
    document.getElementById('energy-advice').textContent = sync.energy.advice;
    
    // Video Recommendation
    const video = sync.recommendations.video;
    document.getElementById('video-title').textContent = video.title;
    document.getElementById('video-meta').textContent = video.duration;
    document.getElementById('video-description').textContent = video.description;
    document.getElementById('video-reason').textContent = video.match_reason;
    document.getElementById('rec-video').onclick = () => window.open(video.url, '_blank');
    
    // Music Recommendation
    const music = sync.recommendations.music;
    document.getElementById('music-title').textContent = music.title;
    document.getElementById('music-meta').textContent = `${music.artist} • ${music.genre}`;
    document.getElementById('music-description').textContent = music.artist;
    document.getElementById('music-reason').textContent = music.match_reason;
    document.getElementById('rec-music').onclick = () => window.open(music.url, '_blank');
    
    // Game Recommendation
    const game = sync.recommendations.game;
    document.getElementById('game-title').textContent = game.title;
    document.getElementById('game-meta').textContent = game.platform;
    document.getElementById('game-description').textContent = game.description;
    document.getElementById('game-reason').textContent = game.match_reason;
    document.getElementById('rec-game').onclick = () => window.open(game.url, '_blank');
    
    // Article Recommendation
    const article = sync.recommendations.article;
    document.getElementById('article-title').textContent = article.title;
    document.getElementById('article-meta').textContent = `${article.source} • ${article.read_time}`;
    document.getElementById('article-description').textContent = article.description;
    document.getElementById('article-reason').textContent = article.match_reason;
    document.getElementById('rec-article').onclick = () => window.open(article.url, '_blank');
    
    // Intervention
    document.getElementById('intervention-action').textContent = sync.intervention.action;
    document.getElementById('intervention-reason').textContent = sync.intervention.reason;
    
    // Why Link
    document.getElementById('why-link').textContent = sync.why_link + ' →';
    document.getElementById('why-link').onclick = (e) => {
        e.preventDefault();
        showWhyExplanation(sync);
    };
    
    // Show the sync
    dailySync.style.display = 'block';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showWhyExplanation(sync) {
    // Create modal or expand section showing the consciousness details
    const explanation = `
This recommendation is based on your consciousness analysis:

Gate: ${sync.gate_info.number} (${sync.gate_info.name})
Theme: ${sync.gate_info.theme}

Primary Dimension: ${sync.dimension.primary} (${(sync.dimension.percentage * 100).toFixed(0)}%)

Your ${sync.dimension.primary} dimension means you process information through ${sync.dimension.primary.toLowerCase()} consciousness. The recommendations align with this frequency.

Coordinate: ${sync.coordinate}

The content, energy forecast, and interventions are mathematically matched to your consciousness state right now.
    `.trim();
    
    alert(explanation); // Simple version - could be a modal
}
