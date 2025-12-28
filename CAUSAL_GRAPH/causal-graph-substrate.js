/**
 * SELF-EVOLVING CAUSAL GRAPH SUBSTRATE
 * 
 * The app doesn't just USE a causal graph - it RUNS ON causality
 * 
 * Features:
 * 1. Apps execute by propagating messages through causal network
 * 2. Self-evolution: System learns new causal edges from user behavior
 * 3. Broadcast: Send signals to all 48 nodes (users/fields/states)
 * 4. Billing/subscription management via causal triggers
 * 5. No hardcoded logic - pure causality-based execution
 */

class CausalGraphSubstrate {
  constructor() {
    // THE GRAPH
    this.nodes = new Map();        // id → { type, data, handlers }
    this.edges = new Map();        // id → { from, to, causalStrength, conditions }
    
    // EXECUTION STATE
    this.activations = new Map();  // nodeId → activation level (0-1)
    this.messageQueue = [];        // Pending causal messages
    this.evolutionHistory = [];    // Track what causes what over time
    
    // SELF-EVOLUTION
    this.observedPatterns = new Map();  // pattern → frequency
    this.proposedEdges = [];            // Edges system wants to add
    
    // BROADCAST REGISTRY
    this.nodeGroups = new Map();   // groupName → Set of nodeIds
    
    console.log('🧬 Causal Graph Substrate initialized');
  }
  
  // ============================================
  // NODE MANAGEMENT
  // ============================================
  
  registerNode(id, config) {
    /**
     * Register a node in the causal network
     * 
     * Nodes can be:
     * - Users (user_123)
     * - HD Gates (gate_48)
     * - App states (billing_active)
     * - Consciousness fields (mind_field)
     * - Anything that can cause or receive effects
     */
    
    this.nodes.set(id, {
      id: id,
      type: config.type || 'generic',
      data: config.data || {},
      handlers: config.handlers || {},
      activation: 0,
      lastFired: null,
      metadata: config.metadata || {}
    });
    
    // Add to groups if specified
    if (config.groups) {
      for (const group of config.groups) {
        if (!this.nodeGroups.has(group)) {
          this.nodeGroups.set(group, new Set());
        }
        this.nodeGroups.get(group).add(id);
      }
    }
    
    console.log(`✓ Registered node: ${id} (${config.type})`);
  }
  
  // ============================================
  // CAUSAL EDGE REGISTRATION
  // ============================================
  
  registerCausalEdge(id, config) {
    /**
     * Register a causal relationship
     * 
     * Example:
     *   "gate_48_active" → "inadequacy_loop" (strength: 0.8)
     *   "user_paid" → "premium_features" (strength: 1.0)
     *   "mind_field_activated" → "heart_response" (strength: 0.6)
     */
    
    this.edges.set(id, {
      id: id,
      from: config.from,           // Source node
      to: config.to,               // Target node
      strength: config.strength || 1.0,   // 0-1, how strong the causal link
      delay: config.delay || 0,    // Propagation delay (ms)
      conditions: config.conditions || null,  // When does this edge fire?
      transform: config.transform || null,    // How to transform the signal
      bidirectional: config.bidirectional || false,
      metadata: config.metadata || {}
    });
    
    console.log(`→ Causal edge: ${config.from} → ${config.to} (${config.strength})`);
  }
  
  // ============================================
  // MESSAGE PROPAGATION (EXECUTION ENGINE)
  // ============================================
  
  async propagate(sourceNodeId, signal = 1.0, metadata = {}) {
    /**
     * THIS IS HOW THE APP EXECUTES
     * 
     * Instead of calling functions, you send signals through causality
     * 
     * Example:
     *   propagate('user_clicked_button', 1.0)
     *   → Causes 'gate_48_activated'
     *   → Causes 'inadequacy_pattern_triggered'
     *   → Causes 'response_generated'
     *   → User sees result
     */
    
    const propagationId = `prop_${Date.now()}_${Math.random()}`;
    
    // Queue initial message
    this.messageQueue.push({
      id: propagationId,
      from: null,
      to: sourceNodeId,
      signal: signal,
      metadata: metadata,
      timestamp: Date.now(),
      path: [sourceNodeId]
    });
    
    // Process queue (breadth-first propagation)
    const visited = new Set();
    const results = [];
    
    while (this.messageQueue.length > 0) {
      const msg = this.messageQueue.shift();
      
      // Skip if already visited (prevent loops)
      const visitKey = `${msg.to}_${propagationId}`;
      if (visited.has(visitKey)) continue;
      visited.add(visitKey);
      
      // Activate node
      const result = await this._activateNode(msg.to, msg.signal, msg.metadata);
      results.push(result);
      
      // Find outgoing edges
      const outgoingEdges = this._findOutgoingEdges(msg.to);
      
      // Propagate to connected nodes
      for (const edge of outgoingEdges) {
        // Check conditions
        if (edge.conditions && !this._evaluateConditions(edge.conditions, msg)) {
          continue;
        }
        
        // Transform signal
        let newSignal = msg.signal * edge.strength;
        if (edge.transform) {
          newSignal = edge.transform(newSignal, msg.metadata);
        }
        
        // Queue message to target
        setTimeout(() => {
          this.messageQueue.push({
            id: propagationId,
            from: msg.to,
            to: edge.to,
            signal: newSignal,
            metadata: { ...msg.metadata, edge: edge.id },
            timestamp: Date.now(),
            path: [...msg.path, edge.to]
          });
        }, edge.delay);
      }
    }
    
    // Learn from this propagation
    this._learnPattern(sourceNodeId, results);
    
    return {
      propagationId: propagationId,
      activatedNodes: results.map(r => r.nodeId),
      finalStates: results
    };
  }
  
