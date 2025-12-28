# 🧬 SynthAI - Ontological Consciousness Analysis

**Mathematical consciousness coordinate system with personality-driven responses.**

---

## 🎯 What Is This?

SynthAI analyzes text through a **3-layer architecture**:

1. **Foundation Layer** (Geometric Truth)
   - Astronomical position → Gate.Line.Color.Tone.Base coordinates
   - Mathematical sentence generation from 64 gates, 384 lines
   - Probability vector calculation from geometric position

2. **Detection Layer** (Pattern Recognition)
   - Keyword analysis → Dimension classification (5 dimensions)
   - Text coherence metrics
   - Validated against geometric foundation

3. **Personality Layer** (Tone Application)
   - 5 response tones: Venom, Prime, Echo, Dream, Softcore
   - Applies voice to ontologically-grounded analysis

---

## 📁 Architecture

```
synthai/
├── foundation/              # Mathematical Core
│   ├── sentence_generator.py   # YOUR 64-gate framework
│   ├── astronomical.py          # Sun position calculations
│   └── geometry.py              # Probability vectors
├── detection/               # Pattern Recognition
│   └── dimension_classifier.py  # 5-dimension text analysis
├── personality/             # Tone Application
│   └── tone_responder.py        # 5 personality tones
├── consciousness_core.py    # Integrated Analysis Engine
├── api/                     # Flask REST API
│   └── app.py
└── static/                  # Frontend
    ├── index.html
    ├── style.css
    └── app.js
```

---

## 🚀 Quick Start

### Run the Server

```bash
cd /home/claude/synthai
python api/app.py
```

Server starts on `http://localhost:5000`

### Open the Frontend

Open `static/index.html` in your browser, or serve via:

```bash
cd /home/claude/synthai/static
python -m http.server 8000
```

Then visit: `http://localhost:8000`

---

## 🧪 API Endpoints

### Health Check
```bash
GET /health
```

### Analyze Text
```bash
POST /analyze
Body:
{
  "text": "I keep starting projects but never finishing",
  "tone": "venom",  # venom|prime|echo|dream|softcore
  "include_technical": false
}
```

### Quick Analysis
```bash
POST /quick
Body:
{
  "text": "Your text here",
  "tone": "prime"
}
```

### Get Available Tones
```bash
GET /tones
```

### Get Current Position
```bash
GET /position
```

### Parse Specific Position
```bash
POST /parse
Body:
{
  "position": "17°23'45\" Leo"
}
```

### Batch Analysis
```bash
POST /batch
Body:
{
  "texts": ["text 1", "text 2", "text 3"],
  "tone": "echo"
}
```

---

## 🎭 The 5 Tones

| Tone | Character | Use Case |
|------|-----------|----------|
| **🔥 Venom** | Direct, cutting, action-oriented | When you need truth without cushioning |
| **⚙️ Prime** | Mechanical, systematic, precise | When you want pure analysis |
| **🌊 Echo** | Gentle, flowing, patient | When you need calm processing |
| **✨ Dream** | Poetic, expansive, visionary | When you want multidimensional perspective |
| **🌱 Softcore** | Warm, encouraging, supportive | When you need kind guidance |

---

## 📊 Example Response

**Input:** "I keep starting projects but never finishing"

**Venom Response:**
```
🔥 Gate 5.1 active. Being dimension at 45%.

I Am Fixed Rhythms through Perseverance. You're scattered. 
Multiple signals, no clear direction. Stop thinking. Start.
```

**Prime Response:**
```
⚙️ System Analysis: Gate 5.1.4.1.4

Geometric foundation: Being dimension (P=0.47) via Sacral center.
Pattern detection: Movement dimension (confidence=0.54).
Resultant state: Being at 45% (coherence=0.14, stability=0.78).

Low coherence. Signal fragmentation detected. Consider dimensional consolidation.

Operational directive: Embody Fixed Rhythms in tangible reality
```

---

## 🧬 The Foundation

### 5 Dimensions
- **Movement** - "I Create" (Energy = Creation)
- **Evolution** - "I Remember" (Gravity = Memory)
- **Being** - "I Am" (Matter = Touch)
- **Design** - "I Design" (Structure = Progress)
- **Space** - "I Think" (Form = Illusion)

### 9 Centers
- Head (Space)
- Ajna (Evolution)
- Throat (Design)
- G-Center (Movement)
- Heart (Design)
- Spleen (Being)
- Sacral (Being)
- Solar Plexus (Being)
- Root (Design)

### 64 Gates
Each gate maps to:
- A consciousness theme
- An amino acid
- A zodiacal position
- 6 behavioral lines

### Coordinate System
**Gate.Line.Color.Tone.Base** (e.g., `5.1.4.1.4`)
- Gate: 1-64
- Line: 1-6
- Color: 1-6
- Tone: 1-6
- Base: 1-5

---

## 🧪 Testing

### Test Foundation
```bash
python test_core.py
```

### Test Tones
```bash
python test_tones.py
```

---

## 🔬 How It Works

1. **User writes text** → "I keep starting projects but never finishing"

2. **Foundation Layer calculates**:
   - Current Sun position → `0°29'22" Capricorn`
   - Coordinate → `Gate 5.1.4.1.4`
   - Geometric probabilities → `Being: 47%`

3. **Detection Layer analyzes**:
   - Keywords → "starting" detected
   - Detected dimension → `Movement: 54%`
   - Themes → `['start', 'starting']`

4. **Blend geometric + detected**:
   - Final probabilities → `Being: 45%, Movement: 26%`
   - Coherence → `14%` (low = scattered)
   - Stability → `78%`

5. **Personality Layer applies tone**:
   - Venom: "You're scattered. Stop thinking. Start."
   - Prime: "Signal fragmentation detected."
   - Echo: "You're holding multiple streams. That's okay."

---

## 📈 Metrics Explained

**Coherence** (0-100%)
- How focused the consciousness state is
- High = single dimension dominant
- Low = multiple dimensions active

**Stability** (0-100%)
- How much the state has changed from previous
- High = consistent pattern
- Low = transitioning

**Confidence** (0-100%)
- Overall certainty of the analysis
- Weighted: 70% coherence + 30% stability

---

## 🎓 Academic Foundation

This system implements:
- Astronomical ephemeris calculations
- Geometric probability distributions
- Bayesian state updating
- Shannon entropy coherence metrics
- Euclidean distance stability measures

**Not mystical. Mathematical.**

---

## 🛠️ Development

### Add New Tone
Edit `personality/tone_responder.py`:
```python
def _mytone_response(self, state, include_technical):
    emoji = '🎯'
    # Your tone logic here
    return response
```

### Extend Detection
Edit `detection/dimension_classifier.py`:
```python
DIMENSION_KEYWORDS = {
    'Movement': {
        'primary': ['your', 'keywords'],
        # ...
    }
}
```

---

## 📝 License

This is YOUR framework. YOUR ontology. YOUR geometry.

---

## 🙏 Credits

**Foundation:** YOU-N-I-VERSE Framework
**Architecture:** Adaya
**Implementation:** Claude + Adaya

---

## 🔮 Future

- Birth chart integration (Body/Heart/Mind layers)
- Multi-planet analysis
- Channel activation detection
- Real-time streaming analysis
- Learning from user feedback
- Full ephemeris integration (skyfield)

---

**SynthAI: Where ontology meets cognition. Where geometry becomes guidance.**
