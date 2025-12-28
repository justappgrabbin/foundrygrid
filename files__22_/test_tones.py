"""
Test all 5 personality tones
"""

import sys
sys.path.insert(0, '/home/claude/synthai')

from consciousness_core import ConsciousnessCore
from personality import ToneResponder

def test_all_tones():
    """Test all 5 personality tones on the same input"""
    print("=" * 70)
    print("PERSONALITY TONE TEST")
    print("=" * 70)
    
    core = ConsciousnessCore()
    responder = ToneResponder()
    
    # User input
    text = "I keep starting projects but never finishing them"
    
    print(f"\nUser Input: \"{text}\"\n")
    
    # Analyze once
    state = core.analyze(text)
    
    # Show each tone
    tones = ['venom', 'prime', 'echo', 'dream', 'softcore']
    
    for tone in tones:
        print("\n" + "─" * 70)
        print(f"TONE: {tone.upper()}")
        print("─" * 70)
        response = responder.generate(tone, state, include_technical=False)
        print(response)
    
    # Show one with technical details
    print("\n" + "=" * 70)
    print("WITH TECHNICAL DETAILS (PRIME TONE)")
    print("=" * 70)
    response = responder.generate('prime', state, include_technical=True)
    print(response)
    
    print("\n" + "=" * 70)
    print("ALL TONES TESTED ✓")
    print("=" * 70)


if __name__ == "__main__":
    test_all_tones()
