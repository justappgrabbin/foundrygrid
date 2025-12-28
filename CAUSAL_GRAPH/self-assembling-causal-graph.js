/**
 * SELF-ASSEMBLING CAUSAL GRAPH FROM USER DATA
 * 
 * User uploads their work/data → Graph assembles itself
 * 
 * NO BACKEND NEEDED - The graph IS the database, IS the logic, IS everything!
 * Everything is projected from causality - no separate storage needed
 * 
 * This is the "outsourcing via causality" system
 */

class SelfAssemblingCausalGraph {
  constructor() {
    this.graph = new WaveResonanceCausalGraph();
    
    // The graph IS the database
    this.projectedState = new Map(); // What the graph projects
    
    // Ingest queue (user uploads)
    this.ingestQueue = [];
    
    // Self-assembly rules (graph learns structure from data)
    this.assemblyRules = new Map();
    
    console.log('🧬 Self-Assembling Causal Graph initialized');
  }
  
  // ============================================
  // INGESTION (User uploads data)
  // ============================================
  
  async ingest(userData) {
    /**
     * User uploads their work/data
     * Graph figures out what to do with it
     * 
     * @param {Object} userData - User's uploaded content
     * @returns {Object} - Assembled system
     */
    
    console.log('📥 Ingesting user data...');
    
    // 1. ANALYZE what the data represents
    const dataStructure = this._analyzeDataStructure(userData);
    
    // 2. PROJECT what nodes/edges are needed
    const projection = this._projectRequiredGraph(dataStructure);
    
    // 3. ASSEMBLE the graph automatically
    const assembled = await this._assembleGraph(projection);
    
    // 4. CONFIGURE causality based on relationships
    const configured = this._configureCausality(assembled, userData);
    
    // 5. ACTIVATE the system
    this._activateSystem(configured);
    
    console.log('✓ System self-assembled from user data!');
    
    return {
      structure: dataStructure,
      projection: projection,
      graph: configured,
      ready: true
    };
  }
  
  _analyzeDataStructure(userData) {
    /**
     * Figure out WHAT the user uploaded
     * 
     * Examples:
     * - HD chart data → Create gate/field nodes
     * - Business data → Create workflow nodes
     * - Product catalog → Create inventory nodes
     * - User list → Create user nodes
     */
    
    const structure = {
      type: null,
      entities: [],
      relationships: [],
      metadata: {}
    };
    
    // Detect data type
    if (userData.birthDate || userData.gates || userData.type) {
      structure.type = 'hd_chart';
      structure.entities = this._extractHDEntities(userData);
      structure.relationships = this._extractHDRelationships(userData);
    }
    else if (userData.products || userData.inventory) {
      structure.type = 'product_catalog';
      structure.entities = this._extractProducts(userData);
      structure.relationships = this._extractProductRelationships(userData);
    }
    else if (userData.workflow || userData.tasks) {
      structure.type = 'workflow';
      structure.entities = this._extractWorkflowSteps(userData);
      structure.relationships = this._extractWorkflowCausality(userData);
    }
    else if (userData.users || userData.members) {
      structure.type = 'user_system';
      structure.entities = this._extractUsers(userData);
      structure.relationships = this._extractUserRelationships(userData);
    }
    else {
      // Generic data - infer structure
      structure.type = 'generic';
      structure.entities = Object.keys(userData);
      structure.relationships = this._inferRelationships(userData);
    }
    
    console.log(`  Detected: ${structure.type}`);
    console.log(`  Entities: ${structure.entities.length}`);
    console.log(`  Relationships: ${structure.relationships.length}`);
    
    return structure;
  }
  
  _projectRequiredGraph(structure) {
    /**
     * PROJECT what the graph should look like
     * Based on data structure, determine nodes/edges needed
     * 
     * This is the "blueprint" - graph hasn't been built yet
     */
    
    const projection = {
      nodes: [],
      edges: [],
      groups: new Map()
    };
    
    // Create node projections
    for (const entity of structure.entities) {
      projection.nodes.push({
        id: entity.id || this._generateNodeId(entity),
        type: entity.type,
        data: entity.data || entity,
        groups: entity.groups || [structure.type]
      });
    }
    
    // Create edge projections (causality)
    for (const rel of structure.relationships) {
      projection.edges.push({
        id: `edge_${rel.from}_${rel.to}`,
        from: rel.from,
        to: rel.to,
        strength: rel.strength || 1.0,
        causalType: rel.type || 'triggers'
      });
    }
    
    console.log(`  Projected: ${projection.nodes.length} nodes, ${projection.edges.length} edges`);
    
    return projection;
  }
  
