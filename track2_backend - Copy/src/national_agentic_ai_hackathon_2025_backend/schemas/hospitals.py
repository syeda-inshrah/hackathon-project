from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class HealthFacility(BaseModel):
    osm_id: int                          # Unique ID from OpenStreetMap
    name: Optional[str] = None                 # Facility name (e.g., "Fatima Dental Hospital")
    amenity: Optional[str] = None              # Type of facility (hospital, clinic, pharmacy, etc.)
    speciality: Optional[str] = None           # Specialized services (e.g., gynecology, dental)
    addr_full: Optional[str] = None     # Full address of the facility
    contact_number: Optional[str] = None      # Phone number of the facility
    x: Optional[float] = None # Longitude (geo position)
    y: Optional[float] = None            # Latitude (geo position)
    changeset_timestamp: Optional[str] = None  # Last updated timestamp in OSM
    available_beds: Optional[int] = None        # Number of available beds (capacity info)
