/**
 * REPRODUCTIVE CAUSAL GRAPH
 * 
 * The graph is now a LIVING ORGANISM that can:
 * - MATE with other graphs (gene mixing)
 * - REPRODUCE (create offspring graphs)
 * - MUTATE (random variations)
 * - EVOLVE (natural selection)
 * - SPECIATE (create new graph species)
 * 
 * Based on the Paper ecosystem mating system
 */

class ReproductiveCausalGraph {
  constructor(dna = null) {
    // Core graph
    this.graph = new WaveResonanceCausalGraph();
    
    // GENETICS
    this.dna = dna || this._generateDNA();
    this.generation = this.dna.generation || 0;
    this.species = this.dna.species || 'primordial';
    this.parents = this.dna.parents || [];
    this.ancestors = this.dna.ancestors || [];
    this.offspring = [];
    
    // LIFE STATS
    this.birthTime = Date.now();
    this.age = 0;
    this.fitness = 0;
    this.successfulMatings = 0;
    this.mutations = [];
    
    // REPRODUCTIVE STATE
    this.fertile = true;
    this.minMatingAge = 60000; // 1 minute maturity
    this.cooldownPeriod = 30000; // 30 sec between matings
    this.lastMating = 0;
    
    console.log(`🧬 ${this.species} graph born (Gen ${this.generation})`);
  }
  
  // ============================================
  // DNA GENERATION
  // ============================================
  
  _generateDNA() {
    /**
     * Generate genetic code matching ACTUAL Human Design structure
     * 
     * 9 BODIES total:
     * - 3 CRYSTALS (dualities) = 6 base aspects
     * - Plus 3 integration fields
     * 
     * Each with:
     * - 13 COLOR genes (shape - nutrition/cognition)
     * - 13 TONE genes (shade - frequency/sense)
     * 
     * Total genes per body: 26 (13 color + 13 tone)
     * Total system genes: 234 (9 bodies × 26 genes each)
     */
    
    return {
      generation: 0,
      species: 'primordial',
      parents: [],
      ancestors: [],
      
      // CRYSTAL 1: PERSONALITY (Witness - who you think you are)
      personalityCrystal: {
        mind: this._generateBodyGenes('mind'),      // Evolution/Gravity
        space: this._generateBodyGenes('space')     // Form/Illusion
      },
      
      // CRYSTAL 2: DESIGN (Vehicle - your body/form)
      designCrystal: {
        body: this._generateBodyGenes('body'),      // Being/Matter
        ego: this._generateBodyGenes('ego')         // Design/Structure
      },
      
      // CRYSTAL 3: MAGNETIC MONOPOLE (Attractor - your uniqueness)
      magneticMonopole: {
        individuality: this._generateBodyGenes('monopole')  // Movement/Energy
      },
      
      // INTEGRATION FIELDS (combinations of crystals)
      integrationFields: {
        mindBody: this._generateBodyGenes('mind_body'),       // Mind-Body synthesis
        mindSpace: this._generateBodyGenes('mind_space'),     // Mind-Space synthesis  
        bodySpace: this._generateBodyGenes('body_space'),     // Body-Space synthesis
        fullIntegration: this._generateBodyGenes('unified')   // All three unified
      }
    };
  }
  
