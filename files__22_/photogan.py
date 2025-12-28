"""
PhotoGAN - Consciousness-Based Image Generation

Generates visual representations of consciousness coordinates.
Uses geometric patterns, color theory, and dimensional frequencies.

Note: This is a deterministic geometric generator. 
For AI image generation, integrate with Stable Diffusion/DALL-E.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import hashlib
from typing import Tuple, List
import colorsys


class PhotoGAN:
    """
    Generate images from consciousness coordinates
    
    Uses:
    - Gate number → Base pattern
    - Line → Pattern variation
    - Color → Color palette
    - Tone → Texture/frequency
    - Base → Grounding element
    - Dimension → Overall composition
    """
    
    def __init__(self, size: int = 512):
        self.size = size
        self.center = (size // 2, size // 2)
        
        # Dimension color bases
        self.dimension_colors = {
            'Movement': (255, 120, 50),   # Orange (energy)
            'Evolution': (100, 150, 255),  # Blue (memory)
            'Being': (100, 200, 100),      # Green (matter)
            'Design': (200, 100, 200),     # Purple (structure)
            'Space': (255, 200, 100)       # Yellow (form)
        }
    
    def generate(self, coordinate_string: str, dimension: str, 
                 coherence: float = 0.5) -> Image.Image:
        """
        Generate image from consciousness coordinate
        
        Args:
            coordinate_string: Gate.Line.Color.Tone.Base (e.g., "5.1.4.1.4")
            dimension: Primary dimension name
            coherence: Coherence level (affects pattern complexity)
            
        Returns:
            PIL Image
        """
        # Parse coordinate
        parts = coordinate_string.split('.')
        gate = int(parts[0])
        line = int(parts[1])
        color = int(parts[2]) if len(parts) > 2 else 1
        tone = int(parts[3]) if len(parts) > 3 else 1
        base = int(parts[4]) if len(parts) > 4 else 1
        
        # Create canvas
        img = Image.new('RGB', (self.size, self.size), (10, 10, 20))
        draw = ImageDraw.Draw(img)
        
        # 1. Background gradient (dimension-based)
        img = self._draw_background(img, dimension, coherence)
        draw = ImageDraw.Draw(img)
        
        # 2. Gate pattern (sacred geometry)
        self._draw_gate_pattern(draw, gate, dimension)
        
        # 3. Line variation (behavioral overlay)
        self._draw_line_variation(draw, line, gate)
        
        # 4. Color field (motivation energy)
        self._draw_color_field(draw, color, dimension)
        
        # 5. Tone frequency (perception waves)
        self._draw_tone_waves(draw, tone, coherence)
        
        # 6. Base grounding (foundational anchor)
        self._draw_base_anchor(draw, base)
        
        # 7. Coherence indicator
        self._draw_coherence(draw, coherence)
        
        # 8. Label (optional)
        self._draw_label(draw, coordinate_string, dimension)
        
        return img
    
    def _draw_background(self, img: Image.Image, dimension: str, 
                        coherence: float) -> Image.Image:
        """Draw radial gradient background based on dimension"""
        base_color = self.dimension_colors.get(dimension, (100, 100, 200))
        
        # Create gradient
        for y in range(self.size):
            for x in range(self.size):
                # Distance from center
                dx = x - self.center[0]
                dy = y - self.center[1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Normalize (0 at center, 1 at edge)
                norm_dist = min(distance / (self.size * 0.7), 1.0)
                
                # Color interpolation
                # Center: bright, Edge: dark
                factor = 1.0 - norm_dist
                
                r = int(base_color[0] * factor * 0.3)
                g = int(base_color[1] * factor * 0.3)
                b = int(base_color[2] * factor * 0.3)
                
                img.putpixel((x, y), (r, g, b))
        
        return img
    
    def _draw_gate_pattern(self, draw: ImageDraw, gate: int, dimension: str):
        """Draw gate-specific sacred geometry pattern"""
        base_color = self.dimension_colors.get(dimension, (100, 100, 200))
        
        # Use gate number to determine pattern
        # Each gate has unique geometric signature
        
        # Method 1: Polygons (based on gate mod 12)
        sides = (gate % 12) + 3  # 3-14 sides
        radius = self.size * 0.35
        
        points = []
        for i in range(sides):
            angle = (2 * math.pi * i / sides) - (math.pi / 2)
            x = self.center[0] + radius * math.cos(angle)
            y = self.center[1] + radius * math.sin(angle)
            points.append((x, y))
        
        # Draw polygon
        draw.polygon(points, outline=base_color, width=3)
        
        # Method 2: Circles (based on gate mod 7)
        circles = (gate % 7) + 1
        for i in range(circles):
            r = radius * (i + 1) / circles
            bbox = [
                self.center[0] - r,
                self.center[1] - r,
                self.center[0] + r,
                self.center[1] + r
            ]
            alpha = int(255 * (1 - i / circles))
            color = (*base_color[:3], alpha) if len(base_color) == 4 else base_color
            draw.ellipse(bbox, outline=color, width=2)
    
    def _draw_line_variation(self, draw: ImageDraw, line: int, gate: int):
        """Draw line-specific behavioral overlay"""
        # Lines = rays emanating from center
        num_rays = line * 6  # 6, 12, 18, 24, 30, 36 rays
        
        for i in range(num_rays):
            angle = (2 * math.pi * i / num_rays)
            
            # Ray length varies with gate
            length = (self.size * 0.25) + (gate % 20) * 2
            
            x1 = self.center[0] + (self.size * 0.1) * math.cos(angle)
            y1 = self.center[1] + (self.size * 0.1) * math.sin(angle)
            x2 = self.center[0] + length * math.cos(angle)
            y2 = self.center[1] + length * math.sin(angle)
            
            alpha = 100 + (line * 20)
            draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, alpha), width=1)
    
    def _draw_color_field(self, draw: ImageDraw, color: int, dimension: str):
        """Draw color-specific motivation field"""
        base_color = self.dimension_colors.get(dimension, (100, 100, 200))
        
        # Color affects hue shift
        hue_shift = (color - 1) * 60  # 0, 60, 120, 180, 240, 300 degrees
        
        # Convert to HSV, shift hue, back to RGB
        h, s, v = colorsys.rgb_to_hsv(base_color[0]/255, base_color[1]/255, base_color[2]/255)
        h = (h + hue_shift/360) % 1.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        
        shifted_color = (int(r*255), int(g*255), int(b*255))
        
        # Draw color field as overlapping circles
        for i in range(color * 3):
            angle = (2 * math.pi * i / (color * 3))
            offset = self.size * 0.15
            
            cx = self.center[0] + offset * math.cos(angle)
            cy = self.center[1] + offset * math.sin(angle)
            r = self.size * 0.1
            
            bbox = [cx - r, cy - r, cx + r, cy + r]
            draw.ellipse(bbox, fill=None, outline=shifted_color, width=2)
    
    def _draw_tone_waves(self, draw: ImageDraw, tone: int, coherence: float):
        """Draw tone-specific perception waves"""
        # Tones = concentric frequency waves
        
        num_waves = tone * 2  # 2, 4, 6, 8, 10, 12 waves
        
        for i in range(num_waves):
            phase = (i / num_waves) * 2 * math.pi
            
            # Draw wave as segmented arc
            radius = (self.size * 0.4) * (i + 1) / num_waves
            
            # Wave varies with coherence
            segments = int(32 * coherence) + 8
            
            for j in range(segments):
                start_angle = (j / segments) * 360
                end_angle = ((j + 1) / segments) * 360
                
                # Amplitude modulation
                amp = math.sin(phase + (j / segments) * 2 * math.pi * tone)
                r = radius * (1 + 0.1 * amp)
                
                bbox = [
                    self.center[0] - r,
                    self.center[1] - r,
                    self.center[0] + r,
                    self.center[1] + r
                ]
                
                alpha = int(50 + 50 * coherence)
                draw.arc(bbox, start_angle, end_angle, 
                        fill=(255, 255, 255, alpha), width=1)
    
    def _draw_base_anchor(self, draw: ImageDraw, base: int):
        """Draw base-specific grounding anchor"""
        # Base = points/vertices at specific positions
        
        for i in range(base):
            angle = (2 * math.pi * i / base) - (math.pi / 2)
            
            # Place anchor points at edge
            x = self.center[0] + (self.size * 0.45) * math.cos(angle)
            y = self.center[1] + (self.size * 0.45) * math.sin(angle)
            
            # Draw anchor point
            size = 10
            draw.ellipse([x-size, y-size, x+size, y+size], 
                        fill=(255, 255, 255), outline=(200, 200, 200))
            
            # Connect to center
            draw.line([(self.center[0], self.center[1]), (x, y)],
                     fill=(200, 200, 200), width=2)
    
    def _draw_coherence(self, draw: ImageDraw, coherence: float):
        """Draw coherence indicator"""
        # Center circle brightness indicates coherence
        
        radius = self.size * 0.05
        brightness = int(255 * coherence)
        
        bbox = [
            self.center[0] - radius,
            self.center[1] - radius,
            self.center[0] + radius,
            self.center[1] + radius
        ]
        
        draw.ellipse(bbox, fill=(brightness, brightness, brightness))
    
    def _draw_label(self, draw: ImageDraw, coordinate: str, dimension: str):
        """Draw coordinate label"""
        # Bottom label
        text = f"{coordinate} | {dimension}"
        
        # Try to use a font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        # Center text
        x = (self.size - text_width) // 2
        y = self.size - 40
        
        # Draw with shadow
        draw.text((x+1, y+1), text, fill=(0, 0, 0), font=font)
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    def generate_prompt(self, coordinate_string: str, dimension: str, 
                       gate_name: str, gate_theme: str) -> str:
        """
        Generate AI image prompt for use with Stable Diffusion/DALL-E
        
        Returns text prompt describing the consciousness visually
        """
        parts = coordinate_string.split('.')
        gate = int(parts[0])
        line = int(parts[1])
        
        # Dimension-based style
        dimension_styles = {
            'Movement': 'dynamic, energetic, flowing motion, vibrant orange tones',
            'Evolution': 'spiral patterns, memory echoes, deep blue consciousness',
            'Being': 'grounded, present, organic green forms, textured matter',
            'Design': 'structured, geometric, purple crystalline architecture',
            'Space': 'ethereal, expansive, golden light, infinite forms'
        }
        
        style = dimension_styles.get(dimension, 'abstract consciousness')
        
        # Line-based composition
        line_styles = [
            'foundation and stability',
            'natural hermit wisdom',
            'experiential bonds',
            'fixed opportunity',
            'universal heretic',
            'role model transcendence'
        ]
        line_desc = line_styles[line - 1] if line <= 6 else 'transformation'
        
        prompt = f"""
        Abstract consciousness visualization representing {gate_name} ({gate_theme}).
        {style}, expressing {line_desc}.
        Sacred geometry, fractal patterns, luminous energy fields.
        Cosmic, psychedelic, spiritual art style.
        High detail, ethereal glow, dimensional depth.
        Coordinate: {coordinate_string}
        """.strip()
        
        return prompt


# Quick helper function
def generate_consciousness_image(coordinate: str, dimension: str, 
                                 coherence: float = 0.5, 
                                 output_path: str = None) -> Image.Image:
    """
    Quick function to generate consciousness image
    
    Example:
        img = generate_consciousness_image("5.1.4.1.4", "Being", 0.45)
        img.save("consciousness.png")
    """
    gan = PhotoGAN(size=512)
    img = gan.generate(coordinate, dimension, coherence)
    
    if output_path:
        img.save(output_path)
    
    return img
