from typing import Optional
from pydantic import BaseModel


class CatastrophicEvent(BaseModel):
    event_id: int                          # Unique ID for the catastrophic event
    event_type: str                        # Type of event (earthquake, flood, fire, etc.)
    severity: Optional[str]                # Severity level (low, medium, high, critical)
    location: Optional[str]                # Name of the location (e.g., Karachi, Lahore)
    latitude: Optional[float]              # Latitude of event
    longitude: Optional[float]             # Longitude of event
    description: Optional[str]             # Details about the event
    reported_by: Optional[str]             # Source (citizen, agency, system)
    contact_number: Optional[str]          # Emergency contact number
    reported_at: Optional[str]             # Timestamp when the event was reported
    status: Optional[str]                  # Current status (active, resolved, monitoring)
