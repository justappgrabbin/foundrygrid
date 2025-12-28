"""
Daily Sync Engine - The Core Product

Generates personalized daily briefings based on consciousness analysis.
This is what users actually interact with - not raw consciousness data.
"""

from datetime import datetime
from typing import Dict, List, Optional
import random


class DailySyncEngine:
    """
    Generates Daily Sync - morning briefing with recommendations
    
    Surface: Practical utility (what to do/watch/play)
    Foundation: Consciousness analysis (why it works)
    """
    
    def __init__(self):
        self.content_db = ContentDatabase()
        self.vibe_profiles = self._load_vibe_profiles()
    
    def generate_sync(self, consciousness_state, user_input: Optional[str] = None) -> Dict:
        """
        Generate complete Daily Sync briefing
        
        Args:
            consciousness_state: ConsciousnessState from analysis
            user_input: Optional user's current feeling/situation
            
        Returns:
            Complete Daily Sync with recommendations
        """
        # Determine user's vibe/archetype
        vibe = self._calculate_vibe(consciousness_state)
        
        # Get energy forecast
        energy = self._forecast_energy(consciousness_state)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(consciousness_state, user_input)
        
        # Get intervention
        intervention = self._suggest_intervention(consciousness_state, user_input)
        
        # Best collaboration time
        collab_time = self._calculate_collab_time(consciousness_state)
        
        return {
            'greeting': self._generate_greeting(),
            'vibe': vibe,
            'gate_info': {
                'number': consciousness_state.gate,
                'name': consciousness_state.gate_name,
                'theme': consciousness_state.gate_theme
            },
            'dimension': {
                'primary': consciousness_state.dimension_name,
                'percentage': consciousness_state.blended_probabilities[consciousness_state.dimension_name]
            },
            'energy': energy,
            'recommendations': recommendations,
            'intervention': intervention,
            'collab_time': collab_time,
            'why_link': self._generate_why_explanation(consciousness_state),
            'coordinate': consciousness_state.coordinate_string  # Hidden by default
        }
    
    def _calculate_vibe(self, state) -> Dict:
        """
        Calculate user's vibe/archetype for the day
        Simple, relatable labels
        """
        primary_dim = state.dimension_name
        coherence = state.coherence
        gate = state.gate
        
        # High coherence = focused vibes
        if coherence > 0.6:
            vibes = {
                'Movement': 'BUILDER',
                'Evolution': 'STRATEGIST', 
                'Being': 'OBSERVER',
                'Design': 'ARCHITECT',
                'Space': 'VISIONARY'
            }
            vibe_name = vibes[primary_dim]
            description = f"You're locked in. Single-minded focus on {primary_dim.lower()}."
        
        # Medium coherence = balanced vibes
        elif coherence > 0.3:
            vibes = {
                'Movement': 'CREATOR',
                'Evolution': 'ANALYZER',
                'Being': 'PROCESSOR',
                'Design': 'PLANNER',
                'Space': 'EXPLORER'
            }
            vibe_name = vibes[primary_dim]
            description = f"You're balanced. {primary_dim} leads but stays flexible."
        
        # Low coherence = scattered vibes
        else:
            vibe_name = 'MULTI-TASKER'
            description = f"You're juggling multiple energies. {primary_dim} at {state.blended_probabilities[primary_dim]:.0%}."
        
        return {
            'name': vibe_name,
            'description': description,
            'emoji': self._get_vibe_emoji(vibe_name)
        }
    
    def _get_vibe_emoji(self, vibe_name: str) -> str:
        emojis = {
            'BUILDER': '🔨',
            'STRATEGIST': '♟️',
            'OBSERVER': '👁️',
            'ARCHITECT': '📐',
            'VISIONARY': '🔮',
            'CREATOR': '🎨',
            'ANALYZER': '🧠',
            'PROCESSOR': '⚙️',
            'PLANNER': '📋',
            'EXPLORER': '🧭',
            'MULTI-TASKER': '🎭'
        }
        return emojis.get(vibe_name, '✨')
    
    def _forecast_energy(self, state) -> Dict:
        """
        Predict energy levels throughout the day
        Based on gate, dimension, and coherence
        """
        primary_dim = state.dimension_name
        coherence = state.coherence
        
        # Movement = high morning energy
        if primary_dim == 'Movement':
            peak = 'morning' if coherence > 0.5 else 'afternoon'
            peak_hours = '9am-2pm' if coherence > 0.5 else '2pm-6pm'
            level = 'high'
        
        # Evolution = steady all day
        elif primary_dim == 'Evolution':
            peak = 'all day'
            peak_hours = '9am-5pm'
            level = 'steady'
        
        # Being = peaks mid-day
        elif primary_dim == 'Being':
            peak = 'midday'
            peak_hours = '11am-3pm'
            level = 'moderate'
        
        # Design = structured peaks
        elif primary_dim == 'Design':
            peak = 'morning'
            peak_hours = '8am-12pm'
            level = 'high'
        
        # Space = evening creativity
        else:
            peak = 'evening'
            peak_hours = '4pm-9pm'
            level = 'high'
        
        return {
            'level': level,
            'peak': peak,
            'peak_hours': peak_hours,
            'advice': f"Your {primary_dim} energy peaks {peak}. Schedule important work during {peak_hours}."
        }
    
    def _generate_recommendations(self, state, user_input: Optional[str]) -> Dict:
        """
        Generate content recommendations
        This is the CORE VALUE - what users come for
        """
        recommendations = {
            'video': self.content_db.recommend_video(state, user_input),
            'music': self.content_db.recommend_music(state, user_input),
            'game': self.content_db.recommend_game(state, user_input),
            'article': self.content_db.recommend_article(state, user_input)
        }
        
        return recommendations
    
    def _suggest_intervention(self, state, user_input: Optional[str]) -> Dict:
        """
        Suggest actionable intervention based on state
        GameGAN-style behavioral prediction
        """
        coherence = state.coherence
        primary_dim = state.dimension_name
        
        # Low coherence = need consolidation
        if coherence < 0.3:
            interventions = {
                'Movement': 'Start ONE project and finish it today',
                'Evolution': 'Review and consolidate your notes/ideas',
                'Being': 'Do a 10-minute grounding meditation',
                'Design': 'Create a priority list and stick to it',
                'Space': 'Brain dump everything, then choose ONE thing'
            }
            action = interventions[primary_dim]
            reason = f"Your coherence is at {coherence:.0%}. You need focus."
        
        # High coherence = leverage it
        elif coherence > 0.6:
            interventions = {
                'Movement': 'Tackle your biggest project while you have this clarity',
                'Evolution': 'Deep dive into learning something new',
                'Being': 'Spend time in presence - walk, observe, absorb',
                'Design': 'Build the system you\'ve been planning',
                'Space': 'Let your imagination run - brainstorm freely'
            }
            action = interventions[primary_dim]
            reason = f"Your coherence is at {coherence:.0%}. Ride this wave."
        
        # Medium coherence = maintain balance
        else:
            interventions = {
                'Movement': 'Work on 2-3 projects, switch when stuck',
                'Evolution': 'Connect different ideas - synthesis time',
                'Being': 'Process your experiences - journaling helps',
                'Design': 'Plan tomorrow while executing today',
                'Space': 'Explore without committing - just observe'
            }
            action = interventions[primary_dim]
            reason = f"Your coherence is at {coherence:.0%}. Stay flexible."
        
        return {
            'action': action,
            'reason': reason,
            'difficulty': 'easy' if coherence > 0.5 else 'moderate'
        }
    
    def _calculate_collab_time(self, state) -> Dict:
        """
        When is best time to collaborate/meet people
        Based on energy and dimension
        """
        energy = self._forecast_energy(state)
        
        return {
            'best_time': energy['peak_hours'],
            'reason': f"Your {state.dimension_name} energy peaks during these hours",
            'avoid': 'Early morning' if energy['peak'] == 'evening' else 'Late evening'
        }
    
    def _generate_why_explanation(self, state) -> str:
        """
        Generate explanation link text
        This is the optional deep dive into consciousness
        """
        return f"Why these recommendations work for {state.gate_name} ({state.dimension_name})"
    
    def _generate_greeting(self) -> str:
        """Generate time-appropriate greeting"""
        hour = datetime.now().hour
        
        if hour < 12:
            return "Good morning"
        elif hour < 17:
            return "Good afternoon"
        else:
            return "Good evening"
    
    def _load_vibe_profiles(self) -> Dict:
        """Load vibe/archetype profiles"""
        # This could be loaded from JSON
        return {}


