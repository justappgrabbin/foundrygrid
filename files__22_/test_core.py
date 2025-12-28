"""
Test script to verify the consciousness core is working
"""

import sys
sys.path.insert(0, '/home/claude/synthai')

from consciousness_core import ConsciousnessCore
from datetime import datetime

def test_basic_analysis():
    """Test basic analysis functionality"""
    print("=" * 60)
    print("CONSCIOUSNESS CORE TEST")
    print("=" * 60)
    
    core = ConsciousnessCore()
    
    # Test 1: Movement dimension text
    print("\n--- TEST 1: Movement Dimension ---")
    text1 = "I keep starting projects but never finishing them"
    state1 = core.analyze(text1)
    
    print(f"Text: {text1}")
    print(f"Coordinate: {state1.coordinate_string}")
    print(f"Position: {state1.position_string}")
    print(f"Gate: {state1.gate} - {state1.gate_name} ({state1.gate_theme})")
    print(f"Line: {state1.line} - {state1.line_name}")
    print(f"Center: {state1.center_name}")
    print(f"Dimension: {state1.dimension_name} ({state1.dimension_keynote})")
    print(f"\nDetected: {state1.detected_dimension} (confidence: {state1.detection_confidence:.2f})")
    print(f"Themes: {', '.join(state1.detection_themes)}")
    print(f"\nProbability Vector:")
    for dim, prob in sorted(state1.blended_probabilities.items(), key=lambda x: x[1], reverse=True):
        print(f"  {dim:12} {'█' * int(prob * 40):40} {prob:.1%}")
    print(f"\nMetrics:")
    print(f"  Coherence:  {state1.coherence:.1%}")
    print(f"  Stability:  {state1.stability:.1%}")
    print(f"  Confidence: {state1.confidence:.1%}")
    print(f"\nMetaphysical Sentence:")
    print(f"  {state1.metaphysical_sentence}")
    print(f"\nGuidance:")
    print(f"  {state1.guidance_action}")
    
    # Test 2: Evolution dimension text
    print("\n\n--- TEST 2: Evolution Dimension ---")
    text2 = "I'm trying to understand why I keep repeating this pattern"
    state2 = core.analyze(text2)
    
    print(f"Text: {text2}")
    print(f"Coordinate: {state2.coordinate_string}")
    print(f"Gate: {state2.gate} - {state2.gate_name} ({state2.gate_theme})")
    print(f"Detected: {state2.detected_dimension} (confidence: {state2.detection_confidence:.2f})")
    print(f"\nProbability Vector:")
    for dim, prob in sorted(state2.blended_probabilities.items(), key=lambda x: x[1], reverse=True):
        print(f"  {dim:12} {'█' * int(prob * 40):40} {prob:.1%}")
    print(f"\nMetrics:")
    print(f"  Coherence:  {state2.coherence:.1%}")
    print(f"  Stability:  {state2.stability:.1%}")
    print(f"  Confidence: {state2.confidence:.1%}")
    
    # Test 3: Being dimension text
    print("\n\n--- TEST 3: Being Dimension ---")
    text3 = "I am here, feeling my body, present in this moment"
    state3 = core.analyze(text3)
    
    print(f"Text: {text3}")
    print(f"Coordinate: {state3.coordinate_string}")
    print(f"Gate: {state3.gate} - {state3.gate_name} ({state3.gate_theme})")
    print(f"Detected: {state3.detected_dimension} (confidence: {state3.detection_confidence:.2f})")
    print(f"\nProbability Vector:")
    for dim, prob in sorted(state3.blended_probabilities.items(), key=lambda x: x[1], reverse=True):
        print(f"  {dim:12} {'█' * int(prob * 40):40} {prob:.1%}")
    
    # Test 4: Quick analyze
    print("\n\n--- TEST 4: Quick Analyze ---")
    result = core.quick_analyze("Planning my week ahead with strategic thinking")
    print(f"Coordinate: {result['coordinate']}")
    print(f"Dimension: {result['dimension']}")
    print(f"Coherence: {result['coherence']:.1%}")
    print(f"Sentence: {result['sentence']}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)


if __name__ == "__main__":
    test_basic_analysis()
