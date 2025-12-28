"""
Consciousness Sentence Generator - Complete Implementation
YOU-N-I-VERSE Framework Integration Module

This is the mathematical foundation - the exact ontological framework
that defines how consciousness coordinates map to sentences.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import math


@dataclass
class Coordinate:
    """Consciousness coordinate in 5-dimensional space"""
    gate: int
    line: int
    color: int
    tone: int
    base: int
    sign: str
    degrees: int
    minutes: int
    seconds: float


@dataclass
class Gate:
    """Gate definition"""
    number: int
    name: str
    theme: str
    center: str
    amino: str


@dataclass
class Center:
    """Center definition"""
    name: str
    dimension: str
    voice: str
    color: str


@dataclass
class Dimension:
    """Dimension definition"""
    name: str
    keynote: str
    phrase: str


class SentenceGenerator:
    """
    The ontological core - converts astronomical positions
    to consciousness coordinates and generates sentences.
    """
    
    # Geometric constants (in arcseconds)
    GATE_WIDTH_SECONDS = 20250    # 5°37'30"
    LINE_WIDTH_SECONDS = 3375     # 56'15"
    COLOR_WIDTH_SECONDS = 562.5   # 9'22.5"
    TONE_WIDTH_SECONDS = 93.75    # 1'33.75"
    BASE_WIDTH_SECONDS = 18.75    # 18.75"
    
    def __init__(self):
        self.zodiac_wheel = self._init_zodiac_wheel()
        self.gates = self._init_gates()
        self.lines = self._init_lines()
        self.colors = self._init_colors()
        self.tones = self._init_tones()
        self.bases = self._init_bases()
        self.centers = self._init_centers()
        self.dimensions = self._init_dimensions()
        self.polarities = self._init_polarities()
        self.grammar = self._init_grammar()
    
    # ═══════════════════════════════════════════════════════════════════
    # MAIN PARSING FUNCTION
    # ═══════════════════════════════════════════════════════════════════
    
    def parse_position(self, degrees: int, minutes: int, seconds: float, zodiac_sign: str) -> Coordinate:
        """
        Convert astronomical position to consciousness coordinate
        
        Args:
            degrees: 0-29 within zodiac sign
            minutes: 0-59
            seconds: 0-59.999
            zodiac_sign: One of 12 zodiac signs
            
        Returns:
            Coordinate with gate.line.color.tone.base
        """
        # Validate inputs
        if not (0 <= degrees < 30):
            raise ValueError(f"Degrees must be 0-29, got {degrees}")
        if not (0 <= minutes < 60):
            raise ValueError(f"Minutes must be 0-59, got {minutes}")
        if not (0 <= seconds < 60):
            raise ValueError(f"Seconds must be 0-59.999, got {seconds}")
        
        # Convert to total arcseconds within the sign
        total_seconds = (degrees * 3600) + (minutes * 60) + seconds
        
        # Find the gate
        gate_info = self._find_gate_from_position(total_seconds, zodiac_sign)
        if not gate_info:
            raise ValueError(f"Invalid position: {degrees}°{minutes}'{seconds}\" {zodiac_sign}")
        
        # Calculate offset within the gate
        offset_in_gate = total_seconds - gate_info['start']
        
        # Calculate subdivisions
        line = min(math.floor(offset_in_gate / self.LINE_WIDTH_SECONDS) + 1, 6)
        line_offset = offset_in_gate % self.LINE_WIDTH_SECONDS
        
        color = min(math.floor(line_offset / self.COLOR_WIDTH_SECONDS) + 1, 6)
        color_offset = line_offset % self.COLOR_WIDTH_SECONDS
        
        tone = min(math.floor(color_offset / self.TONE_WIDTH_SECONDS) + 1, 6)
        tone_offset = color_offset % self.TONE_WIDTH_SECONDS
        
        base = min(math.floor(tone_offset / self.BASE_WIDTH_SECONDS) + 1, 5)
        
        return Coordinate(
            gate=gate_info['number'],
            line=line,
            color=color,
            tone=tone,
            base=base,
            sign=zodiac_sign,
            degrees=degrees,
            minutes=minutes,
            seconds=seconds
        )
    
    def parse(self, input_str: str) -> Coordinate:
        """
        Parse various formats:
        - "17°23'45\" Leo"
        - "17d 23m 45s Leo"
        - "17 23 45 Leo"
        """
        import re
        
        # Extract zodiac sign
        zodiac_signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        sign = None
        for z in zodiac_signs:
            if z.lower() in input_str.lower():
                sign = z
                input_str = input_str.lower().replace(z.lower(), '').strip()
                break
        
        if not sign:
            raise ValueError("No zodiac sign found in input")
        
        # Try different formats
        # Format: 17°23'45"
        match = re.search(r'(\d+)°\s*(\d+)\'\s*(\d+\.?\d*)"?', input_str)
        if match:
            return self.parse_position(
                int(match.group(1)),
                int(match.group(2)),
                float(match.group(3)),
                sign
            )
        
        # Format: 17d 23m 45s
        match = re.search(r'(\d+)d\s*(\d+)m\s*(\d+\.?\d*)s?', input_str, re.I)
        if match:
            return self.parse_position(
                int(match.group(1)),
                int(match.group(2)),
                float(match.group(3)),
                sign
            )
        
        # Format: 17 23 45
        match = re.search(r'(\d+)\s+(\d+)\s+(\d+\.?\d*)', input_str)
        if match:
            return self.parse_position(
                int(match.group(1)),
                int(match.group(2)),
                float(match.group(3)),
                sign
            )
        
        raise ValueError(f"Could not parse position format: {input_str}")
    
    # ═══════════════════════════════════════════════════════════════════
    # SENTENCE GENERATION
    # ═══════════════════════════════════════════════════════════════════
    
    def generate_sentence(self, coordinate: Coordinate) -> Dict:
        """
        Generate complete consciousness sentence from coordinate
        
        Returns:
            Dict with metaphysical, scientific, and guidance sentences
        """
        gate = self.gates[coordinate.gate]
        line = self.lines[coordinate.gate][coordinate.line - 1]
        color = self.colors[coordinate.color - 1]
        tone = self.tones[coordinate.tone - 1]
        base = self.bases[coordinate.base - 1]
        center = self.centers[gate.center]
        dimension = self.dimensions[center.dimension]
        
        # Build sentences
        metaphysical = self._build_metaphysical_sentence(
            dimension, gate, line, color, tone, base, center
        )
        
        scientific = self._build_scientific_sentence(
            dimension, gate, line, color, tone, base, center
        )
        
        guidance = self._build_guidance(
            dimension, gate, line, color, tone, base
        )
        
        polarity = self.polarities.get(coordinate.gate)
        
        return {
            'coordinate': f"{coordinate.gate}.{coordinate.line}.{coordinate.color}.{coordinate.tone}.{coordinate.base}",
            'position': f"{coordinate.degrees}°{coordinate.minutes}'{coordinate.seconds}\" {coordinate.sign}",
            'gate': {
                'number': coordinate.gate,
                'name': gate.name,
                'theme': gate.theme,
                'center': gate.center,
                'amino': gate.amino
            },
            'line': {
                'number': coordinate.line,
                'name': line
            },
            'color': {
                'number': coordinate.color,
                'name': color['name'],
                'motivation': color['motivation'],
                'determination': color['determination']
            },
            'tone': {
                'number': coordinate.tone,
                'name': tone['name'],
                'sense': tone['sense']
            },
            'base': {
                'number': coordinate.base,
                'nature': base['nature']
            },
            'dimension': {
                'name': dimension.name,
                'keynote': dimension.keynote
            },
            'center': {
                'name': center.name,
                'voice': center.voice
            },
            'polarity': {
                'gate': polarity,
                'name': self.gates[polarity].name if polarity else None
            },
            'sentences': {
                'metaphysical': metaphysical,
                'scientific': scientific,
                'guidance': guidance
            }
        }
    
    def _build_metaphysical_sentence(self, dimension, gate, line, color, tone, base, center) -> str:
        """Build metaphysical sentence using grammar"""
        g = self.grammar
        
        return (
            f"{dimension.keynote} {gate.theme} {g['transitioner']} "
            f"{line} {g['collapse']} "
            f"motivated by {color['motivation']} {g['pulse']} "
            f"resonating through {tone['sense']} {g['flicker']} "
            f"rooted in {base['nature']} foundation {g['breath']} "
            f"{center.voice}{g['current']}"
        )
    
    def _build_scientific_sentence(self, dimension, gate, line, color, tone, base, center) -> str:
        """Build scientific sentence"""
        return (
            f"Gate {gate.number} ({gate.amino} amino acid) expresses "
            f"{dimension.name} dimension through {center.name} center, "
            f"manifesting via Line {line.split(':')[0] if ':' in line else line}, "
            f"Color {color['name']} ({color['determination']}), "
            f"Tone {tone['name']} ({tone['sense']} sensory), "
            f"Base {base['nature']}"
        )
    
    def _build_guidance(self, dimension, gate, line, color, tone, base) -> Dict:
        """Build actionable guidance"""
        actions = {
            'Movement': f"Define your unique expression of {gate.theme}",
            'Evolution': f"Remember the wisdom within {gate.theme}",
            'Being': f"Embody {gate.theme} in tangible reality",
            'Design': f"Structure your life around {gate.theme}",
            'Space': f"Imagine the possibilities of {gate.theme}"
        }
        
        approach = (
            f"Your motivation is {color['motivation'].lower()}, "
            f"perceived through {tone['sense'].lower()}. "
            f"Approach this from a {base['nature'].lower()} perspective."
        )
        
        return {
            'keynote': dimension.keynote,
            'action': actions[dimension.name],
            'approach': approach,
            'theme': gate.theme,
            'expression': line
        }
    
    # ═══════════════════════════════════════════════════════════════════
    # HELPER FUNCTIONS
    # ═══════════════════════════════════════════════════════════════════
    
    def _find_gate_from_position(self, arcseconds: float, zodiac_sign: str) -> Optional[Dict]:
        """Find which gate contains this position"""
        sign_gates = self.zodiac_wheel.get(zodiac_sign)
        if not sign_gates:
            return None
        
        for gate_info in sign_gates:
            if gate_info['start'] <= arcseconds < gate_info['end']:
                return gate_info
        
        return None
    
    # ═══════════════════════════════════════════════════════════════════
    # DATA INITIALIZATION
    # ═══════════════════════════════════════════════════════════════════
    
    def _init_zodiac_wheel(self) -> Dict:
        """Initialize zodiac wheel with gate positions"""
        return {
            'Aries': [
                {'number': 25, 'start': 0, 'end': 20250},
                {'number': 17, 'start': 20250, 'end': 40500},
                {'number': 21, 'start': 40500, 'end': 60750},
                {'number': 51, 'start': 60750, 'end': 81000},
                {'number': 42, 'start': 81000, 'end': 101250}
            ],
            'Taurus': [
                {'number': 3, 'start': 0, 'end': 20250},
                {'number': 27, 'start': 20250, 'end': 40500},
                {'number': 24, 'start': 40500, 'end': 60750},
                {'number': 2, 'start': 60750, 'end': 81000},
                {'number': 23, 'start': 81000, 'end': 101250}
            ],
            'Gemini': [
                {'number': 8, 'start': 0, 'end': 20250},
                {'number': 20, 'start': 20250, 'end': 40500},
                {'number': 16, 'start': 40500, 'end': 60750},
                {'number': 35, 'start': 60750, 'end': 81000},
                {'number': 45, 'start': 81000, 'end': 101250}
            ],
            'Cancer': [
                {'number': 12, 'start': 0, 'end': 20250},
                {'number': 15, 'start': 20250, 'end': 40500},
                {'number': 52, 'start': 40500, 'end': 60750},
                {'number': 39, 'start': 60750, 'end': 81000},
                {'number': 53, 'start': 81000, 'end': 101250}
            ],
            'Leo': [
                {'number': 62, 'start': 0, 'end': 20250},
                {'number': 56, 'start': 20250, 'end': 40500},
                {'number': 31, 'start': 40500, 'end': 60750},
                {'number': 33, 'start': 60750, 'end': 81000},
                {'number': 7, 'start': 81000, 'end': 101250}
            ],
            'Virgo': [
                {'number': 4, 'start': 0, 'end': 20250},
                {'number': 29, 'start': 20250, 'end': 40500},
                {'number': 59, 'start': 40500, 'end': 60750},
                {'number': 40, 'start': 60750, 'end': 81000},
                {'number': 64, 'start': 81000, 'end': 101250}
            ],
            'Libra': [
                {'number': 47, 'start': 0, 'end': 20250},
                {'number': 6, 'start': 20250, 'end': 40500},
                {'number': 46, 'start': 40500, 'end': 60750},
                {'number': 18, 'start': 60750, 'end': 81000},
                {'number': 48, 'start': 81000, 'end': 101250}
            ],
            'Scorpio': [
                {'number': 57, 'start': 0, 'end': 20250},
                {'number': 32, 'start': 20250, 'end': 40500},
                {'number': 50, 'start': 40500, 'end': 60750},
                {'number': 28, 'start': 60750, 'end': 81000},
                {'number': 44, 'start': 81000, 'end': 101250}
            ],
            'Sagittarius': [
                {'number': 1, 'start': 0, 'end': 20250},
                {'number': 43, 'start': 20250, 'end': 40500},
                {'number': 14, 'start': 40500, 'end': 60750},
                {'number': 34, 'start': 60750, 'end': 81000},
                {'number': 9, 'start': 81000, 'end': 101250}
            ],
            'Capricorn': [
                {'number': 5, 'start': 0, 'end': 20250},
                {'number': 26, 'start': 20250, 'end': 40500},
                {'number': 11, 'start': 40500, 'end': 60750},
                {'number': 10, 'start': 60750, 'end': 81000},
                {'number': 58, 'start': 81000, 'end': 101250}
            ],
            'Aquarius': [
                {'number': 38, 'start': 0, 'end': 20250},
                {'number': 54, 'start': 20250, 'end': 40500},
                {'number': 61, 'start': 40500, 'end': 60750},
                {'number': 60, 'start': 60750, 'end': 81000},
                {'number': 41, 'start': 81000, 'end': 101250}
            ],
            'Pisces': [
                {'number': 19, 'start': 0, 'end': 20250},
                {'number': 13, 'start': 20250, 'end': 40500},
                {'number': 49, 'start': 40500, 'end': 60750},
                {'number': 30, 'start': 60750, 'end': 81000},
                {'number': 55, 'start': 81000, 'end': 101250}
            ]
        }
    
    def _init_gates(self) -> Dict[int, Gate]:
        """Initialize all 64 gates"""
        gates_data = [
            (1, "The Creative", "Self-Expression", "G", "Met"),
            (2, "The Receptive", "Direction of the Self", "G", "Ile"),
            (3, "Difficulty at the Beginning", "Ordering", "Sacral", "Leu"),
            (4, "Youthful Folly", "Formulization", "Ajna", "Phe"),
            (5, "Waiting", "Fixed Rhythms", "Sacral", "Ser"),
            (6, "Conflict", "Friction", "Solar Plexus", "Tyr"),
            (7, "The Army", "Role of the Self", "G", "Gly"),
            (8, "Holding Together", "Contribution", "Throat", "Ala"),
            (9, "Taming Power of Small", "Focus", "Sacral", "Val"),
            (10, "Treading", "Behavior of the Self", "G", "Thr"),
            (11, "Peace", "Ideas", "Ajna", "Asp"),
            (12, "Standstill", "Caution", "Throat", "Glu"),
            (13, "Fellowship", "The Listener", "G", "Asn"),
            (14, "Great Possession", "Power Skills", "Sacral", "Gln"),
            (15, "Modesty", "Extremes", "G", "Lys"),
            (16, "Enthusiasm", "Skills", "Throat", "His"),
            (17, "Following", "Opinions", "Ajna", "Arg"),
            (18, "Work on Spoilt", "Correction", "Spleen", "Trp"),
            (19, "Approach", "Wanting", "Root", "Cys"),
            (20, "Contemplation", "Now", "Throat", "Arg"),
            (21, "Biting Through", "Hunter/Huntress", "Heart", "Ser"),
            (22, "Grace", "Openness", "Solar Plexus", "Leu"),
            (23, "Splitting Apart", "Assimilation", "Throat", "Ile"),
            (24, "Return", "Rationalization", "Ajna", "Met"),
            (25, "Innocence", "Spirit of Self", "G", "Phe"),
            (26, "Great Taming", "Egoist", "Heart", "Tyr"),
            (27, "Nourishment", "Caring", "Sacral", "Gly"),
            (28, "Great Excess", "Game Player", "Spleen", "Ala"),
            (29, "Abysmal", "Perseverance", "Sacral", "Val"),
            (30, "Clinging Fire", "Feelings", "Solar Plexus", "Thr"),
            (31, "Influence", "Leading", "Throat", "Asp"),
            (32, "Duration", "Continuity", "Spleen", "Glu"),
            (33, "Retreat", "Privacy", "Throat", "Asn"),
            (34, "Great Power", "Power", "Sacral", "Gln"),
            (35, "Progress", "Change", "Throat", "Lys"),
            (36, "Darkening", "Crisis", "Solar Plexus", "His"),
            (37, "Family", "Friendship", "Solar Plexus", "Arg"),
            (38, "Opposition", "Fighter", "Root", "Trp"),
            (39, "Obstruction", "Provocateur", "Root", "Cys"),
            (40, "Deliverance", "Aloneness", "Heart", "Arg"),
            (41, "Decrease", "Contraction", "Root", "Ser"),
            (42, "Increase", "Growth", "Sacral", "Leu"),
            (43, "Breakthrough", "Insight", "Ajna", "Ile"),
            (44, "Coming to Meet", "Alertness", "Spleen", "Met"),
            (45, "Gathering", "Gathering", "Throat", "Phe"),
            (46, "Pushing Upward", "Determination", "G", "Tyr"),
            (47, "Oppression", "Realization", "Ajna", "Gly"),
            (48, "The Well", "Depth", "Spleen", "Ala"),
            (49, "Revolution", "Principles", "Solar Plexus", "Val"),
            (50, "The Cauldron", "Values", "Spleen", "Thr"),
            (51, "Arousing", "Shock", "Heart", "Asp"),
            (52, "Keeping Still", "Stillness", "Root", "Glu"),
            (53, "Development", "Beginnings", "Root", "Asn"),
            (54, "Marrying Maiden", "Ambition", "Root", "Gln"),
            (55, "Abundance", "Spirit", "Solar Plexus", "Lys"),
            (56, "Wanderer", "Stimulation", "Throat", "His"),
            (57, "Gentle", "Intuitive Clarity", "Spleen", "Arg"),
            (58, "Joyous", "Vitality", "Root", "Trp"),
            (59, "Dispersion", "Sexuality", "Sacral", "Cys"),
            (60, "Limitation", "Acceptance", "Root", "Arg"),
            (61, "Inner Truth", "Mystery", "Head", "Ser"),
            (62, "Small Excess", "Detail", "Throat", "Leu"),
            (63, "After Completion", "Doubt", "Head", "Ile"),
            (64, "Before Completion", "Confusion", "Head", "Met")
        ]
        
        return {
            num: Gate(num, name, theme, center, amino)
            for num, name, theme, center, amino in gates_data
        }
    
    def _init_lines(self) -> Dict[int, List[str]]:
        """Initialize all 384 lines (6 per gate)"""
        return {
            1: ["Objectivity", "Love is Light", "Energy to Sustain Creative Work", "Aloneness as Medium of Creativity", "Energy to Attract Society", "Self-Preservation"],
            2: ["Intuition", "Genius", "Patience", "Secretiveness", "Intelligent Application", "Fixation"],
            3: ["Synthesis", "Immaturity", "Survival", "Charisma", "Victimization", "Surrender"],
            4: ["Pleasure", "Acceptance", "Irresponsibility", "Suspension", "Seduction", "Excess"],
            5: ["Perseverance", "Inner Peace", "Compulsiveness", "The Hunter", "Joy", "Yielding"],
            6: ["Retreat", "The Guerrilla", "Allegiance", "Triumph", "Arbitration", "The Peacemaker"],
            7: ["Authoritarian", "The Democrat", "The Anarchist", "The Abdicator", "The General", "The Administrator"],
            8: ["Honesty", "Service", "Phoniness", "Phasing", "Dharma", "Communion"],
            9: ["Sensibility", "Misery Loves Company", "Straw that Breaks Camel's Back", "Dedication", "Faith", "Gratitude"],
            10: ["Modesty", "The Hermit", "The Martyr", "The Opportunist", "The Heretic", "The Role Model"],
            11: ["Reconnaissance", "Rigor", "Realism", "The Teacher", "The Philanthropist", "Adaptability"],
            12: ["The Monk", "Purification", "Confession", "The Prophet", "The Pragmatist", "Metamorphosis"],
            13: ["Empathy", "Bigotry", "Pessimism", "Fatigue", "The Savior", "Optimism"],
            14: ["Money isn't Everything", "Management", "Service", "Security", "Arrogance", "Humility"],
            15: ["Duty", "Influence", "Ego Inflation", "The Wallflower", "Sensitivity", "Self-Defense"],
            16: ["Delusion", "Cynicism", "Independence", "Leader", "The Grinch", "Gullibility"],
            17: ["Openness", "Discrimination", "Self-Understanding", "Personnel Manager", "No Error", "Bodhisattva"],
            18: ["Conservatism", "Terminal Disease", "The Zealot", "The Incompetent", "Therapy", "Buddhahood"],
            19: ["Interdependence", "Service", "Dedication", "Teamwork", "Sacrifice", "Recluse"],
            20: ["Superficiality", "The Dogmatist", "Self-Awareness", "Application", "Realism", "Wisdom"],
            21: ["Humility", "The Court", "Powerlessness", "Strategy", "Objectivity", "Chaos"],
            22: ["Second Thoughts", "Charm School", "The Believer", "Sensitivity", "Directness", "Maturity"],
            23: ["Proselytization", "Self-Defense", "Individuality", "Fragmentation", "Exegesis", "Fusion"],
            24: ["The Miller", "Recognition", "The Addict", "The Hermit", "Confession", "Gifted Horse"],
            25: ["Selflessness", "Existence", "Sensibility", "Spiritual Nature", "Recuperation", "Ignorance"],
            26: ["Bird in Hand", "Lessons of History", "Influence", "Censorship", "Adaptability", "Authority"],
            27: ["Selfishness", "Self-Sufficiency", "Greed", "Generosity", "Executor", "Wariness"],
            28: ["Preparation", "Shake Hands with Devil", "Adventurism", "Holding On", "Treacherous Nature", "Blaze of Glory"],
            29: ["The Draftsman", "Assessment", "Evaluation", "Directness", "Overreach", "Confusion"],
            30: ["Composure", "Pragmatism", "Resignation", "Burnout", "Irony", "Enforcement"],
            31: ["Manifestation", "Arrogance", "Selectivity", "Intent", "Self-Righteousness", "Application"],
            32: ["Conservation", "Restraint", "Lack of Continuity", "Right is Might", "Flexibility", "Tranquillity"],
            33: ["Avoidance", "Surrender", "Spirit", "Dignity", "Timing", "Disassociation"],
            34: ["Bully", "Momentum", "Machismo", "Triumph", "Annihilation", "Common Sense"],
            35: ["Humility", "Creative Block", "Efficiency", "Hunger", "Altruism", "Rectification"],
            36: ["Resistance", "Support", "Transition", "Espionage", "Underground", "Justice"],
            37: ["Mother/Father", "Responsibility", "Invidiousness", "Leadership", "Love", "Purpose"],
            38: ["Qualification", "Politeness", "Alliance", "Investigation", "Alienation", "Naiveté"],
            39: ["Disengagement", "Confrontation", "Responsibility", "Temperance", "Single-mindedness", "Troubleshooter"],
            40: ["Recuperation", "Resoluteness", "Humility", "Organization", "Rigidity", "Decisiveness"],
            41: ["Reasonableness", "Caution", "Efficiency", "Correction", "Anticipation", "Manifestation"],
            42: ["Diversification", "Identification", "Trial and Error", "Middle Management", "Self-Actualization", "Nurturing"],
            43: ["Patience", "Dedication", "Surrender", "Minds-Eye", "Progression", "Breakthrough"],
            44: ["Conditions", "Management", "Interference", "Honesty", "Manipulation", "Aloofness"],
            45: ["Canvassing", "Consensus", "Exclusion", "Direction", "Leadership", "Reconsideration"],
            46: ["Being Discovered", "Departure", "Projection", "Impact", "Pacing", "Integrity"],
            47: ["Taking Stock", "Ambition", "Self-Oppression", "Constraint", "The Saint", "Futility"],
            48: ["Insignificance", "Degeneracy", "Incommunicado", "Restructuring", "Action", "Self-Fulfillment"],
            49: ["Relevance", "Last Resort", "Popular Discontent", "Platform", "Sacrifice", "Liberty"],
            50: ["Immature Rigidity", "Benevolence", "Adaptability", "Corruption", "Consistency", "Leadership"],
            51: ["Reference", "Withdrawal", "Adaptation", "Limitation", "Symmetry", "Separation"],
            52: ["Think Before You Speak", "Concern", "Controls", "Self-discipline", "Explanation", "Peacefulness"],
            53: ["Accumulation", "Momentum", "Practicality", "Assuredness", "Assertion", "Phasing"],
            54: ["Influence", "Discretion", "Covert Interaction", "Enlightenment/Endarkenment", "Magnanimity", "Selectivity"],
            55: ["Cooperation", "Distrust", "Innocence", "Assimilation", "Cause", "Selfishness"],
            56: ["Quality", "Linkage", "Readiness", "Expediency", "Attracting Attention", "Caution"],
            57: ["Confusion", "Cleansing", "Acuteness", "The Director", "Progression", "Utilization"],
            58: ["Love of Life", "Perversion", "Electricity", "Focusing", "Defense", "Carried Away"],
            59: ["Pre-emptive Strike", "Shyness", "Openness", "Brotherhood/Sisterhood", "Femme Fatale/Casanova", "One Night Stand"],
            60: ["Acceptance", "Decisiveness", "Conservatism", "Resourcefulness", "Leadership", "Rigidity"],
            61: ["Occult Knowledge", "Natural Brilliance", "Dependence", "Research", "Influence", "Appeal"],
            62: ["Routine", "Restraint", "Discovery", "Asceticism", "Discipline", "Self-discipline"],
            63: ["Composure", "Structuring", "Continuance", "Memory", "Affirmation", "Nostalgia"],
            64: ["Conditions", "Qualification", "Over-extension", "Conviction", "Promise", "Victory"]
        }
    
    def _init_colors(self) -> List[Dict]:
        """Initialize 6 colors"""
        return [
            {'name': 'Fear', 'motivation': 'Need to know', 'determination': 'Appetite'},
            {'name': 'Hope', 'motivation': 'Expectation', 'determination': 'Taste'},
            {'name': 'Desire', 'motivation': 'Need to lead/follow', 'determination': 'Thirst'},
            {'name': 'Need', 'motivation': 'Need to master', 'determination': 'Touch'},
            {'name': 'Guilt', 'motivation': 'Need to fix', 'determination': 'Sound'},
            {'name': 'Innocence', 'motivation': 'Observer', 'determination': 'Light'}
        ]
    
    def _init_tones(self) -> List[Dict]:
        """Initialize 6 tones"""
        return [
            {'name': 'Security', 'sense': 'Smell'},
            {'name': 'Uncertainty', 'sense': 'Taste'},
            {'name': 'Action', 'sense': 'Outer Vision'},
            {'name': 'Meditation', 'sense': 'Inner Vision'},
            {'name': 'Judgment', 'sense': 'Feeling'},
            {'name': 'Acceptance', 'sense': 'Touch'}
        ]
    
    def _init_bases(self) -> List[Dict]:
        """Initialize 5 bases"""
        return [
            {'nature': 'Reactive'},
            {'nature': 'Integrative'},
            {'nature': 'Objective'},
            {'nature': 'Progressive'},
            {'nature': 'Subjective'}
        ]
    
    def _init_centers(self) -> Dict[str, Center]:
        """Initialize 9 centers"""
        centers_data = [
            ('Head', 'Space', 'inspiring presence through the pineal', 'Yellow'),
            ('Ajna', 'Evolution', 'mentally conceptualizing through the pituitary', 'Green'),
            ('Throat', 'Design', 'expressing through the thyroid', 'Brown'),
            ('G', 'Movement', 'identifying direction through the liver', 'Yellow'),
            ('Heart', 'Design', 'willing into being through the thymus', 'Red'),
            ('Spleen', 'Being', 'instinctively preserving through the spleen', 'Brown'),
            ('Sacral', 'Being', 'generating life force through gonads', 'Red'),
            ('Solar Plexus', 'Being', 'feeling through emotional waves via kidneys', 'Brown'),
            ('Root', 'Design', 'pressuring into manifestation via adrenals', 'Brown')
        ]
        
        return {
            name: Center(name, dim, voice, color)
            for name, dim, voice, color in centers_data
        }
    
    def _init_dimensions(self) -> Dict[str, Dimension]:
        """Initialize 5 dimensions"""
        dims_data = [
            ('Movement', 'I Create', 'Energy = Creation'),
            ('Evolution', 'I Remember', 'Gravity = Memory'),
            ('Being', 'I Am', 'Matter = Touch'),
            ('Design', 'I Design', 'Structure = Progress'),
            ('Space', 'I Think', 'Form = Illusion')
        ]
        
        return {
            name: Dimension(name, keynote, phrase)
            for name, keynote, phrase in dims_data
        }
    
    def _init_polarities(self) -> Dict[int, int]:
        """Initialize gate polarities (programming partners)"""
        return {
            1: 2, 2: 1, 3: 50, 4: 49, 5: 35, 6: 36, 7: 13, 8: 14,
            9: 16, 10: 15, 11: 12, 12: 11, 13: 7, 14: 8, 15: 10, 16: 9,
            17: 18, 18: 17, 19: 33, 20: 34, 21: 48, 22: 47, 23: 43, 24: 44,
            25: 46, 26: 45, 27: 28, 28: 27, 29: 30, 30: 29, 31: 41, 32: 42,
            33: 19, 34: 20, 35: 5, 36: 6, 37: 40, 38: 39, 39: 38, 40: 37,
            41: 31, 42: 32, 43: 23, 44: 24, 45: 26, 46: 25, 47: 22, 48: 21,
            49: 4, 50: 3, 51: 57, 52: 58, 53: 54, 54: 53, 55: 59, 56: 60,
            57: 51, 58: 52, 59: 55, 60: 56, 61: 62, 62: 61, 63: 64, 64: 63
        }
    
    def _init_grammar(self) -> Dict[str, str]:
        """Initialize consciousness grammar symbols"""
        return {
            'singularity': '•',
            'transitioner': '.',
            'collapse': '°',
            'portal': ':',
            'fork': ';',
            'breath': ',',
            'current': '–',
            'pulse': '′',
            'flicker': '″',
            'container': '"',
            'cocoon': '()',
            'indexGate': '[]',
            'domain': '{}',
            'blade': '/',
            'escape': '\\',
            'starburst': '*',
            'continuation': '…',
            'mirror': '=',
            'vector': '→'
        }