  async _activateNode(nodeId, signal, metadata) {
    /**
     * Activate a node (execute its handler)
     */
    
    const node = this.nodes.get(nodeId);
    if (!node) {
      console.warn(`Node ${nodeId} not found`);
      return null;
    }
    
    // Update activation
    node.activation = Math.min(1.0, node.activation + signal);
    node.lastFired = Date.now();
    
    // Execute handlers
    const handlerResults = {};
    for (const [handlerName, handler] of Object.entries(node.handlers)) {
      try {
        handlerResults[handlerName] = await handler(signal, metadata, node);
      } catch (error) {
        console.error(`Handler ${handlerName} failed:`, error);
      }
    }
    
    return {
      nodeId: nodeId,
      activation: node.activation,
      handlerResults: handlerResults,
      timestamp: Date.now()
    };
  }
  
  _findOutgoingEdges(nodeId) {
    /**
     * Find all edges FROM this node
     */
    const outgoing = [];
    
    for (const edge of this.edges.values()) {
      if (edge.from === nodeId) {
        outgoing.push(edge);
      }
      if (edge.bidirectional && edge.to === nodeId) {
        // Create reverse edge
        outgoing.push({
          ...edge,
          from: edge.to,
          to: edge.from
        });
      }
    }
    
    return outgoing;
  }
  
  _evaluateConditions(conditions, message) {
    /**
     * Evaluate if edge should fire
     */
    if (typeof conditions === 'function') {
      return conditions(message);
    }
    
    // Simple key-value matching
    for (const [key, value] of Object.entries(conditions)) {
      if (message.metadata[key] !== value) {
        return false;
      }
    }
    
    return true;
  }
  
  // ============================================
  // BROADCAST TO NODE GROUPS
  // ============================================
  
  async broadcast(groupName, signal = 1.0, metadata = {}) {
    /**
     * Send signal to ALL nodes in a group
     * 
     * Examples:
     *   broadcast('premium_users', 0.5, { message: 'Payment failed' })
     *   broadcast('all_gates', 1.0, { transit: 'saturn_square' })
     *   broadcast('mind_field_components', 0.8)
     */
    
    const group = this.nodeGroups.get(groupName);
    if (!group) {
      console.warn(`Group ${groupName} not found`);
      return [];
    }
    
    console.log(`📡 Broadcasting to ${group.size} nodes in ${groupName}`);
    
    const results = [];
    for (const nodeId of group) {
      const result = await this.propagate(nodeId, signal, {
        ...metadata,
        broadcast: groupName
      });
      results.push(result);
    }
    
    return results;
  }
  
  // ============================================
  // SELF-EVOLUTION
  // ============================================
  
  _learnPattern(sourceNode, results) {
    /**
     * Observe causal patterns and propose new edges
     * 
     * If A often causes B, suggest adding A → B edge
     */
    
    for (const result of results) {
      if (!result) continue;
      
      const pattern = `${sourceNode}→${result.nodeId}`;
      
      // Track frequency
      if (!this.observedPatterns.has(pattern)) {
        this.observedPatterns.set(pattern, { count: 0, strength: [] });
      }
      
      const observed = this.observedPatterns.get(pattern);
      observed.count++;
      observed.strength.push(result.activation);
      
      // Propose edge if pattern is strong
      if (observed.count > 5) {
        const avgStrength = observed.strength.reduce((a,b) => a+b, 0) / observed.strength.length;
        
        // Check if edge already exists
        const edgeExists = Array.from(this.edges.values()).some(
          e => e.from === sourceNode && e.to === result.nodeId
        );
        
        if (!edgeExists && avgStrength > 0.3) {
          this.proposedEdges.push({
            from: sourceNode,
            to: result.nodeId,
            strength: avgStrength,
            confidence: observed.count / 10,
            reason: `Observed ${observed.count} times with avg strength ${avgStrength.toFixed(2)}`
          });
          
          console.log(`💡 Proposed edge: ${sourceNode} → ${result.nodeId} (${avgStrength.toFixed(2)})`);
        }
      }
    }
  }
  
