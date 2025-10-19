from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PoliceFacility(BaseModel):
    osm_id: int                          # Unique ID from OpenStreetMap
    name: Optional[str]                  # Facility name (e.g., "Gulshan-e-Iqbal Police Station")
    amenity: Optional[str]               # Type of facility (police, checkpoint, station, etc.)
    jurisdiction: Optional[str]          # Area covered by this police station
    addr_full: Optional[str]             # Full address of the facility
    contact_number: Optional[str]        # Phone number of the facility
    x: Optional[float]                   # Longitude (geo position)
    y: Optional[float]                   # Latitude (geo position)
    changeset_timestamp: Optional[str]   # Last updated timestamp in OSM
