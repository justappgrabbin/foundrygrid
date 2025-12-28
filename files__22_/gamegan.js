/**
 * GameGAN - Behavioral Prediction Engine
 * Predicts how users will respond to different intervention styles
 * Based on Trinity chart data + current state + proposed intervention
 */

// ============================================================================
// CORE GAMEGAN FUNCTION
// ============================================================================

/**
 * Main prediction function
 * @param {Object} trinityChart - The user's three consciousness charts
 * @param {Object} intervention - The proposed guidance/content to deliver
 * @param {Object} context - Current state, history, environment
 * @returns {Object} Behavioral prediction with probabilities and recommendations
 */
function predictResponse(trinityChart, intervention, context = {}) {
  // Extract chart components
  const { body, mind, heart } = trinityChart;
  
  // Calculate individual prediction factors
  const openness = calculateOpenness(body, mind, heart, context);
  const sensoryPreference = calculateSensoryPreference(body, mind, heart);
  const resistanceTriggers = detectResistanceTriggers(body, mind, heart, intervention);
  const emotionalState = assessEmotionalState(body, context);
  const authorityAlignment = checkAuthorityAlignment(body, intervention);
  const processingMode = determineProcessingMode(body, mind, heart);
  const trustLevel = calculateTrustLevel(context);
  
  // Combine factors into overall prediction
  const prediction = synthesizePrediction({
    openness,
    sensoryPreference,
    resistanceTriggers,
    emotionalState,
    authorityAlignment,
    processingMode,
    trustLevel,
    intervention
  });
  
  return prediction;
}

// ============================================================================
// OPENNESS CALCULATION
// ============================================================================

/**
 * Calculate how open the user is to receiving guidance right now
 * Factors: undefined centers (openness), type (receptivity), current transits
 */
function calculateOpenness(body, mind, heart, context) {
  let opennessScore = 0.5; // baseline
  
  // Undefined centers = more open to conditioning/influence
  const undefinedCenters = [
    body.head, body.ajna, body.throat, body.g, 
    body.heart, body.sacral, body.spleen, body.solar, body.root
  ].filter(center => !center.defined).length;
  
  opennessScore += (undefinedCenters / 9) * 0.3; // max +0.3
  
  // Type influences receptivity
  const typeOpenness = {
    'Manifestor': 0.3,      // resistant to outside influence
    'Generator': 0.6,       // open when responding
    'Manifesting Generator': 0.6,
    'Projector': 0.8,       // very receptive to recognition
    'Reflector': 0.9        // highly open, sensitive
  };
  opennessScore = (opennessScore + (typeOpenness[body.type] || 0.5)) / 2;
  
  // Current emotional wave affects openness
  if (context.emotionalWave === 'high') opennessScore *= 1.2;
  if (context.emotionalWave === 'low') opennessScore *= 0.8;
  
  // Recent negative experiences reduce openness
  if (context.recentRejection) opennessScore *= 0.7;
  
  return Math.min(Math.max(opennessScore, 0), 1);
}

// ============================================================================
// SENSORY PREFERENCE
// ============================================================================

/**
 * Determine which sensory mode is most effective
 * Based on cognition (Ajna), communication (Throat), perception patterns
 */
