"""Assemble outfits from catalog items."""
from tty import setcbreak
from typing import List, Dict
from .models import Outfit, Item
from .catalog import Catalog


def assemble_outfits(catalog: Catalog, requirements: Dict[str, any], max_outfits: int = 5, min_outfits: int = 3) -> List[Outfit]:
    """
    Assemble outfits based on requirements.
    
    Args:
        catalog: Catalog of available items
        requirements: Extracted requirements
        max_outfits: Maximum number of outfits to generate
        
    Returns:
        List of assembled outfits
    """
    outfits = []
    all_items = catalog.get_all_items()
    
    # Placeholder implementation - create simple outfits
    if len(all_items) == 0:
        return outfits
    
    # Group items by category
    items_by_category = {}
    for item in all_items:
        if item.category not in items_by_category:
            items_by_category[item.category] = []
        items_by_category[item.category].append(item)
    
    # Create basic outfits (one item per category, if available)
    # Build real outfits: (dress OR top+bottom) + shoes
    tops = items_by_category.get("top", [])
    bottoms = items_by_category.get("bottom", [])
    shoes = items_by_category.get("shoe", [])
    outerwear = items_by_category.get("outerwear", [])
    accessories = items_by_category.get("accessory", [])

    outfit_count = 0

    seasonality = requirements.get("seasonality", "").lower()
    min_warmth = requirements.get("min_warmth")
    needs_outerwear = (seasonality == "winter") or (isinstance(min_warmth, int) and min_warmth >= 4)
    used_top_ids = set()
    used_shoe_ids = set()
    used_accessory_ids = set()



    for i in range(max_outfits):
        
        outfit_items = []

        # Base: top + bottom
        if tops and bottoms:
            # Pick a top not used yet (if possible)
            top_choice = None
            for t in tops:
                if t.id not in used_top_ids:
                    top_choice = t
                    break
            if top_choice is None:
                top_choice = tops[i % len(tops)]

            used_top_ids.add(top_choice.id)
            outfit_items.append(top_choice)

            outfit_items.append(bottoms[i % len(bottoms)])
        elif tops:
            outfit_items.append(tops[i % len(tops)])
        else:
            break  # nothing to build with
        # Add outerwear only when cold
        if needs_outerwear and outerwear:
            outfit_items.append(outerwear[i % len(outerwear)])

        # Add shoes if available
        if shoes:
            shoe_choice = None
            for s in shoes:
                if s.id not in used_shoe_ids:
                    shoe_choice = s 
                    break
                if shoe_choice is None:
                    shoe_choice = shoes[i % len(shoes)]

                used_shoe_ids.add(shoe_choice.id)
                outfit_items.append(shoe_choice)


        # Add at most one accessory (optional) — only on some outfits, avoid repeats
        if accessories and (i % 2 == 0):
            accessory_choice = None
            for a in accessories:
                if a.id not in used_accessory_ids:
                    accessory_choice = a
                    break
            if accessory_choice is None:
                accessory_choice = accessories[i % len(accessories)]  # fallback
                
            used_accessory_ids.add(accessory_choice.id)
            outfit_items.append(accessory_choice)

        outfit = Outfit(
            id=f"outfit_{outfit_count + 1}",
            items=outfit_items,
            description=f"Outfit {outfit_count + 1} with {len(outfit_items)} items"
        )
        outfits.append(outfit)
        outfit_count += 1

    return outfits


def filter_items_by_requirements(items: List[Item], requirements: Dict[str, any]) -> List[Item]:
    """
    Filter items based on requirements.
    
    Args:
        items: List of items to filter
        requirements: Requirements dictionary
        
    Returns:
        Filtered list of items
    """
    filtered = items
    
    # Filter by category if specified
    if requirements.get("categories"):
        filtered = [item for item in filtered if item.category in requirements["categories"]]
    
    # Filter by color if specified
    if requirements.get("colors"):
        req_colors = [c.lower() for c in requirements["colors"]]
        filtered = [
            item for item in filtered 
            if (getattr(item, "color_family", "") or "").lower() in req_colors
        ]
    return filtered

