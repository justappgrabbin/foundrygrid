/**
 * TIERED DELIVERY SYSTEM via CAUSAL GRAPH
 * 
 * Users in different tiers automatically get different causality
 * The graph itself updates based on subscription level
 * 
 * FREE TIER → Limited causality (basic features only)
 * BASIC TIER → Expanded causality (more features unlock)
 * PREMIUM TIER → Full causality (everything unlocked)
 * ENTERPRISE → Custom causality (unique features)
 */

class TieredCausalGraph {
  constructor() {
    this.graph = new WaveResonanceCausalGraph(); // Or regular CausalGraphSubstrate
    
    // User registry with tiers
    this.users = new Map(); // userId → { tier, nodes, customEdges }
    
    // Tier definitions
    this.tiers = new Map([
      ['free', {
        name: 'Free Tier',
        monthlyPrice: 0,
        features: ['basic_chart', 'daily_guidance'],
        maxGates: 12, // Only 12 gates accessible
        maxFields: 1, // Only 1 field (Mind)
        updateFrequency: 'weekly',
        aiQuota: 10, // 10 AI queries per month
        causality: 'limited'
      }],
      
      ['basic', {
        name: 'Basic Plan',
        monthlyPrice: 9.99,
        features: ['basic_chart', 'daily_guidance', 'transit_alerts', 'compatibility'],
        maxGates: 32, // Half the gates
        maxFields: 2, // Mind + Heart
        updateFrequency: 'daily',
        aiQuota: 100,
        causality: 'standard'
      }],
      
      ['premium', {
        name: 'Premium Plan',
        monthlyPrice: 29.99,
        features: ['all_features', 'advanced_analytics', 'custom_reports', 'priority_support'],
        maxGates: 64, // ALL gates
        maxFields: 9, // ALL fields
        updateFrequency: 'realtime',
        aiQuota: 1000,
        causality: 'full'
      }],
      
      ['enterprise', {
        name: 'Enterprise',
        monthlyPrice: 99.99,
        features: ['everything', 'custom_integration', 'white_label', 'dedicated_support'],
        maxGates: 64,
        maxFields: 9,
        updateFrequency: 'realtime',
        aiQuota: Infinity,
        causality: 'custom'
      }]
    ]);
    
    console.log('🎯 Tiered Causal Graph initialized');
  }
  
  // ============================================
  // USER REGISTRATION
  // ============================================
  
  registerUser(userId, config) {
    /**
     * Register user with tier
     * Creates user-specific causal subgraph
     */
    
    const tier = config.tier || 'free';
    const tierConfig = this.tiers.get(tier);
    
    if (!tierConfig) {
      throw new Error(`Unknown tier: ${tier}`);
    }
    
    // Create user-specific nodes
    const userNodes = this._createUserNodes(userId, tierConfig);
    
    this.users.set(userId, {
      id: userId,
      tier: tier,
      tierConfig: tierConfig,
      nodes: userNodes,
      customEdges: [],
      metadata: config.metadata || {},
      createdAt: Date.now(),
      lastUpdated: Date.now()
    });
    
    console.log(`✓ User ${userId} registered as ${tier} tier`);
  }
  
