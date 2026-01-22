"""Data models for the outfit agent application."""
from dataclasses import dataclass, field 
from typing import Optional, List


@dataclass
class Item:
    """Represents a clothing item."""
    id: str
    name: str
    category: str
    brand: str
    color_family: str
    price: float
    style_tags: List[str] = field(default_factory=list)    
    occasion_tags: List[str] = field(default_factory=list) 
    seasonality: str = "all"               
    warmth: int = 3                        
    formality: int = 3                     
    image_path: Optional[str] = None


@dataclass
class Outfit:
    """Represents a complete outfit."""
    id: str
    items: List[Item]
    description: str
    score: Optional[float] = None


@dataclass
class BrandVoice:
    """Represents brand voice/style guidelines."""
    brand: str
    style: str
    colors: List[str]
    description: str

