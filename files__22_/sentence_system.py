"""
Sentence System - Consciousness Coordinate Translation

Translates Gate.Line.Color.Tone.Base coordinates into natural language.
This is how the system SPEAKS about consciousness states.

Structure:
Gate → Theme/archetype
Line → Behavioral expression
Color → Motivation
Tone → Perception
Base → Grounding
Dimension → Processing mode

Output: Complete sentence describing the consciousness state
"""

from typing import Dict, List


class SentenceSystem:
    """
    Translates consciousness coordinates into meaningful sentences
    
    This is the LANGUAGE LAYER - how the system communicates
    consciousness states in human-readable form.
    """
    
    def __init__(self):
        # Gate themes (simplified - full version would have all 64)
        self.gate_themes = self._load_gate_themes()
        
        # Line expressions
        self.line_expressions = {
            1: "through foundation and introspection",
            2: "through natural hermit wisdom",
            3: "through experiential bonds and trial",
            4: "through fixed opportunity and networking",
            5: "through universal heretic projection",
            6: "through role model transcendence"
        }
        
        # Color motivations
        self.color_motivations = {
            1: "motivated by survival and fear",
            2: "motivated by hope and aspiration",
            3: "motivated by desire and wanting",
            4: "motivated by pure need",
            5: "motivated by guilt and conscience",
            6: "motivated by innocence and trust"
        }
        
        # Tone perceptions
        self.tone_perceptions = {
            1: "perceiving through smell and security",
            2: "perceiving through taste and discernment",
            3: "perceiving through outer vision and action",
            4: "perceiving through inner vision and meditation",
            5: "perceiving through feeling and judgment",
            6: "perceiving through touch and acceptance"
        }
        
        # Base groundings
        self.base_groundings = {
            1: "grounded in prevention",
            2: "grounded in caves and safety",
            3: "grounded in power and action",
            4: "grounded in wanting and desire",
            5: "grounded in probability and possibility"
        }
        
        # Dimension processing
        self.dimension_processing = {
            'Movement': "processing through kinetic energy and action",
            'Evolution': "processing through memory and pattern recognition",
            'Being': "processing through present moment awareness",
            'Design': "processing through structure and architecture",
            'Space': "processing through infinite possibility"
        }
    
    def _load_gate_themes(self) -> Dict:
        """Load gate themes (simplified version)"""
        return {
            1: "Creative self-expression",
            2: "Direction of the self",
            3: "Ordering and mutation",
            4: "Formulization",
            5: "Fixed rhythms and patterns",
            6: "Friction and conflict",
            7: "Role of the self in interaction",
            8: "Contribution",
            9: "Focus and detail",
            10: "Behavior of the self",
            13: "Listener and fellowship",
            14: "Power skills and resources",
            15: "Extremes and modesty",
            16: "Skills and enthusiasm",
            17: "Opinions and following",
            18: "Correction and perfection",
            19: "Wanting and needs",
            20: "The now and contemplation",
            21: "Control and authority",
            22: "Grace and openness",
            23: "Assimilation and splitting apart",
            24: "Rationalization and return",
            25: "Spirit of the self",
            26: "The egoist and taming power",
            27: "Caring and nourishment",
            28: "The game player and preponderance",
            29: "Saying yes and perseverance",
            30: "Recognition of feelings and fate",
            31: "Leading and influence",
            32: "Continuity and duration",
            33: "Privacy and retreat",
            34: "Power and great power",
            35: "Progress and change",
            36: "Crisis and darkening of light",
            37: "Friendship and family",
            38: "Opposition and fighter",
            39: "Provocation and obstruction",
            40: "Aloneness and deliverance",
            41: "Decrease and contraction",
            42: "Increase and growth",
            43: "Breakthrough and insight",
            44: "Coming to meet and alertness",
            45: "Gathering together",
            46: "Determination and pushing upward",
            47: "Oppression and realization",
            48: "The well and depth",
            49: "Revolution and principles",
            50: "Values and the cauldron",
            51: "Shock and arousing",
            52: "Stillness and keeping still",
            53: "Development and beginnings",
            54: "Ambition and marrying maiden",
            55: "Spirit and abundance",
            56: "Stimulation and wanderer",
            57: "Intuitive clarity and gentle",
            58: "Vitality and joyous",
            59: "Sexuality and dispersion",
            60: "Limitation and acceptance",
            61: "Mystery and inner truth",
            62: "Details and preponderance of small",
            63: "After completion and doubt",
            64: "Before completion and confusion"
        }
    
    def generate_sentence(self, coordinate: str, dimension: str,
                         coherence: float, stability: float = None) -> str:
        """
        Generate complete sentence describing consciousness state
        
        Args:
            coordinate: Gate.Line.Color.Tone.Base
            dimension: Primary dimension name
            coherence: Coherence level (0-1)
            stability: Optional stability level (0-1)
            
        Returns:
            Natural language sentence
        """
        parts = coordinate.split('.')
        gate = int(parts[0])
        line = int(parts[1]) if len(parts) > 1 else 1
        color = int(parts[2]) if len(parts) > 2 else 1
        tone = int(parts[3]) if len(parts) > 3 else 1
        base = int(parts[4]) if len(parts) > 4 else 1
        
        # Build sentence components
        gate_phrase = self.gate_themes.get(gate, "consciousness expression")
        line_phrase = self.line_expressions[line]
        color_phrase = self.color_motivations[color]
        tone_phrase = self.tone_perceptions[tone]
        base_phrase = self.base_groundings[base]
        dim_phrase = self.dimension_processing[dimension]
        
        # Add coherence descriptor
        if coherence > 0.7:
            coherence_desc = "with strong focus and clarity"
        elif coherence > 0.4:
            coherence_desc = "with balanced presence"
        else:
            coherence_desc = "with scattered energy"
        
        # Build complete sentence
        sentence = f"You are expressing {gate_phrase} {line_phrase}, "
        sentence += f"{color_phrase}, {tone_phrase}, and {base_phrase}, "
        sentence += f"while {dim_phrase} {coherence_desc}."
        
        # Add stability context if provided
        if stability is not None:
            if stability > 0.7:
                sentence += " This state is very stable for you."
            elif stability > 0.4:
                sentence += " This state fluctuates naturally."
            else:
                sentence += " This is a transitional state."
        
        return sentence
    
    def generate_short_sentence(self, coordinate: str, dimension: str) -> str:
        """Generate brief sentence (for compact displays)"""
        parts = coordinate.split('.')
        gate = int(parts[0])
        line = int(parts[1]) if len(parts) > 1 else 1
        
        gate_phrase = self.gate_themes.get(gate, "consciousness")
        line_phrase = self.line_expressions[line].split(" and ")[0]  # Just first part
        
        return f"{gate_phrase} {line_phrase}, {dimension} processing"
    
    def generate_path_sentence(self, from_coordinate: str, to_coordinate: str,
                              intervention: str, probability: float) -> str:
        """
        Generate sentence describing a path from one state to another
        
        Used by enhanced GameGAN for path calculation
        """
        # Parse coordinates
        from_parts = from_coordinate.split('.')
        to_parts = to_coordinate.split('.')
        
        from_gate = int(from_parts[0])
        to_gate = int(to_parts[0])
        
        from_theme = self.gate_themes.get(from_gate, "current state")
        to_theme = self.gate_themes.get(to_gate, "new state")
        
        # Probability descriptor
        if probability > 0.8:
            prob_desc = "very likely"
        elif probability > 0.6:
            prob_desc = "likely"
        elif probability > 0.4:
            prob_desc = "possible"
        else:
            prob_desc = "unlikely"
        
        sentence = f"Moving from {from_theme} to {to_theme} "
        sentence += f"through '{intervention}' is {prob_desc} "
        sentence += f"({probability:.0%} probability)."
        
        return sentence
    
    def generate_intervention_sentence(self, intervention_type: str,
                                      dimension: str, coherence: float) -> str:
        """
        Generate sentence recommending intervention
        
        Used by enhanced GameGAN
        """
        interventions = {
            'consolidation': {
                'high': f"Your {dimension} energy is scattered. Consolidate by focusing on one thing.",
                'medium': f"Your {dimension} processing would benefit from gentle focusing.",
                'low': f"With low coherence, {dimension} awareness needs immediate grounding."
            },
            'expansion': {
                'high': f"Your focused {dimension} state can now expand into new territory.",
                'medium': f"Balanced {dimension} energy supports careful expansion.",
                'low': f"Before expanding, consolidate your {dimension} processing first."
            },
            'maintenance': {
                'high': f"Your {dimension} coherence is strong - maintain this clarity.",
                'medium': f"Keep this balanced {dimension} state through consistent practice.",
                'low': f"Low {dimension} coherence requires immediate stabilization."
            }
        }
        
        # Determine coherence level
        if coherence > 0.6:
            level = 'high'
        elif coherence > 0.3:
            level = 'medium'
        else:
            level = 'low'
        
        return interventions.get(intervention_type, {}).get(level, 
            f"Focus on {dimension} awareness.")
    
    def explain_coordinate(self, coordinate: str) -> Dict[str, str]:
        """
        Full explanation of coordinate components
        
        Returns dictionary with explanations for each layer
        """
        parts = coordinate.split('.')
        gate = int(parts[0])
        line = int(parts[1]) if len(parts) > 1 else 1
        color = int(parts[2]) if len(parts) > 2 else 1
        tone = int(parts[3]) if len(parts) > 3 else 1
        base = int(parts[4]) if len(parts) > 4 else 1
        
        return {
            'coordinate': coordinate,
            'gate': {
                'number': gate,
                'theme': self.gate_themes.get(gate, "Unknown"),
                'explanation': f"Gate {gate} represents {self.gate_themes.get(gate, 'consciousness').lower()}"
            },
            'line': {
                'number': line,
                'expression': self.line_expressions[line],
                'explanation': f"Line {line} expresses {self.line_expressions[line]}"
            },
            'color': {
                'number': color,
                'motivation': self.color_motivations[color],
                'explanation': f"Color {color} is {self.color_motivations[color]}"
            },
            'tone': {
                'number': tone,
                'perception': self.tone_perceptions[tone],
                'explanation': f"Tone {tone} is {self.tone_perceptions[tone]}"
            },
            'base': {
                'number': base,
                'grounding': self.base_groundings[base],
                'explanation': f"Base {base} is {self.base_groundings[base]}"
            }
        }


