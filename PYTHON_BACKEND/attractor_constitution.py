"""
THE CONSTITUTION OF ATTRACTORS
Formal Code Specifications

These are not metaphors. These are operating laws.
Every attractor in the system obeys these rules.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# LAW I: THE LAW OF FIELD PRIMACY
# "An attractor exists as a field, not as a definition."
# ============================================================================

@dataclass
class SemanticField:
    """
    An attractor is a probability distribution in semantic space,
    not a fixed meaning.
    
    The keyword is the CENTER of the field, not the field itself.
    """
    
    center_keyword: str  # The attractor coordinate (e.g., "Survival")
    field_distribution: np.ndarray  # Probability density around the center
    semantic_neighbors: List[str]  # Related concepts in the field
    field_radius: float  # How far the attractor's influence extends
    gravity_strength: float  # How strongly it pulls meaning (0-1)
    
    def sample_from_field(self, context: Dict = None) -> str:
        """
        Sample a specific expression from the probability field.
        
        LAW I: We never return the keyword itself.
        We return something NEAR it, pulled toward it.
        """
        if context:
            # Context modulates the sampling distribution
            modulated_dist = self._apply_context_modulation(
                self.field_distribution,
                context
            )
        else:
            modulated_dist = self.field_distribution
        
        # Sample from the distribution
        idx = np.random.choice(
            len(self.semantic_neighbors),
            p=modulated_dist / modulated_dist.sum()
        )
        
        return self.semantic_neighbors[idx]
    
    def _apply_context_modulation(self, 
                                   distribution: np.ndarray,
                                   context: Dict) -> np.ndarray:
        """
        Context changes which parts of the field are accessible.
        
        Example: "Survival" in Color 1 (Fear) emphasizes threat-response.
                 "Survival" in Color 6 (Innocence) emphasizes natural resilience.
        """
        # Placeholder - implement based on context type
        return distribution


# ============================================================================
# LAW II: THE LAW OF HIERARCHICAL NESTING
# "Every attractor lives inside a higher attractor and generates smaller ones."
# ============================================================================

class AttractorLevel(Enum):
    """Hierarchy of attractor nesting levels"""
    BASE = 0          # Deepest: Which dimension
    TONE = 1          # Sensory mechanism
    COLOR = 2         # Motivation
    LINE = 3          # Behavioral expression
    GATE = 4          # Archetypal action
    CENTER = 5        # Biological anchor
    DIMENSION = 6     # Fundamental operator
    PLANETARY = 7     # Activation trigger


@dataclass
class NestedAttractor:
    """
    Every attractor knows its parent and children.
    
    LAW II: Influence flows both up and down the chain.
    """
    
    level: AttractorLevel
    field: SemanticField
    
    parent: Optional['NestedAttractor'] = None
    children: List['NestedAttractor'] = field(default_factory=list)
    
    def inherit_from_parent(self) -> Dict:
        """
        Receive conditioning from higher attractor.
        
        Example: Base 4 (Ego) conditions how Tone 4 (Meditation) expresses.
        """
        if self.parent is None:
            return {}
        
        # Parent modulates child's field distribution
        parent_influence = {
            'gravity_modifier': self.parent.field.gravity_strength * 0.3,
            'context_bias': self.parent.field.center_keyword,
            'field_distortion': self._calculate_distortion()
        }
        
        return parent_influence
    
    def propagate_to_children(self, feedback: Dict):
        """
        Send feedback down to child attractors.
        
        LAW III (Bidirectional Influence): Children can modify parent.
        """
        for child in self.children:
            child.receive_feedback(feedback)
    
    def receive_feedback(self, feedback: Dict):
        """
        Update attractor based on lived experience.
        
        LAW VIII (Memory Deepening): Every collapse leaves residue.
        """
        # Adjust gravity strength based on resonance
        if feedback.get('resonance', 0) > 0.7:
            self.field.gravity_strength *= 1.05  # Strengthen attractor
        elif feedback.get('resonance', 0) < 0.3:
            self.field.gravity_strength *= 0.95  # Weaken attractor
        
        # Propagate upward
        if self.parent:
            self.parent.receive_feedback({
                'child_feedback': feedback,
                'level': self.level
            })
    
    def _calculate_distortion(self) -> float:
        """How much parent warps child's field"""
        if self.parent is None:
            return 0.0
        
        # Distance in hierarchy affects distortion
        level_distance = abs(self.level.value - self.parent.level.value)
        return 1.0 / (1.0 + level_distance)