  _createUserNodes(userId, tierConfig) {
    /**
     * Create nodes based on tier limits
     */
    
    const nodes = [];
    
    // User meta-node
    this.graph.registerNode(`user_${userId}`, {
      type: 'user',
      groups: ['all_users', `${tierConfig.name.toLowerCase()}_users`],
      data: { tier: tierConfig.name },
      handler: (signal, metadata) => {
        console.log(`User ${userId} activated (${tierConfig.name})`);
      }
    });
    nodes.push(`user_${userId}`);
    
    // Gates (limited by tier)
    for (let gate = 1; gate <= tierConfig.maxGates; gate++) {
      const nodeId = `user_${userId}_gate_${gate}`;
      this.graph.registerNode(nodeId, {
        type: 'user_gate',
        gate: gate,
        groups: [`user_${userId}_nodes`],
        handler: (signal, metadata) => {
          console.log(`Gate ${gate} activated for user ${userId}`);
        }
      });
      nodes.push(nodeId);
    }
    
    // Fields (limited by tier)
    const fieldNames = ['Mind', 'Heart', 'Body', 'Shadow', 'Light', 'Neutral', 'Sun', 'Moon', 'Mercury'];
    for (let i = 0; i < tierConfig.maxFields; i++) {
      const fieldName = fieldNames[i];
      const nodeId = `user_${userId}_field_${fieldName}`;
      this.graph.registerNode(nodeId, {
        type: 'user_field',
        field: fieldName,
        groups: [`user_${userId}_nodes`],
        handler: (signal, metadata) => {
          console.log(`${fieldName} field activated for user ${userId}`);
        }
      });
      nodes.push(nodeId);
    }
    
    return nodes;
  }
  
  // ============================================
  // TIER MANAGEMENT
  // ============================================
  
  upgradeTier(userId, newTier) {
    /**
     * Upgrade user to new tier
     * EXPANDS their causal graph automatically
     */
    
    const user = this.users.get(userId);
    if (!user) {
      throw new Error(`User ${userId} not found`);
    }
    
    const oldTierConfig = user.tierConfig;
    const newTierConfig = this.tiers.get(newTier);
    
    if (!newTierConfig) {
      throw new Error(`Unknown tier: ${newTier}`);
    }
    
    console.log(`🔼 Upgrading ${userId} from ${user.tier} → ${newTier}`);
    
    // Add new gates if tier allows more
    if (newTierConfig.maxGates > oldTierConfig.maxGates) {
      for (let gate = oldTierConfig.maxGates + 1; gate <= newTierConfig.maxGates; gate++) {
        const nodeId = `user_${userId}_gate_${gate}`;
        this.graph.registerNode(nodeId, {
          type: 'user_gate',
          gate: gate,
          groups: [`user_${userId}_nodes`],
          handler: (signal) => console.log(`Gate ${gate} unlocked for ${userId}!`)
        });
        user.nodes.push(nodeId);
      }
      console.log(`  ✓ Unlocked ${newTierConfig.maxGates - oldTierConfig.maxGates} additional gates`);
    }
    
    // Add new fields
    if (newTierConfig.maxFields > oldTierConfig.maxFields) {
      const fieldNames = ['Mind', 'Heart', 'Body', 'Shadow', 'Light', 'Neutral', 'Sun', 'Moon', 'Mercury'];
      for (let i = oldTierConfig.maxFields; i < newTierConfig.maxFields; i++) {
        const fieldName = fieldNames[i];
        const nodeId = `user_${userId}_field_${fieldName}`;
        this.graph.registerNode(nodeId, {
          type: 'user_field',
          field: fieldName,
          groups: [`user_${userId}_nodes`],
          handler: (signal) => console.log(`${fieldName} field unlocked for ${userId}!`)
        });
        user.nodes.push(nodeId);
      }
      console.log(`  ✓ Unlocked ${newTierConfig.maxFields - oldTierConfig.maxFields} additional fields`);
    }
    
    // Update user record
    user.tier = newTier;
    user.tierConfig = newTierConfig;
    user.lastUpdated = Date.now();
    
    // Move to new tier group
    const userNode = this.graph.nodes.get(`user_${userId}`);
    if (userNode) {
      userNode.groups = userNode.groups.filter(g => !g.includes('_users'));
      userNode.groups.push(`${newTier}_users`);
    }
    
    // Trigger upgrade event
    this.graph.propagate(`user_${userId}`, 1.0, {
      event: 'tier_upgrade',
      oldTier: oldTierConfig.name,
      newTier: newTierConfig.name
    });
    
    console.log(`✅ Upgrade complete!`);
  }
  
