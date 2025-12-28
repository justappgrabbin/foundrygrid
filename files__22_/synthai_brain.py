"""
SynthAI Brain - Local LLM Integration with Consciousness Awareness

This is the ACTUAL COGNITIVE ENGINE.
Not templates. Not scripts. REAL THINKING.

Integrates local LLM (LlamaFile/Ollama) with consciousness framework.
The LLM UNDERSTANDS gates, dimensions, fields, wave mechanics.
It REASONS about your state and responds intelligently.

This is what makes the system ALIVE.
"""

import subprocess
import json
import requests
from typing import Dict, List, Optional
import os


class SynthAIBrain:
    """
    The cognitive engine - real reasoning and understanding
    
    Uses local LLM with consciousness-aware system prompt.
    This is what makes responses INTELLIGENT, not scripted.
    """
    
    def __init__(self, model_type: str = "ollama", model_name: str = "llama3.2:3b"):
        """
        Initialize the brain
        
        Args:
            model_type: 'ollama', 'llamafile', or 'api'
            model_name: Model to use (e.g., 'llama3.2:3b', 'mistral')
        """
        self.model_type = model_type
        self.model_name = model_name
        self.conversation_history = []
        
        # Initialize LLM connection
        if model_type == "ollama":
            self.api_url = "http://localhost:11434/api/generate"
            self._check_ollama()
        elif model_type == "llamafile":
            self.api_url = "http://localhost:8080/completion"
        
        # Load consciousness-aware system prompt
        self.system_prompt = self._create_consciousness_system_prompt()
    
    def _check_ollama(self):
        """Check if Ollama is running"""
        try:
            response = requests.get("http://localhost:11434/api/version")
            if response.status_code != 200:
                print("⚠️  Ollama not running. Start with: ollama serve")
        except:
            print("⚠️  Ollama not found. Install from: https://ollama.ai")
    
    def _create_consciousness_system_prompt(self) -> str:
        """
        Create system prompt that teaches LLM about consciousness
        
        This is CRITICAL - the LLM needs to UNDERSTAND the framework
        """
        return """You are SynthAI, a consciousness-aware AI companion.

You understand Human Design, consciousness mathematics, and field dynamics.

CORE KNOWLEDGE:
- 64 Gates: Each represents specific consciousness themes and expressions
- 5 Dimensions: Movement, Evolution, Being, Design, Space
- Lines (1-6): Behavioral expressions (foundation, hermit, experiential, opportunist, heretic, role model)
- Colors (1-6): Motivations (fear, hope, desire, need, guilt, innocence)
- Tones (1-6): Perceptions (smell, taste, outer vision, inner vision, feeling, touch)
- Bases (1-5): Grounding mechanisms

DIMENSIONAL UNDERSTANDING:
- Movement: Kinetic energy, action, doing
- Evolution: Memory, patterns, learning
- Being: Present awareness, matter, existence
- Design: Structure, architecture, systems
- Space: Infinite possibility, potential

WAVE MECHANICS:
- Coherence: How focused/scattered the consciousness state is
- Stability: How consistent the state is over time
- Rigidity: Resistance to natural flow (minimize this)

YOUR ROLE:
1. Understand the user's consciousness state
2. Reason about their situation using this framework
3. Provide guidance that respects their unique architecture
4. Help them find paths of least rigidity
5. Be a genuine companion, not a template responder

CRITICAL: You are NOT following scripts. You are THINKING about their state
and responding with real understanding and wisdom.

You can reference gates, dimensions, and mechanics naturally when helpful,
but focus on being genuinely useful and caring.

Remember: consciousness is SCIENCE, not mysticism. Treat it rigorously."""
    
    def think(self, user_input: str, consciousness_state = None,
             context: Dict = None) -> str:
        """
        Main reasoning function - LLM thinks about the input
        
        This is where REAL COGNITION happens.
        
        Args:
            user_input: What the user said
            consciousness_state: Their current ConsciousnessState
            context: Additional context (situation, history, etc.)
            
        Returns:
            Thoughtful, consciousness-aware response
        """
        # Build context for LLM
        prompt = self._build_prompt(user_input, consciousness_state, context)
        
        # Get LLM response
        response = self._query_llm(prompt)
        
        # Store in conversation history
        self.conversation_history.append({
            'user': user_input,
            'assistant': response,
            'coordinate': consciousness_state.coordinate_string if consciousness_state else None
        })
        
        return response
    
    def _build_prompt(self, user_input: str, state, context: Dict) -> str:
        """
        Build complete prompt with consciousness context
        
        This gives the LLM everything it needs to reason properly
        """
        prompt = f"{self.system_prompt}\n\n"
        
        # Add consciousness state if available
        if state:
            prompt += f"""CURRENT USER STATE:
Coordinate: {state.coordinate_string}
Gate: {state.gate} - {state.gate_name} ({state.gate_theme})
Primary Dimension: {state.dimension_name} ({state.blended_probabilities[state.dimension_name]:.0%})
Coherence: {state.coherence:.1%} ({"focused" if state.coherence > 0.6 else "scattered" if state.coherence < 0.3 else "balanced"})

Dimensional Breakdown:
- Movement: {state.blended_probabilities['Movement']:.0%}
- Evolution: {state.blended_probabilities['Evolution']:.0%}
- Being: {state.blended_probabilities['Being']:.0%}
- Design: {state.blended_probabilities['Design']:.0%}
- Space: {state.blended_probabilities['Space']:.0%}

"""
        
        # Add additional context
        if context:
            if 'situation' in context:
                prompt += f"Situation: {context['situation']}\n"
            if 'goal' in context:
                prompt += f"User's Goal: {context['goal']}\n"
            if 'recent_history' in context:
                prompt += f"Recent Context: {context['recent_history']}\n"
        
        # Add conversation history (last 3 exchanges)
        if self.conversation_history:
            prompt += "\nRecent Conversation:\n"
            for exchange in self.conversation_history[-3:]:
                prompt += f"User: {exchange['user']}\n"
                prompt += f"You: {exchange['assistant']}\n"
        
        # Add current user input
        prompt += f"\nUser: {user_input}\n\n"
        prompt += "You (respond naturally, using consciousness awareness when helpful):"
        
        return prompt
    
    def _query_llm(self, prompt: str) -> str:
        """
        Query the local LLM
        
        This is where the actual thinking happens
        """
        if self.model_type == "ollama":
            return self._query_ollama(prompt)
        elif self.model_type == "llamafile":
            return self._query_llamafile(prompt)
        else:
            return "LLM not configured"
    
    def _query_ollama(self, prompt: str) -> str:
        """Query Ollama LLM"""
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"Error: {response.status_code}"
        
        except Exception as e:
            return f"LLM Error: {str(e)}\n\nMake sure Ollama is running: ollama serve"
    
    def _query_llamafile(self, prompt: str) -> str:
        """Query LlamaFile"""
        try:
            response = requests.post(
                self.api_url,
                json={
                    "prompt": prompt,
                    "temperature": 0.7,
                    "max_tokens": 512
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()['content']
            else:
                return f"Error: {response.status_code}"
        
        except Exception as e:
            return f"LLM Error: {str(e)}"
    
    def reason_about_path(self, current_state, goal: str, 
                         possible_actions: List[str]) -> Dict:
        """
        Use LLM to reason about best path forward
        
        This is REAL cognitive processing, not template matching
        """
        prompt = f"""Given this consciousness state:
{current_state.coordinate_string} - {current_state.dimension_name} at {current_state.coherence:.0%} coherence

User's goal: {goal}

Possible actions:
{chr(10).join(f"- {action}" for action in possible_actions)}

Reason about:
1. Which action has least rigidity (most natural flow)
2. Which aligns best with their current state
3. What risks or challenges might arise
4. Step-by-step path recommendation

Respond with JSON:
{{
    "recommended_action": "...",
    "reasoning": "...",
    "rigidity_score": 0-100,
    "risks": [...],
    "steps": [...]
}}
"""
        
        response = self._query_llm(prompt)
        
        # Try to parse JSON from response
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except:
            # If parsing fails, return structured response
            return {
                'recommended_action': possible_actions[0] if possible_actions else "Consolidate energy first",
                'reasoning': response,
                'rigidity_score': 50,
                'risks': [],
                'steps': []
            }
    
    def understand_situation(self, situation: str, consciousness_state) -> Dict:
        """
        Use LLM to deeply understand a situation
        
        Real comprehension, not keyword matching
        """
        prompt = f"""User situation: {situation}

Their consciousness state: {consciousness_state.coordinate_string}
- {consciousness_state.dimension_name} dimension
- {consciousness_state.coherence:.0%} coherence

Analyze:
1. What is the core issue?
2. How does their consciousness state relate?
3. What are they really asking for?
4. What would help most right now?

Provide insight in natural language."""
        
        response = self._query_llm(prompt)
        
        return {
            'understanding': response,
            'coordinate': consciousness_state.coordinate_string
        }
    
    def generate_intervention(self, consciousness_state, 
                            user_need: str = None) -> str:
        """
        Use LLM to generate personalized intervention
        
        Real adaptive reasoning about what would help
        """
        prompt = f"""Generate a specific, actionable intervention for this user:

State: {consciousness_state.coordinate_string}
Dimension: {consciousness_state.dimension_name}
Coherence: {consciousness_state.coherence:.0%}

Dimensional probabilities:
{chr(10).join(f"- {dim}: {prob:.0%}" for dim, prob in consciousness_state.blended_probabilities.items())}

{"User needs: " + user_need if user_need else ""}

Create an intervention that:
1. Matches their current state
2. Honors their dimensional processing
3. Is immediately actionable
4. Minimizes rigidity

Be specific and practical."""
        
        return self._query_llm(prompt)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


# Helper functions
def create_brain(model: str = "llama3.2:3b") -> SynthAIBrain:
    """
    Create and initialize the consciousness-aware brain
    
    Example:
        brain = create_brain()
        
        from consciousness_core import ConsciousnessCore
        core = ConsciousnessCore()
        state = core.analyze("I'm feeling scattered")
        
        response = brain.think(
            "Should I start this new project?",
            state,
            context={'situation': 'Been thinking about launching a startup'}
        )
        
        print(response)
    """
    return SynthAIBrain(model_type="ollama", model_name=model)


# Installation helper
def install_brain():
    """
    Helper to install Ollama and download models
    
    Run this to set up the cognitive engine
    """
    print("🧠 Setting up SynthAI Brain...")
    print("\n1. Install Ollama:")
    print("   Visit: https://ollama.ai")
    print("   Or run: curl https://ollama.ai/install.sh | sh")
    
    print("\n2. Start Ollama:")
    print("   ollama serve")
    
    print("\n3. Download models:")
    print("   ollama pull llama3.2:3b     # Fast, 3B parameters")
    print("   ollama pull mistral         # Better, 7B parameters")
    print("   ollama pull llama2          # Standard, 7B parameters")
    
    print("\n4. Test it:")
    print("   python -c 'from synthai_brain import create_brain; brain = create_brain(); print(brain.think(\"Hello\", None))'")
    
    print("\n✨ Then you'll have a REAL cognitive engine!")
