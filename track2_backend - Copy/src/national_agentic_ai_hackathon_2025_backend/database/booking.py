from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from national_agentic_ai_hackathon_2025_backend.schemas.booking import (
    Appointment, 
    AppointmentCreate, 
    AppointmentUpdate, 
    AppointmentStatus,
    AppointmentType
)
from national_agentic_ai_hackathon_2025_backend.database.base import DataBase
import uuid


class BookingDB(DataBase):
    """Database operations for Appointment entities"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "appointments"
    
    async def create_appointment(self, appointment: AppointmentCreate) -> Dict[str, Any]:
        """
        Create a new appointment in the database
        
        Args:
            appointment: AppointmentCreate object to create
            
        Returns:
            Dict containing the created appointment data
        """
        try:
            # Generate unique appointment ID
            appointment_id = str(uuid.uuid4())
            
            # Check for conflicts
            conflict_check = await self._check_appointment_conflicts(
                appointment.facility_id, 
                appointment.appointment_date,
                appointment.duration_minutes
            )
            
            if not conflict_check["available"]:
                return {
                    "success": False, 
                    "error": f"Time slot not available. {conflict_check['message']}"
                }
            
            # Create appointment data
            appointment_data = {
                "appointment_id": appointment_id,
                "user_id": appointment.user_id,
                "facility_id": appointment.facility_id,
                "facility_name": appointment.facility_name,
                "appointment_date": appointment.appointment_date.isoformat(),
                "appointment_type": appointment.appointment_type.value,
                "status": AppointmentStatus.SCHEDULED.value,
                "patient_name": appointment.patient_name,
                "patient_phone": appointment.patient_phone,
                "patient_age": appointment.patient_age,
                "reason_for_visit": appointment.reason_for_visit,
                "notes": appointment.notes,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "doctor_name": appointment.doctor_name,
                "duration_minutes": appointment.duration_minutes
            }
            
            result = self.supabase.table(self.table_name).insert(appointment_data).execute()
            
            if result.data:
                return {"success": True, "data": result.data[0], "appointment_id": appointment_id}
            else:
                return {"success": False, "error": "Failed to create appointment"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_appointment_by_id(self, appointment_id: str) -> Dict[str, Any]:
        """
        Get an appointment by its ID
        
        Args:
            appointment_id: ID of the appointment
            
        Returns:
            Dict containing the appointment data or error
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq("appointment_id", appointment_id).execute()
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "Appointment not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_appointments_by_user(self, user_id: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get all appointments for a specific user
        
        Args:
            user_id: ID of the user
            limit: Maximum number of results
            
        Returns:
            Dict containing list of user's appointments
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq(
                "user_id", user_id
            ).order("appointment_date", desc=False).limit(limit).execute()
            
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_appointments_by_facility(
        self, 
        facility_id: int, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get appointments for a specific facility within a date range
        
        Args:
            facility_id: OSM ID of the facility
            start_date: Start date for filtering (optional)
            end_date: End date for filtering (optional)
            limit: Maximum number of results
            
        Returns:
            Dict containing list of facility appointments
        """
        try:
            query = self.supabase.table(self.table_name).select("*").eq("facility_id", facility_id)
            
            if start_date:
                query = query.gte("appointment_date", start_date.isoformat())
            if end_date:
                query = query.lte("appointment_date", end_date.isoformat())
                
            result = query.order("appointment_date", desc=False).limit(limit).execute()
            
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_appointment(self, appointment_id: str, updates: AppointmentUpdate) -> Dict[str, Any]:
        """
        Update an existing appointment
        
        Args:
            appointment_id: ID of the appointment to update
            updates: AppointmentUpdate object with fields to update
            
        Returns:
            Dict containing success status and updated data
        """
        try:
            # Check if appointment exists
            existing = await self.get_appointment_by_id(appointment_id)
            if not existing["success"]:
                return existing
            
            # If updating appointment date, check for conflicts
            if updates.appointment_date:
                facility_id = existing["data"]["facility_id"]
                duration = updates.duration_minutes or existing["data"]["duration_minutes"]
                
                conflict_check = await self._check_appointment_conflicts(
                    facility_id, 
                    updates.appointment_date,
                    duration,
                    exclude_appointment_id=appointment_id
                )
                
                if not conflict_check["available"]:
                    return {
                        "success": False, 
                        "error": f"New time slot not available. {conflict_check['message']}"
                    }
            
            # Prepare update data
            update_data = {}
            for field, value in updates.model_dump(exclude_unset=True).items():
                if value is not None:
                    if field == "appointment_date":
                        update_data[field] = value.isoformat()
                    elif field in ["appointment_type", "status"]:
                        update_data[field] = value.value
                    else:
                        update_data[field] = value
            
            update_data["updated_at"] = datetime.now().isoformat()
            
            result = self.supabase.table(self.table_name).update(update_data).eq(
                "appointment_id", appointment_id
            ).execute()
            
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "Appointment not found or no changes made"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def cancel_appointment(self, appointment_id: str) -> Dict[str, Any]:
        """
        Cancel an appointment by updating its status
        
        Args:
            appointment_id: ID of the appointment to cancel
            
        Returns:
            Dict containing success status
        """
        try:
            result = self.supabase.table(self.table_name).update({
                "status": AppointmentStatus.CANCELLED.value,
                "updated_at": datetime.now().isoformat()
            }).eq("appointment_id", appointment_id).execute()
            
            if result.data:
                return {"success": True, "data": result.data[0], "message": "Appointment cancelled successfully"}
            else:
                return {"success": False, "error": "Appointment not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def delete_appointment(self, appointment_id: str) -> Dict[str, Any]:
        """
        Delete an appointment from the database
        
        Args:
            appointment_id: ID of the appointment to delete
            
        Returns:
            Dict containing success status
        """
        try:
            result = self.supabase.table(self.table_name).delete().eq(
                "appointment_id", appointment_id
            ).execute()
            
            if result.data:
                return {"success": True, "message": "Appointment deleted successfully"}
            else:
                return {"success": False, "error": "Appointment not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_available_slots(
        self, 
        facility_id: int, 
        date: datetime, 
        duration_minutes: int = 30
    ) -> Dict[str, Any]:
        """
        Get available time slots for a facility on a specific date
        
        Args:
            facility_id: OSM ID of the facility
            date: Date to check availability
            duration_minutes: Duration of appointment in minutes
            
        Returns:
            Dict containing available time slots
        """
        try:
            # Get start and end of day
            start_of_day = date.replace(hour=9, minute=0, second=0, microsecond=0)
            end_of_day = date.replace(hour=18, minute=0, second=0, microsecond=0)
            
            # Get existing appointments for the day
            existing_appointments = await self.get_appointments_by_facility(
                facility_id, start_of_day, end_of_day
            )
            
            if not existing_appointments["success"]:
                return existing_appointments
            
            # Generate available slots
            available_slots = []
            current_time = start_of_day
            
            while current_time + timedelta(minutes=duration_minutes) <= end_of_day:
                slot_end = current_time + timedelta(minutes=duration_minutes)
                
                # Check if this slot conflicts with existing appointments
                is_available = True
                for appointment in existing_appointments["data"]:
                    if appointment["status"] in [AppointmentStatus.CANCELLED.value, AppointmentStatus.COMPLETED.value]:
                        continue
                        
                    apt_start = datetime.fromisoformat(appointment["appointment_date"])
                    apt_end = apt_start + timedelta(minutes=appointment["duration_minutes"])
                    
                    # Check for overlap
                    if (current_time < apt_end and slot_end > apt_start):
                        is_available = False
                        break
                
                if is_available:
                    available_slots.append({
                        "start_time": current_time.isoformat(),
                        "end_time": slot_end.isoformat(),
                        "duration_minutes": duration_minutes
                    })
                
                # Move to next slot (30-minute intervals)
                current_time += timedelta(minutes=30)
            
            return {"success": True, "available_slots": available_slots}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _check_appointment_conflicts(
        self, 
        facility_id: int, 
        appointment_date: datetime, 
        duration_minutes: int,
        exclude_appointment_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check if an appointment time conflicts with existing appointments
        
        Args:
            facility_id: OSM ID of the facility
            appointment_date: Proposed appointment date/time
            duration_minutes: Duration of the appointment
            exclude_appointment_id: ID of appointment to exclude from conflict check
            
        Returns:
            Dict containing conflict check result
        """
        try:
            # Get appointments for the same day
            start_of_day = appointment_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = appointment_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            result = self.supabase.table(self.table_name).select("*").eq(
                "facility_id", facility_id
            ).gte("appointment_date", start_of_day.isoformat()).lte(
                "appointment_date", end_of_day.isoformat()
            ).neq("status", AppointmentStatus.CANCELLED.value).execute()
            
            if not result.data:
                return {"available": True, "message": "Time slot is available"}
            
            # Check for conflicts
            appointment_end = appointment_date + timedelta(minutes=duration_minutes)
            
            for appointment in result.data:
                if exclude_appointment_id and appointment["appointment_id"] == exclude_appointment_id:
                    continue
                    
                if appointment["status"] in [AppointmentStatus.CANCELLED.value, AppointmentStatus.COMPLETED.value]:
                    continue
                
                apt_start = datetime.fromisoformat(appointment["appointment_date"])
                apt_end = apt_start + timedelta(minutes=appointment["duration_minutes"])
                
                # Check for overlap
                if (appointment_date < apt_end and appointment_end > apt_start):
                    return {
                        "available": False, 
                        "message": f"Conflicts with existing appointment from {apt_start.strftime('%H:%M')} to {apt_end.strftime('%H:%M')}"
                    }
            
            return {"available": True, "message": "Time slot is available"}
        except Exception as e:
            return {"available": False, "message": f"Error checking conflicts: {str(e)}"}
    
    async def get_appointments_by_status(
        self, 
        status: AppointmentStatus, 
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get appointments by status
        
        Args:
            status: Appointment status to filter by
            limit: Maximum number of results
            
        Returns:
            Dict containing list of appointments
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq(
                "status", status.value
            ).order("appointment_date", desc=False).limit(limit).execute()
            
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def search_appointments(
        self, 
        query: str, 
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Search appointments by patient name, facility name, or appointment ID
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            Dict containing list of matching appointments
        """
        try:
            result = self.supabase.table(self.table_name).select("*").or_(
                f"patient_name.ilike.%{query}%,facility_name.ilike.%{query}%,appointment_id.ilike.%{query}%"
            ).order("appointment_date", desc=True).limit(limit).execute()
            
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