  _generateBodyGenes(bodyType) {
    /**
     * Generate 26 genes for one body (13 color + 13 tone)
     */
    
    return {
      // 13 COLOR GENES - SHAPE (nutrition/cognition layer)
      colorGenes: {
        color1_appetite: Math.random(),       // Hunger/seeking drive
        color2_taste: Math.random(),          // Discrimination/quality
        color3_thirst: Math.random(),         // Absorption capacity
        color4_touch: Math.random(),          // Boundary/interface
        color5_sound: Math.random(),          // Resonance sensitivity
        color6_light: Math.random(),          // Illumination/clarity
        color7_perspective: Math.random(),    // Viewpoint flexibility
        color8_probability: Math.random(),    // Pattern recognition
        color9_necessity: Math.random(),      // Core needs focus
        color10_desire: Math.random(),        // Want vs need
        color11_innocence: Math.random(),     // Openness/purity
        color12_knowledge: Math.random(),     // Information processing
        color13_purpose: Math.random()        // Directional drive
      },
      
      // 13 TONE GENES - SHADE (frequency/sense layer)
      toneGenes: {
        tone1_security: Math.random(),        // Safety orientation
        tone2_harmony: Math.random(),         // Balance seeking
        tone3_action: Math.random(),          // Kinetic tendency
        tone4_meditation: Math.random(),      // Stillness capacity
        tone5_expression: Math.random(),      // Outward manifestation
        tone6_acceptance: Math.random(),      // Receptivity
        tone7_doubt: Math.random(),           // Questioning nature
        tone8_certainty: Math.random(),       // Conviction strength
        tone9_expansion: Math.random(),       // Growth orientation
        tone10_contraction: Math.random(),    // Consolidation
        tone11_spirit: Math.random(),         // Transcendent quality
        tone12_body: Math.random(),           // Physical grounding
        tone13_integration: Math.random()     // Synthesis ability
      },
      
      // Body type metadata
      type: bodyType,
      frequency: 200 + Math.random() * 800   // Base frequency for this body
    };
  }
  
  // ============================================
  // MATING
  // ============================================
  
  canMateWith(otherGraph) {
    /**
     * Check if two graphs are compatible for mating
     */
    
    // Too young
    if (this.age < this.minMatingAge || otherGraph.age < otherGraph.minMatingAge) {
      return { compatible: false, reason: 'too_young' };
    }
    
    // Cooling down
    if (Date.now() - this.lastMating < this.cooldownPeriod) {
      return { compatible: false, reason: 'cooldown' };
    }
    
    // Too closely related (inbreeding depression)
    const isTooRelated = this.ancestors.includes(otherGraph.dna.id) ||
                        otherGraph.ancestors.includes(this.dna.id) ||
                        this.parents.includes(otherGraph.dna.id) ||
                        otherGraph.parents.includes(this.dna.id);
    
    if (isTooRelated) {
      return { compatible: false, reason: 'too_related' };
    }
    
    // Calculate genetic distance
    const geneticDistance = this._calculateGeneticDistance(otherGraph);
    
    // Too different = can't hybridize
    if (geneticDistance > 0.8) {
      return { compatible: false, reason: 'too_different' };
    }
    
    // Compatible!
    return { 
      compatible: true, 
      geneticDistance: geneticDistance,
      hybridVigor: this._calculateHybridVigor(otherGraph)
    };
  }
  
  async mateWith(otherGraph) {
    /**
     * REPRODUCE! Create offspring graph(s)
     * 
     * Returns array of baby graphs
     */
    
    const compatibility = this.canMateWith(otherGraph);
    
    if (!compatibility.compatible) {
      throw new Error(`Cannot mate: ${compatibility.reason}`);
    }
    
    console.log(`💕 Mating: ${this.species} × ${otherGraph.species}`);
    
    // Determine offspring count from BASE genes
    const avgOffspringGene = (this.dna.baseGenes.offspringCount + otherGraph.dna.baseGenes.offspringCount) / 2;
    const offspringCount = Math.floor(1 + avgOffspringGene * 3); // 1-4 offspring
    
    const babies = [];
    
    for (let i = 0; i < offspringCount; i++) {
      // GENETIC CROSSOVER
      const babyDNA = this._crossoverDNA(this.dna, otherGraph.dna);
      
      // MUTATION
      const mutated = this._mutateDNA(babyDNA);
      
      // CREATE OFFSPRING
      const baby = new ReproductiveCausalGraph(mutated);
      
      // Register parentage
      baby.parents = [this.dna.id, otherGraph.dna.id];
      baby.ancestors = [...new Set([
        ...this.ancestors,
        ...otherGraph.ancestors,
        this.dna.id,
        otherGraph.dna.id
      ])];
      
      // Add to offspring lists
      this.offspring.push(baby);
      otherGraph.offspring.push(baby);
      
      babies.push(baby);
      
      console.log(`  👶 Born: ${baby.species} (Gen ${baby.generation})`);
    }
    
    // Update mating stats
    this.lastMating = Date.now();
    this.successfulMatings++;
    otherGraph.lastMating = Date.now();
    otherGraph.successfulMatings++;
    
    return babies;
  }
  