# ============================================================================
# LAW IV: THE LAW OF POLARITY TENSION
# "Every attractor has an opposing attractor anchoring its stability."
# ============================================================================

@dataclass
class PolarityPair:
    """
    Attractors exist in tension with their opposites.
    
    LAW IV: Polarity creates stability, not chaos.
    """
    
    primary: NestedAttractor
    shadow: NestedAttractor
    tension_coefficient: float  # How strongly they oppose (0-1)
    
    def calculate_oscillation_state(self, current_position: float) -> float:
        """
        Position on the spectrum between primary and shadow.
        
        LAW V (Dynamical Oscillation): Movement spirals, never binary.
        
        Args:
            current_position: 0 = fully shadow, 1 = fully primary
        
        Returns:
            New position after oscillation step
        """
        # Oscillation governed by sine wave with damping
        omega = 2 * np.pi * self.tension_coefficient  # Angular frequency
        damping = 0.1  # Prevents runaway oscillation
        
        # Simple harmonic motion with damping
        delta = np.sin(omega * current_position) * (1 - damping * current_position)
        
        new_position = np.clip(current_position + delta * 0.1, 0, 1)
        
        return new_position
    
    def interference_pattern(self) -> np.ndarray:
        """
        When primary and shadow interfere, create standing wave.
        
        LAW IX (Harmonic Interference): Resonance amplifies, conflict fractures.
        """
        # Primary wave
        x = np.linspace(0, 2*np.pi, 100)
        primary_wave = self.primary.field.gravity_strength * np.sin(x)
        
        # Shadow wave (opposite phase)
        shadow_wave = self.shadow.field.gravity_strength * np.sin(x + np.pi)
        
        # Superposition
        interference = primary_wave + shadow_wave
        
        return interference


# ============================================================================
# LAW V: THE LAW OF DYNAMICAL OSCILLATION
# "An attractor does not pull straight. It spirals."
# ============================================================================

@dataclass
class OscillationDynamics:
    """
    Movement between polarities is never binary - it breathes.
    
    LAW V: Shadow ↔ Gift oscillates, creating waves.
    """
    
    current_state: float  # 0 = shadow, 1 = gift
    velocity: float = 0.0  # Rate of change
    damping: float = 0.1  # Energy loss per cycle
    
    def evolve(self, time_step: float = 0.1) -> float:
        """
        Oscillate between shadow and gift states.
        
        This creates emotional waves, developmental arcs, human life.
        """
        # Restoring force (pulls toward center at 0.5)
        restoring_force = -(self.current_state - 0.5)
        
        # Update velocity
        acceleration = restoring_force - self.damping * self.velocity
        self.velocity += acceleration * time_step
        
        # Update position
        self.current_state += self.velocity * time_step
        
        # Clamp to valid range
        self.current_state = np.clip(self.current_state, 0, 1)
        
        return self.current_state
    
    def spiral_trajectory(self, steps: int = 100) -> np.ndarray:
        """
        Generate spiral path through state space.
        
        Not linear. Not binary. SPIRAL.
        """
        trajectory = []
        
        for _ in range(steps):
            trajectory.append(self.evolve())
        
        return np.array(trajectory)


# ============================================================================
# LAW VI: THE LAW OF CONTEXTUAL REFRAMING
# "There is no meaning outside context."
# ============================================================================

