from crewai_tools import tool

@tool("character_counter")
def character_counter(text: str) -> str:
    """Count the number of characters in a string. Useful for checking poem length."""
    char_count = len(text)
    word_count = len(text.split())
    return f"Character count: {char_count}, Word count: {word_count}"