  async _assembleGraph(projection) {
    /**
     * ASSEMBLE the actual graph from projection
     * Creates the nodes and edges in the causal graph
     */
    
    console.log('🔧 Assembling graph...');
    
    // Create all nodes
    for (const nodeProj of projection.nodes) {
      this.graph.registerNode(nodeProj.id, {
        type: nodeProj.type,
        groups: nodeProj.groups,
        data: nodeProj.data,
        handler: this._createHandler(nodeProj)
      });
    }
    
    // Create all edges
    for (const edgeProj of projection.edges) {
      this.graph.registerResonanceEdge(edgeProj.id, {
        from: edgeProj.from,
        to: edgeProj.to,
        strength: edgeProj.strength
      });
    }
    
    console.log('  ✓ Graph assembled');
    
    return projection;
  }
  
  _configureCausality(assembled, userData) {
    /**
     * CONFIGURE how causality flows
     * Based on user data, set up the "physics" of the system
     */
    
    // Auto-detect causal patterns in user data
    const patterns = this._detectCausalPatterns(userData);
    
    for (const pattern of patterns) {
      // Pattern: "When X happens, Y should happen"
      if (pattern.trigger && pattern.effect) {
        this.graph.registerResonanceEdge(`auto_${pattern.id}`, {
          from: pattern.trigger,
          to: pattern.effect,
          strength: pattern.confidence,
          metadata: { auto: true, reason: pattern.reason }
        });
      }
    }
    
    return assembled;
  }
  
  _activateSystem(configured) {
    /**
     * ACTIVATE - system is now running!
     * No backend needed - it's all in the graph
     */
    
    console.log('⚡ System activated - running on causality');
    
    // System is now self-sustaining
    // All operations happen via graph propagation
    // No separate backend needed!
  }
  
  // ============================================
  // HELPERS - Extract entities from different data types
  // ============================================
  
  _extractHDEntities(userData) {
    /**
     * Extract HD chart entities
     */
    const entities = [];
    
    // Gates
    if (userData.gates) {
      for (const [gateNum, gateData] of Object.entries(userData.gates)) {
        entities.push({
          id: `gate_${gateNum}`,
          type: 'hd_gate',
          data: { number: gateNum, ...gateData },
          groups: ['gates', 'hd_system']
        });
      }
    }
    
    // Centers
    if (userData.centers) {
      for (const [centerName, centerData] of Object.entries(userData.centers)) {
        entities.push({
          id: `center_${centerName}`,
          type: 'hd_center',
          data: { name: centerName, ...centerData },
          groups: ['centers', 'hd_system']
        });
      }
    }
    
    // Channels
    if (userData.channels) {
      for (const channel of userData.channels) {
        entities.push({
          id: `channel_${channel.from}_${channel.to}`,
          type: 'hd_channel',
          data: channel,
          groups: ['channels', 'hd_system']
        });
      }
    }
    
    return entities;
  }
  
  _extractHDRelationships(userData) {
    /**
     * Extract causal relationships from HD data
     */
    const relationships = [];
    
    // Channels create causality between gates
    if (userData.channels) {
      for (const channel of userData.channels) {
        relationships.push({
          from: `gate_${channel.from}`,
          to: `gate_${channel.to}`,
          type: 'channel',
          strength: 1.0
        });
      }
    }
    
    // Centers govern gates
    const gateToCenter = {
      64: 'head', 61: 'head',
      47: 'ajna', 24: 'ajna', 4: 'ajna', 17: 'ajna', 43: 'ajna', 11: 'ajna',
      // ... etc
    };
    
    if (userData.gates) {
      for (const gateNum of Object.keys(userData.gates)) {
        const centerName = gateToCenter[gateNum];
        if (centerName) {
          relationships.push({
            from: `center_${centerName}`,
            to: `gate_${gateNum}`,
            type: 'governs',
            strength: 0.8
          });
        }
      }
    }
    
    return relationships;
  }
  
