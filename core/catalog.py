"""Catalog management for clothing items."""
import pandas as pd
from pathlib import Path
from typing import List, Optional
from .models import Item


class Catalog:
    """Manages the clothing item catalog."""
    
    def __init__(self, catalog_path: str = None):
        """Initialize catalog from CSV file."""
        if catalog_path is None:
            # Default to data/catalog.csv relative to project root
            project_root = Path(__file__).parent.parent
            catalog_path = project_root / "data" / "catalog.csv"
        self.catalog_path = str(catalog_path)
        self.items: List[Item] = []
        self._load_catalog()
    
    def _load_catalog(self) -> None:
        """Load items from CSV file."""
        try:
            df = pd.read_csv(self.catalog_path)
            self.items = [
                Item(
                    id=str(row.get('item_id', '')),
                    name=str(row.get('name', '')),
                    category=str(row.get('category', '')),
                    brand=str(row.get('brand', '')),
                    color_family=str(row.get('color_family', '')),
                    price=float(row.get('price', 0.0)),
                    style_tags=str(row.get('style_tags', '')).split('|') if str(row.get('style_tags', '')).strip() else [],
                    occasion_tags=str(row.get('occasion_tags', '')).split('|') if str(row.get('occasion_tags', '')).strip() else [],
                    seasonality=str(row.get('seasonality', 'all')),
                    warmth=int(row.get('warmth', 3)) if str(row.get('warmth', '')).strip() else 3,
                    formality=int(row.get('formality', 3)) if str(row.get('formality', "")).strip() else 3,
                    image_path=row.get('image_path')
                )
                for _, row in df.iterrows()
            ]
        except FileNotFoundError:
            # If catalog doesn't exist, start with empty list
            self.items = []
    
    def get_all_items(self) -> List[Item]:
        """Get all items in the catalog."""
        return self.items
    
    def get_item_by_id(self, item_id: str) -> Optional[Item]:
        """Get an item by its ID."""
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def get_items_by_category(self, category: str) -> List[Item]:
        """Get all items in a specific category."""
        return [item for item in self.items if item.category == category]

