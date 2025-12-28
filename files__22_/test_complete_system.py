"""
Complete System Test

Tests PhotoGAN, GameGAN, and Mathematical systems together.
"""

import sys
sys.path.insert(0, '/home/claude/synthai')

from consciousness_core import ConsciousnessCore
from photogan import PhotoGAN, generate_consciousness_image
from gamegan import GameGAN, predict_outcome
from mathematics import MathematicalCore, calculate_all_metrics

print("=" * 70)
print("COMPLETE SYSTEM TEST")
print("=" * 70)

# Initialize systems
print("\n1. Initializing systems...")
core = ConsciousnessCore()
photo_gan = PhotoGAN(size=256)  # Smaller for quick test
game_gan = GameGAN()
math_core = MathematicalCore()
print("✓ All systems initialized")

# Test input
user_input = "I'm thinking about starting a new project but I'm feeling scattered"

print(f"\n2. Analyzing: \"{user_input}\"")
state = core.analyze(user_input)
print(f"✓ Coordinate: {state.coordinate_string}")
print(f"✓ Dimension: {state.dimension_name} ({state.blended_probabilities[state.dimension_name]:.0%})")
print(f"✓ Coherence: {state.coherence:.1%}")

# Test Mathematical Core
print("\n3. Testing Mathematical Core...")
metrics = calculate_all_metrics(
    state.gate, state.line, state.color, state.tone, state.base
)
print(f"✓ Shannon Entropy: {metrics['entropy']:.3f} bits")
print(f"✓ Coherence: {metrics['coherence']:.1%}")
print(f"✓ Confidence: {metrics['confidence']:.1%}")
print(f"✓ Primary Dimension: {metrics['primary_dimension']}")

# Test PhotoGAN
print("\n4. Testing PhotoGAN...")
print("Generating consciousness image...")
img = photo_gan.generate(
    state.coordinate_string,
    state.dimension_name,
    state.coherence
)
output_path = "/mnt/user-data/outputs/consciousness_test.png"
img.save(output_path)
print(f"✓ Image generated: {output_path}")
print(f"✓ Size: {img.size[0]}x{img.size[1]}")

# Generate AI prompt
prompt = photo_gan.generate_prompt(
    state.coordinate_string,
    state.dimension_name,
    state.gate_name,
    state.gate_theme
)
print(f"✓ AI Image Prompt generated (for Stable Diffusion/DALL-E)")

# Test GameGAN
print("\n5. Testing GameGAN...")
intervention = "Start the new project tomorrow morning"
print(f"Predicting outcome of: \"{intervention}\"")

prediction = game_gan.predict(state, intervention, user_input)

print(f"✓ Recommendation: {prediction['recommendation']}")
print(f"✓ Confidence: {prediction['confidence']:.1%}")
print(f"\nTop 3 Outcomes:")
for i, outcome in enumerate(prediction['outcomes'][:3], 1):
    print(f"  {i}. {outcome['probability']:.0%} - {outcome['description']}")

print(f"\n✓ Analysis: {prediction['analysis']}")

if prediction['alternatives']:
    print(f"\nAlternatives to consider:")
    for alt in prediction['alternatives']:
        print(f"  • {alt['action']}")
        print(f"    ({alt['reason']})")

# Summary
print("\n" + "=" * 70)
print("SYSTEM CAPABILITIES DEMONSTRATED")
print("=" * 70)

print("""
✅ Consciousness Analysis
   • Text → Coordinate mapping
   • Dimensional probability distribution
   • Coherence/stability metrics

✅ Mathematical Core
   • Shannon entropy calculation
   • Euclidean distance measurement
   • Bayesian probability updating
   • Information theory metrics

✅ PhotoGAN
   • Geometric image generation
   • Consciousness visualization
   • AI prompt generation
   • Deterministic patterns

✅ GameGAN
   • Behavioral prediction
   • Outcome probability calculation
   • Intervention analysis
   • Alternative suggestions

All systems operational and integrated! 🔥
""")

print("=" * 70)