  downgradeTier(userId, newTier) {
    /**
     * Downgrade user (remove access to premium features)
     * CONTRACTS their causal graph
     */
    
    const user = this.users.get(userId);
    if (!user) return;
    
    const newTierConfig = this.tiers.get(newTier);
    
    console.log(`🔽 Downgrading ${userId} to ${newTier}`);
    
    // Remove gates beyond new tier limit
    const gatesToRemove = user.nodes.filter(nodeId => {
      const node = this.graph.nodes.get(nodeId);
      return node && node.type === 'user_gate' && node.gate > newTierConfig.maxGates;
    });
    
    for (const nodeId of gatesToRemove) {
      this.graph.nodes.delete(nodeId);
      user.nodes = user.nodes.filter(n => n !== nodeId);
    }
    
    console.log(`  ✓ Removed ${gatesToRemove.length} gates`);
    
    // Update tier
    user.tier = newTier;
    user.tierConfig = newTierConfig;
  }
  
  // ============================================
  // TIER-BASED BROADCASTING
  // ============================================
  
  broadcastToTier(tierName, signal, metadata) {
    /**
     * Broadcast to ALL users in a specific tier
     * 
     * Example: Send update to all premium users
     */
    
    const groupName = `${tierName}_users`;
    return this.graph.broadcast(groupName, signal, metadata);
  }
  
  broadcastFeature(featureName, signal, metadata) {
    /**
     * Broadcast to users who have access to a feature
     */
    
    const eligibleUsers = Array.from(this.users.values())
      .filter(user => user.tierConfig.features.includes(featureName))
      .map(user => `user_${user.id}`);
    
    console.log(`📡 Broadcasting ${featureName} to ${eligibleUsers.length} users`);
    
    for (const nodeId of eligibleUsers) {
      this.graph.propagate(nodeId, signal, { ...metadata, feature: featureName });
    }
  }
  
  // ============================================
  // BILLING INTEGRATION
  // ============================================
  
  handlePayment(userId, amount, success) {
    /**
     * Payment causes tier changes via causality
     */
    
    if (success) {
      // Payment successful → activate subscription
      this.graph.propagate(`user_${userId}`, 1.0, {
        event: 'payment_success',
        amount: amount
      });
      
      console.log(`✓ Payment processed for ${userId}: $${amount}`);
    } else {
      // Payment failed → trigger downgrade
      this.graph.propagate(`user_${userId}`, 0, {
        event: 'payment_failed',
        amount: amount
      });
      
      // Auto-downgrade after grace period
      setTimeout(() => {
        this.downgradeTier(userId, 'free');
      }, 7 * 24 * 60 * 60 * 1000); // 7 day grace period
      
      console.log(`⚠️ Payment failed for ${userId} - grace period started`);
    }
  }
  
  revokeAccess(userId, reason) {
    /**
     * Immediately revoke premium access
     */
    
    this.graph.propagate(`user_${userId}`, 0, {
      event: 'access_revoked',
      reason: reason
    });
    
    this.downgradeTier(userId, 'free');
    
    console.log(`🚫 Access revoked for ${userId}: ${reason}`);
  }
  
  // ============================================
  // FEATURE GATING via CAUSALITY
  // ============================================
  
  canAccessFeature(userId, featureName) {
    /**
     * Check if user's tier allows feature
     */
    
    const user = this.users.get(userId);
    if (!user) return false;
    
    return user.tierConfig.features.includes(featureName) ||
           user.tierConfig.features.includes('all_features');
  }
  
  requireFeature(userId, featureName) {
    /**
     * Throw error if user can't access feature
     * Trigger upsell causality
     */
    
    if (!this.canAccessFeature(userId, featureName)) {
      // Trigger upsell node
      this.graph.propagate(`upsell_${featureName}`, 1.0, {
        userId: userId,
        requestedFeature: featureName
      });
      
      throw new Error(`Feature '${featureName}' requires upgrade. Current tier: ${this.users.get(userId).tier}`);
    }
  }
  
  // ============================================
  // ANALYTICS
  // ============================================
  
