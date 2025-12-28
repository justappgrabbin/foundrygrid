/**
 * WAVE-BASED CAUSAL GRAPH SUBSTRATE
 * Mathematical foundation using frequency, resonance, and interference
 * 
 * Instead of arbitrary causality, nodes communicate via WAVE RESONANCE
 * Gates have frequencies, fields have harmonics, causality = wave interference
 * 
 * Based on your PDF's frequency calculation:
 *   frequency = baseFreq * gateMultiplier * lineMultiplier
 *   where gateMultiplier = 1 + (gate / 64)
 *   and lineMultiplier = 1 + (line / 12)
 */

class WaveResonanceCausalGraph {
  constructor() {
    // Wave parameters
    this.baseFrequency = 220; // A3 fundamental (from your PDF)
    this.sampleRate = 1000; // Updates per second
    this.time = 0;
    
    // Nodes as oscillators
    this.nodes = new Map(); // id → { freq, phase, amplitude, waveform }
    
    // Edges as resonance couplings
    this.edges = new Map(); // id → { from, to, resonanceStrength, phaseShift }
    
    // Field state (wave superposition)
    this.fieldState = new Map(); // nodeId → current amplitude
    
    // Evolution tracking
    this.resonanceHistory = [];
    this.proposedResonances = [];
    
    console.log('🌊 Wave-Resonance Causal Graph initialized');
  }
  
  // ============================================
  // NODE REGISTRATION (as oscillators)
  // ============================================
  
  registerNode(id, config) {
    /**
     * Register a node as a wave oscillator
     * 
     * @param {string} id - Node identifier
     * @param {Object} config
     * @param {number} config.gate - HD gate number (1-64)
     * @param {number} config.line - HD line number (1-6)
     * @param {number} config.color - HD color (1-6)
     * @param {number} config.tone - HD tone (1-6)
     * @param {string} config.field - Mind/Heart/Body
     * @param {Function} config.handler - Activation callback
     */
    
    const frequency = this._calculateFrequency(
      config.gate,
      config.line,
      config.color,
      config.tone
    );
    
    const fieldHarmonic = this._getFieldHarmonic(config.field);
    
    this.nodes.set(id, {
      id: id,
      gate: config.gate,
      line: config.line,
      color: config.color,
      tone: config.tone,
      field: config.field,
      
      // Wave properties
      frequency: frequency * fieldHarmonic,
      phase: Math.random() * Math.PI * 2, // Random initial phase
      amplitude: 0, // Current amplitude (0-1)
      waveform: config.waveform || 'sine', // sine, square, sawtooth, triangle
      
      // Callback
      handler: config.handler || null,
      
      // Metadata
      groups: config.groups || [],
      metadata: config.metadata || {}
    });
    
    // Initialize field state
    this.fieldState.set(id, 0);
    
    console.log(`✓ Registered wave node: ${id} @ ${frequency.toFixed(2)}Hz`);
  }
  
  _calculateFrequency(gate, line = 3, color = 3, tone = 3) {
    /**
     * Calculate frequency from HD coordinates
     * Based on your PDF formula + extensions for color/tone
     */
    
    const gateMultiplier = 1 + (gate / 64);       // 1.015 to 2.0
    const lineMultiplier = 1 + (line / 12);       // 1.08 to 1.5
    const colorMultiplier = 1 + (color / 60);     // 1.016 to 1.1
    const toneMultiplier = 1 + (tone / 120);      // 1.008 to 1.05
    
    const frequency = this.baseFrequency 
                    * gateMultiplier 
                    * lineMultiplier
                    * colorMultiplier
                    * toneMultiplier;
    
    // Clamp to audible/useful range
    return Math.max(200, Math.min(2000, frequency));
  }
  
  _getFieldHarmonic(field) {
    /**
     * Each field has its own harmonic multiplier
     * Mind (Sidereal) = higher frequencies
     * Heart (Tropical) = middle frequencies  
     * Body (Draconic) = lower frequencies
     */
    
    const harmonics = {
      'Mind': 1.5,      // Octave + fifth (fast, sharp)
      'Heart': 1.0,     // Fundamental (balanced)
      'Body': 0.75,     // Below fundamental (slow, deep)
      
      // Extended fields
      'Shadow': 0.5,    // Very low
      'Light': 2.0,     // Very high
      'Neutral': 1.25,  // Golden ratio-ish
      
      // Planetary bodies
      'Sun': 1.618,     // Phi
      'Moon': 1.414,    // √2
      'Mercury': 1.732  // √3
    };
    
    return harmonics[field] || 1.0;
  }
  
