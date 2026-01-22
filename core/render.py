"""Rendering utilities for outfits."""
from typing import List
from .models import Outfit, Item

BRAND_VOICE = {
    "brand_name": "YourBrand",
    "tone": "confident, modern, concise",
    "signature_phrases": ["clean lines", "elevated essentials", "effortless style"]
}

def render_outfit_description(outfit: Outfit, requirements: dict | None = None) -> str:
    """
    Generate a text description of an outfit.
    
    Args:
        outfit: The outfit to describe
        
    Returns:
        Formatted description string
    """
    if not outfit.items:
        return "Empty outfit"
    
    item_descriptions = []
    for item in outfit.items:
        item_desc = f"{item.name} ({item.brand}, {item.color_family}, ${item.price})"
        item_descriptions.append(item_desc)
    
    occasion = (requirements or {}).get("occasion") or "the moment"
    seasonality = (requirements or {}).get("seasonality") or "all-seasons"

    opener = (
            f"{BRAND_VOICE['signature_phrases'][0].title()} meet "
            f"{BRAND_VOICE['signature_phrases'][2]}—"
            f"built for {occasion} in {seasonality}."
    )

    description = f"{opener}\n\n{outfit.description}\n\nItems:\n"
    description += "\n".join(f"- {desc}" for desc in item_descriptions)
    
    ## Why this works
    if requirements:
        reasons = []

        # Occasion
        if requirements.get("occassion"):
            reasons.append(f"Alligned to occassion: {requirements['occasion']}")

        # Season / warmth
        if requirements.get("seasonality"):
            reasons.append(f"Season-ready for {requirements['seasonality']}.")

        # Formality
        if requirements.get("formality_target") is not None:
            reasons.append(f"Formality targeted around {requirements['formality_target']}/5.")

        # Colors / palette
        if requirements.get("colors"):
            reasons.append(f"Color direction: {', '.join(requirements['colors'])}.")

        if reasons:
            description += "\n\nWhy this works:\n"
            description += "\n".join(f"- {r}" for r in reasons)


    if outfit.score is not None:
        description += f"\n\nScore: {outfit.score:.2f}"
    
    return description


def render_outfit_summary(outfit: Outfit) -> str:
    """
    Generate a short summary of an outfit.
    
    Args:
        outfit: The outfit to summarize
        
    Returns:
        Short summary string
    """
    if not outfit.items:
        return "No items"
    
    categories = [item.category for item in outfit.items]
    total_price = sum(item.price for item in outfit.items)
    
    summary = f"{len(outfit.items)} items"
    if categories:
        summary += f" ({', '.join(set(categories))})"
    summary += f" - ${total_price:.2f}"
    
    return summary

