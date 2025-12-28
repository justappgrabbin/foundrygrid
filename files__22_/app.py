"""
SynthAI Flask API

REST API for consciousness analysis with personality tones.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from consciousness_core import ConsciousnessCore
from personality import ToneResponder

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize core systems
core = ConsciousnessCore()
responder = ToneResponder()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SynthAI',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze text and return consciousness state
    
    POST body:
    {
        "text": "user's text to analyze",
        "tone": "venom|prime|echo|dream|softcore" (optional),
        "include_technical": true|false (optional),
        "note_id": "optional identifier" (optional)
    }
    
    Returns:
    {
        "state": { ... complete consciousness state ... },
        "response": "formatted response in specified tone",
        "timestamp": "ISO timestamp"
    }
    """
    try:
        data = request.json
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing required field: text'}), 400
        
        text = data['text']
        tone = data.get('tone', 'prime').lower()
        include_technical = data.get('include_technical', False)
        note_id = data.get('note_id')
        
        # Validate tone
        valid_tones = ['venom', 'prime', 'echo', 'dream', 'softcore']
        if tone not in valid_tones:
            return jsonify({
                'error': f'Invalid tone. Must be one of: {", ".join(valid_tones)}'
            }), 400
        
        # Analyze
        state = core.analyze(text, note_id=note_id)
        
        # Generate response in specified tone
        response_text = responder.generate(tone, state, include_technical)
        
        return jsonify({
            'state': state.to_dict(),
            'response': response_text,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/quick', methods=['POST'])
def quick_analyze():
    """
    Quick analysis returning simplified response
    
    POST body:
    {
        "text": "user's text to analyze",
        "tone": "venom|prime|echo|dream|softcore" (optional)
    }
    
    Returns:
    {
        "coordinate": "5.1.4.1.1",
        "dimension": "Being",
        "coherence": 0.14,
        "confidence": 0.33,
        "response": "formatted response",
        "timestamp": "ISO timestamp"
    }
    """
    try:
        data = request.json
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing required field: text'}), 400
        
        text = data['text']
        tone = data.get('tone', 'prime').lower()
        
        # Analyze
        state = core.analyze(text)
        
        # Generate response
        response_text = responder.generate(tone, state, include_technical=False)
        
        return jsonify({
            'coordinate': state.coordinate_string,
            'dimension': state.dimension_name,
            'coherence': state.coherence,
            'confidence': state.confidence,
            'response': response_text,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/tones', methods=['GET'])
def get_tones():
    """
    Get list of available tones with descriptions
    
    Returns:
    {
        "tones": {
            "venom": "description...",
            "prime": "description...",
            ...
        }
    }
    """
    return jsonify({
        'tones': responder.get_available_tones()
    })


@app.route('/position', methods=['GET'])
def get_current_position():
    """
    Get current astronomical position and coordinate
    
    Returns:
    {
        "position": "0°29'22.49\" Capricorn",
        "coordinate": "5.1.4.1.4",
        "gate": {...},
        "dimension": {...},
        "timestamp": "ISO timestamp"
    }
    """
    try:
        # Get current position
        state = core.analyze("current position check")
        
        return jsonify({
            'position': state.position_string,
            'coordinate': state.coordinate_string,
            'gate': {
                'number': state.gate,
                'name': state.gate_name,
                'theme': state.gate_theme,
                'center': state.gate_center
            },
            'dimension': {
                'name': state.dimension_name,
                'keynote': state.dimension_keynote
            },
            'probabilities': state.geometric_probabilities,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/parse', methods=['POST'])
def parse_position():
    """
    Parse a specific astronomical position
    
    POST body:
    {
        "position": "17°23'45\" Leo"  // or other format
    }
    
    Returns:
    {
        "coordinate": "4.1.4.2.3",
        "gate": {...},
        "sentence": {...},
        "timestamp": "ISO timestamp"
    }
    """
    try:
        data = request.json
        
        if not data or 'position' not in data:
            return jsonify({'error': 'Missing required field: position'}), 400
        
        position_str = data['position']
        
        # Parse position
        from foundation import SentenceGenerator
        gen = SentenceGenerator()
        coordinate = gen.parse(position_str)
        sentence_data = gen.generate_sentence(coordinate)
        
        return jsonify({
            'coordinate': sentence_data['coordinate'],
            'position': sentence_data['position'],
            'gate': sentence_data['gate'],
            'line': sentence_data['line'],
            'color': sentence_data['color'],
            'tone': sentence_data['tone'],
            'base': sentence_data['base'],
            'dimension': sentence_data['dimension'],
            'center': sentence_data['center'],
            'sentences': sentence_data['sentences'],
            'polarity': sentence_data['polarity'],
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/batch', methods=['POST'])
def batch_analyze():
    """
    Batch analyze multiple texts
    
    POST body:
    {
        "texts": ["text 1", "text 2", ...],
        "tone": "venom|prime|echo|dream|softcore" (optional)
    }
    
    Returns:
    {
        "results": [
            { "text": "...", "response": "...", ... },
            ...
        ],
        "timestamp": "ISO timestamp"
    }
    """
    try:
        data = request.json
        
        if not data or 'texts' not in data:
            return jsonify({'error': 'Missing required field: texts'}), 400
        
        texts = data['texts']
        tone = data.get('tone', 'prime').lower()
        
        if not isinstance(texts, list):
            return jsonify({'error': 'texts must be an array'}), 400
        
        results = []
        
        for text in texts:
            state = core.analyze(text)
            response_text = responder.generate(tone, state, include_technical=False)
            
            results.append({
                'text': text,
                'coordinate': state.coordinate_string,
                'dimension': state.dimension_name,
                'coherence': state.coherence,
                'response': response_text
            })
        
        return jsonify({
            'results': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("SynthAI API Server")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /health          - Health check")
    print("  POST /analyze         - Full analysis with tone response")
    print("  POST /quick           - Quick simplified analysis")
    print("  GET  /tones           - List available tones")
    print("  GET  /position        - Current astronomical position")
    print("  POST /parse           - Parse specific position")
    print("  POST /batch           - Batch analyze multiple texts")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