  // ============================================
  // RESONANCE EDGES (wave coupling)
  // ============================================
  
  registerResonanceEdge(id, config) {
    /**
     * Create resonance coupling between two oscillators
     * 
     * @param {Object} config
     * @param {string} config.from - Source node
     * @param {string} config.to - Target node
     * @param {number} config.strength - Coupling strength (0-1)
     * @param {number} config.phaseShift - Phase offset (radians)
     */
    
    const fromNode = this.nodes.get(config.from);
    const toNode = this.nodes.get(config.to);
    
    if (!fromNode || !toNode) {
      console.warn(`Can't create edge: missing node`);
      return;
    }
    
    // Calculate resonance based on frequency ratio
    const freqRatio = toNode.frequency / fromNode.frequency;
    const harmonicResonance = this._calculateHarmonicResonance(freqRatio);
    
    this.edges.set(id, {
      id: id,
      from: config.from,
      to: config.to,
      strength: config.strength || 1.0,
      phaseShift: config.phaseShift || 0,
      harmonicResonance: harmonicResonance,
      bidirectional: config.bidirectional || false
    });
    
    console.log(`→ Resonance edge: ${config.from} → ${config.to} (harmonic: ${harmonicResonance.toFixed(2)})`);
  }
  
  _calculateHarmonicResonance(freqRatio) {
    /**
     * How much do two frequencies resonate?
     * Perfect resonance at simple ratios: 1:1, 1:2, 2:3, 3:4, etc.
     */
    
    // Find closest simple ratio
    const ratios = [
      { ratio: 1, name: 'unison', strength: 1.0 },
      { ratio: 2, name: 'octave', strength: 0.9 },
      { ratio: 1.5, name: 'fifth', strength: 0.8 },
      { ratio: 1.333, name: 'fourth', strength: 0.7 },
      { ratio: 1.25, name: 'major third', strength: 0.6 },
      { ratio: 1.618, name: 'phi', strength: 0.75 } // Golden ratio
    ];
    
    let bestResonance = 0;
    for (const { ratio, strength } of ratios) {
      const diff = Math.abs(freqRatio - ratio);
      if (diff < 0.05) { // Within 5% of harmonic ratio
        bestResonance = Math.max(bestResonance, strength * (1 - diff));
      }
    }
    
    return bestResonance;
  }
  
  // ============================================
  // WAVE PROPAGATION (the execution engine)
  // ============================================
  
  async propagate(sourceNodeId, amplitude = 1.0, duration = 1000) {
    /**
     * Propagate wave from source
     * This is a CONTINUOUS PROCESS, not discrete events
     * 
     * @param {string} sourceNodeId - Starting oscillator
     * @param {number} amplitude - Initial amplitude (0-1)
     * @param {number} duration - How long to propagate (ms)
     */
    
    const sourceNode = this.nodes.get(sourceNodeId);
    if (!sourceNode) return;
    
    // Set source amplitude
    sourceNode.amplitude = amplitude;
    
    console.log(`🌊 Propagating from ${sourceNodeId} @ ${sourceNode.frequency.toFixed(2)}Hz`);
    
    // Propagate for duration
    const steps = Math.floor(duration / (1000 / this.sampleRate));
    
    for (let step = 0; step < steps; step++) {
      await this._updateWaveField(step);
      await new Promise(resolve => setTimeout(resolve, 1000 / this.sampleRate));
    }
    
    // Decay source
    sourceNode.amplitude *= 0.95;
  }
  