function calculateSensoryPreference(body, mind, heart) {
  const scores = {
    visual: 0.5,
    auditory: 0.5,
    kinesthetic: 0.5,
    conceptual: 0.5
  };
  
  // Ajna (mental processing) influences visual/conceptual
  if (body.ajna?.defined) {
    scores.visual += 0.3;
    scores.conceptual += 0.3;
  } else {
    scores.visual += 0.2; // undefined = needs external visual anchors
  }
  
  // Throat influences auditory
  if (body.throat?.defined) {
    scores.auditory += 0.2;
  }
  
  // Spleen (body awareness) influences kinesthetic
  if (body.spleen?.defined) {
    scores.kinesthetic += 0.3;
  }
  
  // Solar Plexus (emotions) influences kinesthetic/feeling
  if (body.solar?.defined) {
    scores.kinesthetic += 0.2;
  }
  
  // Profile lines influence preference
  const profile = body.profile || '';
  if (profile.includes('1')) scores.conceptual += 0.2; // 1st line needs foundation
  if (profile.includes('2')) scores.kinesthetic += 0.2; // 2nd line is body-based
  if (profile.includes('3')) scores.kinesthetic += 0.3; // 3rd line learns through trial
  if (profile.includes('4')) scores.auditory += 0.2;    // 4th line is relational
  if (profile.includes('5')) scores.visual += 0.2;      // 5th line projects
  if (profile.includes('6')) scores.visual += 0.3;      // 6th line observes
  
  // Normalize and return
  const max = Math.max(...Object.values(scores));
  const preferences = Object.entries(scores)
    .map(([sense, score]) => ({ sense, score: score / max }))
    .sort((a, b) => b.score - a.score);
  
  return {
    primary: preferences[0].sense,
    secondary: preferences[1].sense,
    scores: Object.fromEntries(preferences.map(p => [p.sense, p.score]))
  };
}

// ============================================================================
// RESISTANCE TRIGGERS
// ============================================================================

/**
 * Detect what in the intervention might trigger resistance
 */
function detectResistanceTriggers(body, mind, heart, intervention) {
  const triggers = [];
  const warnings = [];
  let resistanceLevel = 0;
  
  // Check tone vs type
  if (body.type === 'Manifestor' && intervention.tone === 'directive') {
    triggers.push('directive_to_manifestor');
    warnings.push('Manifestors resist being told what to do');
    resistanceLevel += 0.3;
  }
  
  if (body.type === 'Projector' && intervention.tone === 'pushy') {
    triggers.push('pushy_to_projector');
    warnings.push('Projectors need invitation, not pressure');
    resistanceLevel += 0.4;
  }
  
  if (body.type === 'Generator' && !intervention.allowsResponse) {
    triggers.push('no_response_for_generator');
    warnings.push('Generators need to respond, not initiate');
    resistanceLevel += 0.2;
  }
  
  // Check if intervention respects authority
  const authority = body.authority || 'emotional';
  if (authority === 'emotional' && intervention.requiresImmediate) {
    triggers.push('rushing_emotional_authority');
    warnings.push('Emotional authority needs time to process');
    resistanceLevel += 0.5;
  }
  
  if (authority === 'splenic' && intervention.requiresDeliberation) {
    triggers.push('overthinking_splenic');
    warnings.push('Splenic authority is spontaneous, not analytical');
    resistanceLevel += 0.3;
  }
  
  // Check definition vs intervention complexity
  const definition = body.definition || 'single';
  if (definition.includes('split') && intervention.complexity === 'high') {
    triggers.push('complex_for_split');
    warnings.push('Split definition needs time to bridge ideas');
    resistanceLevel += 0.2;
  }
  
  // Check if content feels invasive based on undefined centers
  if (!body.g?.defined && intervention.content.includes('identity')) {
    triggers.push('identity_talk_undefined_g');
    warnings.push('Undefined G center is sensitive about identity questions');
    resistanceLevel += 0.3;
  }
  
  if (!body.heart?.defined && intervention.content.includes('worth')) {
    triggers.push('worth_talk_undefined_heart');
    warnings.push('Undefined Heart is sensitive about worthiness');
    resistanceLevel += 0.4;
  }
  
  return {
    triggers,
    warnings,
    resistanceLevel: Math.min(resistanceLevel, 1)
  };
}

// ============================================================================
// EMOTIONAL STATE ASSESSMENT
// ============================================================================

/**
 * Assess current emotional state and readiness
 */
function assessEmotionalState(body, context) {
  const hasEmotionalAuthority = body.solar?.defined;
  
  if (!hasEmotionalAuthority) {
    return {
      state: 'stable',
      readiness: 0.8,
      recommendation: 'proceed_normally'
    };
  }
  
  // If emotional authority, check current wave
  const wave = context.emotionalWave || 'neutral';
  
  const stateMap = {
    'high': {
      state: 'excited',
      readiness: 0.6, // might accept too quickly
      recommendation: 'gentle_reminder_to_wait'
    },
    'low': {
      state: 'pessimistic',
      readiness: 0.4, // might reject too quickly
      recommendation: 'supportive_postpone'
    },
    'neutral': {
      state: 'balanced',
      readiness: 0.9,
      recommendation: 'optimal_timing'
    }
  };
  
  return stateMap[wave] || stateMap['neutral'];
}