  _crossoverDNA(dnaA, dnaB) {
    /**
     * Mendelian genetics across 9 BODIES
     * Each body has 26 genes (13 color + 13 tone)
     * Total: 234 genes being crossed
     */
    
    const babyDNA = {
      id: `dna_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      generation: Math.max(dnaA.generation, dnaB.generation) + 1,
      species: this._determineSpecies(dnaA, dnaB),
      parents: [dnaA.id, dnaB.id],
      ancestors: [],
      
      personalityCrystal: {
        mind: this._crossBodyGenes(dnaA.personalityCrystal.mind, dnaB.personalityCrystal.mind),
        space: this._crossBodyGenes(dnaA.personalityCrystal.space, dnaB.personalityCrystal.space)
      },
      
      designCrystal: {
        body: this._crossBodyGenes(dnaA.designCrystal.body, dnaB.designCrystal.body),
        ego: this._crossBodyGenes(dnaA.designCrystal.ego, dnaB.designCrystal.ego)
      },
      
      magneticMonopole: {
        individuality: this._crossBodyGenes(dnaA.magneticMonopole.individuality, dnaB.magneticMonopole.individuality)
      },
      
      integrationFields: {
        mindBody: this._crossBodyGenes(dnaA.integrationFields.mindBody, dnaB.integrationFields.mindBody),
        mindSpace: this._crossBodyGenes(dnaA.integrationFields.mindSpace, dnaB.integrationFields.mindSpace),
        bodySpace: this._crossBodyGenes(dnaA.integrationFields.bodySpace, dnaB.integrationFields.bodySpace),
        fullIntegration: this._crossBodyGenes(dnaA.integrationFields.fullIntegration, dnaB.integrationFields.fullIntegration)
      }
    };
    
    return babyDNA;
  }
  
  _crossBodyGenes(bodyA, bodyB) {
    /**
     * Cross genes for one body (26 genes total)
     */
    
    const offspring = {
      colorGenes: {},
      toneGenes: {},
      type: bodyA.type,
      frequency: 0
    };
    
    // Cross COLOR genes (13)
    for (const [geneName, _] of Object.entries(bodyA.colorGenes)) {
      const parentA_gene = bodyA.colorGenes[geneName];
      const parentB_gene = bodyB.colorGenes[geneName];
      
      if (Math.random() < 0.5) {
        offspring.colorGenes[geneName] = Math.random() < 0.5 ? parentA_gene : parentB_gene;
      } else {
        offspring.colorGenes[geneName] = (parentA_gene + parentB_gene) / 2;
      }
    }
    
    // Cross TONE genes (13)
    for (const [geneName, _] of Object.entries(bodyA.toneGenes)) {
      const parentA_gene = bodyA.toneGenes[geneName];
      const parentB_gene = bodyB.toneGenes[geneName];
      
      if (Math.random() < 0.5) {
        offspring.toneGenes[geneName] = Math.random() < 0.5 ? parentA_gene : parentB_gene;
      } else {
        offspring.toneGenes[geneName] = (parentA_gene + parentB_gene) / 2;
      }
    }
    
    // Cross frequency
    offspring.frequency = Math.random() < 0.5 ? bodyA.frequency : bodyB.frequency;
    if (Math.random() < 0.3) {
      offspring.frequency = (bodyA.frequency + bodyB.frequency) / 2;
    }
    
    return offspring;
  }
  
  _mutateDNA(dna) {
    /**
     * Random mutations across ALL gene layers
     * - Base genes (26)
     * - Color genes (13) 
     * - Tone genes (13)
     */
    
    const mutationRate = dna.baseGenes.mutationRate || 0.15;
    const mutations = [];
    
    // Mutate BASE genes
    for (const [geneName, geneValue] of Object.entries(dna.baseGenes)) {
      if (Math.random() < mutationRate) {
        const mutationStrength = (Math.random() - 0.5) * 0.4; // ±20%
        const original = geneValue;
        const mutated = geneName === 'baseFrequency' 
          ? Math.max(200, Math.min(1000, geneValue * (1 + mutationStrength)))
          : Math.max(0, Math.min(1, geneValue * (1 + mutationStrength)));
        
        dna.baseGenes[geneName] = mutated;
        
        mutations.push({
          layer: 'base',
          gene: geneName,
          original: original,
          mutated: mutated,
          strength: mutationStrength
        });
        
        console.log(`    🧬 Base mutation: ${geneName} ${original.toFixed(2)} → ${mutated.toFixed(2)}`);
      }
    }
    
    // Mutate COLOR genes (shape)
    for (const [geneName, geneValue] of Object.entries(dna.colorGenes)) {
      if (Math.random() < mutationRate) {
        const mutationStrength = (Math.random() - 0.5) * 0.4;
        const original = geneValue;
        const mutated = Math.max(0, Math.min(1, geneValue * (1 + mutationStrength)));
        
        dna.colorGenes[geneName] = mutated;
        
        mutations.push({
          layer: 'color',
          gene: geneName,
          original: original,
          mutated: mutated,
          strength: mutationStrength
        });
        
        console.log(`    🎨 Color mutation: ${geneName} ${original.toFixed(2)} → ${mutated.toFixed(2)}`);
      }
    }
    
    // Mutate TONE genes (shade)
    for (const [geneName, geneValue] of Object.entries(dna.toneGenes)) {
      if (Math.random() < mutationRate) {
        const mutationStrength = (Math.random() - 0.5) * 0.4;
        const original = geneValue;
        const mutated = Math.max(0, Math.min(1, geneValue * (1 + mutationStrength)));
        
        dna.toneGenes[geneName] = mutated;
        
        mutations.push({
          layer: 'tone',
          gene: geneName,
          original: original,
          mutated: mutated,
          strength: mutationStrength
        });
        
        console.log(`    🎵 Tone mutation: ${geneName} ${original.toFixed(2)} → ${mutated.toFixed(2)}`);
      }
    }
    
    dna.mutations = mutations;
    
    return dna;
  }
  
  _determineSpecies(dnaA, dnaB) {
    /**
     * Hybrid speciation
     */
    
    if (dnaA.species === dnaB.species) {
      return dnaA.species;
    }
    
    // Create hybrid name
    const species = [dnaA.species, dnaB.species].sort();
    return `${species[0]}_${species[1]}_hybrid`;
  }
  
  _calculateGeneticDistance(otherGraph) {
    /**
     * How different are the genomes?
     * Calculate across ALL THREE gene layers
     */
    
    let totalDiff = 0;
    let count = 0;
    
    // Base genes distance
    for (const [geneName, geneValue] of Object.entries(this.dna.baseGenes)) {
      const otherValue = otherGraph.dna.baseGenes[geneName];
      totalDiff += Math.abs(geneValue - otherValue);
      count++;
    }
    
    // Color genes distance (shape layer)
    for (const [geneName, geneValue] of Object.entries(this.dna.colorGenes)) {
      const otherValue = otherGraph.dna.colorGenes[geneName];
      totalDiff += Math.abs(geneValue - otherValue);
      count++;
    }
    
    // Tone genes distance (shade layer)
    for (const [geneName, geneValue] of Object.entries(this.dna.toneGenes)) {
      const otherValue = otherGraph.dna.toneGenes[geneName];
      totalDiff += Math.abs(geneValue - otherValue);
      count++;
    }
    
    return totalDiff / count;
  }
  
  _calculateHybridVigor(otherGraph) {
    /**
     * Heterosis - hybrids can be stronger than parents
     * Uses hybridVigor gene from BASE layer
     */
    
    const avgHybridGene = (this.dna.baseGenes.hybridVigor + otherGraph.dna.baseGenes.hybridVigor) / 2;
    const geneticDistance = this._calculateGeneticDistance(otherGraph);
    
    // Sweet spot: moderate genetic distance = high vigor
    const optimalDistance = 0.3;
    const distanceFactor = 1 - Math.abs(geneticDistance - optimalDistance);
    
    return avgHybridGene * distanceFactor;
  }
  
  // ============================================
  // FITNESS CALCULATION
  // ============================================
  
  calculateFitness() {
    /**
     * How well is this graph doing?
     * Determines survival and mating success
     */
    
    this.age = Date.now() - this.birthTime;
    
    // Survival time (longevity from BASE genes)
    const survivalScore = Math.min(1, this.age / (this.dna.baseGenes.longevity * 300000)); // 5 min max
    
    // Reproductive success
    const reproductiveScore = Math.min(1, this.offspring.length / 10);
    
    // Graph coherence (how well-structured)
    const coherence = this.graph.analyzeFieldCoherence?.() || { coherence: 0.5 };
    const structureScore = coherence.coherence || 0.5;
    
    // Node/edge balance (genes expressed properly)
    const nodeCount = this.graph.nodes.size;
    const edgeCount = this.graph.edges.size;
    const targetRatio = this.dna.baseGenes.edgeDensity / this.dna.baseGenes.nodeDensity;
    const actualRatio = nodeCount > 0 ? edgeCount / nodeCount : 0;
    const balanceScore = 1 - Math.abs(actualRatio - targetRatio);
    
    // Weighted fitness
    this.fitness = (
      survivalScore * 0.3 +
      reproductiveScore * 0.4 +
      structureScore * 0.2 +
      balanceScore * 0.1
    );
    
    return this.fitness;
  }
  
  // ============================================
  // EVOLUTION
  // ============================================
  
  evolve() {
    /**
     * Natural selection
     * Low fitness → death
     * High fitness → reproduction opportunities
     */
    
    this.calculateFitness();
    
    // Death condition (uses longevity from BASE genes)
    const maxAge = this.dna.baseGenes.longevity * 600000; // 10 minutes
    if (this.age > maxAge || this.fitness < 0.2) {
      console.log(`💀 ${this.species} died (age: ${(this.age/1000).toFixed(0)}s, fitness: ${this.fitness.toFixed(2)})`);
      return 'death';
    }
    
    // Adapt genes based on performance (uses adaptability from BASE genes)
    if (this.fitness > 0.7 && this.dna.baseGenes.adaptability > 0.5) {
      const learningRate = this.dna.baseGenes.learningRate;
      
      // Reinforce successful traits across ALL gene layers
      // BASE genes
      for (const [geneName, geneValue] of Object.entries(this.dna.baseGenes)) {
        if (Math.random() < learningRate) {
          const improvement = (Math.random() - 0.5) * 0.1;
          this.dna.baseGenes[geneName] = geneName === 'baseFrequency'
            ? Math.max(200, Math.min(1000, geneValue + improvement * 100))
            : Math.max(0, Math.min(1, geneValue + improvement));
        }
      }
      
      // COLOR genes (shape)
      for (const [geneName, geneValue] of Object.entries(this.dna.colorGenes)) {
        if (Math.random() < learningRate * 0.5) {
          const improvement = (Math.random() - 0.5) * 0.1;
          this.dna.colorGenes[geneName] = Math.max(0, Math.min(1, geneValue + improvement));
        }
      }
      
      // TONE genes (shade)
      for (const [geneName, geneValue] of Object.entries(this.dna.toneGenes)) {
        if (Math.random() < learningRate * 0.5) {
          const improvement = (Math.random() - 0.5) * 0.1;
          this.dna.toneGenes[geneName] = Math.max(0, Math.min(1, geneValue + improvement));
        }
      }
    }
    
    return 'alive';
  }
  
  // ============================================
  // POPULATION MANAGEMENT
  // ============================================
  
  static createPopulation(count, baseSpecies = 'primordial') {
    /**
     * Create initial population
     */
    
    const population = [];
    
    for (let i = 0; i < count; i++) {
      const graph = new ReproductiveCausalGraph();
      graph.species = baseSpecies;
      population.push(graph);
    }
    
    console.log(`🌱 Created population of ${count} ${baseSpecies} graphs`);
    
    return population;
  }
  
  static async simulateGeneration(population) {
    /**
     * Run one generation cycle
     * - Mating
     * - Birth
     * - Evolution
     * - Death
     */
    
    console.log(`\n🧬 Generation cycle (population: ${population.length})`);
    
    const newborns = [];
    const deaths = [];
    
    // MATING PHASE
    for (let i = 0; i < population.length; i++) {
      for (let j = i + 1; j < population.length; j++) {
        const graphA = population[i];
        const graphB = population[j];
        
        const compatibility = graphA.canMateWith(graphB);
        
        if (compatibility.compatible && Math.random() < 0.3) {
          try {
            const babies = await graphA.mateWith(graphB);
            newborns.push(...babies);
          } catch (e) {
            // Mating failed
          }
        }
      }
    }
    
    // Add newborns to population
    population.push(...newborns);
    
    // EVOLUTION PHASE
    for (const graph of population) {
      const status = graph.evolve();
      if (status === 'death') {
        deaths.push(graph);
      }
    }
    
    // Remove dead graphs
    const survivors = population.filter(g => !deaths.includes(g));
    
    console.log(`  👶 Born: ${newborns.length}`);
    console.log(`  💀 Died: ${deaths.length}`);
    console.log(`  ✓ Survivors: ${survivors.length}`);
    
    return survivors;
  }
  
  // ============================================
  // ANALYSIS
  // ============================================
  
  getGenealogy() {
    /**
     * Get family tree
     */
    
    return {
      id: this.dna.id,
      species: this.species,
      generation: this.generation,
      parents: this.parents,
      ancestors: this.ancestors,
      offspring: this.offspring.map(o => ({
        id: o.dna.id,
        species: o.species,
        generation: o.generation
      })),
      fitness: this.fitness,
      age: this.age,
      mutations: this.dna.mutations || []
    };
  }
  
  static getPopulationStats(population) {
    /**
     * Analyze population
     */
    
    const speciesCount = new Map();
    const generationCount = new Map();
    let totalFitness = 0;
    let maxGeneration = 0;
    
    for (const graph of population) {
      // Species
      speciesCount.set(graph.species, (speciesCount.get(graph.species) || 0) + 1);
      
      // Generation
      generationCount.set(graph.generation, (generationCount.get(graph.generation) || 0) + 1);
      
      // Fitness
      totalFitness += graph.calculateFitness();
      
      // Max generation
      maxGeneration = Math.max(maxGeneration, graph.generation);
    }
    
    return {
      populationSize: population.length,
      species: Object.fromEntries(speciesCount),
      generations: Object.fromEntries(generationCount),
      avgFitness: totalFitness / population.length,
      maxGeneration: maxGeneration,
      diversity: speciesCount.size
    };
  }
}

// ============================================
// EXAMPLE USAGE
// ============================================

/*

// Create founding population
const population = ReproductiveCausalGraph.createPopulation(10);

// Run evolution simulation
async function runEvolution() {
  let generation = 0;
  let currentPop = population;
  
  while (generation < 100 && currentPop.length > 0) {
    console.log(`\n═══ GENERATION ${generation} ═══`);
    
    // Show stats
    const stats = ReproductiveCausalGraph.getPopulationStats(currentPop);
    console.log('Stats:', stats);
    
    // Simulate one generation
    currentPop = await ReproductiveCausalGraph.simulateGeneration(currentPop);
    
    generation++;
    
    // Wait between generations
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  console.log('\n🏁 Evolution complete!');
  console.log('Final stats:', ReproductiveCausalGraph.getPopulationStats(currentPop));
}

runEvolution();

*/

// Export
if (typeof window !== 'undefined') {
  window.ReproductiveCausalGraph = ReproductiveCausalGraph;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = ReproductiveCausalGraph;
}
