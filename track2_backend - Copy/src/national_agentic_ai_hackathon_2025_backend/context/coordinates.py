from pydantic import BaseModel

from typing import Optional

class Coordinates(BaseModel):
    latitude: float
    longitude: float
    formatted_coordinates: Optional[str] = None

    def _format_coordinates(self):
        """
        Convert Coordinates into a clean system prompt block.
        Only non-empty fields are included.
        """
        data = self.dict(exclude_none=True)

        labels = {
            "latitude": "Latitude",
            "longitude": "Longitude",
        }

        lines = [f"{labels[key]}: {value}" for key, value in data.items() if key in labels]

        if not lines:
            return ""  # No context to add

        prompt_block = (
            "\n---\n" +
            "**Coordinates Context**\n"
            + "\n".join(lines) +
            "\n---\n"
        )
        self.formatted_coordinates = prompt_block
        return prompt_block

    def __init__(self, **data):
        super().__init__(**data)
        self._format_coordinates()