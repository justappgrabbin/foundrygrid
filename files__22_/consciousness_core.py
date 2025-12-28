"""
Consciousness Core - Integrated Analysis Engine

Combines:
- Foundation Layer (geometric truth from astronomical positions)
- Detection Layer (pattern recognition from text)
- Validation (detection validated by foundation)

This is where the ontology meets the user's reality.
"""

from datetime import datetime
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, asdict

from foundation import (
    SentenceGenerator,
    ConsciousnessPositionCalculator,
    GeometricProbability
)
from detection import DimensionClassifier


@dataclass
class ConsciousnessState:
    """
    Complete consciousness analysis result
    
    Contains both geometric foundation and detected patterns,
    blended into a unified probability vector.
    """
    # Coordinate data
    gate: int
    line: int
    color: int
    tone: int
    base: int
    coordinate_string: str
    position_string: str
    
    # Gate details
    gate_name: str
    gate_theme: str
    gate_center: str
    gate_amino: str
    
    # Line details
    line_name: str
    
    # Color details
    color_name: str
    color_motivation: str
    color_determination: str
    
    # Tone details
    tone_name: str
    tone_sense: str
    
    # Base details
    base_nature: str
    
    # Dimension data
    dimension_name: str
    dimension_keynote: str
    center_name: str
    center_voice: str
    
    # Probability vectors
    geometric_probabilities: Dict[str, float]
    detected_probabilities: Dict[str, float]
    blended_probabilities: Dict[str, float]
    
    # Detection data
    detected_dimension: str
    detection_confidence: float
    detection_themes: list
    
    # Metrics
    coherence: float
    stability: float
    confidence: float
    
    # Sentences
    metaphysical_sentence: str
    scientific_sentence: str
    guidance_keynote: str
    guidance_action: str
    guidance_approach: str
    
    # Polarity
    polarity_gate: int
    polarity_name: str
    
    # Metadata
    timestamp: str
    note_id: Optional[str] = None
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