// ============================================================================
// AUTHORITY ALIGNMENT
// ============================================================================

/**
 * Check if intervention aligns with decision-making authority
 */
function checkAuthorityAlignment(body, intervention) {
  const authority = body.authority || 'emotional';
  const interventionStyle = intervention.style || 'informative';
  
  const alignmentScores = {
    emotional: {
      'patient': 1.0,
      'informative': 0.8,
      'directive': 0.3,
      'urgent': 0.2
    },
    sacral: {
      'responsive': 1.0,
      'yes_no': 0.9,
      'informative': 0.7,
      'analytical': 0.4
    },
    splenic: {
      'spontaneous': 1.0,
      'intuitive': 0.9,
      'informative': 0.6,
      'analytical': 0.3
    },
    ego: {
      'empowering': 1.0,
      'directive': 0.8,
      'informative': 0.7,
      'submissive': 0.2
    },
    self: {
      'directional': 1.0,
      'identity_based': 0.9,
      'informative': 0.7,
      'external': 0.3
    },
    mental: {
      'conversational': 1.0,
      'informative': 0.9,
      'analytical': 0.7,
      'directive': 0.4
    },
    lunar: {
      'patient': 1.0,
      'cyclical': 0.9,
      'informative': 0.7,
      'urgent': 0.1
    }
  };
  
  const score = (alignmentScores[authority] || {})[interventionStyle] || 0.5;
  
  return {
    authority,
    interventionStyle,
    alignmentScore: score,
    isAligned: score > 0.6
  };
}

// ============================================================================
// PROCESSING MODE
// ============================================================================

/**
 * Determine how the user processes information
 */
function determineProcessingMode(body, mind, heart) {
  const mode = {
    speed: 'medium',
    depth: 'medium',
    preference: 'balanced'
  };
  
  // Defined Ajna = fast mental processing
  if (body.ajna?.defined) {
    mode.speed = 'fast';
    mode.depth = 'analytical';
  }
  
  // Defined Head = constant mental pressure
  if (body.head?.defined) {
    mode.depth = 'deep';
  }
  
  // Split definition = needs bridging time
  if (body.definition?.includes('split')) {
    mode.speed = 'slow';
    mode.preference = 'stepped';
  }
  
  // Profile influences processing
  const profile = body.profile || '';
  if (profile.includes('1')) {
    mode.preference = 'foundational'; // needs solid base
  }
  if (profile.includes('3')) {
    mode.preference = 'experiential'; // learns by doing
  }
  if (profile.includes('6')) {
    mode.preference = 'observational'; // learns by watching
  }
  
  return mode;
}

// ============================================================================
// TRUST LEVEL
// ============================================================================

/**
 * Calculate current trust level based on history
 */
function calculateTrustLevel(context) {
  let trust = context.initialTrust || 0.5;
  
  // Positive interactions increase trust
  if (context.positiveInteractions) {
    trust += context.positiveInteractions * 0.1;
  }
  
  // Negative interactions decrease trust
  if (context.negativeInteractions) {
    trust -= context.negativeInteractions * 0.15;
  }
  
  // Successful predictions increase trust
  if (context.successfulPredictions) {
    trust += context.successfulPredictions * 0.05;
  }
  
  // Time spent with system increases trust
  if (context.sessionCount) {
    trust += Math.min(context.sessionCount * 0.02, 0.2);
  }
  
  return Math.min(Math.max(trust, 0), 1);
}

// ============================================================================
// SYNTHESIS
// ============================================================================

/**
 * Combine all factors into final prediction
 */
