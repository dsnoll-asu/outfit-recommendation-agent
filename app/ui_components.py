"""UI components for the Streamlit app."""
import streamlit as st
from typing import List
from pathlib import Path
from core.models import Outfit
from core.render import render_outfit_description

def render_outfit_card(outfit: Outfit, requirements: dict | None = None) -> None:
    """
    Render a single outfit as a card in the UI.
    
    Args:
        outfit: The outfit to display
    """
    with st.container():
        st.subheader(f"Outfit: {outfit.id}")
        st.write(render_outfit_description(outfit, requirements))
        
        if outfit.score is not None:
            st.metric("Score", f"{outfit.score:.2f}")
        
        st.write("**Items:**")
        for item in outfit.items:
            col_image, col1, col2 = st.columns([1, 3, 1])

            with col_image:
                raw_path = getattr(item, "image_path", None)
                if raw_path:
                    raw_path = str(raw_path).strip()  # protect against whitespace
                    img_path = Path(raw_path)

        # Resolve relative paths from project root
                if not img_path.is_absolute():
                    project_root = Path(__file__).parent.parent
                    img_path = project_root / img_path

        # Only show if it's a real file
                if img_path.exists() and img_path.is_file():
                    st.image(str(img_path), use_container_width=True)
                else:
            # TEMP DEBUG: shows which row is broken
                    st.caption(f"Image not found: {raw_path}")

            with col1:
                st.write(f"- {item.name} ({item.brand})")
            with col2:
                st.write(f"${item.price:.2f}")


def render_outfit_list(outfits: List[Outfit], requirements: dict | None = None) -> None:
    """
    Render a list of outfits.
    
    Args:
        outfits: List of outfits to display
    """
    if not outfits:
        st.info("No outfits found. Try adjusting your requirements.")
        return
    
    st.write(f"Found {len(outfits)} outfit(s):")
    for outfit in outfits:
        render_outfit_card(outfit, requirements)
        st.divider()


def render_demo_prompts(prompts: List[str]) -> None:
    """
    Render demo prompts as clickable buttons.
    
    Args:
        prompts: List of demo prompt strings
    """
    st.write("**Try these examples:**")
    cols = st.columns(len(prompts))
    for i, prompt in enumerate(prompts):
        with cols[i]:
            if st.button(prompt, key=f"demo_{i}"):
                st.session_state.user_input = prompt