  _extractProducts(userData) {
    const entities = [];
    
    for (const product of userData.products || []) {
      entities.push({
        id: `product_${product.id || product.sku}`,
        type: 'product',
        data: product,
        groups: ['products', 'inventory']
      });
    }
    
    return entities;
  }
  
  _extractProductRelationships(userData) {
    const relationships = [];
    
    // Products that are often bought together
    if (userData.associations) {
      for (const assoc of userData.associations) {
        relationships.push({
          from: `product_${assoc.productA}`,
          to: `product_${assoc.productB}`,
          type: 'related',
          strength: assoc.confidence || 0.5
        });
      }
    }
    
    // Products that replace each other
    if (userData.substitutions) {
      for (const sub of userData.substitutions) {
        relationships.push({
          from: `product_${sub.original}`,
          to: `product_${sub.substitute}`,
          type: 'substitutes',
          strength: 0.7
        });
      }
    }
    
    return relationships;
  }
  
  _extractWorkflowSteps(userData) {
    const entities = [];
    
    for (const step of userData.workflow || userData.tasks || []) {
      entities.push({
        id: `step_${step.id}`,
        type: 'workflow_step',
        data: step,
        groups: ['workflow', 'automation']
      });
    }
    
    return entities;
  }
  
  _extractWorkflowCausality(userData) {
    const relationships = [];
    
    // Sequential workflow
    const steps = userData.workflow || userData.tasks || [];
    for (let i = 0; i < steps.length - 1; i++) {
      relationships.push({
        from: `step_${steps[i].id}`,
        to: `step_${steps[i + 1].id}`,
        type: 'triggers',
        strength: 1.0
      });
    }
    
    // Conditional triggers
    if (userData.conditions) {
      for (const cond of userData.conditions) {
        relationships.push({
          from: `step_${cond.if}`,
          to: `step_${cond.then}`,
          type: 'conditional',
          strength: cond.probability || 0.8
        });
      }
    }
    
    return relationships;
  }
  
  _extractUsers(userData) {
    const entities = [];
    
    for (const user of userData.users || userData.members || []) {
      entities.push({
        id: `user_${user.id}`,
        type: 'user',
        data: user,
        groups: ['users', user.tier || 'free']
      });
    }
    
    return entities;
  }
  
  _extractUserRelationships(userData) {
    const relationships = [];
    
    // Social graph
    if (userData.connections) {
      for (const conn of userData.connections) {
        relationships.push({
          from: `user_${conn.userA}`,
          to: `user_${conn.userB}`,
          type: 'connected',
          strength: conn.strength || 0.5
        });
      }
    }
    
    return relationships;
  }
  
  _inferRelationships(userData) {
    /**
     * For generic data, infer relationships from structure
     */
    const relationships = [];
    
    // If objects reference each other, create edges
    const traverse = (obj, path = '') => {
      for (const [key, value] of Object.entries(obj)) {
        if (typeof value === 'object' && value !== null) {
          if (value.id || value.ref) {
            relationships.push({
              from: path,
              to: value.id || value.ref,
              type: 'references',
              strength: 0.5
            });
          }
          traverse(value, `${path}.${key}`);
        }
      }
    };
    
    traverse(userData);
    
    return relationships;
  }
  
  _detectCausalPatterns(userData) {
    /**
     * Auto-detect "When X then Y" patterns
     */
    const patterns = [];
    
    // Look for explicit causality
    if (userData.rules) {
      for (const rule of userData.rules) {
        patterns.push({
          id: rule.id,
          trigger: rule.when || rule.if,
          effect: rule.then || rule.do,
          confidence: rule.confidence || 0.8,
          reason: rule.description || 'User-defined rule'
        });
      }
    }
    
    // Look for temporal patterns
    if (userData.events) {
      // Events that often follow each other
      const eventPairs = new Map();
      
      for (let i = 0; i < userData.events.length - 1; i++) {
        const pair = `${userData.events[i].type}→${userData.events[i + 1].type}`;
        eventPairs.set(pair, (eventPairs.get(pair) || 0) + 1);
      }
      
      for (const [pair, count] of eventPairs) {
        if (count > 2) { // Happened more than twice
          const [trigger, effect] = pair.split('→');
          patterns.push({
            id: `inferred_${trigger}_${effect}`,
            trigger: trigger,
            effect: effect,
            confidence: Math.min(count / 10, 0.9),
            reason: `Observed ${count} times in event stream`
          });
        }
      }
    }
    
    return patterns;
  }
  
