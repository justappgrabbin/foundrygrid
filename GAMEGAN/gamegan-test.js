/**
 * GameGAN Test Harness
 * Tests behavioral predictions across different scenarios
 */

const GameGAN = require('./gamegan.js');

// ============================================================================
// TEST SCENARIOS
// ============================================================================

const scenarios = [
  {
    name: 'Projector with Splenic Authority - Gentle Guidance',
    chart: {
      body: {
        type: 'Projector',
        profile: '2/4',
        authority: 'splenic',
        definition: 'single',
        head: { defined: false },
        ajna: { defined: true },
        throat: { defined: false },
        g: { defined: true },
        heart: { defined: false },
        sacral: { defined: false },
        spleen: { defined: true },
        solar: { defined: false },
        root: { defined: false }
      },
      mind: {},
      heart: {}
    },
    intervention: {
      content: 'You might benefit from taking a break',
      tone: 'gentle',
      style: 'informative',
      allowsResponse: true,
      requiresImmediate: false,
      complexity: 'low'
    },
    context: {
      emotionalWave: 'neutral',
      positiveInteractions: 5,
      sessionCount: 10,
      initialTrust: 0.6
    }
  },
  
  {
    name: 'Manifestor - Directive Approach (Should Trigger Resistance)',
    chart: {
      body: {
        type: 'Manifestor',
        profile: '1/3',
        authority: 'emotional',
        definition: 'single',
        head: { defined: true },
        ajna: { defined: true },
        throat: { defined: true },
        g: { defined: false },
        heart: { defined: true },
        sacral: { defined: false },
        spleen: { defined: false },
        solar: { defined: true },
        root: { defined: false }
      },
      mind: {},
      heart: {}
    },
    intervention: {
      content: 'You need to do this right now',
      tone: 'directive',
      style: 'urgent',
      allowsResponse: false,
      requiresImmediate: true,
      complexity: 'medium'
    },
    context: {
      emotionalWave: 'high',
      positiveInteractions: 2,
      sessionCount: 3,
      initialTrust: 0.4
    }
  },
  
  {
    name: 'Generator - Response-Based Intervention',
    chart: {
      body: {
        type: 'Generator',
        profile: '5/1',
        authority: 'sacral',
        definition: 'single',
        head: { defined: false },
        ajna: { defined: false },
        throat: { defined: false },
        g: { defined: true },
        heart: { defined: false },
        sacral: { defined: true },
        spleen: { defined: false },
        solar: { defined: false },
        root: { defined: true }
      },
      mind: {},
      heart: {}
    },
    intervention: {
      content: 'Does this resonate with you?',
      tone: 'gentle',
      style: 'responsive',
      allowsResponse: true,
      requiresImmediate: false,
      complexity: 'low'
    },
    context: {
      emotionalWave: 'neutral',
      positiveInteractions: 8,
      sessionCount: 15,
      initialTrust: 0.8
    }
  },
  
  {
    name: 'Reflector - High Sensitivity, Needs Patience',
    chart: {
      body: {
        type: 'Reflector',
        profile: '6/2',
        authority: 'lunar',
        definition: 'none',
        head: { defined: false },
        ajna: { defined: false },
        throat: { defined: false },
        g: { defined: false },
        heart: { defined: false },
        sacral: { defined: false },
        spleen: { defined: false },
        solar: { defined: false },
        root: { defined: false }
      },
      mind: {},
      heart: {}
    },
    intervention: {
      content: 'Take your time to feel into this over the next lunar cycle',
      tone: 'gentle',
      style: 'patient',
      allowsResponse: true,
      requiresImmediate: false,
      complexity: 'low'
    },
    context: {
      emotionalWave: 'neutral',
      positiveInteractions: 3,
      sessionCount: 5,
      initialTrust: 0.5
    }
  },
  
  {
    name: 'Emotional Generator - Rushed Decision (Bad Timing)',
    chart: {
      body: {
        type: 'Generator',
        profile: '3/5',
        authority: 'emotional',
        definition: 'triple split',
        head: { defined: true },
        ajna: { defined: false },
        throat: { defined: false },
        g: { defined: false },
        heart: { defined: false },
        sacral: { defined: true },
        spleen: { defined: false },
        solar: { defined: true },
        root: { defined: true }
      },
      mind: {},
      heart: {}
    },
    intervention: {
      content: 'Make a decision now',
      tone: 'directive',
      style: 'urgent',
      allowsResponse: false,
      requiresImmediate: true,
      complexity: 'high'
    },
    context: {
      emotionalWave: 'low',
      negativeInteractions: 2,
      sessionCount: 7,
      initialTrust: 0.5
    }
  }
];

// ============================================================================
// RUN TESTS
// ============================================================================

console.log('🎮 GameGAN Behavioral Prediction Tests\n');
console.log('=' .repeat(80));

scenarios.forEach((scenario, index) => {
  console.log(`\nTest ${index + 1}: ${scenario.name}`);
  console.log('-'.repeat(80));
  
  const prediction = GameGAN.predictResponse(
    scenario.chart,
    scenario.intervention,
    scenario.context
  );
  
  console.log('\n📊 Prediction Results:');
  console.log(`   Acceptance Probability: ${(prediction.acceptanceProbability * 100).toFixed(0)}%`);
  console.log(`   Resistance Level: ${(prediction.resistanceLevel * 100).toFixed(0)}%`);
  console.log(`   Predicted Outcome: ${prediction.predictedOutcome}`);
  console.log(`   Optimal Tone: ${prediction.optimalTone}`);
  console.log(`   Optimal Sense: ${prediction.optimalSense}`);
  console.log(`   Confidence: ${(prediction.confidence * 100).toFixed(0)}%`);
  
  if (prediction.warnings.length > 0) {
    console.log('\n⚠️  Warnings:');
    prediction.warnings.forEach(w => console.log(`   - ${w}`));
  }
  
  if (prediction.suggestions.length > 0) {
    console.log('\n💡 Suggestions:');
    prediction.suggestions.forEach(s => console.log(`   - ${s}`));
  }
  
  console.log('\n📈 Details:');
  console.log(`   Openness: ${(prediction.details.openness * 100).toFixed(0)}%`);
  console.log(`   Emotional State: ${prediction.details.emotionalState}`);
  console.log(`   Authority Aligned: ${prediction.details.authorityAlignment}`);
  console.log(`   Processing Mode: ${prediction.details.processingMode}`);
  console.log(`   Trust Level: ${(prediction.details.trustLevel * 100).toFixed(0)}%`);
  
  console.log('\n' + '='.repeat(80));
});

console.log('\n✅ All tests complete!\n');