class ContentDatabase:
    """
    Content database with consciousness-tagged items
    Real implementation would query actual APIs (YouTube, Spotify, etc.)
    """
    
    def __init__(self):
        # Mock content database
        # Real version would have thousands of items
        self.videos = self._load_videos()
        self.music = self._load_music()
        self.games = self._load_games()
        self.articles = self._load_articles()
    
    def recommend_video(self, state, user_input: Optional[str]) -> Dict:
        """Recommend video based on consciousness state"""
        primary_dim = state.dimension_name
        coherence = state.coherence
        
        # Filter by dimension
        candidates = [v for v in self.videos if primary_dim in v['dimensions']]
        
        # Filter by coherence (low coherence = calming content)
        if coherence < 0.3:
            candidates = [v for v in candidates if v['pace'] in ['slow', 'calm']]
        elif coherence > 0.6:
            candidates = [v for v in candidates if v['pace'] in ['fast', 'engaging']]
        
        # Pick best match
        if candidates:
            video = random.choice(candidates)
        else:
            video = random.choice(self.videos)
        
        return {
            'title': video['title'],
            'description': video['description'],
            'url': video['url'],
            'duration': video['duration'],
            'match_reason': f"Matches your {primary_dim} dimension and {coherence:.0%} coherence"
        }
    
    def recommend_music(self, state, user_input: Optional[str]) -> Dict:
        """Recommend music based on consciousness state"""
        tone = state.tone_sense
        primary_dim = state.dimension_name
        
        # Match by sensory tone
        candidates = [m for m in self.music if tone.lower() in m['tags']]
        
        if not candidates:
            candidates = [m for m in self.music if primary_dim in m['dimensions']]
        
        if candidates:
            music = random.choice(candidates)
        else:
            music = random.choice(self.music)
        
        return {
            'title': music['title'],
            'artist': music['artist'],
            'genre': music['genre'],
            'url': music['url'],
            'match_reason': f"Resonates with your {tone} sensory tone"
        }
    
    def recommend_game(self, state, user_input: Optional[str]) -> Dict:
        """Recommend game based on consciousness state"""
        primary_dim = state.dimension_name
        line = state.line_name
        
        candidates = [g for g in self.games if primary_dim in g['dimensions']]
        
        if candidates:
            game = random.choice(candidates)
        else:
            game = random.choice(self.games)
        
        return {
            'title': game['title'],
            'description': game['description'],
            'platform': game['platform'],
            'url': game['url'],
            'match_reason': f"Aligns with {primary_dim} expression and {line} approach"
        }
    
    def recommend_article(self, state, user_input: Optional[str]) -> Dict:
        """Recommend article based on consciousness state"""
        primary_dim = state.dimension_name
        
        candidates = [a for a in self.articles if primary_dim in a['dimensions']]
        
        if candidates:
            article = random.choice(candidates)
        else:
            article = random.choice(self.articles)
        
        return {
            'title': article['title'],
            'description': article['description'],
            'source': article['source'],
            'url': article['url'],
            'read_time': article['read_time'],
            'match_reason': f"Explores themes relevant to {primary_dim}"
        }
    
    def _load_videos(self) -> List[Dict]:
        """Mock video database"""
        return [
            {
                'title': 'How It\'s Made: Modern Marvels',
                'description': 'Documentary series on engineering',
                'url': 'https://youtube.com/watch?v=example',
                'duration': '45 min',
                'pace': 'medium',
                'dimensions': ['Design', 'Movement']
            },
            {
                'title': 'Slow TV: Norwegian Coastal Voyage',
                'description': '3-hour journey along the coast',
                'url': 'https://youtube.com/watch?v=example',
                'duration': '180 min',
                'pace': 'slow',
                'dimensions': ['Being', 'Space']
            },
            {
                'title': 'The Art of Problem Solving',
                'description': 'TED talk on pattern recognition',
                'url': 'https://youtube.com/watch?v=example',
                'duration': '18 min',
                'pace': 'engaging',
                'dimensions': ['Evolution', 'Design']
            },
            {
                'title': 'Creative Coding: Generative Art',
                'description': 'Building art with algorithms',
                'url': 'https://youtube.com/watch?v=example',
                'duration': '30 min',
                'pace': 'fast',
                'dimensions': ['Movement', 'Space']
            }
        ]
    
    def _load_music(self) -> List[Dict]:
        """Mock music database"""
        return [
            {
                'title': 'Lo-fi Hip Hop Radio',
                'artist': 'ChilledCow',
                'genre': 'Lo-fi',
                'url': 'https://open.spotify.com/playlist/example',
                'tags': ['smell', 'organic', 'grounded'],
                'dimensions': ['Being']
            },
            {
                'title': 'Epic Cinematic Scores',
                'artist': 'Two Steps From Hell',
                'genre': 'Orchestral',
                'url': 'https://open.spotify.com/playlist/example',
                'tags': ['outer vision', 'epic', 'powerful'],
                'dimensions': ['Movement', 'Space']
            },
            {
                'title': 'Ambient Space Music',
                'artist': 'Brian Eno',
                'genre': 'Ambient',
                'url': 'https://open.spotify.com/playlist/example',
                'tags': ['inner vision', 'meditative', 'ethereal'],
                'dimensions': ['Space', 'Evolution']
            },
            {
                'title': 'Productivity Flow State',
                'artist': 'Focus@Will',
                'genre': 'Electronic',
                'url': 'https://open.spotify.com/playlist/example',
                'tags': ['touch', 'rhythmic', 'structured'],
                'dimensions': ['Design', 'Movement']
            }
        ]
    
    def _load_games(self) -> List[Dict]:
        """Mock game database"""
        return [
            {
                'title': 'Stardew Valley',
                'description': 'Farming simulation with rhythm and cycles',
                'platform': 'PC, Console',
                'url': 'https://store.steampowered.com/app/413150',
                'dimensions': ['Being', 'Design']
            },
            {
                'title': 'Factorio',
                'description': 'Factory building and optimization',
                'platform': 'PC',
                'url': 'https://factorio.com',
                'dimensions': ['Design', 'Movement']
            },
            {
                'title': 'The Witness',
                'description': 'Puzzle game about pattern recognition',
                'platform': 'PC, Console',
                'url': 'https://store.steampowered.com/app/210970',
                'dimensions': ['Evolution', 'Space']
            },
            {
                'title': 'Journey',
                'description': 'Meditative exploration game',
                'platform': 'PlayStation, PC',
                'url': 'https://thatgamecompany.com/journey',
                'dimensions': ['Being', 'Space']
            }
        ]
    
    def _load_articles(self) -> List[Dict]:
        """Mock article database"""
        return [
            {
                'title': 'The Power of Patience in Strategy',
                'description': 'How waiting creates opportunity',
                'source': 'Harvard Business Review',
                'url': 'https://hbr.org/example',
                'read_time': '8 min',
                'dimensions': ['Being', 'Design']
            },
            {
                'title': 'Pattern Recognition in Complex Systems',
                'description': 'Finding order in chaos',
                'source': 'Quanta Magazine',
                'url': 'https://quantamagazine.org/example',
                'read_time': '12 min',
                'dimensions': ['Evolution', 'Design']
            },
            {
                'title': 'The Creative Process: From Idea to Reality',
                'description': 'How makers make',
                'source': 'Aeon',
                'url': 'https://aeon.co/example',
                'read_time': '15 min',
                'dimensions': ['Movement', 'Space']
            }
        ]
