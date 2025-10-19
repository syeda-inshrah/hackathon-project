from typing import List, Optional, Dict, Any
from national_agentic_ai_hackathon_2025_backend.schemas.police import PoliceFacility
from national_agentic_ai_hackathon_2025_backend.database.base import DataBase


class PoliceFacilityDB(DataBase):
    """Database operations for PoliceFacility entities"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "police_facility"
    
    async def create_police_facility(self, facility: PoliceFacility) -> Dict[str, Any]:
        """
        Create a new police facility in the database
        """
        try:
            facility_data = facility.model_dump()
            result = self.supabase.table(self.table_name).insert(facility_data).execute()
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_police_facility_by_id(self, osm_id: int) -> Dict[str, Any]:
        """
        Get a police facility by its OSM ID
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq("osm_id", osm_id).execute()
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "Facility not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_police_facilities_by_location(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float = 10.0,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get police facilities within a specified radius of given coordinates
        """
        try:
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
        except Exception:
            return await self._get_facilities_by_bounding_box(latitude, longitude, radius_km, limit)
    
    async def _get_facilities_by_bounding_box(
        self, latitude: float, longitude: float, radius_km: float, limit: int
    ) -> Dict[str, Any]:
        """Fallback method using bounding box approximation"""
        try:
            lat_offset = radius_km / 111.0
            lng_offset = radius_km / (111.0 * abs(latitude / 90.0))
            
            result = self.supabase.table(self.table_name).select("*").gte(
                "Y", latitude - lat_offset
            ).lte(
                "Y", latitude + lat_offset
            ).gte(
                "X", longitude - lng_offset
            ).lte(
                "X", longitude + lng_offset
            ).limit(limit).execute()
            
            facilities_with_distance = []
            for facility in result.data:
                if facility.get('X') and facility.get('Y'):
                    distance = self._calculate_distance(latitude, longitude, facility['Y'], facility['X'])
                    if distance <= radius_km:
                        facility['distance_km'] = distance
                        facilities_with_distance.append(facility)
            
            facilities_with_distance.sort(key=lambda x: x['distance_km'])
            return {"success": True, "data": facilities_with_distance}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Haversine distance"""
        import math
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat/2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon/2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    async def get_police_facilities_by_amenity(self, amenity: str, limit: int = 100) -> Dict[str, Any]:
        """Get police facilities by amenity type (police, checkpoint, station, etc.)"""
        try:
            result = self.supabase.table(self.table_name).select("*").eq("amenity", amenity).limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_police_facilities_by_jurisdiction(self, jurisdiction: str, limit: int = 100) -> Dict[str, Any]:
        """Get police facilities by jurisdiction (area covered)"""
        try:
            result = self.supabase.table(self.table_name).select("*").ilike("jurisdiction", f"%{jurisdiction}%").limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_police_facility(self, osm_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a police facility's information"""
        try:
            result = self.supabase.table(self.table_name).update(updates).eq("osm_id", osm_id).execute()
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "Facility not found or no changes made"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def delete_police_facility(self, osm_id: int) -> Dict[str, Any]:
        """Delete a police facility"""
        try:
            result = self.supabase.table(self.table_name).delete().eq("osm_id", osm_id).execute()
            if result.data:
                return {"success": True, "message": "Facility deleted successfully"}
            else:
                return {"success": False, "error": "Facility not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def search_police_facilities(self, query: str, limit: int = 50) -> Dict[str, Any]:
        """Search police facilities by name or address"""
        try:
            result = self.supabase.table(self.table_name).select("*").or_(
                f"name.ilike.%{query}%,addr_full.ilike.%{query}%"
            ).limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_all_police_facility(self, limit: int = 1000) -> Dict[str, Any]:
        """
        Retrieve all police facilities from the database.
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