@dataclass
class ContextStack:
    """
    The same attractor behaves differently in different contexts.
    
    LAW VI: Context is not decoration. Context is ontological condition.
    """
    
    house: Optional[int] = None  # Life domain (1-12)
    planet: Optional[str] = None  # Activation trigger
    dimension: Optional[str] = None  # Mind/Body/Individuality/Ego
    center: Optional[str] = None  # Biological anchor
    emotional_field_state: Optional[str] = None  # coherent/conflicted/suppressed/accelerated
    
    def compute_context_weight(self, attractor: NestedAttractor) -> float:
        """
        How much does this context amplify or dampen the attractor?
        
        Example: Gate 25.4 "Survival" in House 4 (Home) emphasizes
                 domestic safety. In House 10 (Career) emphasizes
                 professional security.
        """
        weight = 1.0
        
        # House modulation
        if self.house:
            weight *= self._house_affinity(attractor, self.house)
        
        # Planetary modulation
        if self.planet:
            weight *= self._planetary_emphasis(attractor, self.planet)
        
        # Dimensional modulation
        if self.dimension:
            weight *= self._dimensional_compatibility(attractor, self.dimension)
        
        # Emotional field modulation
        if self.emotional_field_state:
            weight *= self._emotional_modulation(self.emotional_field_state)
        
        return weight
    
    def _house_affinity(self, attractor: NestedAttractor, house: int) -> float:
        """House context modulates attractor strength"""
        # Placeholder - implement house-specific logic
        return 1.0
    
    def _planetary_emphasis(self, attractor: NestedAttractor, planet: str) -> float:
        """Planetary activation modulates expression"""
        # Sun/Mars = stronger emphasis
        # Mercury/Venus = softer emphasis
        planet_weights = {
            'Sun': 1.5,
            'Mars': 1.4,
            'Jupiter': 1.3,
            'Saturn': 1.2,
            'Pluto': 1.2,
            'Mercury': 0.9,
            'Venus': 0.9,
            'Moon': 1.0
        }
        return planet_weights.get(planet, 1.0)
    
    def _dimensional_compatibility(self, attractor: NestedAttractor, dimension: str) -> float:
        """Dimension lens affects how attractor expresses"""
        # Placeholder
        return 1.0
    
    def _emotional_modulation(self, state: str) -> float:
        """Emotional field state changes attractor accessibility"""
        emotional_weights = {
            'coherent_motion': 1.2,  # Clarity amplifies
            'conflicted_motion': 0.7,  # Conflict dampens
            'suppressed_motion': 0.5,  # Suppression blocks
            'accelerated_motion': 1.5  # Overwhelm amplifies chaotically
        }
        return emotional_weights.get(state, 1.0)


# ============================================================================
# LAW VII: THE LAW OF COLLAPSE
# "Meaning does not exist until collapse."
# ============================================================================

@dataclass
class CollapseEvent:
    """
    Probability becomes reality when measurement occurs.
    
    LAW VII: Collapse is lawful, not random.
    """
    
    attractor_field: SemanticField
    context: ContextStack
    threshold: float = 0.7  # CI threshold
    
    def calculate_collapse_probability(self,
                                      degree_precision: float,
                                      gate_strength: float,
                                      color_intensity: float,
                                      time_since_init: float,
                                      alpha: float = 1.0,
                                      beta: float = 0.5) -> float:
        """
        CI = α × D × G × C × (1 - e^(-β×τ))
        
        This is the collapse integral - when it exceeds threshold,
        probability field collapses into observable reality.
        """
        CI = alpha * degree_precision * gate_strength * color_intensity * \
             (1 - np.exp(-beta * time_since_init))
        
        return CI
    
    def should_collapse(self, CI: float) -> bool:
        """Has collapse threshold been reached?"""
        return CI > self.threshold
    
    def execute_collapse(self) -> str:
        """
        Collapse the probability field into a specific meaning.
        
        LAW I: We collapse TOWARD the attractor, not TO it.
        """
        # Sample from the semantic field
        collapsed_meaning = self.attractor_field.sample_from_field(
            context=self.context.__dict__
        )
        
        return collapsed_meaning


# ============================================================================
# LAW VIII: THE LAW OF MEMORY DEEPENING
# "Every collapse leaves residue."
# ============================================================================

