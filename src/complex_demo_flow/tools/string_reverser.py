from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class StringReverserInput(BaseModel):
    """Input schema for StringReverser."""
    text: str = Field(..., description="The text to reverse")

class StringReverserTool(BaseTool):
    name: str = "string_reverser"
    description: str = "Reverse a string. Useful for creating mirror effects or testing text manipulation."
    args_schema: Type[BaseModel] = StringReverserInput

    def _run(self, text: str) -> str:
        """Execute the string reverser tool."""
        return text[::-1]

string_reverser = StringReverserTool()
