"""
GameGAN - Behavioral Prediction Engine

Predicts behavioral outcomes based on consciousness state and interventions.
"If I do X, what's the probability of Y outcome?"

Uses consciousness coordinates to model decision-making patterns.
"""

from typing import Dict, List, Tuple
import math


class GameGAN:
    """
    Behavioral prediction engine
    
    Predicts outcomes based on:
    - Current consciousness state
    - Proposed intervention/action
    - Historical patterns
    - Dimensional dynamics
    """
    
    def __init__(self):
        self.outcome_db = self._load_outcome_patterns()
    
    def predict(self, consciousness_state, intervention: str, 
                situation: str = None) -> Dict:
        """
        Predict outcome of intervention given consciousness state
        
        Args:
            consciousness_state: ConsciousnessState object
            intervention: What action/decision to take
            situation: Optional context
            
        Returns:
            {
                'outcomes': [{outcome, probability, reasoning}, ...],
                'recommendation': 'best' or 'reconsider',
                'confidence': 0.0-1.0,
                'alternatives': [...]
            }
        """
        # Analyze intervention type
        intervention_type = self._classify_intervention(intervention)
        
        # Get possible outcomes
        outcomes = self._generate_outcomes(
            consciousness_state,
            intervention_type,
            situation
        )
        
        # Calculate probabilities
        for outcome in outcomes:
            outcome['probability'] = self._calculate_probability(
                consciousness_state,
                intervention_type,
                outcome['outcome_type']
            )
        
        # Sort by probability
        outcomes.sort(key=lambda x: x['probability'], reverse=True)
        
        # Generate recommendation
        best_outcome = outcomes[0]
        recommendation = 'proceed' if best_outcome['probability'] > 0.6 else 'reconsider'
        
        # Calculate confidence
        confidence = self._calculate_confidence(consciousness_state, outcomes)
        
        # Generate alternatives
        alternatives = self._generate_alternatives(
            consciousness_state,
            intervention_type,
            outcomes
        )
        
        return {
            'outcomes': outcomes,
            'recommendation': recommendation,
            'confidence': confidence,
            'alternatives': alternatives,
            'analysis': self._generate_analysis(consciousness_state, intervention, outcomes[0])
        }
    
    def _classify_intervention(self, intervention: str) -> str:
        """Classify type of intervention"""
        intervention_lower = intervention.lower()
        
        if any(word in intervention_lower for word in ['start', 'begin', 'create', 'build', 'make']):
            return 'initiation'
        elif any(word in intervention_lower for word in ['quit', 'stop', 'end', 'leave']):
            return 'termination'
        elif any(word in intervention_lower for word in ['change', 'shift', 'pivot', 'transform']):
            return 'transformation'
        elif any(word in intervention_lower for word in ['wait', 'pause', 'delay', 'postpone']):
            return 'patience'
        elif any(word in intervention_lower for word in ['push', 'accelerate', 'force', 'rush']):
            return 'acceleration'
        elif any(word in intervention_lower for word in ['collaborate', 'partner', 'team', 'join']):
            return 'collaboration'
        elif any(word in intervention_lower for word in ['learn', 'study', 'research', 'explore']):
            return 'exploration'
        else:
            return 'general_action'
    
    def _generate_outcomes(self, state, intervention_type: str, 
                          situation: str) -> List[Dict]:
        """Generate possible outcomes"""
        # Base outcomes template
        outcomes = []
        
        if intervention_type == 'initiation':
            outcomes = [
                {'outcome_type': 'successful_start', 'description': 'Project launches successfully and gains momentum'},
                {'outcome_type': 'scattered_start', 'description': 'Initial excitement fades, project stalls'},
                {'outcome_type': 'overwhelm', 'description': 'Too much too fast, energy depletes'}
            ]
        
        elif intervention_type == 'termination':
            outcomes = [
                {'outcome_type': 'clean_break', 'description': 'Clear ending, energy freed for new direction'},
                {'outcome_type': 'regret', 'description': 'Second thoughts, difficulty moving on'},
                {'outcome_type': 'relief', 'description': 'Immediate relief, clarity emerges'}
            ]
        
        elif intervention_type == 'transformation':
            outcomes = [
                {'outcome_type': 'successful_pivot', 'description': 'Smooth transition, new path opens'},
                {'outcome_type': 'resistance', 'description': 'Internal or external resistance slows change'},
                {'outcome_type': 'chaos', 'description': 'Temporary disruption before stabilization'}
            ]
        
        elif intervention_type == 'patience':
            outcomes = [
                {'outcome_type': 'clarity_emerges', 'description': 'Waiting reveals better timing/opportunity'},
                {'outcome_type': 'missed_window', 'description': 'Opportunity passes while waiting'},
                {'outcome_type': 'productive_patience', 'description': 'Preparation during wait improves outcome'}
            ]
        
        elif intervention_type == 'acceleration':
            outcomes = [
                {'outcome_type': 'breakthrough', 'description': 'Momentum carries through to completion'},
                {'outcome_type': 'burnout', 'description': 'Unsustainable pace leads to crash'},
                {'outcome_type': 'quality_compromise', 'description': 'Speed sacrifices thoroughness'}
            ]
        
        elif intervention_type == 'collaboration':
            outcomes = [
                {'outcome_type': 'synergy', 'description': 'Combined strengths amplify results'},
                {'outcome_type': 'conflict', 'description': 'Different approaches create friction'},
                {'outcome_type': 'dependency', 'description': 'Over-reliance on partner limits autonomy'}
            ]
        
        elif intervention_type == 'exploration':
            outcomes = [
                {'outcome_type': 'discovery', 'description': 'New insights/skills acquired'},
                {'outcome_type': 'distraction', 'description': 'Exploration becomes procrastination'},
                {'outcome_type': 'integration', 'description': 'Learning connects with existing knowledge'}
            ]
        
        else:
            outcomes = [
                {'outcome_type': 'success', 'description': 'Action achieves intended result'},
                {'outcome_type': 'partial_success', 'description': 'Some goals met, others not'},
                {'outcome_type': 'failure', 'description': "Action doesn't produce desired outcome"}
            ]
        
        return outcomes
    
    def _calculate_probability(self, state, intervention_type: str, 
                               outcome_type: str) -> float:
        """
        Calculate probability of outcome given state and intervention
        
        Uses consciousness dimensions to model behavior patterns
        """
        primary_dim = state.dimension_name
        coherence = state.coherence
        stability = state.stability
        
        # Base probability
        prob = 0.33  # Start at 33%
        
        # Dimension modifiers for different interventions
        if intervention_type == 'initiation':
            if primary_dim == 'Movement':
                if outcome_type == 'successful_start':
                    prob += 0.30  # Movement excels at starting
                elif outcome_type == 'scattered_start':
                    prob -= 0.10
            elif primary_dim == 'Being':
                if outcome_type == 'successful_start':
                    prob -= 0.10  # Being slower to start
                elif outcome_type == 'overwhelm':
                    prob -= 0.15  # Being resists overwhelm
            elif primary_dim == 'Design':
                if outcome_type == 'successful_start':
                    prob += 0.15  # Design plans well
        
        elif intervention_type == 'patience':
            if primary_dim == 'Being':
                if outcome_type == 'clarity_emerges':
                    prob += 0.35  # Being benefits from waiting
                elif outcome_type == 'missed_window':
                    prob -= 0.20
            elif primary_dim == 'Movement':
                if outcome_type == 'clarity_emerges':
                    prob -= 0.15  # Movement struggles with waiting
                elif outcome_type == 'missed_window':
                    prob += 0.20
        
        elif intervention_type == 'acceleration':
            if primary_dim == 'Movement':
                if outcome_type == 'breakthrough':
                    prob += 0.25
                elif outcome_type == 'burnout':
                    prob += 0.10  # Movement can overdo it
            elif primary_dim == 'Being':
                if outcome_type == 'burnout':
                    prob += 0.20  # Being resists acceleration
                elif outcome_type == 'breakthrough':
                    prob -= 0.15
        
        elif intervention_type == 'collaboration':
            if primary_dim == 'Design':
                if outcome_type == 'synergy':
                    prob += 0.25  # Design excels in structured collaboration
            elif primary_dim == 'Space':
                if outcome_type == 'conflict':
                    prob += 0.15  # Space needs autonomy
        
        # Coherence modifiers
        if coherence > 0.6:
            # High coherence = more predictable outcomes
            if outcome_type in ['successful_start', 'clean_break', 'successful_pivot', 
                               'clarity_emerges', 'breakthrough', 'synergy', 'discovery']:
                prob += 0.15
        elif coherence < 0.3:
            # Low coherence = more scattered outcomes
            if outcome_type in ['scattered_start', 'resistance', 'chaos', 
                               'burnout', 'distraction']:
                prob += 0.15
        
        # Stability modifiers
        if stability > 0.7:
            # High stability = consistent patterns
            prob += 0.05
        elif stability < 0.4:
            # Low stability = unpredictable
            prob -= 0.05
        
        # Clamp to 0-1
        prob = max(0.05, min(0.95, prob))
        
        return prob
    
    def _calculate_confidence(self, state, outcomes: List[Dict]) -> float:
        """Calculate confidence in predictions"""
        # Higher coherence + stability = higher confidence
        base_confidence = (state.coherence * 0.6) + (state.stability * 0.4)
        
        # If outcomes are very spread out, lower confidence
        probs = [o['probability'] for o in outcomes]
        if len(probs) > 1:
            max_prob = max(probs)
            min_prob = min(probs)
            spread = max_prob - min_prob
            
            if spread < 0.2:
                # Outcomes too similar = uncertain
                base_confidence *= 0.8
        
        return base_confidence
    
    def _generate_alternatives(self, state, intervention_type: str, 
                               outcomes: List[Dict]) -> List[Dict]:
        """Generate alternative actions to consider"""
        primary_dim = state.dimension_name
        coherence = state.coherence
        
        alternatives = []
        
        # Low coherence = suggest consolidation first
        if coherence < 0.3:
            alternatives.append({
                'action': 'First consolidate your energy',
                'reason': f'Your coherence is at {coherence:.0%}. Focus first, then act.',
                'priority': 'high'
            })
        
        # Dimension-specific alternatives
        if intervention_type == 'initiation':
            if primary_dim == 'Being':
                alternatives.append({
                    'action': 'Start with small daily practice',
                    'reason': 'Being dimension thrives with consistent rhythm',
                    'priority': 'medium'
                })
            elif primary_dim == 'Design':
                alternatives.append({
                    'action': 'Create detailed plan before starting',
                    'reason': 'Design dimension benefits from structure',
                    'priority': 'high'
                })
        
        elif intervention_type == 'acceleration':
            if primary_dim != 'Movement':
                alternatives.append({
                    'action': 'Maintain current pace with focus',
                    'reason': f'{primary_dim} dimension resists rushing',
                    'priority': 'high'
                })
        
        return alternatives
    
    def _generate_analysis(self, state, intervention: str, 
                          best_outcome: Dict) -> str:
        """Generate natural language analysis"""
        dimension = state.dimension_name
        coherence = state.coherence
        prob = best_outcome['probability']
        
        analysis = f"Based on your {dimension} dimension at {coherence:.0%} coherence, "
        
        if prob > 0.7:
            analysis += f"this intervention has a strong probability ({prob:.0%}) of success. "
        elif prob > 0.5:
            analysis += f"this intervention has moderate probability ({prob:.0%}) of working. "
        else:
            analysis += f"this intervention has lower probability ({prob:.0%}) of the desired outcome. "
        
        if coherence < 0.3:
            analysis += "Your current scattered state suggests focusing your energy first. "
        elif coherence > 0.7:
            analysis += "Your high coherence gives you clarity to execute well. "
        
        analysis += f"Most likely outcome: {best_outcome['description']}"
        
        return analysis
    
    def _load_outcome_patterns(self) -> Dict:
        """Load historical outcome patterns"""
        # In real version, this would load from database
        # For now, patterns are in the calculation logic
        return {}


# Quick helper function
def predict_outcome(consciousness_state, intervention: str, 
                   situation: str = None) -> Dict:
    """
    Quick function to predict outcome
    
    Example:
        from consciousness_core import ConsciousnessCore
        core = ConsciousnessCore()
        state = core.analyze("I'm feeling scattered")
        
        prediction = predict_outcome(
            state, 
            "Start a new business", 
            "Want to quit my job and launch startup"
        )
        
        print(prediction['recommendation'])
        for outcome in prediction['outcomes']:
            print(f"{outcome['probability']:.0%}: {outcome['description']}")
    """
    gan = GameGAN()
    return gan.predict(consciousness_state, intervention, situation)
