"""
GameGAN Core Prediction Module
Behavioral prediction engine for consciousness-aware applications
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class TrinityChart:
    """Three-chart consciousness architecture"""
    body: Dict[str, Any]
    mind: Dict[str, Any]
    heart: Dict[str, Any]


@dataclass
class Intervention:
    """Proposed guidance or content to deliver"""
    content: str
    tone: str
    style: str
    allows_response: bool
    requires_immediate: bool
    complexity: str


@dataclass
class Context:
    """Current state and interaction history"""
    emotional_wave: str = "neutral"
    positive_interactions: int = 0
    negative_interactions: int = 0
    successful_predictions: int = 0
    session_count: int = 0
    initial_trust: float = 0.5
    recent_rejection: bool = False


@dataclass
class Prediction:
    """Complete behavioral prediction output"""
    acceptance_probability: float
    resistance_level: float
    optimal_tone: str
    optimal_sense: str
    secondary_sense: str
    predicted_outcome: str
    confidence: float
    warnings: List[str]
    suggestions: List[str]
    details: Dict[str, Any]


def predict_response(
    trinity_chart: TrinityChart,
    intervention: Intervention,
    context: Context = None
) -> Prediction:
    """
    Main prediction function that forecasts behavioral response
    
    Args:
        trinity_chart: User's consciousness architecture
        intervention: Proposed guidance to deliver
        context: Current state and history
        
    Returns:
        Prediction object with probabilities and recommendations
    """
    if context is None:
        context = Context()
    
    body = trinity_chart.body
    mind = trinity_chart.mind
    heart = trinity_chart.heart
    
    # Calculate individual prediction factors
    openness = calculate_openness(body, mind, heart, context)
    sensory_pref = calculate_sensory_preference(body, mind, heart)
    resistance = detect_resistance_triggers(body, mind, heart, intervention)
    emotional_state = assess_emotional_state(body, context)
    authority_align = check_authority_alignment(body, intervention)
    processing = determine_processing_mode(body, mind, heart)
    trust = calculate_trust_level(context)
    
    # Synthesize prediction
    prediction = synthesize_prediction(
        openness=openness,
        sensory_preference=sensory_pref,
        resistance_triggers=resistance,
        emotional_state=emotional_state,
        authority_alignment=authority_align,
        processing_mode=processing,
        trust_level=trust,
        intervention=intervention
    )
    
    return prediction


def calculate_openness(
    body: Dict,
    mind: Dict,
    heart: Dict,
    context: Context
) -> float:
    """Calculate how open user is to receiving guidance right now"""
    openness_score = 0.5  # baseline
    
    # Count undefined centers (more open to conditioning)
    centers = ['head', 'ajna', 'throat', 'g', 'heart', 'sacral', 'spleen', 'solar', 'root']
    undefined_count = sum(1 for c in centers if not body.get(c, {}).get('defined', False))
    openness_score += (undefined_count / 9) * 0.3
    
    # Type influences receptivity
    type_openness = {
        'Manifestor': 0.3,
        'Generator': 0.6,
        'Manifesting Generator': 0.6,
        'Projector': 0.8,
        'Reflector': 0.9
    }
    user_type = body.get('type', 'Generator')
    openness_score = (openness_score + type_openness.get(user_type, 0.5)) / 2
    
    # Emotional wave affects openness
    if context.emotional_wave == 'high':
        openness_score *= 1.2
    elif context.emotional_wave == 'low':
        openness_score *= 0.8
    
    # Recent negative experiences reduce openness
    if context.recent_rejection:
        openness_score *= 0.7
    
    return min(max(openness_score, 0), 1)


def calculate_sensory_preference(
    body: Dict,
    mind: Dict,
    heart: Dict
) -> Dict[str, Any]:
    """Determine which sensory mode is most effective"""
    scores = {
        'visual': 0.5,
        'auditory': 0.5,
        'kinesthetic': 0.5,
        'conceptual': 0.5
    }
    
    # Ajna influences visual/conceptual
    if body.get('ajna', {}).get('defined', False):
        scores['visual'] += 0.3
        scores['conceptual'] += 0.3
    else:
        scores['visual'] += 0.2  # undefined needs external anchors
    
    # Throat influences auditory
    if body.get('throat', {}).get('defined', False):
        scores['auditory'] += 0.2
    
    # Spleen influences kinesthetic
    if body.get('spleen', {}).get('defined', False):
        scores['kinesthetic'] += 0.3
    
    # Solar Plexus influences kinesthetic
    if body.get('solar', {}).get('defined', False):
        scores['kinesthetic'] += 0.2
    
    # Profile lines influence preference
    profile = body.get('profile', '')
    if '1' in profile:
        scores['conceptual'] += 0.2
    if '2' in profile:
        scores['kinesthetic'] += 0.2
    if '3' in profile:
        scores['kinesthetic'] += 0.3
    if '4' in profile:
        scores['auditory'] += 0.2
    if '5' in profile:
        scores['visual'] += 0.2
    if '6' in profile:
        scores['visual'] += 0.3
    
    # Normalize and return
    max_score = max(scores.values())
    preferences = sorted(
        [(sense, score / max_score) for sense, score in scores.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    return {
        'primary': preferences[0][0],
        'secondary': preferences[1][0],
        'scores': dict(preferences)
    }


def detect_resistance_triggers(
    body: Dict,
    mind: Dict,
    heart: Dict,
    intervention: Intervention
) -> Dict[str, Any]:
    """Detect what in the intervention might trigger resistance"""
    triggers = []
    warnings = []
    resistance_level = 0.0
    
    user_type = body.get('type', 'Generator')
    authority = body.get('authority', 'emotional')
    definition = body.get('definition', 'single')
    
    # Check tone vs type
    if user_type == 'Manifestor' and intervention.tone == 'directive':
        triggers.append('directive_to_manifestor')
        warnings.append('Manifestors resist being told what to do')
        resistance_level += 0.3
    
    if user_type == 'Projector' and intervention.tone == 'pushy':
        triggers.append('pushy_to_projector')
        warnings.append('Projectors need invitation, not pressure')
        resistance_level += 0.4
    
    if user_type == 'Generator' and not intervention.allows_response:
        triggers.append('no_response_for_generator')
        warnings.append('Generators need to respond, not initiate')
        resistance_level += 0.2
    
    # Check if intervention respects authority
    if authority == 'emotional' and intervention.requires_immediate:
        triggers.append('rushing_emotional_authority')
        warnings.append('Emotional authority needs time to process')
        resistance_level += 0.5
    
    if authority == 'splenic' and intervention.complexity == 'high':
        triggers.append('overthinking_splenic')
        warnings.append('Splenic authority is spontaneous, not analytical')
        resistance_level += 0.3
    
    # Check definition vs complexity
    if 'split' in definition and intervention.complexity == 'high':
        triggers.append('complex_for_split')
        warnings.append('Split definition needs time to bridge ideas')
        resistance_level += 0.2
    
    # Check undefined centers sensitivity
    if not body.get('g', {}).get('defined', False) and 'identity' in intervention.content.lower():
        triggers.append('identity_talk_undefined_g')
        warnings.append('Undefined G center is sensitive about identity questions')
        resistance_level += 0.3
    
    if not body.get('heart', {}).get('defined', False) and 'worth' in intervention.content.lower():
        triggers.append('worth_talk_undefined_heart')
        warnings.append('Undefined Heart is sensitive about worthiness')
        resistance_level += 0.4
    
    return {
        'triggers': triggers,
        'warnings': warnings,
        'resistance_level': min(resistance_level, 1.0)
    }


def assess_emotional_state(body: Dict, context: Context) -> Dict[str, Any]:
    """Assess current emotional state and readiness"""
    has_emotional_authority = body.get('solar', {}).get('defined', False)
    
    if not has_emotional_authority:
        return {
            'state': 'stable',
            'readiness': 0.8,
            'recommendation': 'proceed_normally'
        }
    
    wave = context.emotional_wave
    
    state_map = {
        'high': {
            'state': 'excited',
            'readiness': 0.6,
            'recommendation': 'gentle_reminder_to_wait'
        },
        'low': {
            'state': 'pessimistic',
            'readiness': 0.4,
            'recommendation': 'supportive_postpone'
        },
        'neutral': {
            'state': 'balanced',
            'readiness': 0.9,
            'recommendation': 'optimal_timing'
        }
    }
    
    return state_map.get(wave, state_map['neutral'])


def check_authority_alignment(body: Dict, intervention: Intervention) -> Dict[str, Any]:
    """Check if intervention aligns with decision-making authority"""
    authority = body.get('authority', 'emotional')
    intervention_style = intervention.style
    
    alignment_scores = {
        'emotional': {
            'patient': 1.0,
            'informative': 0.8,
            'directive': 0.3,
            'urgent': 0.2
        },
        'sacral': {
            'responsive': 1.0,
            'yes_no': 0.9,
            'informative': 0.7,
            'analytical': 0.4
        },
        'splenic': {
            'spontaneous': 1.0,
            'intuitive': 0.9,
            'informative': 0.6,
            'analytical': 0.3
        },
        'ego': {
            'empowering': 1.0,
            'directive': 0.8,
            'informative': 0.7,
            'submissive': 0.2
        },
        'self': {
            'directional': 1.0,
            'identity_based': 0.9,
            'informative': 0.7,
            'external': 0.3
        },
        'mental': {
            'conversational': 1.0,
            'informative': 0.9,
            'analytical': 0.7,
            'directive': 0.4
        },
        'lunar': {
            'patient': 1.0,
            'cyclical': 0.9,
            'informative': 0.7,
            'urgent': 0.1
        }
    }
    
    score = alignment_scores.get(authority, {}).get(intervention_style, 0.5)
    
    return {
        'authority': authority,
        'intervention_style': intervention_style,
        'alignment_score': score,
        'is_aligned': score > 0.6
    }


def determine_processing_mode(body: Dict, mind: Dict, heart: Dict) -> Dict[str, str]:
    """Determine how the user processes information"""
    mode = {
        'speed': 'medium',
        'depth': 'medium',
        'preference': 'balanced'
    }
    
    # Defined Ajna = fast mental processing
    if body.get('ajna', {}).get('defined', False):
        mode['speed'] = 'fast'
        mode['depth'] = 'analytical'
    
    # Defined Head = constant mental pressure
    if body.get('head', {}).get('defined', False):
        mode['depth'] = 'deep'
    
    # Split definition = needs bridging time
    if 'split' in body.get('definition', ''):
        mode['speed'] = 'slow'
        mode['preference'] = 'stepped'
    
    # Profile influences processing
    profile = body.get('profile', '')
    if '1' in profile:
        mode['preference'] = 'foundational'
    elif '3' in profile:
        mode['preference'] = 'experiential'
    elif '6' in profile:
        mode['preference'] = 'observational'
    
    return mode


def calculate_trust_level(context: Context) -> float:
    """Calculate current trust level based on history"""
    trust = context.initial_trust
    
    # Positive interactions increase trust
    trust += context.positive_interactions * 0.1
    
    # Negative interactions decrease trust
    trust -= context.negative_interactions * 0.15
    
    # Successful predictions increase trust
    trust += context.successful_predictions * 0.05
    
    # Time spent increases trust
    trust += min(context.session_count * 0.02, 0.2)
    
    return min(max(trust, 0), 1)


def synthesize_prediction(**factors) -> Prediction:
    """Combine all factors into final prediction"""
    openness = factors['openness']
    sensory_pref = factors['sensory_preference']
    resistance = factors['resistance_triggers']
    emotional_state = factors['emotional_state']
    authority_align = factors['authority_alignment']
    processing = factors['processing_mode']
    trust = factors['trust_level']
    
    # Calculate acceptance probability
    acceptance = 0.5
    acceptance += openness * 0.3
    acceptance += emotional_state['readiness'] * 0.2
    acceptance += authority_align['alignment_score'] * 0.2
    acceptance += trust * 0.2
    acceptance -= resistance['resistance_level'] * 0.3
    acceptance = min(max(acceptance, 0), 1)
    
    # Determine predicted outcome
    if acceptance > 0.75:
        outcome = 'integration'
    elif acceptance > 0.5:
        outcome = 'partial'
    elif acceptance > 0.3:
        outcome = 'delayed'
    else:
        outcome = 'rejection'
    
    # Determine optimal tone
    optimal_tone = 'gentle'
    if trust > 0.7 and openness > 0.7:
        optimal_tone = 'direct'
    if emotional_state['state'] == 'pessimistic':
        optimal_tone = 'supportive'
    if resistance['resistance_level'] > 0.5:
        optimal_tone = 'very_gentle'
    
    # Generate suggestions
    suggestions = []
    if sensory_pref['primary'] == 'visual':
        suggestions.append('Include visual diagram or image')
    if processing['preference'] == 'foundational':
        suggestions.append('Start with basic principles before details')
    if emotional_state['recommendation'] == 'supportive_postpone':
        suggestions.append('Acknowledge emotional state, suggest revisiting later')
    if not authority_align['is_aligned']:
        suggestions.append(f"Adjust style to respect {authority_align['authority']} authority")
    
    # Calculate confidence
    confidence = 0.7
    if trust > 0.6:
        confidence += 0.1
    if len(resistance['triggers']) == 0:
        confidence += 0.1
    confidence = min(confidence, 0.95)
    
    return Prediction(
        acceptance_probability=round(acceptance, 2),
        resistance_level=round(resistance['resistance_level'], 2),
        optimal_tone=optimal_tone,
        optimal_sense=sensory_pref['primary'],
        secondary_sense=sensory_pref['secondary'],
        predicted_outcome=outcome,
        confidence=round(confidence, 2),
        warnings=resistance['warnings'],
        suggestions=suggestions,
        details={
            'openness': round(openness, 2),
            'emotional_state': emotional_state['state'],
            'authority_alignment': authority_align['is_aligned'],
            'processing_mode': processing['preference'],
            'trust_level': round(trust, 2)
        }
    )