  getTierStats() {
    /**
     * Get user distribution across tiers
     */
    
    const stats = {};
    
    for (const tierName of this.tiers.keys()) {
      stats[tierName] = {
        count: 0,
        revenue: 0
      };
    }
    
    for (const user of this.users.values()) {
      stats[user.tier].count++;
      stats[user.tier].revenue += user.tierConfig.monthlyPrice;
    }
    
    return stats;
  }
  
  getUserTier(userId) {
    const user = this.users.get(userId);
    return user ? user.tier : null;
  }
  
  // ============================================
  // EXAMPLES
  // ============================================
  
  example_TieredAccess() {
    /**
     * Example: User journey through tiers
     */
    
    // New user signs up (free)
    this.registerUser('alice', { tier: 'free' });
    // → Gets 12 gates, 1 field, 10 AI queries/month
    
    // Alice tries premium feature
    try {
      this.requireFeature('alice', 'advanced_analytics');
    } catch (e) {
      console.log(e.message); // "Feature requires upgrade"
      // → Upsell causality triggers
    }
    
    // Alice upgrades to premium
    this.handlePayment('alice', 29.99, true);
    this.upgradeTier('alice', 'premium');
    // → Gets all 64 gates, all 9 fields, 1000 AI queries/month
    // → Graph expands automatically!
    
    // Now she can access everything
    this.requireFeature('alice', 'advanced_analytics'); // ✓ Works!
    
    // Broadcast to all premium users
    this.broadcastToTier('premium', 1.0, {
      message: 'New premium feature launched!'
    });
  }
  
  example_BillingFailure() {
    /**
     * Example: Payment failure handling
     */
    
    // User's payment fails
    this.handlePayment('bob', 29.99, false);
    // → Grace period starts (7 days)
    // → After 7 days: auto-downgrade to free
    // → Causal graph contracts automatically
    
    // Immediate revocation (e.g., fraud)
    this.revokeAccess('charlie', 'fraudulent_payment');
    // → Instant downgrade to free tier
  }
  
  example_TargetedBroadcast() {
    /**
     * Example: Send different content to different tiers
     */
    
    // Free users: Show upgrade prompt
    this.broadcastToTier('free', 0.5, {
      type: 'upsell',
      message: 'Unlock all 64 gates with Premium!'
    });
    
    // Premium users: Thank you message
    this.broadcastToTier('premium', 1.0, {
      type: 'appreciation',
      message: 'Thanks for being a Premium member!'
    });
    
    // Enterprise: Custom feature announcement
    this.broadcastToTier('enterprise', 1.0, {
      type: 'announcement',
      message: 'Your custom integration is ready'
    });
  }
}

// Export
if (typeof window !== 'undefined') {
  window.TieredCausalGraph = TieredCausalGraph;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = TieredCausalGraph;
}

// ============================================
// USAGE EXAMPLE
// ============================================

/*

// Initialize
const tieredGraph = new TieredCausalGraph();

// Register users
tieredGraph.registerUser('user_001', { tier: 'free' });
tieredGraph.registerUser('user_002', { tier: 'premium' });
tieredGraph.registerUser('user_003', { tier: 'enterprise' });

// User upgrades
tieredGraph.handlePayment('user_001', 29.99, true);
tieredGraph.upgradeTier('user_001', 'premium');
// → Causal graph expands! New gates unlock!

// Broadcast to tiers
tieredGraph.broadcastToTier('premium', 1.0, {
  message: 'Premium-only transit alert!'
});

// Feature gating
tieredGraph.requireFeature('user_001', 'advanced_analytics');
// ✓ Works because user_001 is premium

tieredGraph.requireFeature('user_004', 'advanced_analytics');
// ✗ Throws error, triggers upsell

// Analytics
const stats = tieredGraph.getTierStats();
console.log(stats);
// {
//   free: { count: 100, revenue: 0 },
//   premium: { count: 50, revenue: 1499.50 },
//   enterprise: { count: 5, revenue: 499.95 }
// }

*/
