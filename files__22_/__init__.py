"""
Foundation Layer - Mathematical Core

This is the ontological foundation - YOUR exact framework.
Everything else is built on top of this.
"""

from .sentence_generator import (
    SentenceGenerator,
    Coordinate,
    Gate,
    Center,
    Dimension
)

from .astronomical import (
    AstronomicalCalculator,
    ConsciousnessPositionCalculator,
    get_sun_position_now,
    get_coordinate_now,
    get_sentence_now
)

from .geometry import GeometricProbability

__all__ = [
    'SentenceGenerator',
    'Coordinate',
    'Gate',
    'Center',
    'Dimension',
    'AstronomicalCalculator',
    'ConsciousnessPositionCalculator',
    'GeometricProbability',
    'get_sun_position_now',
    'get_coordinate_now',
    'get_sentence_now'
]
