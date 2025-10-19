from typing import Dict, Any
from national_agentic_ai_hackathon_2025_backend.schemas.catastrophic import CatastrophicEvent
from national_agentic_ai_hackathon_2025_backend.database.base import DataBase


class CatastrophicEventDB(DataBase):
    """Database operations for CatastrophicEvent entities"""

    def __init__(self):
        super().__init__()
        self.table_name = "catastrophic_event"

    async def create_event(self, event: CatastrophicEvent) -> Dict[str, Any]:
        """Create a new catastrophic event"""
        try:
            event_data = event.model_dump()
            result = self.supabase.table(self.table_name).insert(event_data).execute()
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_event_by_id(self, event_id: int) -> Dict[str, Any]:
        """Get event by ID"""
        try:
            result = self.supabase.table(self.table_name).select("*").eq("event_id", event_id).execute()
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "Event not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_events_by_type(self, event_type: str, limit: int = 100) -> Dict[str, Any]:
        """Filter events by type (earthquake, flood, etc.)"""
        try:
            result = self.supabase.table(self.table_name).select("*").eq("event_type", event_type).limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_active_events(self, limit: int = 100) -> Dict[str, Any]:
        """Get all active catastrophic events"""
        try:
            result = self.supabase.table(self.table_name).select("*").eq("status", "active").limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def update_event(self, event_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update catastrophic event details"""
        try:
            result = self.supabase.table(self.table_name).update(updates).eq("event_id", event_id).execute()
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "Event not found or no changes made"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def delete_event(self, event_id: int) -> Dict[str, Any]:
        """Delete catastrophic event"""
        try:
            result = self.supabase.table(self.table_name).delete().eq("event_id", event_id).execute()
            if result.data:
                return {"success": True, "message": "Event deleted successfully"}
            else:
                return {"success": False, "error": "Event not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def search_events(self, query: str, limit: int = 50) -> Dict[str, Any]:
        """Search catastrophic events by location or description"""
        try:
            result = self.supabase.table(self.table_name).select("*").or_(
                f"location.ilike.%{query}%,description.ilike.%{query}%"
            ).limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_all_events(self, limit: int = 1000) -> Dict[str, Any]:
        """Retrieve all catastrophic events"""
        try:
            result = self.supabase.table(self.table_name).select("*").limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
