"""
Dimension Classifier

Analyzes text to detect which of the 5 consciousness dimensions
is most present. This detection is validated against the geometric
foundation (current Sun position).
"""

from typing import Tuple, Dict
import re
from collections import Counter


class DimensionClassifier:
    """
    Classifies text into one of 5 consciousness dimensions.
    
    This is pattern recognition validated by geometric truth.
    When detection aligns with foundation, confidence increases.
    """
    
    # Keyword mappings for each dimension
    DIMENSION_KEYWORDS = {
        'Movement': {
            # Action, creation, doing
            'primary': [
                'create', 'do', 'make', 'build', 'start', 'begin', 'initiate',
                'action', 'act', 'move', 'go', 'drive', 'push', 'launch',
                'energy', 'power', 'force', 'momentum', 'generate', 'produce'
            ],
            'secondary': [
                'doing', 'making', 'creating', 'starting', 'moving', 'going',
                'active', 'dynamic', 'energetic', 'powerful', 'driven',
                'initiative', 'spontaneous', 'immediate', 'now', 'today'
            ],
            'themes': [
                'self-expression', 'identity', 'direction', 'purpose',
                'manifestation', 'will', 'intention', 'desire'
            ]
        },
        
        'Evolution': {
            # Memory, process, understanding
            'primary': [
                'remember', 'recall', 'memory', 'understand', 'learn',
                'process', 'think', 'reflect', 'consider', 'analyze',
                'wisdom', 'knowledge', 'insight', 'realize', 'recognize'
            ],
            'secondary': [
                'thinking', 'processing', 'understanding', 'learning',
                'reflective', 'analytical', 'thoughtful', 'wise',
                'mental', 'cognitive', 'intellectual', 'cerebral',
                'past', 'history', 'experience', 'lesson'
            ],
            'themes': [
                'pattern', 'meaning', 'gravity', 'depth', 'synthesis',
                'integration', 'comprehension', 'awareness'
            ]
        },
        
        'Being': {
            # Presence, embodiment, existence
            'primary': [
                'am', 'is', 'be', 'being', 'exist', 'presence', 'here',
                'feel', 'sense', 'body', 'touch', 'physical', 'material',
                'alive', 'breath', 'heart', 'gut', 'instinct', 'visceral'
            ],
            'secondary': [
                'existing', 'present', 'embodied', 'grounded', 'rooted',
                'feeling', 'sensing', 'experiencing', 'living',
                'bodily', 'tangible', 'concrete', 'real', 'actual',
                'now', 'currently', 'immediate', 'direct'
            ],
            'themes': [
                'matter', 'substance', 'form', 'reality', 'truth',
                'survival', 'life force', 'vitality', 'essence'
            ]
        },
        
        'Design': {
            # Structure, organization, planning
            'primary': [
                'plan', 'design', 'structure', 'organize', 'arrange',
                'system', 'order', 'pattern', 'framework', 'build',
                'construct', 'engineer', 'architect', 'strategy', 'method'
            ],
            'secondary': [
                'planning', 'designing', 'structuring', 'organizing',
                'systematic', 'ordered', 'methodical', 'strategic',
                'logical', 'rational', 'structured', 'organized',
                'future', 'goal', 'objective', 'target', 'aim'
            ],
            'themes': [
                'progress', 'development', 'growth', 'evolution',
                'improvement', 'optimization', 'refinement', 'clarity'
            ]
        },
        
        'Space': {
            # Imagination, possibility, vision
            'primary': [
                'imagine', 'dream', 'vision', 'see', 'visualize',
                'possibility', 'potential', 'could', 'might', 'maybe',
                'wonder', 'curious', 'explore', 'discover', 'envision'
            ],
            'secondary': [
                'imagining', 'dreaming', 'envisioning', 'wondering',
                'imaginative', 'creative', 'visionary', 'inspired',
                'possible', 'potential', 'conceptual', 'abstract',
                'what if', 'illusion', 'form', 'idea', 'concept'
            ],
            'themes': [
                'inspiration', 'creativity', 'innovation', 'novelty',
                'transcendence', 'expansion', 'freedom', 'openness'
            ]
        }
    }
    
    # Phrase patterns that strongly indicate dimensions
    DIMENSION_PATTERNS = {
        'Movement': [
            r'\bI (create|do|make|start|begin)',
            r'\b(need to|want to|going to) (do|make|create|start)',
            r'\b(action|doing|creating|making)',
        ],
        'Evolution': [
            r'\bI (remember|think|understand|realize)',
            r'\b(trying to understand|learning|processing)',
            r'\b(pattern|meaning|why|how come)',
        ],
        'Being': [
            r'\bI am\b',
            r'\b(feel|sense|body|physical)',
            r'\b(here|now|present|alive)',
        ],
        'Design': [
            r'\bI (plan|design|organize|structure)',
            r'\b(need to (plan|organize|fix))',
            r'\b(system|structure|strategy|method)',
        ],
        'Space': [
            r'\bI (imagine|dream|wonder|envision)',
            r'\b(what if|could|might|possibly)',
            r'\b(possibility|potential|vision)',
        ]
    }
    
    def classify(self, text: str, geometric_dimension: str = None) -> Tuple[str, float]:
        """
        Classify text into a dimension
        
        Args:
            text: User's text to analyze
            geometric_dimension: The dimension from geometric foundation (optional)
            
        Returns:
            Tuple of (dimension_name, confidence)
        """
        text_lower = text.lower()
        
        # Calculate scores for each dimension
        scores = {}
        for dimension, keywords in self.DIMENSION_KEYWORDS.items():
            score = self._calculate_dimension_score(text_lower, keywords, dimension)
            scores[dimension] = score
        
        # Get the highest scoring dimension
        if not scores or max(scores.values()) == 0:
            # No clear signal - return geometric dimension if available
            if geometric_dimension:
                return geometric_dimension, 0.50
            else:
                return 'Being', 0.20  # Default to Being (presence)
        
        detected_dimension = max(scores.items(), key=lambda x: x[1])[0]
        raw_confidence = scores[detected_dimension]
        
        # Normalize confidence (0.0 to 1.0)
        total_score = sum(scores.values())
        if total_score > 0:
            base_confidence = raw_confidence / total_score
        else:
            base_confidence = 0.20
        
        # Boost confidence if detection matches geometric foundation
        if geometric_dimension:
            if detected_dimension == geometric_dimension:
                # Alignment boost
                confidence = min(base_confidence * 1.3, 0.95)
            else:
                # Slight reduction for misalignment
                confidence = base_confidence * 0.9
        else:
            confidence = base_confidence
        
        return detected_dimension, confidence
    
    def _calculate_dimension_score(self, text: str, keywords: Dict, dimension: str) -> float:
        """
        Calculate score for a specific dimension based on keyword matches
        """
        score = 0.0
        
        # Primary keywords (weight: 3.0)
        for keyword in keywords.get('primary', []):
            count = text.count(keyword)
            score += count * 3.0
        
        # Secondary keywords (weight: 1.5)
        for keyword in keywords.get('secondary', []):
            count = text.count(keyword)
            score += count * 1.5
        
        # Theme keywords (weight: 2.0)
        for keyword in keywords.get('themes', []):
            count = text.count(keyword)
            score += count * 2.0
        
        # Pattern matches (weight: 5.0 each)
        patterns = self.DIMENSION_PATTERNS.get(dimension, [])
        for pattern in patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 5.0
        
        return score
    
    def get_dimension_breakdown(self, text: str) -> Dict[str, float]:
        """
        Get scores for all dimensions
        
        Args:
            text: User's text to analyze
            
        Returns:
            Dict mapping dimension names to normalized scores
        """
        text_lower = text.lower()
        
        scores = {}
        for dimension, keywords in self.DIMENSION_KEYWORDS.items():
            score = self._calculate_dimension_score(text_lower, keywords, dimension)
            scores[dimension] = score
        
        # Normalize
        total = sum(scores.values())
        if total > 0:
            return {k: v / total for k, v in scores.items()}
        else:
            # Uniform distribution if no signal
            return {k: 0.20 for k in scores.keys()}
    
    def extract_key_themes(self, text: str, dimension: str) -> list:
        """
        Extract key themes related to the detected dimension
        
        Args:
            text: User's text
            dimension: Detected dimension
            
        Returns:
            List of theme keywords found in text
        """
        text_lower = text.lower()
        keywords = self.DIMENSION_KEYWORDS.get(dimension, {})
        
        found_themes = []
        
        # Check all keyword categories
        for category in ['primary', 'secondary', 'themes']:
            for keyword in keywords.get(category, []):
                if keyword in text_lower:
                    found_themes.append(keyword)
        
        return found_themes[:5]  # Return top 5
