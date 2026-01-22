"""Scoring logic for outfit evaluation (metadata-driven)."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple
from .models import Outfit, Item


WEIGHTS = {
    "completeness": 0.05,
    "occasion": 0.15,
    "style": 0.25,
    "color": 0.15,
    "seasonality": 0.15,
    "warmth": 0.10,
    "formality": 0.15,
}

NEUTRALS = {"black", "white", "gray", "navy", "beige", "brown"}


def _as_list(x: Any) -> List[str]:
    if not x:
        return []
    if isinstance(x, list):
        return [str(v).strip().lower() for v in x if v]
    # if tags accidentally come in as "a|b|c"
    if isinstance(x, str) and "|" in x:
        return [p.strip().lower() for p in x.split("|") if p.strip()]
    return [str(x).strip().lower()]


def _get(item: Item, attr: str, default: Any = None) -> Any:
    return getattr(item, attr, default)


def _tag_overlap_score(item_tags: List[str], target_tags: List[str]) -> float:
    """0..1 based on fraction of target tags matched by the item."""
    if not target_tags:
        return 0.0
    i = set(item_tags)
    t = set(target_tags)
    return len(i & t) / max(1, len(t))


def score_item(item: Item, requirements: Dict[str, Any], preferences: Dict[str, Any]) -> Tuple[float, List[str]]:
    reasons: List[str] = []
    score = 0.0
    max_score = 0.0

    # Extracted fields (from your extractor)
    occasion_req = (requirements.get("occasion") or "").strip().lower()
    seasonality_req = (requirements.get("seasonality") or "").strip().lower()
    min_warmth = requirements.get("min_warmth")
    formality_target = requirements.get("formality_target")

    style_cues = _as_list(preferences.get("style_cues"))
    palette = (preferences.get("palette") or "").strip().lower()
    preferred_colors = _as_list(preferences.get("preferred_colors"))
    avoid_colors = _as_list(preferences.get("avoid_colors"))

    # Item metadata (from your catalog/item model)
    item_occ_tags = _as_list(_get(item, "occasion_tags", []))
    item_style_tags = _as_list(_get(item, "style_tags", []))
    item_color_family = (_get(item, "color_family", "") or "").strip().lower()
    item_seasonality = (_get(item, "seasonality", "all") or "all").strip().lower()
    item_warmth = _get(item, "warmth", None)
    item_formality = _get(item, "formality", None)

    # Occasion match (0..1)
    max_score += 1.0
    if occasion_req:
        if occasion_req in item_occ_tags:
            score += 1.0
            reasons.append(f"Occasion tag match: {occasion_req}")

    # Style match (0..1)
    max_score += 1.0
    if style_cues:
        s = _tag_overlap_score(item_style_tags, style_cues)
        score += s
        if s > 0:
            reasons.append(f"Style overlap: {', '.join(sorted(set(item_style_tags) & set(style_cues)))}")

    # Color / palette match (0..1)
    max_score += 1.0
    color_points = 0.0
    if item_color_family:
        if item_color_family in avoid_colors:
            color_points = 0.0
            reasons.append(f"Avoid color: {item_color_family}")
        else:
            if preferred_colors and item_color_family in preferred_colors:
                color_points = 1.0
                reasons.append(f"Preferred color: {item_color_family}")
            elif palette in ("monochrome", "neutrals") and item_color_family in NEUTRALS:
                color_points = 0.7
                reasons.append("Palette fit (neutral/tonal)")
    score += color_points

    # Seasonality match (0..1)
    max_score += 1.0
    if seasonality_req:
        if item_seasonality in (seasonality_req, "all"):
            score += 1.0
            reasons.append(f"Seasonality fit: {item_seasonality}")

    # Warmth match (0..1)
    max_score += 1.0
    if isinstance(min_warmth, int) and isinstance(item_warmth, int):
        if item_warmth >= min_warmth:
            score += 1.0
            reasons.append(f"Warmth meets min: {item_warmth} >= {min_warmth}")
        else:
            score += max(0.0, item_warmth / max(1, min_warmth))

    # Formality closeness (0..1)
    max_score += 1.0
    if isinstance(formality_target, int) and isinstance(item_formality, int):
        diff = abs(item_formality - formality_target)  # 0..4
        score += max(0.0, 1.0 - diff / 4.0)
        reasons.append(f"Formality: {item_formality} vs {formality_target}")

    return (score / max_score if max_score else 0.0), reasons


def score_outfit(outfit: Outfit, requirements: Dict[str, Any], preferences: Dict[str, Any]) -> float:
    if not outfit.items:
        return 0.0

    # Completeness heuristic (encourage base + shoes at minimum)
    categories = [(_get(i, "category", "") or "").lower() for i in outfit.items]
    completeness = 0.0
    if "shoe" in categories:
        completeness += 0.5
    if "dress" in categories or ("top" in categories and "bottom" in categories):
        completeness += 0.5

    # Item-level metadata score
    item_scores: List[float] = []
    reasons: List[str] = []
    for item in outfit.items:
        s, r = score_item(item, requirements, preferences)
        item_scores.append(s)
        reasons.extend(r)

    meta_score = sum(item_scores) / len(item_scores) if item_scores else 0.0

    # Weighted blend
    final = (
        WEIGHTS["completeness"] * completeness
        + (1.0 - WEIGHTS["completeness"]) * meta_score
    )

    # Optional: attach reasons for UI if you want
    if hasattr(outfit, "reasons"):
        setattr(outfit, "reasons", reasons[:12])

    return max(0.0, min(1.0, final))


def rank_outfits(outfits: List[Outfit], requirements: Dict[str, Any], preferences: Dict[str, Any]) -> List[Outfit]:
    for outfit in outfits:
        outfit.score = score_outfit(outfit, requirements, preferences)
    return sorted(outfits, key=lambda x: x.score or 0.0, reverse=True)