  async _updateWaveField(step) {
    /**
     * Update entire field state (one timestep)
     * This is where the MATH happens!
     */
    
    this.time = step / this.sampleRate;
    
    // Calculate each node's wave contribution
    for (const [nodeId, node] of this.nodes) {
      // Generate wave at current time
      const waveValue = this._generateWave(
        node.amplitude,
        node.frequency,
        node.phase,
        this.time,
        node.waveform
      );
      
      this.fieldState.set(nodeId, waveValue);
    }
    
    // Apply resonance couplings (wave interference)
    for (const edge of this.edges.values()) {
      const sourceValue = this.fieldState.get(edge.from) || 0;
      const targetNode = this.nodes.get(edge.to);
      
      if (!targetNode) continue;
      
      // Transfer energy via resonance
      const transferred = sourceValue 
                        * edge.strength 
                        * edge.harmonicResonance
                        * Math.cos(edge.phaseShift);
      
      // Increase target amplitude
      targetNode.amplitude = Math.min(1.0, targetNode.amplitude + Math.abs(transferred) * 0.01);
      
      // Trigger handler if threshold crossed
      if (targetNode.amplitude > 0.5 && targetNode.handler) {
        targetNode.handler(targetNode.amplitude, {
          sourceFreq: this.nodes.get(edge.from).frequency,
          resonance: edge.harmonicResonance
        });
      }
    }
    
    // Learn resonance patterns
    if (step % 100 === 0) {
      this._learnResonancePatterns();
    }
  }
  
  _generateWave(amplitude, frequency, phase, time, waveform) {
    /**
     * Generate wave value at time t
     * Different waveforms = different characters
     */
    
    const omega = 2 * Math.PI * frequency;
    const arg = omega * time + phase;
    
    switch (waveform) {
      case 'sine':
        return amplitude * Math.sin(arg);
        
      case 'square':
        return amplitude * Math.sign(Math.sin(arg));
        
      case 'sawtooth':
        return amplitude * (2 * (arg / (2 * Math.PI) - Math.floor(arg / (2 * Math.PI) + 0.5)));
        
      case 'triangle':
        const t = (arg / (2 * Math.PI)) % 1;
        return amplitude * (t < 0.5 ? 4 * t - 1 : -4 * t + 3);
        
      default:
        return amplitude * Math.sin(arg);
    }
  }
  
  // ============================================
  // BROADCAST (wave superposition)
  // ============================================
  
  async broadcast(groupName, amplitude = 1.0, duration = 1000) {
    /**
     * Excite all oscillators in a group simultaneously
     * Creates SUPERPOSITION of waves → interference patterns
     */
    
    const nodeIds = Array.from(this.nodes.values())
      .filter(n => n.groups.includes(groupName))
      .map(n => n.id);
    
    if (nodeIds.length === 0) {
      console.warn(`Group ${groupName} has no nodes`);
      return;
    }
    
    console.log(`📡 Broadcasting to ${nodeIds.length} oscillators in ${groupName}`);
    
    // Excite all simultaneously
    for (const nodeId of nodeIds) {
      const node = this.nodes.get(nodeId);
      node.amplitude = amplitude;
      node.phase = Math.random() * Math.PI * 2; // Random phase = complex interference
    }
    
    // Let them interfere
    await this._updateWaveField(0);
    
    return nodeIds;
  }
  
  // ============================================
  // SELF-EVOLUTION (resonance learning)
  // ============================================
  
  _learnResonancePatterns() {
    /**
     * Observe which frequencies resonate together
     * Propose new edges when resonance is detected
     */
    
    // Find nodes with high simultaneous amplitude
    const activeNodes = Array.from(this.nodes.values())
      .filter(n => n.amplitude > 0.3);
    
    // Check pairs for resonance
    for (let i = 0; i < activeNodes.length; i++) {
      for (let j = i + 1; j < activeNodes.length; j++) {
        const nodeA = activeNodes[i];
        const nodeB = activeNodes[j];
        
        // Calculate frequency ratio
        const freqRatio = nodeB.frequency / nodeA.frequency;
        const resonance = this._calculateHarmonicResonance(freqRatio);
        
        // If strong resonance detected
        if (resonance > 0.6) {
          // Check if edge already exists
          const edgeExists = Array.from(this.edges.values()).some(
            e => (e.from === nodeA.id && e.to === nodeB.id) ||
                 (e.from === nodeB.id && e.to === nodeA.id)
          );
          
          if (!edgeExists) {
            this.proposedResonances.push({
              from: nodeA.id,
              to: nodeB.id,
              resonance: resonance,
              freqRatio: freqRatio,
              reason: `Frequencies ${nodeA.frequency.toFixed(1)}Hz and ${nodeB.frequency.toFixed(1)}Hz resonate harmonically (ratio: ${freqRatio.toFixed(2)})`
            });
            
            console.log(`💡 Discovered resonance: ${nodeA.id} ↔ ${nodeB.id} (${resonance.toFixed(2)})`);
          }
        }
      }
    }
  }
  
