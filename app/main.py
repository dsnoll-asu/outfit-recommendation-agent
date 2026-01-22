"""Main Streamlit application entry point."""
import sys
from pathlib import Path

# Ensure repo root is on sys.path so `core` imports work
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

# IMPORTANT: Must be the first Streamlit command, and called only once
st.set_page_config(
    page_title="Outfit Agent Demo",
    page_icon="👔",
    layout="wide"
)

from core.catalog import Catalog
from core.extract import extract_requirements, extract_preferences
from core.assemble import assemble_outfits
from core.score import rank_outfits
from core.demo_prompts import get_demo_prompts
from app.ui_components import render_outfit_list, render_demo_prompts


def main() -> None:
    st.title("👔 Outfit Agent Demo")
    st.write("Describe your outfit needs and we'll help you assemble the perfect look!")

    # Initialize session state
    if "catalog" not in st.session_state:
        st.session_state.catalog = Catalog()

    # Sidebar for demo prompts
    with st.sidebar:
        st.header("Demo Prompts")
        demo_prompts = get_demo_prompts()
        render_demo_prompts(demo_prompts)

    # Main input area
    user_input = st.text_area(
        "Describe your outfit needs:",
        value=st.session_state.get("user_input", ""),
        height=100,
        placeholder="e.g., 'Create a casual outfit for a weekend brunch'",
    )

    col1, _ = st.columns([1, 4])
    with col1:
        generate_button = st.button("Generate Outfits", type="primary")

    if generate_button and user_input:
        with st.spinner("Generating outfits..."):
            requirements = extract_requirements(user_input)
            requirements["_seed"] = user_input
            preferences = extract_preferences(user_input)

            outfits = assemble_outfits(
                st.session_state.catalog,
                requirements,
                max_outfits=5,
            )

            ranked_outfits = rank_outfits(outfits, requirements, preferences)

            st.success(f"Generated {len(ranked_outfits)} outfit(s)")
            render_outfit_list(ranked_outfits, requirements)

    # Display catalog stats
    with st.expander("Catalog Information"):
        catalog = st.session_state.catalog
        items = catalog.get_all_items()
        st.write(f"Total items in catalog: {len(items)}")
        if items:
            categories = sorted({item.category for item in items})
            st.write(f"Categories: {', '.join(categories)}")


if __name__ == "__main__":
    main()

