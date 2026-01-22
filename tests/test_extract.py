"""Tests for extract module."""
import pytest
from core.extract import extract_requirements, extract_preferences


def test_extract_requirements_casual():
    """Test extracting casual style requirements."""
    text = "I need a casual outfit for the weekend"
    requirements = extract_requirements(text)
    
    assert "style" in requirements
    assert requirements["style"] == "casual"


def test_extract_requirements_formal():
    """Test extracting formal style requirements."""
    text = "Create a formal outfit for a business meeting"
    requirements = extract_requirements(text)
    
    assert "style" in requirements
    assert requirements["style"] == "formal"


def test_extract_requirements_occasion():
    """Test extracting occasion requirements."""
    text = "I need an outfit for work"
    requirements = extract_requirements(text)
    
    assert "occasion" in requirements
    assert requirements["occasion"] == "work"


def test_extract_preferences():
    """Test extracting user preferences."""
    text = "I prefer blue colors and BrandA"
    preferences = extract_preferences(text)
    
    assert "preferred_colors" in preferences
    assert "preferred_brands" in preferences
    assert isinstance(preferences["preferred_colors"], list)
    assert isinstance(preferences["preferred_brands"], list)


def test_extract_requirements_empty():
    """Test extracting requirements from empty text."""
    text = ""
    requirements = extract_requirements(text)
    
    assert isinstance(requirements, dict)
    assert "style" in requirements
    assert "occasion" in requirements