  getProposedResonances() {
    return this.proposedResonances.filter(r => r.resonance > 0.7);
  }
  
  approveResonance(index) {
    const proposed = this.proposedResonances[index];
    if (!proposed) return;
    
    this.registerResonanceEdge(`evolved_resonance_${Date.now()}`, {
      from: proposed.from,
      to: proposed.to,
      strength: proposed.resonance,
      bidirectional: true
    });
    
    this.proposedResonances.splice(index, 1);
    
    console.log(`🧬 System evolved! New resonance coupling added`);
  }
  
  // ============================================
  // ANALYSIS & VISUALIZATION
  // ============================================
  
  analyzeFieldCoherence() {
    /**
     * Measure how coherent the field is
     * High coherence = waves aligned, low = chaotic
     */
    
    let totalAmplitude = 0;
    let maxAmplitude = 0;
    
    for (const amplitude of this.fieldState.values()) {
      totalAmplitude += Math.abs(amplitude);
      maxAmplitude = Math.max(maxAmplitude, Math.abs(amplitude));
    }
    
    const avgAmplitude = totalAmplitude / this.nodes.size;
    const coherence = avgAmplitude / (maxAmplitude || 1);
    
    return {
      coherence: coherence,
      avgAmplitude: avgAmplitude,
      maxAmplitude: maxAmplitude,
      activeNodes: Array.from(this.nodes.values()).filter(n => n.amplitude > 0.1).length
    };
  }
  
  getFrequencySpectrum() {
    /**
     * Get power spectrum of current field
     */
    
    const spectrum = {};
    
    for (const node of this.nodes.values()) {
      const freq = Math.round(node.frequency);
      spectrum[freq] = (spectrum[freq] || 0) + node.amplitude;
    }
    
    return spectrum;
  }
  
  visualizeState() {
    /**
     * Get visualization-ready state
     */
    
    return {
      nodes: Array.from(this.nodes.values()).map(n => ({
        id: n.id,
        gate: n.gate,
        line: n.line,
        field: n.field,
        frequency: n.frequency,
        amplitude: n.amplitude,
        phase: n.phase,
        groups: n.groups
      })),
      edges: Array.from(this.edges.values()).map(e => ({
        from: e.from,
        to: e.to,
        strength: e.strength,
        resonance: e.harmonicResonance
      })),
      coherence: this.analyzeFieldCoherence(),
      spectrum: this.getFrequencySpectrum()
    };
  }
  
  // ============================================
  // REAL-WORLD INTEGRATION
  // ============================================
  
  setupAll64Gates() {
    /**
     * Create all 64 HD gates as wave oscillators
     */
    
    for (let gate = 1; gate <= 64; gate++) {
      for (let line = 1; line <= 6; line++) {
        this.registerNode(`gate_${gate}_line_${line}`, {
          gate: gate,
          line: line,
          color: 3, // Default
          tone: 3,  // Default
          field: 'Mind', // Can be configured per gate
          groups: ['all_64_gates', `gate_${gate}`, `line_${line}`],
          waveform: 'sine'
        });
      }
    }
    
    console.log('✓ Created 384 wave oscillators (64 gates × 6 lines)');
  }
  
  connectHarmonicGates() {
    /**
     * Auto-connect gates that are harmonically related
     */
    
    const gates = Array.from(this.nodes.values());
    
    for (let i = 0; i < gates.length; i++) {
      for (let j = i + 1; j < gates.length; j++) {
        const freqRatio = gates[j].frequency / gates[i].frequency;
        const resonance = this._calculateHarmonicResonance(freqRatio);
        
        if (resonance > 0.7) {
          this.registerResonanceEdge(`harmonic_${i}_${j}`, {
            from: gates[i].id,
            to: gates[j].id,
            strength: resonance,
            bidirectional: true
          });
        }
      }
    }
    
    console.log(`✓ Connected ${this.edges.size} harmonic gate pairs`);
  }
}

// Export
if (typeof window !== 'undefined') {
  window.WaveResonanceCausalGraph = WaveResonanceCausalGraph;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = WaveResonanceCausalGraph;
}
