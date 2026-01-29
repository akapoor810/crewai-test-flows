from crewai_tools import tool

@tool("string_reverser")
def string_reverser(text: str) -> str:
    """Reverse a string to force tool execution in trace."""
    return text[::-1]