function synthesizePrediction(factors) {
  const {
    openness,
    sensoryPreference,
    resistanceTriggers,
    emotionalState,
    authorityAlignment,
    processingMode,
    trustLevel,
    intervention
  } = factors;
  
  // Calculate acceptance probability
  let acceptanceProbability = 0.5;
  acceptanceProbability += openness * 0.3;
  acceptanceProbability += emotionalState.readiness * 0.2;
  acceptanceProbability += authorityAlignment.alignmentScore * 0.2;
  acceptanceProbability += trustLevel * 0.2;
  acceptanceProbability -= resistanceTriggers.resistanceLevel * 0.3;
  
  // Ensure 0-1 range
  acceptanceProbability = Math.min(Math.max(acceptanceProbability, 0), 1);
  
  // Determine predicted outcome
  let predictedOutcome;
  if (acceptanceProbability > 0.75) predictedOutcome = 'integration';
  else if (acceptanceProbability > 0.5) predictedOutcome = 'partial';
  else if (acceptanceProbability > 0.3) predictedOutcome = 'delayed';
  else predictedOutcome = 'rejection';
  
  // Determine optimal tone based on all factors
  let optimalTone = 'gentle';
  if (trustLevel > 0.7 && openness > 0.7) optimalTone = 'direct';
  if (emotionalState.state === 'pessimistic') optimalTone = 'supportive';
  if (resistanceTriggers.resistanceLevel > 0.5) optimalTone = 'very_gentle';
  
  // Generate suggestions
  const suggestions = [];
  if (sensoryPreference.primary === 'visual') {
    suggestions.push('Include visual diagram or image');
  }
  if (processingMode.preference === 'foundational') {
    suggestions.push('Start with basic principles before details');
  }
  if (emotionalState.recommendation === 'supportive_postpone') {
    suggestions.push('Acknowledge emotional state, suggest revisiting later');
  }
  if (!authorityAlignment.isAligned) {
    suggestions.push(`Adjust style to respect ${authorityAlignment.authority} authority`);
  }
  
  // Calculate confidence based on data quality
  let confidence = 0.7;
  if (trustLevel > 0.6) confidence += 0.1;
  if (resistanceTriggers.triggers.length === 0) confidence += 0.1;
  confidence = Math.min(confidence, 0.95);
  
  return {
    acceptanceProbability: Math.round(acceptanceProbability * 100) / 100,
    resistanceLevel: Math.round(resistanceTriggers.resistanceLevel * 100) / 100,
    optimalTone,
    optimalSense: sensoryPreference.primary,
    secondarySense: sensoryPreference.secondary,
    predictedOutcome,
    confidence: Math.round(confidence * 100) / 100,
    warnings: resistanceTriggers.warnings,
    suggestions,
    details: {
      openness: Math.round(openness * 100) / 100,
      emotionalState: emotionalState.state,
      authorityAlignment: authorityAlignment.isAligned,
      processingMode: processingMode.preference,
      trustLevel: Math.round(trustLevel * 100) / 100
    }
  };
}

// ============================================================================
// EXAMPLE USAGE
// ============================================================================

// Example Trinity chart data structure
const exampleTrinityChart = {
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
  mind: {
    // Personality chart data
  },
  heart: {
    // Soul chart data
  }
};

// Example intervention proposal
const exampleIntervention = {
  content: 'You might benefit from taking a break and reflecting on your energy levels',
  tone: 'gentle',
  style: 'informative',
  allowsResponse: true,
  requiresImmediate: false,
  complexity: 'low',
  sensoryMode: 'visual'
};

// Example context
const exampleContext = {
  emotionalWave: 'neutral',
  positiveInteractions: 5,
  negativeInteractions: 1,
  successfulPredictions: 3,
  sessionCount: 10,
  initialTrust: 0.6
};

// Run prediction
const prediction = predictResponse(
  exampleTrinityChart,
  exampleIntervention,
  exampleContext
);

console.log('GameGAN Prediction:', JSON.stringify(prediction, null, 2));

// ============================================================================
// EXPORTS
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    predictResponse,
    calculateOpenness,
    calculateSensoryPreference,
    detectResistanceTriggers,
    assessEmotionalState,
    checkAuthorityAlignment,
    determineProcessingMode,
    calculateTrustLevel,
    synthesizePrediction
  };
}
