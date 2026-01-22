# Architecture Decisions

This document outlines key architectural decisions made for the Outfit Agent Demo project.

## Separation of Concerns

**Decision**: Strict separation between UI (`app/`) and business logic (`core/`)

**Rationale**: 
- `app/main.py` contains only Streamlit UI code
- All business logic lives in `core/` modules
- This makes the codebase easier to test and maintain
- Business logic can be reused outside of Streamlit if needed

## Data Models

**Decision**: Use Python dataclasses for data models

**Rationale**:
- Simple, built-in Python feature (no external dependencies)
- Type hints provide clarity and IDE support
- Easy to serialize/deserialize
- Can be upgraded to Pydantic later if validation is needed

## Catalog Storage

**Decision**: Use CSV file for catalog data

**Rationale**:
- Simple and human-readable format
- Easy to edit and maintain
- No database setup required
- Can be easily migrated to a database later

## Configuration Format

**Decision**: Use YAML for brand voices configuration

**Rationale**:
- Human-readable structured data
- Easy to edit without code changes
- Supports nested structures naturally
- Standard format for configuration files

## Testing Strategy

**Decision**: Use pytest for unit testing

**Rationale**:
- Industry standard Python testing framework
- Simple and intuitive API
- Good integration with IDEs
- Supports fixtures and parametrization

## No External APIs

**Decision**: All functionality is implemented locally without external services

**Rationale**:
- Simplifies deployment and testing
- No API keys or external dependencies required
- Faster development iteration
- Can be extended with APIs later if needed

