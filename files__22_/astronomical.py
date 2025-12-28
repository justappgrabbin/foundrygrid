"""
Astronomical Position Calculator

Calculates celestial positions (primarily Sun) and converts them
to consciousness coordinates via the sentence generator.
"""

from datetime import datetime, timezone
from typing import Tuple
import math


class AstronomicalCalculator:
    """
    Calculate astronomical positions for consciousness coordinate system.
    
    Uses simplified ephemeris calculations for Sun position.
    For production, consider using skyfield or pyephem for higher precision.
    """
    
    # Zodiac sign boundaries (tropical zodiac)
    ZODIAC_SIGNS = [
        ('Aries', 0),
        ('Taurus', 30),
        ('Gemini', 60),
        ('Cancer', 90),
        ('Leo', 120),
        ('Virgo', 150),
        ('Libra', 180),
        ('Scorpio', 210),
        ('Sagittarius', 240),
        ('Capricorn', 270),
        ('Aquarius', 300),
        ('Pisces', 330)
    ]
    
    def calculate_sun_position(self, dt: datetime = None) -> Tuple[int, int, float, str]:
        """
        Calculate Sun's tropical zodiac position
        
        Args:
            dt: Datetime to calculate for (defaults to now)
            
        Returns:
            Tuple of (degrees, minutes, seconds, zodiac_sign)
        """
        if dt is None:
            dt = datetime.now(timezone.utc)
        
        # Ensure timezone-aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        
        # Calculate ecliptic longitude using simplified formula
        # Reference epoch: J2000.0 (Jan 1, 2000, 12:00 TT)
        j2000 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        
        # Days since J2000
        delta = dt - j2000
        days = delta.total_seconds() / 86400.0
        
        # Mean longitude of Sun (simplified)
        # L = L0 + n * days
        # where L0 = 280.460° (mean longitude at epoch)
        # and n = 0.9856474° per day (mean daily motion)
        
        L0 = 280.460  # degrees
        n = 0.9856474  # degrees per day
        
        mean_longitude = (L0 + n * days) % 360
        
        # Mean anomaly
        M0 = 357.528  # degrees
        M = (M0 + n * days) % 360
        M_rad = math.radians(M)
        
        # Equation of center (simplified - first order only)
        C = 1.915 * math.sin(M_rad) + 0.020 * math.sin(2 * M_rad)
        
        # Ecliptic longitude
        ecliptic_longitude = (mean_longitude + C) % 360
        
        # Convert to zodiac position
        return self._ecliptic_to_zodiac(ecliptic_longitude)
    
    def _ecliptic_to_zodiac(self, longitude: float) -> Tuple[int, int, float, str]:
        """
        Convert ecliptic longitude to zodiac position
        
        Args:
            longitude: Ecliptic longitude in degrees (0-360)
            
        Returns:
            Tuple of (degrees, minutes, seconds, zodiac_sign)
        """
        # Find zodiac sign
        zodiac_sign = None
        sign_start = 0
        
        for sign, start_degree in self.ZODIAC_SIGNS:
            if longitude >= start_degree:
                zodiac_sign = sign
                sign_start = start_degree
            else:
                break
        
        # Handle wraparound (Pisces to Aries)
        if zodiac_sign is None:
            zodiac_sign = 'Pisces'
            sign_start = 330
        
        # Calculate position within sign (0-30 degrees)
        position_in_sign = longitude - sign_start
        
        # Convert to degrees, minutes, seconds
        degrees = int(position_in_sign)
        decimal_minutes = (position_in_sign - degrees) * 60
        minutes = int(decimal_minutes)
        seconds = (decimal_minutes - minutes) * 60
        
        return (degrees, minutes, seconds, zodiac_sign)
    
    def zodiac_to_ecliptic(self, degrees: int, minutes: int, seconds: float, sign: str) -> float:
        """
        Convert zodiac position back to ecliptic longitude
        
        Args:
            degrees: 0-29 within sign
            minutes: 0-59
            seconds: 0-59.999
            sign: Zodiac sign name
            
        Returns:
            Ecliptic longitude (0-360 degrees)
        """
        # Find sign offset
        sign_offset = 0
        for s, offset in self.ZODIAC_SIGNS:
            if s == sign:
                sign_offset = offset
                break
        
        # Convert DMS to decimal
        decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
        
        # Add sign offset
        return sign_offset + decimal_degrees
    
    def calculate_planetary_position(self, body: str, dt: datetime = None) -> Tuple[int, int, float, str]:
        """
        Calculate position of other celestial bodies
        
        NOTE: This is a placeholder. For production, use a proper ephemeris
        library like skyfield or pyephem for accurate planetary positions.
        
        Args:
            body: 'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', etc.
            dt: Datetime to calculate for
            
        Returns:
            Tuple of (degrees, minutes, seconds, zodiac_sign)
        """
        if body.lower() == 'sun':
            return self.calculate_sun_position(dt)
        else:
            raise NotImplementedError(
                f"Planetary calculations for {body} not yet implemented. "
                "Consider integrating skyfield or pyephem for full ephemeris."
            )


class ConsciousnessPositionCalculator:
    """
    Combines astronomical calculations with consciousness coordinate system
    """
    
    def __init__(self, sentence_generator):
        """
        Args:
            sentence_generator: Instance of SentenceGenerator
        """
        self.astro = AstronomicalCalculator()
        self.sentence_gen = sentence_generator
    
    def get_current_coordinate(self):
        """
        Get consciousness coordinate for current moment
        
        Returns:
            Coordinate object from sentence generator
        """
        degrees, minutes, seconds, sign = self.astro.calculate_sun_position()
        return self.sentence_gen.parse_position(degrees, minutes, seconds, sign)
    
    def get_coordinate_at_time(self, dt: datetime):
        """
        Get consciousness coordinate for specific datetime
        
        Args:
            dt: Datetime to calculate for
            
        Returns:
            Coordinate object
        """
        degrees, minutes, seconds, sign = self.astro.calculate_sun_position(dt)
        return self.sentence_gen.parse_position(degrees, minutes, seconds, sign)
    
    def get_current_sentence(self):
        """
        Generate consciousness sentence for current moment
        
        Returns:
            Complete sentence dictionary
        """
        coord = self.get_current_coordinate()
        return self.sentence_gen.generate_sentence(coord)
    
    def get_sentence_at_time(self, dt: datetime):
        """
        Generate consciousness sentence for specific datetime
        
        Args:
            dt: Datetime to calculate for
            
        Returns:
            Complete sentence dictionary
        """
        coord = self.get_coordinate_at_time(dt)
        return self.sentence_gen.generate_sentence(coord)


# Utility functions for quick access
def get_sun_position_now() -> Tuple[int, int, float, str]:
    """Quick function to get current Sun position"""
    calc = AstronomicalCalculator()
    return calc.calculate_sun_position()


def get_coordinate_now(sentence_generator):
    """Quick function to get current consciousness coordinate"""
    calc = ConsciousnessPositionCalculator(sentence_generator)
    return calc.get_current_coordinate()


def get_sentence_now(sentence_generator):
    """Quick function to get current consciousness sentence"""
    calc = ConsciousnessPositionCalculator(sentence_generator)
    return calc.get_current_sentence()
