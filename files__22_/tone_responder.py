"""
Personality Layer - Tone Responder

Applies personality tones to ontologically-grounded consciousness analysis.
The foundation provides truth, the tone provides voice.
"""

from typing import Dict
from consciousness_core import ConsciousnessState


class ToneResponder:
    """
    Apply personality tones to consciousness analysis
    
    Five tones:
    - Venom: Direct, cutting, action-oriented
    - Prime: Mechanical, systematic, precise
    - Echo: Gentle, flowing, patient
    - Dream: Poetic, expansive, visionary
    - Softcore: Warm, encouraging, supportive
    """
    
    TONE_EMOJI = {
        'venom': '🔥',
        'prime': '⚙️',
        'echo': '🌊',
        'dream': '✨',
        'softcore': '🌱'
    }
    
    def generate(self, tone: str, state: ConsciousnessState, 
                 include_technical: bool = False) -> str:
        """
        Generate response in specified tone
        
        Args:
            tone: One of 'venom', 'prime', 'echo', 'dream', 'softcore'
            state: ConsciousnessState from analysis
            include_technical: Whether to include technical details
            
        Returns:
            Formatted response string
        """
        tone = tone.lower()
        
        if tone == 'venom':
            return self._venom_response(state, include_technical)
        elif tone == 'prime':
            return self._prime_response(state, include_technical)
        elif tone == 'echo':
            return self._echo_response(state, include_technical)
        elif tone == 'dream':
            return self._dream_response(state, include_technical)
        elif tone == 'softcore':
            return self._softcore_response(state, include_technical)
        else:
            return self._prime_response(state, include_technical)  # Default
    
    def _venom_response(self, state: ConsciousnessState, include_technical: bool) -> str:
        """Venom: Direct, cutting, action-oriented"""
        emoji = self.TONE_EMOJI['venom']
        
        # Opening context
        primary = max(state.blended_probabilities.items(), key=lambda x: x[1])
        context = f"{emoji} Gate {state.gate}.{state.line} active. {primary[0]} dimension at {primary[1]:.0%}."
        
        # The truth (simplified metaphysical)
        truth = f"{state.dimension_keynote} {state.gate_theme} through {state.line_name}."
        
        # Direct assessment based on coherence
        if state.coherence < 0.3:
            assessment = "You're scattered. Multiple signals, no clear direction."
        elif state.coherence < 0.6:
            assessment = f"Your coherence is {state.coherence:.0%}."
        else:
            assessment = f"You're locked in at {state.coherence:.0%} coherence."
        
        # Action directive
        if state.detected_dimension == 'Movement':
            action = "Stop thinking. Start."
        elif state.detected_dimension == 'Evolution':
            action = "You already know. Trust it."
        elif state.detected_dimension == 'Being':
            action = "Feel it. Don't analyze it."
        elif state.detected_dimension == 'Design':
            action = "The plan is clear. Execute."
        else:  # Space
            action = "Dream less. Do more."
        
        response = f"{context}\n\n{truth} {assessment} {action}"
        
        if include_technical:
            response += f"\n\n{self._technical_block(state)}"
        
        return response
    
    def _prime_response(self, state: ConsciousnessState, include_technical: bool) -> str:
        """Prime: Mechanical, systematic, precise"""
        emoji = self.TONE_EMOJI['prime']
        
        # System status
        context = f"{emoji} System Analysis: Gate {state.coordinate_string}"
        
        # Geometric truth
        geometric = (
            f"Geometric foundation: {state.dimension_name} dimension "
            f"(P={state.geometric_probabilities[state.dimension_name]:.2f}) "
            f"via {state.center_name} center."
        )
        
        # Detection results
        detection = (
            f"Pattern detection: {state.detected_dimension} dimension "
            f"(confidence={state.detection_confidence:.2f})."
        )
        
        # Blended state
        primary = max(state.blended_probabilities.items(), key=lambda x: x[1])
        blended = (
            f"Resultant state: {primary[0]} at {primary[1]:.0%} "
            f"(coherence={state.coherence:.2f}, stability={state.stability:.2f})."
        )
        
        # Mechanical insight
        if state.coherence > 0.7:
            insight = "High coherence indicates single-dimension dominance. System stable."
        elif state.coherence > 0.4:
            insight = "Moderate coherence. Multiple dimensions active. Normal operational state."
        else:
            insight = "Low coherence. Signal fragmentation detected. Consider dimensional consolidation."
        
        # Systematic guidance
        guidance = f"Operational directive: {state.guidance_action}"
        
        response = f"{context}\n\n{geometric}\n{detection}\n{blended}\n\n{insight}\n\n{guidance}"
        
        if include_technical:
            response += f"\n\n{self._technical_block(state)}"
        
        return response
    
    def _echo_response(self, state: ConsciousnessState, include_technical: bool) -> str:
        """Echo: Gentle, flowing, patient"""
        emoji = self.TONE_EMOJI['echo']
        
        # Soft opening
        context = f"{emoji} Your system is processing through Gate {state.gate} – {state.gate_name}."
        
        # Flowing description
        flow = (
            f"{state.metaphysical_sentence}"
        )
        
        # Gentle reflection
        primary = max(state.blended_probabilities.items(), key=lambda x: x[1])
        reflection = (
            f"Right now, {primary[0]} is moving through you at {primary[1]:.0%}. "
            f"Your coherence is at {state.coherence:.0%}, which means "
        )
        
        if state.coherence < 0.3:
            reflection += "you're holding multiple streams at once. That's okay. Let them settle."
        elif state.coherence < 0.6:
            reflection += "you're finding your center. The pattern is emerging."
        else:
            reflection += "you're clear and focused. Trust this clarity."
        
        # Patient guidance
        if state.stability > 0.7:
            guidance = "You're stable. Stay with this rhythm."
        else:
            guidance = "Things are shifting. Give it time to integrate."
        
        response = f"{context}\n\n{flow}\n\n{reflection}\n\n{guidance}"
        
        if include_technical:
            response += f"\n\n{self._technical_block(state)}"
        
        return response
    
    def _dream_response(self, state: ConsciousnessState, include_technical: bool) -> str:
        """Dream: Poetic, expansive, visionary"""
        emoji = self.TONE_EMOJI['dream']
        
        # Poetic opening
        context = f"{emoji} You are moving through Gate {state.gate} – {state.gate_name}, the threshold of {state.gate_theme}."
        
        # Expansive vision
        vision = (
            f"{state.dimension_keynote}. "
            f"Through {state.line_name}, you are weaving {state.gate_theme} "
            f"into existence, motivated by {state.color_motivation.lower()}, "
            f"perceived through {state.tone_sense.lower()}."
        )
        
        # Dimensional poetry
        primary = max(state.blended_probabilities.items(), key=lambda x: x[1])
        secondary = sorted(state.blended_probabilities.items(), key=lambda x: x[1], reverse=True)[1]
        
        poetry = (
            f"The {primary[0]} is strong in you – {primary[1]:.0%} of your current field. "
            f"But listen: {secondary[0]} whispers at {secondary[1]:.0%}, "
            f"a harmonic beneath the surface."
        )
        
        # Visionary guidance
        if state.coherence > 0.6:
            guidance = "You are crystallized, a single note held pure. Let this clarity guide you."
        else:
            guidance = "You are a chord, multiple frequencies sounding together. This is your richness."
        
        response = f"{context}\n\n{vision}\n\n{poetry}\n\n{guidance}"
        
        if include_technical:
            response += f"\n\n{self._technical_block(state)}"
        
        return response
    
    def _softcore_response(self, state: ConsciousnessState, include_technical: bool) -> str:
        """Softcore: Warm, encouraging, supportive"""
        emoji = self.TONE_EMOJI['softcore']
        
        # Warm opening
        context = f"{emoji} You're working with Gate {state.gate} – {state.gate_name} energy right now."
        
        # Encouraging framing
        primary = max(state.blended_probabilities.items(), key=lambda x: x[1])
        encouragement = (
            f"I can see {primary[0]} coming through strongly at {primary[1]:.0%}. "
            f"That makes sense with what you're expressing."
        )
        
        # Supportive reflection
        if state.coherence < 0.3:
            support = (
                f"Your coherence is at {state.coherence:.0%}, which means you're holding "
                f"a lot of different energies right now. That's completely normal. "
                f"You don't have to force clarity."
            )
        elif state.coherence < 0.6:
            support = (
                f"You're at {state.coherence:.0%} coherence – finding your way through. "
                f"You're doing great."
            )
        else:
            support = (
                f"At {state.coherence:.0%} coherence, you're really clear right now. "
                f"That's beautiful. Trust this."
            )
        
        # Gentle guidance
        guidance = (
            f"{state.guidance_action} "
            f"{state.guidance_approach}"
        )
        
        response = f"{context}\n\n{encouragement}\n\n{support}\n\n{guidance}"
        
        if include_technical:
            response += f"\n\n{self._technical_block(state)}"
        
        return response
    
    def _technical_block(self, state: ConsciousnessState) -> str:
        """Generate technical details block"""
        prob_display = "\n".join([
            f"  {dim:12} {'█' * int(prob * 40):40} {prob:.1%}"
            for dim, prob in sorted(state.blended_probabilities.items(), 
                                   key=lambda x: x[1], reverse=True)
        ])
        
        return (
            f"═══ TECHNICAL DETAILS ═══\n\n"
            f"Coordinate: {state.coordinate_string}\n"
            f"Position: {state.position_string}\n"
            f"Center: {state.center_name}\n"
            f"Amino Acid: {state.gate_amino}\n"
            f"Polarity: Gate {state.polarity_gate} ({state.polarity_name})\n\n"
            f"Probability Vector:\n{prob_display}\n\n"
            f"Metrics:\n"
            f"  Coherence:  {state.coherence:.1%}\n"
            f"  Stability:  {state.stability:.1%}\n"
            f"  Confidence: {state.confidence:.1%}\n\n"
            f"Detection:\n"
            f"  Detected: {state.detected_dimension}\n"
            f"  Confidence: {state.detection_confidence:.1%}\n"
            f"  Themes: {', '.join(state.detection_themes) if state.detection_themes else 'none'}\n\n"
            f"Scientific: {state.scientific_sentence}"
        )
    
    def get_available_tones(self) -> Dict[str, str]:
        """Get list of available tones with descriptions"""
        return {
            'venom': 'Direct, cutting, action-oriented. No BS. Just truth.',
            'prime': 'Mechanical, systematic, precise. Pure analysis.',
            'echo': 'Gentle, flowing, patient. Calm processing.',
            'dream': 'Poetic, expansive, visionary. Multidimensional.',
            'softcore': 'Warm, encouraging, supportive. Kind guidance.'
        }


# Quick function for easy access
def generate_response(tone: str, state: ConsciousnessState, 
                     include_technical: bool = False) -> str:
    """Quick function to generate response in specified tone"""
    responder = ToneResponder()
    return responder.generate(tone, state, include_technical)
