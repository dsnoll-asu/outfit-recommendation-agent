# Outfit Agent Demo

A Streamlit-based application for assembling and recommending outfits based on user requirements and preferences.

## Project Structure

```
outfit-agent-demo/
  app/
    main.py              # Main Streamlit UI entry point
    ui_components.py     # Reusable UI components
  core/
    models.py            # Data models (Item, Outfit, BrandVoice)
    catalog.py           # Catalog management
    extract.py           # Extract requirements/preferences from text
    score.py             # Outfit scoring logic
    assemble.py          # Outfit assembly logic
    render.py            # Outfit rendering utilities
    demo_prompts.py      # Demo prompts for testing
  data/
    catalog.csv          # Clothing item catalog
    brand_voices.yaml    # Brand style guidelines
    images/              # Item images directory
  tests/
    test_extract.py      # Tests for extract module
    test_assemble.py     # Tests for assemble module
```

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the Streamlit app:

```bash
streamlit run app/main.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Usage

1. Enter your outfit requirements in the text area (e.g., "Create a casual outfit for a weekend brunch")
2. Click "Generate Outfits" to see recommendations
3. Use the demo prompts in the sidebar to try example queries

## Running Tests

To run the test suite:

```bash
pytest tests/
```

To run with verbose output:

```bash
pytest tests/ -v
```

## Architecture

- **UI Layer** (`app/`): Contains only UI logic and Streamlit components
- **Business Logic** (`core/`): All application logic is separated from UI
- **Data Models**: Uses Python dataclasses for type-safe data structures
- **Data**: CSV catalog and YAML configuration files

## Development

The project follows a clean architecture pattern:
- UI components are in `app/ui_components.py`
- Business logic is in `core/` modules
- Data models are defined in `core/models.py`
- No external APIs or services are used (all logic is local)