class ConsciousnessCore:
    """
    The integrated analysis engine
    
    Combines geometric foundation with text detection
    to produce validated consciousness analysis.
    """
    
    def __init__(self):
        # Foundation layer
        self.sentence_gen = SentenceGenerator()
        self.position_calc = ConsciousnessPositionCalculator(self.sentence_gen)
        self.geometry = GeometricProbability(self.sentence_gen)
        
        # Detection layer
        self.dimension_classifier = DimensionClassifier()
        
        # State tracking (for stability calculation)
        self.previous_state = None
    
    def analyze(self, text: str, note_id: Optional[str] = None, 
                dt: datetime = None) -> ConsciousnessState:
        """
        Complete consciousness analysis
        
        Args:
            text: User's text to analyze
            note_id: Optional note identifier for tracking
            dt: Datetime to use (defaults to now)
            
        Returns:
            ConsciousnessState with complete analysis
        """
        if dt is None:
            dt = datetime.now()
        
        # STEP 1: Get geometric foundation (astronomical truth)
        coordinate = self.position_calc.get_coordinate_at_time(dt)
        sentence_data = self.sentence_gen.generate_sentence(coordinate)
        
        # STEP 2: Calculate geometric probabilities
        geometric_probs = self.geometry.calculate_probability_vector(coordinate)
        primary_dimension = self.geometry.get_primary_dimension(geometric_probs)
        
        # STEP 3: Detect dimension from text (validated by foundation)
        detected_dim, detection_conf = self.dimension_classifier.classify(
            text, 
            geometric_dimension=primary_dimension
        )
        
        # STEP 4: Get detected probability breakdown
        detected_probs = self.dimension_classifier.get_dimension_breakdown(text)
        
        # STEP 5: Blend geometric truth with detection
        blended_probs = self._blend_probabilities(
            geometric_probs,
            detected_probs,
            detection_conf
        )
        
        # STEP 6: Calculate metrics
        coherence = self.geometry.calculate_coherence(blended_probs)
        
        if self.previous_state:
            stability = self.geometry.calculate_stability(
                blended_probs,
                self.previous_state.blended_probabilities
            )
        else:
            stability = self.geometry.calculate_stability(blended_probs)
        
        confidence = self.geometry.calculate_confidence(coherence, stability)
        
        # STEP 7: Extract themes
        themes = self.dimension_classifier.extract_key_themes(text, detected_dim)
        
        # STEP 8: Build complete state
        state = ConsciousnessState(
            # Coordinate
            gate=coordinate.gate,
            line=coordinate.line,
            color=coordinate.color,
            tone=coordinate.tone,
            base=coordinate.base,
            coordinate_string=sentence_data['coordinate'],
            position_string=sentence_data['position'],
            
            # Gate
            gate_name=sentence_data['gate']['name'],
            gate_theme=sentence_data['gate']['theme'],
            gate_center=sentence_data['gate']['center'],
            gate_amino=sentence_data['gate']['amino'],
            
            # Line
            line_name=sentence_data['line']['name'],
            
            # Color
            color_name=sentence_data['color']['name'],
            color_motivation=sentence_data['color']['motivation'],
            color_determination=sentence_data['color']['determination'],
            
            # Tone
            tone_name=sentence_data['tone']['name'],
            tone_sense=sentence_data['tone']['sense'],
            
            # Base
            base_nature=sentence_data['base']['nature'],
            
            # Dimension
            dimension_name=sentence_data['dimension']['name'],
            dimension_keynote=sentence_data['dimension']['keynote'],
            center_name=sentence_data['center']['name'],
            center_voice=sentence_data['center']['voice'],
            
            # Probabilities
            geometric_probabilities=geometric_probs,
            detected_probabilities=detected_probs,
            blended_probabilities=blended_probs,
            
            # Detection
            detected_dimension=detected_dim,
            detection_confidence=detection_conf,
            detection_themes=themes,
            
            # Metrics
            coherence=coherence,
            stability=stability,
            confidence=confidence,
            
            # Sentences
            metaphysical_sentence=sentence_data['sentences']['metaphysical'],
            scientific_sentence=sentence_data['sentences']['scientific'],
            guidance_keynote=sentence_data['sentences']['guidance']['keynote'],
            guidance_action=sentence_data['sentences']['guidance']['action'],
            guidance_approach=sentence_data['sentences']['guidance']['approach'],
            
            # Polarity
            polarity_gate=sentence_data['polarity']['gate'],
            polarity_name=sentence_data['polarity']['name'],
            
            # Metadata
            timestamp=dt.isoformat(),
            note_id=note_id
        )
        
        # Update previous state for next stability calculation
        self.previous_state = state
        
        return state
    
    def _blend_probabilities(self, geometric: Dict[str, float], 
                            detected: Dict[str, float],
                            detection_confidence: float) -> Dict[str, float]:
        """
        Blend geometric truth with detected patterns
        
        High detection confidence → more weight to detection
        Low detection confidence → more weight to geometric foundation
        
        Args:
            geometric: Probability vector from geometric foundation
            detected: Probability vector from text detection
            detection_confidence: How confident we are in the detection
            
        Returns:
            Blended probability vector
        """
        # Calculate blend weights
        # If detection confidence is high (0.8), give it 40% weight
        # If detection confidence is low (0.3), give it only 10% weight
        detection_weight = 0.5 * detection_confidence
        geometric_weight = 1.0 - detection_weight
        
        # Blend
        blended = {}
        for dim in geometric.keys():
            blended[dim] = (
                geometric_weight * geometric[dim] +
                detection_weight * detected.get(dim, 0.20)
            )
        
        # Normalize
        total = sum(blended.values())
        return {k: v / total for k, v in blended.items()}
    
    def quick_analyze(self, text: str) -> Dict:
        """
        Quick analysis returning simplified dict
        
        Args:
            text: User's text
            
        Returns:
            Dict with essential analysis data
        """
        state = self.analyze(text)
        
        return {
            'coordinate': state.coordinate_string,
            'position': state.position_string,
            'dimension': state.dimension_name,
            'probabilities': state.blended_probabilities,
            'coherence': state.coherence,
            'confidence': state.confidence,
            'sentence': state.metaphysical_sentence,
            'guidance': state.guidance_action
        }
