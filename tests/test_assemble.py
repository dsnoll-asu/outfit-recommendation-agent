"""Tests for assemble module."""
import pytest
from core.assemble import assemble_outfits, filter_items_by_requirements
from core.catalog import Catalog
from core.models import Item


def test_assemble_outfits_empty_catalog():
    """Test assembling outfits with empty catalog."""
    catalog = Catalog()
    catalog.items = []  # Ensure empty
    
    requirements = {"style": "casual"}
    outfits = assemble_outfits(catalog, requirements)
    
    assert isinstance(outfits, list)
    assert len(outfits) == 0


def test_assemble_outfits_with_items():
    """Test assembling outfits with items in catalog."""
    catalog = Catalog()
    catalog.items = [
        Item(id="1", name="Shirt", category="shirt", brand="A", color="white", size="M", price=29.99),
        Item(id="2", name="Pants", category="pants", brand="B", color="blue", size="M", price=49.99),
    ]
    
    requirements = {"style": "casual"}
    outfits = assemble_outfits(catalog, requirements, max_outfits=3)
    
    assert isinstance(outfits, list)
    assert len(outfits) > 0
    assert all(outfit.items for outfit in outfits)


def test_filter_items_by_requirements_category():
    """Test filtering items by category."""
    items = [
        Item(id="1", name="Shirt", category="shirt", brand="A", color="white", size="M", price=29.99),
        Item(id="2", name="Pants", category="pants", brand="B", color="blue", size="M", price=49.99),
        Item(id="3", name="Dress", category="dress", brand="C", color="red", size="S", price=59.99),
    ]
    
    requirements = {"categories": ["shirt", "pants"]}
    filtered = filter_items_by_requirements(items, requirements)
    
    assert len(filtered) == 2
    assert all(item.category in ["shirt", "pants"] for item in filtered)


def test_filter_items_by_requirements_color():
    """Test filtering items by color."""
    items = [
        Item(id="1", name="Shirt", category="shirt", brand="A", color="white", size="M", price=29.99),
        Item(id="2", name="Pants", category="pants", brand="B", color="blue", size="M", price=49.99),
        Item(id="3", name="Dress", category="dress", brand="C", color="red", size="S", price=59.99),
    ]
    
    requirements = {"colors": ["white", "blue"]}
    filtered = filter_items_by_requirements(items, requirements)
    
    assert len(filtered) == 2
    assert all(item.color.lower() in ["white", "blue"] for item in filtered)

