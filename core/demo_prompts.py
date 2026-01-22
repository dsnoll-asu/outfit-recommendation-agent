"""Demo prompts for testing and demonstration."""
from typing import List


def get_demo_prompts() -> List[str]:
    """
    Get a list of demo prompts for users to try.
    
    Returns:
        List of example prompt strings
    """
    return [
        "Create a casual outfit for a weekend brunch",
        "I need a formal outfit for a business meeting",
        "Show me a party outfit in black and white",
        "Assemble a work-appropriate outfit under $200",
        "Create a summer casual outfit with blue colors",
        "I'm going to a formal wedding and need to wear a tie"
    ]


def get_random_demo_prompt() -> str:
    """
    Get a random demo prompt.
    
    Returns:
        A single demo prompt string
    """
    prompts = get_demo_prompts()
    return prompts[0] if prompts else "Create a casual outfit"

