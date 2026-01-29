from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class CharacterCounterInput(BaseModel):
    """Input schema for CharacterCounter."""
    text: str = Field(..., description="The text to count characters and words in")

class CharacterCounterTool(BaseTool):
    name: str = "character_counter"
    description: str = "Count the number of characters and words in a text. Useful for checking poem length and statistics."
    args_schema: Type[BaseModel] = CharacterCounterInput

    def _run(self, text: str) -> str:
        """Execute the character counter tool."""
        char_count = len(text)
        word_count = len(text.split())
        return f"Character count: {char_count}, Word count: {word_count}"

character_counter = CharacterCounterTool()
