// SynthAI Frontend Application

const API_URL = 'http://localhost:5000';

// State
let selectedTone = 'venom';

// DOM Elements
const userInput = document.getElementById('user-input');
const analyzeBtn = document.getElementById('analyze-btn');
const technicalToggle = document.getElementById('technical-toggle');
const responseSection = document.getElementById('response-section');
const loading = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const currentPositionDiv = document.getElementById('current-position');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupToneSelector();
    setupAnalyzeButton();
    loadCurrentPosition();
});

// Setup Tone Selector
function setupToneSelector() {
    const toneBtns = document.querySelectorAll('.tone-btn');
    
    toneBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            toneBtns.forEach(b => b.classList.remove('active'));
            // Add active to clicked
            btn.classList.add('active');
            // Update selected tone
            selectedTone = btn.dataset.tone;
        });
    });
}

// Setup Analyze Button
function setupAnalyzeButton() {
    analyzeBtn.addEventListener('click', analyzeText);
    
    // Also allow Enter + Cmd/Ctrl to trigger
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
            analyzeText();
        }
    });
}

// Load Current Position
async function loadCurrentPosition() {
    try {
        const response = await fetch(`${API_URL}/position`);
        const data = await response.json();
        
        currentPositionDiv.innerHTML = `
            <strong>${data.coordinate}</strong> @ ${data.position} 
            | Gate ${data.gate.number} - ${data.gate.name}
            | ${data.dimension.name}
        `;
    } catch (error) {
        console.error('Failed to load current position:', error);
    }
}

// Analyze Text
async function analyzeText() {
    const text = userInput.value.trim();
    
    if (!text) {
        showError('Please enter some text to analyze');
        return;
    }
    
    // Show loading
    hideError();
    responseSection.style.display = 'none';
    loading.style.display = 'block';
    
    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                tone: selectedTone,
                include_technical: technicalToggle.checked
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide loading
        loading.style.display = 'none';
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        loading.style.display = 'none';
        showError(`Analysis failed: ${error.message}`);
    }
}

// Display Results
function displayResults(data) {
    const state = data.state;
    
    // Coordinate Display
    document.getElementById('coordinate').textContent = state.coordinate_string;
    document.getElementById('position').textContent = state.position_string;
    document.getElementById('gate').textContent = `${state.gate} - ${state.gate_name}`;
    document.getElementById('dimension').textContent = state.dimension_name;
    
    // Probability Bars
    displayProbabilities(state.blended_probabilities);
    
    // Metrics
    updateMetric('coherence', state.coherence);
    updateMetric('stability', state.stability);
    updateMetric('confidence', state.confidence);
    
    // Response Text
    document.getElementById('response-content').textContent = data.response;
    
    // Show response section
    responseSection.style.display = 'block';
    
    // Scroll to results
    responseSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Display Probability Bars
function displayProbabilities(probabilities) {
    const container = document.getElementById('probability-bars');
    
    // Sort by value descending
    const sorted = Object.entries(probabilities).sort((a, b) => b[1] - a[1]);
    
    // Create bars
    container.innerHTML = sorted.map(([dimension, value]) => `
        <div class="prob-bar">
            <span class="prob-label">${dimension}</span>
            <div class="prob-bar-container">
                <div class="prob-bar-fill" style="width: ${value * 100}%">
                    <span style="color: white; font-size: 0.85em;">${(value * 100).toFixed(0)}%</span>
                </div>
            </div>
            <span class="prob-value">${(value * 100).toFixed(1)}%</span>
        </div>
    `).join('');
}

// Update Metric
function updateMetric(name, value) {
    const bar = document.getElementById(`${name}-bar`);
    const valueSpan = document.getElementById(`${name}-value`);
    
    bar.style.width = `${value * 100}%`;
    valueSpan.textContent = `${(value * 100).toFixed(1)}%`;
}

// Show Error
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Hide Error
function hideError() {
    errorDiv.style.display = 'none';
}
