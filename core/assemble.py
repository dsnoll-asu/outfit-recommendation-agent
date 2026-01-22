"""Assemble outfits from catalog items."""
import random
from typing import List, Dict
from .models import Outfit, Item
from .catalog import Catalog


def assemble_outfits(catalog: Catalog, requirements: Dict[str, any], max_outfits: int = 5) -> List[Outfit]:
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
    all_items = filter_items_by_requirements(catalog.get_all_items(), requirements)
    
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
    shoes = items_by_category.get("shoe", []) + items_by_category.get("shoes", [])
    outerwear = items_by_category.get("outerwear", [])
    accessories = items_by_category.get("accessory", [])

    outfit_count = 0

    seasonality = requirements.get("seasonality", "").lower()
    min_warmth = requirements.get("min_warmth")
    needs_outerwear = (seasonality == "winter") or (isinstance(min_warmth, int) and min_warmth >= 4)
    is_summer = seasonality == "summer"
    is_hot = seasonality == "summer" or (isinstance(min_warmth, int) and min_warmth <= 2)
    is_casual = (requirements.get("occasion") or "").lower() == "casual" or (requirements.get("style") or "").lower() == "casual"
    used_top_ids = set()
    used_shoe_ids = set()
    used_accessory_ids = set()

    bottoms = items_by_category.get("bottom", [])

    # Prefer summer-appropriate bottoms when hot weather
    bottoms_pref = None
    if bottoms and is_hot:
        bottoms_pref = []
        for b in bottoms:
            b_season = (getattr(b, "seasonality", "all") or "all").lower()
            b_warmth = getattr(b, "warmth", 1)
            # Check for "spring | summer" format too
            if "summer" in b_season or (b_season in {"all", "spring"} and isinstance(b_warmth, int) and b_warmth <= 2):
                bottoms_pref.append(b)
        if not bottoms_pref:
            bottoms_pref = None

    # Prefer casual-tagged bottoms when casual occasion
    if is_casual and bottoms:
        casual_bottoms = [b for b in bottoms if "casual" in getattr(b, "occasion_tags", [])]
        if casual_bottoms:
            bottoms = casual_bottoms

    # Prefer casual-tagged tops when casual occasion
    if is_casual and tops:
        casual_tops = [t for t in tops if "casual" in getattr(t, "occasion_tags", [])]
        if casual_tops:
            tops = casual_tops

    # Prefer summer-appropriate tops when hot weather
    tops_pref = None
    if tops and is_hot:
        tops_pref = []
        for t in tops:
            t_season = (getattr(t, "seasonality", "all") or "all").lower()
            t_warmth = getattr(t, "warmth", 1)
            if "summer" in t_season or (t_season in {"all", "spring"} and isinstance(t_warmth, int) and t_warmth <= 2):
                tops_pref.append(t)
        if not tops_pref:
            tops_pref = None



    for i in range(max_outfits):
        
        outfit_items = []

        # Base: top + bottom
        if tops and bottoms:
            # Pick a top not used yet (if possible), prefer summer-appropriate when hot
            top_list = tops_pref if tops_pref else tops
            top_choice = None
            for t in top_list:
                if t.id not in used_top_ids:
                    top_choice = t
                    break
            if top_choice is None:
                top_choice = top_list[i % len(top_list)]

            used_top_ids.add(top_choice.id)
            outfit_items.append(top_choice)

            # Prefer summer-appropriate bottoms when hot
            bottom_list = bottoms_pref if bottoms_pref else bottoms
            outfit_items.append(bottom_list[i % len(bottom_list)])
        elif tops:
            outfit_items.append(tops[i % len(tops)])
        else:
            continue 
        # Add outerwear only when cold
        if needs_outerwear and outerwear:
            outfit_items.append(outerwear[i % len(outerwear)])

        # Add shoes if available
        if shoes:
            shoe_choice = shoes[i % len(shoes)]
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

            seed_text = f"{requirements.get("style", "")}-{requirements.get("occasion", "")}-{requirements.get("_seed", "")}"
            rng = random.Random(seed_text)

            for k in items_by_category:
                rng.shuffle(items_by_category[k])


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
    """
    filtered = items

    style = (requirements.get("style") or "").lower()
    occasion = (requirements.get("occasion") or "").lower()
    seasonality = (requirements.get("seasonality") or "").lower()

    is_casual = (style == "casual") or (occasion == "casual")
    is_summer = (seasonality == "summer")

    # 1) Filter by category if specified
    if requirements.get("categories"):
        cats = set([c.lower() for c in requirements["categories"]])
        filtered = [item for item in filtered if (item.category or "").lower() in cats]

    # 2) Filter by color_family if specified
    if requirements.get("colors"):
        req_colors = [c.lower() for c in requirements["colors"]]
        filtered = [
            item for item in filtered
            if (getattr(item, "color_family", "") or "").lower() in req_colors
        ]

    # 3) Summer + casual: prefer shorts-like bottoms (low warmth, summer/all)
    if is_summer and is_casual:
        hot_bottoms = []
        for item in filtered:
            if (item.category or "").lower() != "bottom":
                continue

            try:
                w = int(getattr(item, "warmth", 3))
            except Exception:
                w = 3

            seas = (getattr(item, "seasonality", "all") or "all").lower()
            if w <= 2 and seas in {"summer", "all"}:
                hot_bottoms.append(item)

        # If we found any shorts-like bottoms, remove other bottoms
        if hot_bottoms:
            non_bottoms = [x for x in filtered if (x.category or "").lower() != "bottom"]
            filtered = non_bottoms + hot_bottoms

    # 4) Casual: prefer casual shoes (low formality)
    if is_casual:
        casual_shoes = []
        for item in filtered:
            if (item.category or "").lower() != "shoe":
                continue
            try:
                f = int(getattr(item, "formality", 3))
            except Exception:
                f = 3
            if f <= 2:
                casual_shoes.append(item)

        if casual_shoes:
            non_shoes = [x for x in filtered if (x.category or "").lower() != "shoe"]
            filtered = non_shoes + casual_shoes

        # 5) Casual: remove "tie" and ultra-formal accessories (if you have them)
        tightened = []
        for item in filtered:
            if (item.category or "").lower() == "accessory":
                name = (item.name or "").lower()
                try:
                    f = int(getattr(item, "formality", 3))
                except Exception:
                    f = 3
                if "tie" in name or f >= 5:
                    continue
            tightened.append(item)
        filtered = tightened

    return filtered