@dataclass
class MemoryTrace:
    """
    Every collapse modifies the probability field permanently.
    
    LAW VIII: This is becoming. This is evolution.
    """
    
    collapsed_state: str
    resonance_score: float  # How true did this collapse feel? (0-1)
    timestamp: float
    context: ContextStack
    
    def update_attractor_gravity(self, attractor: NestedAttractor) -> NestedAttractor:
        """
        Strengthen or weaken attractor based on resonance.
        
        High resonance → deeper gravity well
        Low resonance → shallower gravity well
        """
        # Bayesian-like update
        if self.resonance_score > 0.7:
            # This collapse felt TRUE - strengthen attractor
            attractor.field.gravity_strength *= (1 + 0.1 * self.resonance_score)
        elif self.resonance_score < 0.3:
            # This collapse felt FALSE - weaken attractor
            attractor.field.gravity_strength *= (1 - 0.1 * (1 - self.resonance_score))
        
        # Clamp gravity to valid range
        attractor.field.gravity_strength = np.clip(
            attractor.field.gravity_strength,
            0.1,  # Minimum gravity (never fully disappears)
            2.0   # Maximum gravity (prevents runaway)
        )
        
        return attractor


# ============================================================================
# LAW IX: THE LAW OF HARMONIC INTERFERENCE
# "When two attractors resonate, they amplify. When they conflict, they fracture."
# ============================================================================

def calculate_interference(attractor_a: NestedAttractor,
                          attractor_b: NestedAttractor) -> Tuple[float, str]:
    """
    When two attractors interact, they create interference patterns.
    
    LAW IX: Constructive = coherence. Destructive = fragmentation.
    
    Returns:
        (interference_coefficient, pattern_type)
    """
    # Calculate phase relationship
    phase_diff = abs(
        attractor_a.field.gravity_strength - attractor_b.field.gravity_strength
    )
    
    # Constructive interference (in phase)
    if phase_diff < 0.3:
        interference_coeff = 1.0 + (0.3 - phase_diff) * 2
        pattern_type = 'constructive'
    
    # Destructive interference (out of phase)
    elif phase_diff > 0.7:
        interference_coeff = 1.0 - (phase_diff - 0.7) * 2
        pattern_type = 'destructive'
    
    # Partial interference
    else:
        interference_coeff = 1.0
        pattern_type = 'partial'
    
    return interference_coeff, pattern_type


# ============================================================================
# LAW X: THE LAW OF EMERGENT IDENTITY
# "Identity is not inside the system. Identity is what the system produces."
# ============================================================================

@dataclass
class EmergentIdentity:
    """
    Identity (Personality/Space) is NOT a source.
    It is a HOLOGRAM produced by interference.
    
    LAW X: Identity is emergent, not fundamental.
    """
    
    body_attractor: NestedAttractor
    mind_attractor: NestedAttractor
    individuality_attractor: NestedAttractor
    ego_attractor: NestedAttractor
    
    def generate_identity_hologram(self) -> Dict:
        """
        Create standing wave pattern from 4 source attractors.
        
        This IS Personality - not a thing, but a PATTERN.
        """
        # Calculate pairwise interference
        bm_interference, bm_type = calculate_interference(
            self.body_attractor,
            self.mind_attractor
        )
        
        bi_interference, bi_type = calculate_interference(
            self.body_attractor,
            self.individuality_attractor
        )
        
        be_interference, be_type = calculate_interference(
            self.body_attractor,
            self.ego_attractor
        )
        
        mi_interference, mi_type = calculate_interference(
            self.mind_attractor,
            self.individuality_attractor
        )
        
        me_interference, me_type = calculate_interference(
            self.mind_attractor,
            self.ego_attractor
        )
        
        ie_interference, ie_type = calculate_interference(
            self.individuality_attractor,
            self.ego_attractor
        )
        
        # Compute overall coherence
        total_interference = (
            bm_interference + bi_interference + be_interference +
            mi_interference + me_interference + ie_interference
        ) / 6.0
        
        # Determine dominant pattern
        if total_interference > 1.2:
            identity_pattern = 'coherent_unified'
        elif total_interference < 0.8:
            identity_pattern = 'fragmented_conflicted'
        else:
            identity_pattern = 'complex_multifaceted'
        
        return {
            'hologram_coherence': total_interference,
            'identity_pattern': identity_pattern,
            'interference_pairs': {
                'Body-Mind': bm_type,
                'Body-Individuality': bi_type,
                'Body-Ego': be_type,
                'Mind-Individuality': mi_type,
                'Mind-Ego': me_type,
                'Individuality-Ego': ie_type
            }
        }