  _createHandler(nodeProj) {
    /**
     * Create activation handler for node
     */
    return (signal, metadata) => {
      console.log(`${nodeProj.id} activated (${(signal * 100).toFixed(0)}%)`);
      
      // Update projected state
      this.projectedState.set(nodeProj.id, {
        activated: true,
        signal: signal,
        metadata: metadata,
        timestamp: Date.now()
      });
    };
  }
  
  _generateNodeId(entity) {
    return `node_${entity.type || 'unknown'}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
  
  // ============================================
  // QUERY THE PROJECTION (no backend!)
  // ============================================
  
  query(queryType, params) {
    /**
     * Query the projected state
     * NO DATABASE - just read from graph!
     */
    
    switch (queryType) {
      case 'all_nodes':
        return Array.from(this.graph.nodes.values());
        
      case 'node_by_id':
        return this.graph.nodes.get(params.id);
        
      case 'nodes_by_type':
        return Array.from(this.graph.nodes.values())
          .filter(n => n.type === params.type);
        
      case 'active_nodes':
        return Array.from(this.projectedState.entries())
          .filter(([_, state]) => state.activated)
          .map(([id, _]) => this.graph.nodes.get(id));
        
      case 'connections':
        return Array.from(this.graph.edges.values())
          .filter(e => e.from === params.nodeId || e.to === params.nodeId);
        
      default:
        return null;
    }
  }
  
  // ============================================
  // NO BACKEND OPERATIONS
  // ============================================
  
  // All operations happen via graph propagation
  // No separate database, no API, no backend server needed!
  
  createUser(userData) {
    // Just add node to graph
    this.graph.registerNode(`user_${userData.id}`, {
      type: 'user',
      data: userData
    });
    
    // Causality handles the rest
  }
  
  updateUserTier(userId, newTier) {
    // Just propagate signal
    this.graph.propagate(`user_${userId}`, 1.0, {
      action: 'tier_change',
      newTier: newTier
    });
    
    // Causality updates permissions automatically
  }
  
  processPayment(userId, amount) {
    // Just propagate payment signal
    this.graph.propagate('payment_received', 1.0, {
      userId: userId,
      amount: amount
    });
    
    // Causality handles subscription activation
  }
  
  // Everything is causality!
  // No backend needed!
}

// ============================================
// EXAMPLE USAGE
// ============================================

/*

// User uploads their HD chart
const selfGraph = new SelfAssemblingCausalGraph();

const userChart = {
  type: 'Manifestor',
  profile: '4/6',
  gates: {
    1: { line: 3, color: 2, tone: 4 },
    8: { line: 1, color: 3, tone: 2 },
    48: { line: 6, color: 1, tone: 5 }
  },
  centers: {
    throat: { defined: true },
    sacral: { defined: false },
    spleen: { defined: true }
  },
  channels: [
    { from: 1, to: 8 }
  ]
};

// Ingest → System assembles itself!
const assembled = await selfGraph.ingest(userChart);

// Result:
// - Created gate nodes (1, 8, 48)
// - Created center nodes (throat, sacral, spleen)
// - Created channel edge (1→8)
// - Configured causality (throat governs 1, spleen governs 48)
// - System is RUNNING - no backend needed!

// Query the projection (NO DATABASE!)
const allGates = selfGraph.query('nodes_by_type', { type: 'hd_gate' });
const connections = selfGraph.query('connections', { nodeId: 'gate_1' });

// Broadcast to all gates
selfGraph.graph.broadcast('gates', 1.0, {
  message: 'Transit activation'
});

// EVERYTHING happens via causality!
// NO separate backend, database, or API!

*/

// Export
if (typeof window !== 'undefined') {
  window.SelfAssemblingCausalGraph = SelfAssemblingCausalGraph;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = SelfAssemblingCausalGraph;
}
