from multiprocessing import context
from typing import Optional
from pydantic import BaseModel

class UserContext(BaseModel):
    phone_number: str
    username: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    formatted_user: Optional[str] = None

    def _format_user(self):
        """
        Convert UserContext into a clean system prompt block.
        Only non-empty fields are included.
        """
        # Get dict with None values removed
        data = self.dict(exclude_none=True)

        # Map field names to readable labels
        labels = {
            "phone_number": "Phone Number",
            "username": "Username",
            "address": "Address",
            "email": "Email",
        }
    
        # Build lines only for fields that exist
        lines = [f"{labels[key]}: {value}" for key, value in data.items() if key in labels]
    
        if not lines:
            return ""  # No context to add
    
        # Format in a clear block for system prompt
        prompt_block = (
            "\n---\n" +
            "**User Context**\n"
            + "\n".join(lines) +
            "\n---\n"
        )
        self.formatted_user = prompt_block
        return prompt_block
    
    def __init__(self, **data):
        super().__init__(**data)
        self._format_user()