  getProposedEvolutions() {
    /**
     * Get suggestions for new causal edges
     * User can approve these to evolve the system
     */
    return this.proposedEdges.filter(e => e.confidence > 0.5);
  }
  
  approveEvolution(edgeIndex) {
    /**
     * User approves a proposed edge - system evolves!
     */
    const proposed = this.proposedEdges[edgeIndex];
    if (!proposed) return;
    
    const edgeId = `evolved_${Date.now()}`;
    this.registerCausalEdge(edgeId, {
      from: proposed.from,
      to: proposed.to,
      strength: proposed.strength,
      metadata: {
        evolved: true,
        confidence: proposed.confidence,
        reason: proposed.reason
      }
    });
    
    // Remove from proposals
    this.proposedEdges.splice(edgeIndex, 1);
    
    // Record evolution event
    this.evolutionHistory.push({
      timestamp: Date.now(),
      type: 'edge_added',
      edge: edgeId,
      reason: proposed.reason
    });
    
    console.log(`🧬 System evolved! New edge: ${proposed.from} → ${proposed.to}`);
  }
  
  // ============================================
  // SPECIAL USE CASES
  // ============================================
  
  setupBillingCausality() {
    /**
     * Example: Billing system via causality
     */
    
    // Register billing nodes
    this.registerNode('payment_received', {
      type: 'billing_event',
      groups: ['billing_events']
    });
    
    this.registerNode('subscription_active', {
      type: 'billing_state',
      data: { status: 'inactive' },
      handlers: {
        activate: (signal, metadata, node) => {
          node.data.status = 'active';
          console.log(`✓ Subscription activated for ${metadata.userId}`);
        }
      }
    });
    
    this.registerNode('premium_features', {
      type: 'feature_gate',
      handlers: {
        unlock: (signal, metadata, node) => {
          console.log(`🔓 Premium features unlocked for ${metadata.userId}`);
          return { unlocked: true };
        }
      }
    });
    
    // Causal edges
    this.registerCausalEdge('payment_causes_activation', {
      from: 'payment_received',
      to: 'subscription_active',
      strength: 1.0
    });
    
    this.registerCausalEdge('activation_unlocks_premium', {
      from: 'subscription_active',
      to: 'premium_features',
      strength: 1.0,
      conditions: (msg) => msg.metadata.paymentValid === true
    });
    
    console.log('✓ Billing causality configured');
  }
  
  setupHDGateCausality() {
    /**
     * Example: All 64 Human Design gates as causal nodes
     */
    
    // Register all 64 gates
    for (let gateNum = 1; gateNum <= 64; gateNum++) {
      this.registerNode(`gate_${gateNum}`, {
        type: 'hd_gate',
        groups: ['all_64_gates', 'hd_system'],
        data: { 
          number: gateNum, 
          active: false 
        },
        handlers: {
          activate: (signal, metadata, node) => {
            node.data.active = true;
            console.log(`🌊 Gate ${gateNum} activated (signal: ${signal.toFixed(2)})`);
          }
        }
      });
    }
    
    // Example causal edges between gates
    this.registerCausalEdge('gate48_to_16', {
      from: 'gate_48',
      to: 'gate_16',
      strength: 0.8,
      metadata: { theme: 'depth_to_skill' }
    });
    
    this.registerCausalEdge('gate16_to_9', {
      from: 'gate_16',
      to: 'gate_9',
      strength: 0.7,
      metadata: { theme: 'skill_to_focus' }
    });
    
    console.log('✓ All 64 HD Gates registered as causal nodes');
  }
  
  setupAll64GatesBroadcast() {
    /**
     * Broadcast to ALL 64 gates at once
     * Use case: Transit activation, field resonance, etc.
     */
    
    return this.broadcast('all_64_gates', 1.0, {
      type: 'transit_activation',
      timestamp: Date.now()
    });
  }
  
  // ============================================
  // UTILITIES
  // ============================================
  
  visualize() {
    /**
     * Generate graph visualization data
     */
    return {
      nodes: Array.from(this.nodes.values()).map(n => ({
        id: n.id,
        type: n.type,
        activation: n.activation,
        groups: Array.from(this.nodeGroups.entries())
          .filter(([_, nodes]) => nodes.has(n.id))
          .map(([name]) => name)
      })),
      edges: Array.from(this.edges.values()).map(e => ({
        from: e.from,
        to: e.to,
        strength: e.strength
      }))
    };
  }
  
  exportState() {
    return {
      nodes: Array.from(this.nodes.entries()),
      edges: Array.from(this.edges.entries()),
      groups: Array.from(this.nodeGroups.entries()).map(([k,v]) => [k, Array.from(v)]),
      evolution: this.evolutionHistory
    };
  }
}

// Make available globally
if (typeof window !== 'undefined') {
  window.CausalGraphSubstrate = CausalGraphSubstrate;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = CausalGraphSubstrate;
}
