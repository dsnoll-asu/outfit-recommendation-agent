"""Extract requirements and preferences from user input (deterministic)."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple


# ----------------------------
# Keyword maps (edit freely)
# ----------------------------

OCCASION_KEYWORDS = {
    "work": ["work", "office", "meeting", "presentation", "interview", "client", "conference"],
    "date": ["date", "dinner", "night out", "restaurant"],
    "casual": ["casual", "weekend", "brunch", "coffee", "errands", "hangout"],
    "formal": ["formal", "black tie", "gala", "wedding", "cocktail", "event"],
    "travel": ["travel", "airport", "flight", "plane", "hotel", "vacation"],
    "outdoors": ["outdoor", "hike", "trail", "camp", "festival"],
}

STYLE_KEYWORDS = {
    "minimal": ["minimal", "clean", "simple", "sleek", "pared-back"],
    "tailored": ["tailored", "structured", "sharp", "polished", "blazer"],
    "classic": ["classic", "timeless", "preppy", "heritage"],
    "streetwear": ["streetwear", "oversized", "graphic", "sneaker", "hoodie"],
    "boho": ["boho", "bohemian", "flowy", "floral"],
    "edgy": ["edgy", "leather", "black", "punk"],
    "sporty": ["sporty", "athleisure", "active", "gym", "running"],
}

COLOR_KEYWORDS = {
    "black": ["black"],
    "white": ["white", "ivory"],
    "navy": ["navy"],
    "gray": ["gray", "grey", "charcoal"],
    "beige": ["beige", "tan", "camel", "khaki"],
    "brown": ["brown", "chocolate"],
    "red": ["red", "burgundy", "maroon"],
    "green": ["green", "olive", "sage"],
    "blue": ["blue", "cobalt"],
    "pink": ["pink", "fuchsia"],
    "purple": ["purple", "lavender"],
    "yellow": ["yellow", "mustard"],
    "orange": ["orange", "rust"],
}

PALETTE_KEYWORDS = {
    "monochrome": ["monochrome", "all black", "all-white", "one color"],
    "neutrals": ["neutral", "neutrals", "tonal", "earth tones"],
    "colorful": ["colorful", "bright", "bold color", "vibrant"],
}

# Weather/season signals → we map these to "seasonality" and/or "warmth"
SEASON_KEYWORDS = {
    "winter": ["winter", "cold", "snow", "freezing", "chilly"],
    "summer": ["summer", "hot", "heat", "humid"],
    "spring": ["spring"],
    "fall": ["fall", "autumn", "crisp"],
    "rainy": ["rain", "rainy", "drizzle", "wet"],
}

EXCLUSION_KEYWORDS = {
    "no_heels": ["no heels", "without heels", "no high heels"],
    "no_denim": ["no denim", "without denim"],
    "no_leather": ["no leather", "vegan"],
}


# ----------------------------
# Helpers
# ----------------------------

def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _match_any(text: str, keywords: List[str]) -> bool:
    return any(k in text for k in keywords)


def _extract_first_match(text: str, mapping: Dict[str, List[str]]) -> str:
    for label, keywords in mapping.items():
        if _match_any(text, keywords):
            return label
    return ""


def _extract_multi_matches(text: str, mapping: Dict[str, List[str]]) -> List[str]:
    matches: List[str] = []
    for label, keywords in mapping.items():
        if _match_any(text, keywords):
            matches.append(label)
    return matches


def _extract_budget(text: str) -> Optional[Tuple[Optional[float], Optional[float]]]:
    """
    Extract a budget or price range. Supports:
      - "$150"
      - "under $200" / "below 200"
      - "$100-$250" / "100 to 250"
    Returns (min_price, max_price)
    """
    t = text

    # Range: $100-$250 or 100-250 or 100 to 250
    m = re.search(r"\$?\s*(\d{2,5})\s*(?:-|to)\s*\$?\s*(\d{2,5})", t)
    if m:
        return (float(m.group(1)), float(m.group(2)))

    # Under / below
    m = re.search(r"(?:under|below|less than)\s*\$?\s*(\d{2,5})", t)
    if m:
        return (None, float(m.group(1)))

    # Single dollar amount: "$150"
    m = re.search(r"\$\s*(\d{2,5})", t)
    if m:
        val = float(m.group(1))
        return (None, val)

    return None


def _extract_temperature_f(text: str) -> Optional[int]:
    """
    Extract a Fahrenheit temperature like 45F, 45°F, 45 degrees.
    """
    m = re.search(r"(\d{2,3})\s*°?\s*f\b", text)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d{2,3})\s*degrees", text)
    if m:
        return int(m.group(1))
    return None


def _temperature_to_warmth(temp_f: int) -> int:
    """
    Convert temp to warmth rating 1-5 (rough heuristic).
    """
    if temp_f <= 35:
        return 5
    if temp_f <= 50:
        return 4
    if temp_f <= 65:
        return 3
    if temp_f <= 80:
        return 2
    return 1


# ----------------------------
# Public API
# ----------------------------

def extract_requirements(text: str) -> Dict[str, Any]:
    """
    Extract outfit requirements from user text input.

    Returns dict with fields that downstream logic can rely on:
      - occasion: str (e.g., "work", "date", "casual", "formal", ...)
      - seasonality: str (winter/summer/spring/fall/rainy/"")
      - min_warmth: Optional[int]  (1-5)
      - formality_target: Optional[int] (1-5)
      - required_categories: List[str] (optional; usually empty)
      - colors: List[str] (color_family values)
      - exclusions: List[str] (e.g., ["no_heels"])
      - budget: Optional[Tuple[min,max]]
    """
    t = _normalize(text)

    occasion = _extract_first_match(t, OCCASION_KEYWORDS)
    seasonality = _extract_first_match(t, SEASON_KEYWORDS)

    colors = _extract_multi_matches(t, COLOR_KEYWORDS)
    exclusions = _extract_multi_matches(t, EXCLUSION_KEYWORDS)

    temp_f = _extract_temperature_f(t)
    min_warmth: Optional[int] = _temperature_to_warmth(temp_f) if temp_f is not None else None

    # Simple formality heuristic: map occasion/style terms to a target formality 1–5
    formality_target: Optional[int] = None
    if occasion in ("formal",):
        formality_target = 5
    elif occasion in ("work", "date"):
        formality_target = 4
    elif occasion in ("travel",):
        formality_target = 2
    elif occasion in ("casual", "outdoors"):
        formality_target = 2

    budget = _extract_budget(t)

    requirements: Dict[str, Any] = {
        "occasion": occasion,
        "seasonality": seasonality,
        "min_warmth": min_warmth,
        "formality_target": formality_target,
        "required_categories": [],  # optional future extension
        "colors": colors,
        "exclusions": exclusions,
        "budget": budget,
    }
    return requirements


def extract_preferences(text: str) -> Dict[str, Any]:
    """
    Extract user preferences from text input.

    Returns dict with fields aligned to typical catalog tagging:
      - style_cues: List[str] (e.g., ["minimal", "tailored"])
      - palette: str ("monochrome"/"neutrals"/"colorful"/"")
      - preferred_colors: List[str]
      - avoid_colors: List[str]
      - avoid_tags: List[str] (optional)
    """
    t = _normalize(text)

    style_cues = _extract_multi_matches(t, STYLE_KEYWORDS)
    palette = _extract_first_match(t, PALETTE_KEYWORDS)

    preferred_colors = _extract_multi_matches(t, COLOR_KEYWORDS)

    # Basic "avoid color" parsing (optional but useful)
    avoid_colors: List[str] = []
    m = re.search(r"(?:avoid|no)\s+([a-z\s]+)", t)
    if m:
        phrase = m.group(1)
        avoid_colors = _extract_multi_matches(phrase, COLOR_KEYWORDS)

    preferences: Dict[str, Any] = {
        "style_cues": style_cues,
        "palette": palette,
        "preferred_colors": preferred_colors,
        "avoid_colors": avoid_colors,
        "avoid_tags": [],  # optional future extension
    }
    return preferences
