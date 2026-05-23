"""
Planetary frequency calculator.

Theory:
  - Pythagoras: 12 zodiac signs = 12 chromatic semitones.
    Three sacred intervals: perfect fifth (3:2), perfect fourth (4:3), octave (2:1).
  - Hans Cousto (1978): planetary base frequencies from orbital periods via octave transposition.
  - Formula: freq = base * 2^(semitone/12) * 2^(degree/29/12)
  - Tuning: 432 Hz
"""

import ssl, certifi, os
os.environ['SSL_CERT_FILE']      = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

from kerykeion import AstrologicalSubject
from timezonefinder import TimezoneFinder
import math

# Planetary base frequencies (Hans Cousto, 1978)
PLANET_BASE_FREQ = {
    "Sun":     126.22, "Moon":    210.42, "Mercury": 141.27,
    "Venus":   221.23, "Earth":   194.18, "Mars":    144.72,
    "Jupiter": 183.58, "Saturn":  147.85, "Uranus":  207.36,
    "Neptune": 211.44, "Pluto":   140.25,
}

# Orbital periods in days
PLANET_PERIODS = {
    "Sun":     365.25,  "Moon":     27.32,  "Mercury":  87.97,
    "Venus":   224.70,  "Mars":    686.97,  "Jupiter": 4332.59,
    "Saturn": 10759.22, "Uranus": 30688.50, "Neptune": 60182.00,
    "Pluto":  90560.00,
}

# 12 zodiac signs = 12 chromatic semitones (Pythagoras)
SIGN_SEMITONE = {
    "Ari":0, "Tau":1, "Gem":2, "Can":3,
    "Leo":4, "Vir":5, "Lib":6, "Sco":7,
    "Sag":8, "Cap":9, "Aqu":10,"Pis":11,
}

SIGN_FULL_NAME = {
    "Ari": "Aries",       "Tau": "Taurus",      "Gem": "Gemini",
    "Can": "Cancer",      "Leo": "Leo",          "Vir": "Virgo",
    "Lib": "Libra",       "Sco": "Scorpio",      "Sag": "Sagittarius",
    "Cap": "Capricorn",   "Aqu": "Aquarius",     "Pis": "Pisces",
}

PLANET_COLOR = {
    "Sun":    (255,200, 50), "Moon":   (200,210,255),
    "Mercury":(180,180,200), "Venus":  (255,180,120),
    "Mars":   (220, 80, 60), "Jupiter":(200,160,100),
    "Saturn": (210,190,130), "Uranus": (100,220,210),
    "Neptune":( 60,100,220), "Pluto":  (140, 60,180),
}

# 432 Hz tuning (Cousto). Standard A=440 Hz was adopted in 1939.
TUNING_432 = 432 / 440


def calc_freq(planet: str, sign: str, degree: float) -> float:
    """
    Pythagorean chromatic frequency:
      freq = base * 2^(semitone/12) * 2^(degree/29/12) * (432/440)
    """
    base     = PLANET_BASE_FREQ[planet]
    semitone = SIGN_SEMITONE.get(sign[:3], 0)
    freq     = base * (2**(semitone/12)) * (2**(degree/29/12))
    return round(freq * TUNING_432, 2)


def calc_bpm(planet: str) -> float:
    """Orbital period → BPM via octave transposition (same method as frequencies)."""
    bpm = (1.0 / PLANET_PERIODS[planet]) * 1440
    while bpm < 0.5: bpm *= 2
    while bpm > 120: bpm /= 2
    return bpm


def resolve_timezone(lat: float, lng: float) -> str:
    """Coordinates → IANA timezone string via local shapefile (no network)."""
    tz = TimezoneFinder().timezone_at(lat=lat, lng=lng)
    if not tz:
        raise ValueError(f"Could not determine timezone for coordinates ({lat}, {lng}).")
    return tz


def build_chart(year, month, day, hour, minute, lat: float, lng: float) -> dict:
    """Build a natal chart and return planetary frequencies for all 10 planets."""
    tz = resolve_timezone(lat, lng)
    subj = AstrologicalSubject(
        "chart", year, month, day, hour, minute,
        lng=lng, lat=lat, tz_str=tz
    )
    raw = {
        "Sun":     subj.sun,     "Moon":    subj.moon,
        "Mercury": subj.mercury, "Venus":   subj.venus,
        "Mars":    subj.mars,    "Jupiter": subj.jupiter,
        "Saturn":  subj.saturn,  "Uranus":  subj.uranus,
        "Neptune": subj.neptune, "Pluto":   subj.pluto,
    }
    chart = {}
    for name, obj in raw.items():
        deg       = float(obj.position)
        sign_abbr = obj.sign[:3]
        sign      = SIGN_FULL_NAME.get(sign_abbr, sign_abbr)
        chart[name] = {
            "freq":  calc_freq(name, sign_abbr, deg),
            "bpm":   calc_bpm(name),
            "sign":  sign,
            "deg":   deg,
            "color": PLANET_COLOR[name],
        }
    return chart
