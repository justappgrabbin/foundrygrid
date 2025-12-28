"""
Geometric Probability Calculator

Derives probability vectors from consciousness coordinates
based on the ontological geometry of the system.
"""

from typing import Dict, List
import math


class GeometricProbability:
    """
    Calculate probability distributions from consciousness coordinates.
    
    This is the mathematical heart of the system - it converts geometric
    positions (gate.line.color.tone.base) into probability vectors that
    represent cognitive states.
    """
    
    def __init__(self, sentence_generator):
        """
        Args:
            sentence_generator: Instance of SentenceGenerator for data access
        """
        self.gen = sentence_generator
        
        # Dimension influence weights for different coordinate levels
        self.WEIGHTS = {
            'center': 0.60,      # Primary dimension from center
            'line': 0.20,        # Behavioral mode influence
            'color': 0.12,       # Motivational influence
            'tone': 0.08         # Perceptual influence
        }
    
    def calculate_probability_vector(self, coordinate) -> Dict[str, float]:
        """
        Calculate probability distribution across 5 dimensions
        
        Args:
            coordinate: Coordinate object with gate.line.color.tone.base
            
        Returns:
            Dict mapping dimension names to probabilities (sum = 1.0)
        """
        # Get the primary dimension from the gate's center
        gate = self.gen.gates[coordinate.gate]
        center = self.gen.centers[gate.center]
        primary_dimension = center.dimension
        
        # Initialize base probabilities (uniform distribution)
        probs = {
            'Movement': 0.05,
            'Evolution': 0.05,
            'Being': 0.05,
            'Design': 0.05,
            'Space': 0.05
        }
        
        # Apply center influence (60% weight)
        center_influence = self._calculate_center_influence(primary_dimension)
        for dim in probs:
            probs[dim] = (1 - self.WEIGHTS['center']) * probs[dim] + \
                        self.WEIGHTS['center'] * center_influence[dim]
        
        # Apply line influence (20% weight)
        line_influence = self._calculate_line_influence(coordinate.line, gate)
        for dim in probs:
            probs[dim] = (1 - self.WEIGHTS['line']) * probs[dim] + \
                        self.WEIGHTS['line'] * line_influence.get(dim, probs[dim])
        
        # Apply color influence (12% weight)
        color = self.gen.colors[coordinate.color - 1]
        color_influence = self._calculate_color_influence(color)
        for dim in probs:
            probs[dim] = (1 - self.WEIGHTS['color']) * probs[dim] + \
                        self.WEIGHTS['color'] * color_influence.get(dim, probs[dim])
        
        # Apply tone influence (8% weight)
        tone = self.gen.tones[coordinate.tone - 1]
        tone_influence = self._calculate_tone_influence(tone)
        for dim in probs:
            probs[dim] = (1 - self.WEIGHTS['tone']) * probs[dim] + \
                        self.WEIGHTS['tone'] * tone_influence.get(dim, probs[dim])
        
        # Normalize to ensure sum = 1.0
        total = sum(probs.values())
        return {k: v / total for k, v in probs.items()}
    
    def _calculate_center_influence(self, primary_dimension: str) -> Dict[str, float]:
        """
        Calculate dimension probabilities from center
        Primary dimension gets 0.70, others split the remainder
        """
        influence = {
            'Movement': 0.075,
            'Evolution': 0.075,
            'Being': 0.075,
            'Design': 0.075,
            'Space': 0.075
        }
        influence[primary_dimension] = 0.70
        
        total = sum(influence.values())
        return {k: v / total for k, v in influence.items()}
    
    def _calculate_line_influence(self, line_number: int, gate) -> Dict[str, float]:
        """
        Calculate dimension influence based on line behavioral mode
        
        Lines 1-6 have different cognitive patterns:
        1: Foundation (Being +)
        2: Duality (Evolution +)
        3: Process (Evolution +)
        4: Fixed (Design +)
        5: Projection (Space +)
        6: Transition (Movement +)
        """
        # Base distribution
        influence = {
            'Movement': 0.20,
            'Evolution': 0.20,
            'Being': 0.20,
            'Design': 0.20,
            'Space': 0.20
        }
        
        # Line-specific modulation
        line_modulation = {
            1: {'Being': 0.35, 'Movement': 0.25},      # Foundation
            2: {'Evolution': 0.35, 'Design': 0.25},    # Duality
            3: {'Evolution': 0.35, 'Being': 0.25},     # Process/Martyr
            4: {'Design': 0.35, 'Being': 0.25},        # Fixed
            5: {'Space': 0.35, 'Movement': 0.25},      # Projection
            6: {'Movement': 0.35, 'Evolution': 0.25}   # Transition
        }
        
        if line_number in line_modulation:
            influence.update(line_modulation[line_number])
        
        # Normalize
        total = sum(influence.values())
        return {k: v / total for k, v in influence.items()}
    
    def _calculate_color_influence(self, color: Dict) -> Dict[str, float]:
        """
        Calculate dimension influence based on color motivation
        
        Colors:
        1 Fear (Need to know) → Evolution
        2 Hope (Expectation) → Space
        3 Desire (Need to lead/follow) → Movement
        4 Need (Need to master) → Design
        5 Guilt (Need to fix) → Design
        6 Innocence (Observer) → Being
        """
        color_to_dimension = {
            'Fear': 'Evolution',
            'Hope': 'Space',
            'Desire': 'Movement',
            'Need': 'Design',
            'Guilt': 'Design',
            'Innocence': 'Being'
        }
        
        influence = {
            'Movement': 0.20,
            'Evolution': 0.20,
            'Being': 0.20,
            'Design': 0.20,
            'Space': 0.20
        }
        
        # Boost the dimension associated with this color
        associated_dim = color_to_dimension.get(color['name'])
        if associated_dim:
            influence[associated_dim] = 0.40
        
        # Normalize
        total = sum(influence.values())
        return {k: v / total for k, v in influence.items()}
    
    def _calculate_tone_influence(self, tone: Dict) -> Dict[str, float]:
        """
        Calculate dimension influence based on tone perception
        
        Tones:
        1 Security (Smell) → Being
        2 Uncertainty (Taste) → Evolution
        3 Action (Outer Vision) → Movement
        4 Meditation (Inner Vision) → Space
        5 Judgment (Feeling) → Evolution
        6 Acceptance (Touch) → Being
        """
        tone_to_dimension = {
            'Security': 'Being',
            'Uncertainty': 'Evolution',
            'Action': 'Movement',
            'Meditation': 'Space',
            'Judgment': 'Evolution',
            'Acceptance': 'Being'
        }
        
        influence = {
            'Movement': 0.20,
            'Evolution': 0.20,
            'Being': 0.20,
            'Design': 0.20,
            'Space': 0.20
        }
        
        # Boost the dimension associated with this tone
        associated_dim = tone_to_dimension.get(tone['name'])
        if associated_dim:
            influence[associated_dim] = 0.40
        
        # Normalize
        total = sum(influence.values())
        return {k: v / total for k, v in influence.items()}
    
    def calculate_coherence(self, prob_vector: Dict[str, float]) -> float:
        """
        Calculate coherence as inverse of entropy
        
        High coherence = one dimension strongly dominant
        Low coherence = probabilities spread across dimensions
        
        Args:
            prob_vector: Probability distribution across dimensions
            
        Returns:
            Coherence score (0.0 to 1.0)
        """
        # Calculate Shannon entropy
        entropy = 0.0
        for p in prob_vector.values():
            if p > 0:
                entropy -= p * math.log2(p)
        
        # Maximum entropy for 5 dimensions
        max_entropy = math.log2(5)
        
        # Coherence is inverse of normalized entropy
        normalized_entropy = entropy / max_entropy
        coherence = 1.0 - normalized_entropy
        
        return coherence
    
    def calculate_stability(self, current_probs: Dict[str, float], 
                          previous_probs: Dict[str, float] = None) -> float:
        """
        Calculate stability by comparing current to previous state
        
        If no previous state, use maximum entropy (uniform) as baseline
        
        Args:
            current_probs: Current probability distribution
            previous_probs: Previous probability distribution (optional)
            
        Returns:
            Stability score (0.0 to 1.0)
        """
        if previous_probs is None:
            # Use uniform distribution as baseline
            previous_probs = {dim: 0.20 for dim in current_probs.keys()}
        
        # Calculate Euclidean distance between distributions
        distance = 0.0
        for dim in current_probs:
            diff = current_probs[dim] - previous_probs.get(dim, 0.20)
            distance += diff ** 2
        
        distance = math.sqrt(distance)
        
        # Maximum possible distance (all prob mass shifts to one dimension)
        max_distance = math.sqrt(2)  # sqrt((1-0.2)^2 + 4*(0-0.2)^2)
        
        # Stability is inverse of normalized distance
        stability = 1.0 - (distance / max_distance)
        
        return max(0.0, min(1.0, stability))
    
    def calculate_confidence(self, coherence: float, stability: float) -> float:
        """
        Calculate overall confidence from coherence and stability
        
        Args:
            coherence: Coherence score (0.0 to 1.0)
            stability: Stability score (0.0 to 1.0)
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        # Weight coherence more heavily (70%) than stability (30%)
        confidence = 0.70 * coherence + 0.30 * stability
        return confidence
    
    def get_primary_dimension(self, prob_vector: Dict[str, float]) -> str:
        """
        Get the dimension with highest probability
        
        Args:
            prob_vector: Probability distribution
            
        Returns:
            Name of primary dimension
        """
        return max(prob_vector.items(), key=lambda x: x[1])[0]
    
    def get_secondary_dimension(self, prob_vector: Dict[str, float]) -> str:
        """
        Get the dimension with second-highest probability
        
        Args:
            prob_vector: Probability distribution
            
        Returns:
            Name of secondary dimension
        """
        sorted_dims = sorted(prob_vector.items(), key=lambda x: x[1], reverse=True)
        return sorted_dims[1][0] if len(sorted_dims) > 1 else sorted_dims[0][0]