# Helper functions
def translate_coordinate(coordinate: str, dimension: str,
                        coherence: float = 0.5) -> str:
    """
    Quick function to translate coordinate to sentence
    
    Example:
        sentence = translate_coordinate("5.1.4.1.4", "Being", 0.45)
        print(sentence)
    """
    system = SentenceSystem()
    return system.generate_sentence(coordinate, dimension, coherence)


def explain_state(coordinate: str, dimension: str, coherence: float) -> str:
    """
    Generate full explanation of current state
    
    Example:
        explanation = explain_state("5.1.4.1.4", "Being", 0.45)
        print(explanation)
    """
    system = SentenceSystem()
    
    # Get sentence
    sentence = system.generate_sentence(coordinate, dimension, coherence)
    
    # Get detailed explanation
    details = system.explain_coordinate(coordinate)
    
    # Build full explanation
    explanation = f"{sentence}\n\n"
    explanation += "Breakdown:\n"
    explanation += f"• Gate {details['gate']['number']}: {details['gate']['theme']}\n"
    explanation += f"• Line {details['line']['number']}: {details['line']['expression']}\n"
    explanation += f"• Color {details['color']['number']}: {details['color']['motivation']}\n"
    explanation += f"• Tone {details['tone']['number']}: {details['tone']['perception']}\n"
    explanation += f"• Base {details['base']['number']}: {details['base']['grounding']}\n"
    explanation += f"• Dimension: {dimension}\n"
    explanation += f"• Coherence: {coherence:.1%}"
    
    return explanation