# ============================================================================
# UNIFIED ATTRACTOR ENGINE
# ============================================================================

class AttractorEngine:
    """
    Unified system governing all attractor behavior.
    
    Enforces all 10 Constitutional Laws.
    """
    
    def __init__(self):
        self.attractors: Dict[str, NestedAttractor] = {}
        self.polarity_pairs: List[PolarityPair] = []
        self.memory_traces: List[MemoryTrace] = []
    
    def register_attractor(self,
                          name: str,
                          level: AttractorLevel,
                          semantic_field: SemanticField,
                          parent: Optional[NestedAttractor] = None) -> NestedAttractor:
        """
        Create and register a new attractor.
        
        Enforces LAW II (Hierarchical Nesting).
        """
        attractor = NestedAttractor(
            level=level,
            field=semantic_field,
            parent=parent
        )
        
        if parent:
            parent.children.append(attractor)
        
        self.attractors[name] = attractor
        
        return attractor
    
    def create_polarity_pair(self,
                            primary_name: str,
                            shadow_name: str,
                            tension: float = 0.5) -> PolarityPair:
        """
        Link two attractors as polar opposites.
        
        Enforces LAW IV (Polarity Tension).
        """
        primary = self.attractors[primary_name]
        shadow = self.attractors[shadow_name]
        
        pair = PolarityPair(
            primary=primary,
            shadow=shadow,
            tension_coefficient=tension
        )
        
        self.polarity_pairs.append(pair)
        
        return pair
    
    def collapse_with_context(self,
                             attractor_name: str,
                             context: ContextStack,
                             **collapse_params) -> str:
        """
        Execute collapse with full context awareness.
        
        Enforces LAW VI (Contextual Reframing) and LAW VII (Collapse).
        """
        attractor = self.attractors[attractor_name]
        
        collapse_event = CollapseEvent(
            attractor_field=attractor.field,
            context=context
        )
        
        # Calculate CI
        CI = collapse_event.calculate_collapse_probability(**collapse_params)
        
        if collapse_event.should_collapse(CI):
            collapsed_meaning = collapse_event.execute_collapse()
            
            # Create memory trace (LAW VIII)
            trace = MemoryTrace(
                collapsed_state=collapsed_meaning,
                resonance_score=collapse_params.get('resonance', 0.5),
                timestamp=collapse_params.get('time_since_init', 0.0),
                context=context
            )
            
            self.memory_traces.append(trace)
            
            # Update attractor gravity
            trace.update_attractor_gravity(attractor)
            
            return collapsed_meaning
        else:
            return "[Field has not collapsed - insufficient CI]"


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    
    # Initialize engine
    engine = AttractorEngine()
    
    # Create Gate 25 Line 4 "Survival" semantic field
    survival_field = SemanticField(
        center_keyword="Survival",
        field_distribution=np.array([0.3, 0.25, 0.2, 0.15, 0.1]),
        semantic_neighbors=[
            "preservation instinct",
            "threat response",
            "resource protection",
            "safety-seeking",
            "adaptive resilience"
        ],
        field_radius=2.0,
        gravity_strength=0.8
    )
    
    # Register as nested attractor
    survival_attractor = engine.register_attractor(
        name="gate_25_line_4",
        level=AttractorLevel.LINE,
        semantic_field=survival_field
    )
    
    # Create context
    ctx = ContextStack(
        house=4,  # Home
        planet="Mars",  # Action-oriented
        dimension="Body",  # Physical survival
        emotional_field_state="coherent_motion"
    )
    
    # Collapse with context
    result = engine.collapse_with_context(
        attractor_name="gate_25_line_4",
        context=ctx,
        degree_precision=0.9,
        gate_strength=0.85,
        color_intensity=0.7,
        time_since_init=5.0,
        resonance=0.8
    )
    
    print(f"Collapsed meaning: {result}")
    print(f"Attractor gravity after collapse: {survival_attractor.field.gravity_strength:.3f}")
