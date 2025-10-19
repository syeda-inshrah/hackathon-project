from typing import List, Optional, Dict, Any
from national_agentic_ai_hackathon_2025_backend.schemas.hospitals import HealthFacility
from national_agentic_ai_hackathon_2025_backend.database.base import DataBase


class HealthFacilityDB(DataBase):
    """Database operations for HealthFacility entities"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "health_facility"
    
    async def create_health_facility(self, facility: HealthFacility) -> Dict[str, Any]:
        """
        Create a new health facility in the database
        
        Args:
            facility: HealthFacility object to create
            
        Returns:
            Dict containing the created facility data
        """
        try:
            facility_data = facility.model_dump()
            result = self.supabase.table(self.table_name).insert(facility_data).execute()
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            print(f"Hello {e}")
            return {"success": False, "error": str(e)}
    
    async def get_health_facility_by_id(self, osm_id: int) -> Dict[str, Any]:
        """
        Get a health facility by its OSM ID
        
        Args:
            osm_id: OpenStreetMap ID of the facility
            
        Returns:
            Dict containing the facility data or error
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq("osm_id", osm_id).execute()
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "Facility not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_health_facilities_by_location(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float = 10.0,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get health facilities within a specified radius of given coordinates
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius_km: Search radius in kilometers (default: 10km)
            limit: Maximum number of results to return
            
        Returns:
            Dict containing list of nearby facilities
        """
        try:
            # Using PostGIS ST_DWithin for geographic distance calculation
            # This assumes your Supabase table has a geography column or similar
            query = f"""
            SELECT *, 
                   ST_Distance(
                       ST_GeogFromText('POINT({longitude} {latitude})'),
                       ST_GeogFromText('POINT(' || X || ' ' || Y || ')')
                   ) / 1000 as distance_km
            FROM {self.table_name}
            WHERE ST_DWithin(
                ST_GeogFromText('POINT({longitude} {latitude})'),
                ST_GeogFromText('POINT(' || X || ' ' || Y || ')'),
                {radius_km * 1000}
            )
            ORDER BY distance_km
            LIMIT {limit}
            """
            
            result = self.supabase.rpc('execute_sql', {'query': query}).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            # Fallback to simple bounding box search if PostGIS is not available
            return await self._get_facilities_by_bounding_box(latitude, longitude, radius_km, limit)
    
    async def _get_facilities_by_bounding_box(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float, 
        limit: int
    ) -> Dict[str, Any]:
        """
        Fallback method using bounding box approximation for location-based search
        """
        try:
            # Approximate bounding box (rough calculation)
            lat_offset = radius_km / 111.0  # Rough km per degree latitude
            lng_offset = radius_km / (111.0 * abs(latitude / 90.0))  # Adjust for longitude
            
            result = self.supabase.table(self.table_name).select("*").gte(
                "Y", latitude - lat_offset
            ).lte(
                "Y", latitude + lat_offset
            ).gte(
                "X", longitude - lng_offset
            ).lte(
                "X", longitude + lng_offset
            ).limit(limit).execute()
            
            # Calculate actual distances and sort
            facilities_with_distance = []
            for facility in result.data:
                if facility.get('X') and facility.get('Y'):
                    distance = self._calculate_distance(
                        latitude, longitude, 
                        facility['Y'], facility['X']
                    )
                    if distance <= radius_km:
                        facility['distance_km'] = distance
                        facilities_with_distance.append(facility)
            
            # Sort by distance
            facilities_with_distance.sort(key=lambda x: x['distance_km'])
            
            return {"success": True, "data": facilities_with_distance}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        
        Returns:
            Distance in kilometers
        """
        import math
        
        R = 6371  # Earth's radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon/2) * math.sin(dlon/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    async def get_health_facilities_by_amenity(self, amenity: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get health facilities by amenity type (hospital, clinic, pharmacy, etc.)
        
        Args:
            amenity: Type of facility to search for
            limit: Maximum number of results
            
        Returns:
            Dict containing list of facilities
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq(
                "amenity", amenity
            ).limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_health_facilities_by_speciality(self, speciality: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get health facilities by speciality
        
        Args:
            speciality: Medical speciality to search for
            limit: Maximum number of results
            
        Returns:
            Dict containing list of facilities
        """
        try:
            result = self.supabase.table(self.table_name).select("*").ilike(
                "speciality", f"%{speciality}%"
            ).limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_health_facility(self, osm_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a health facility's information
        
        Args:
            osm_id: OSM ID of the facility to update
            updates: Dictionary of fields to update
            
        Returns:
            Dict containing success status and updated data
        """
        try:
            result = self.supabase.table(self.table_name).update(updates).eq(
                "osm_id", osm_id
            ).execute()
            
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "Facility not found or no changes made"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def delete_health_facility(self, osm_id: int) -> Dict[str, Any]:
        """
        Delete a health facility from the database
        
        Args:
            osm_id: OSM ID of the facility to delete
            
        Returns:
            Dict containing success status
        """
        try:
            result = self.supabase.table(self.table_name).delete().eq(
                "osm_id", osm_id
            ).execute()
            
            if result.data:
                return {"success": True, "message": "Facility deleted successfully"}
            else:
                return {"success": False, "error": "Facility not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def search_health_facilities(
        self, 
        query: str, 
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Search health facilities by name or address
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            Dict containing list of matching facilities
        """
        try:
            result = self.supabase.table(self.table_name).select("*").or_(
                f"name.ilike.%{query}%,addr_full.ilike.%{query}%"
            ).limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_facilities_with_available_beds(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get health facilities that have available beds information
        
        Args:
            limit: Maximum number of results
            
        Returns:
            Dict containing list of facilities with bed information
        """
        try:
            result = self.supabase.table(self.table_name).select("*").not_.is_(
                "available_beds", "null"
            ).gt("available_beds", 0).limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}


    async def get_all_health_facility(self, limit: int = 1000) -> Dict[str, Any]:
            """
            Retrieve all health facilities from the database.
            Args:
                limit: Maximum number of results to return (default: 1000)
            Returns:
                Dict containing list of all facilities or error
            """
            try:
                result = self.supabase.table(self.table_name).select("*").limit(limit).execute()
                return {"success": True, "data": result.data if result.data else []}
            except Exception as e:
                return {"success": False, "error": str(e)}