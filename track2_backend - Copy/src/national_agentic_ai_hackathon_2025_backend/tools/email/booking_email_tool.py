"""
Booking Email Tool for the Booking Agent
Provides email functionality for sending notifications to facilities
"""

from typing import Dict, Any, Optional
from national_agentic_ai_hackathon_2025_backend.tools.email.email_service import EmailService
from national_agentic_ai_hackathon_2025_backend._debug import Logger
from national_agentic_ai_hackathon_2025_backend.schemas.booking import Appointment


def create_booking_email_tool(context):
    """
    Create a booking email tool that can be used by the booking agent
    
    Args:
        context: The context object containing user and global information
    
    Returns:
        Dict: Tool configuration for the agent
    """
    
    email_service = EmailService()
    
    async def send_booking_confirmation_email(
        appointment_data: Dict[str, Any],
        facility_data: Dict[str, Any],
        facility_type: str = "healthcare"
    ) -> Dict[str, Any]:
        """
        Send booking confirmation email to a facility
        
        Args:
            appointment_data: Dictionary containing appointment information
            facility_data: Dictionary containing facility information
            facility_type: Type of facility ("healthcare" or "police")
        
        Returns:
            Dict containing success status and message
        """
        try:
            # Create appointment object from data
            appointment = Appointment(**appointment_data)
            
            # Send email
            success = await email_service.send_booking_confirmation_email(
                appointment=appointment,
                facility=facility_data,
                facility_type=facility_type
            )
            
            if success:
                Logger.success(f"✅ Booking confirmation email sent to {facility_data.get('name', 'facility')}")
                return {
                    "success": True,
                    "message": f"Booking confirmation email sent successfully to {facility_data.get('name', 'facility')}",
                    "facility_name": facility_data.get('name', 'Unknown'),
                    "facility_type": facility_type
                }
            else:
                Logger.error(f"❌ Failed to send booking confirmation email to {facility_data.get('name', 'facility')}")
                return {
                    "success": False,
                    "message": f"Failed to send booking confirmation email to {facility_data.get('name', 'facility')}",
                    "facility_name": facility_data.get('name', 'Unknown'),
                    "facility_type": facility_type
                }
                
        except Exception as e:
            Logger.error(f"Error in send_booking_confirmation_email: {e}")
            return {
                "success": False,
                "message": f"Error sending booking confirmation email: {str(e)}",
                "facility_name": facility_data.get('name', 'Unknown'),
                "facility_type": facility_type
            }
    
    async def send_appointment_reminder_email(
        appointment_data: Dict[str, Any],
        facility_data: Dict[str, Any],
        facility_type: str = "healthcare"
    ) -> Dict[str, Any]:
        """
        Send appointment reminder email to a facility
        
        Args:
            appointment_data: Dictionary containing appointment information
            facility_data: Dictionary containing facility information
            facility_type: Type of facility ("healthcare" or "police")
        
        Returns:
            Dict containing success status and message
        """
        try:
            # Create appointment object from data
            appointment = Appointment(**appointment_data)
            
            # Send email
            success = await email_service.send_appointment_reminder_email(
                appointment=appointment,
                facility=facility_data,
                facility_type=facility_type
            )
            
            if success:
                Logger.success(f"✅ Appointment reminder email sent to {facility_data.get('name', 'facility')}")
                return {
                    "success": True,
                    "message": f"Appointment reminder email sent successfully to {facility_data.get('name', 'facility')}",
                    "facility_name": facility_data.get('name', 'Unknown'),
                    "facility_type": facility_type
                }
            else:
                Logger.error(f"❌ Failed to send appointment reminder email to {facility_data.get('name', 'facility')}")
                return {
                    "success": False,
                    "message": f"Failed to send appointment reminder email to {facility_data.get('name', 'facility')}",
                    "facility_name": facility_data.get('name', 'Unknown'),
                    "facility_type": facility_type
                }
                
        except Exception as e:
            Logger.error(f"Error in send_appointment_reminder_email: {e}")
            return {
                "success": False,
                "message": f"Error sending appointment reminder email: {str(e)}",
                "facility_name": facility_data.get('name', 'Unknown'),
                "facility_type": facility_type
            }
    
    async def send_appointment_cancellation_email(
        appointment_data: Dict[str, Any],
        facility_data: Dict[str, Any],
        facility_type: str = "healthcare",
        cancellation_reason: str = "Not specified"
    ) -> Dict[str, Any]:
        """
        Send appointment cancellation email to a facility
        
        Args:
            appointment_data: Dictionary containing appointment information
            facility_data: Dictionary containing facility information
            facility_type: Type of facility ("healthcare" or "police")
            cancellation_reason: Reason for cancellation
        
        Returns:
            Dict containing success status and message
        """
        try:
            # Create appointment object from data
            appointment = Appointment(**appointment_data)
            
            # Send email
            success = await email_service.send_appointment_cancellation_email(
                appointment=appointment,
                facility=facility_data,
                facility_type=facility_type,
                cancellation_reason=cancellation_reason
            )
            
            if success:
                Logger.success(f"✅ Appointment cancellation email sent to {facility_data.get('name', 'facility')}")
                return {
                    "success": True,
                    "message": f"Appointment cancellation email sent successfully to {facility_data.get('name', 'facility')}",
                    "facility_name": facility_data.get('name', 'Unknown'),
                    "facility_type": facility_type
                }
            else:
                Logger.error(f"❌ Failed to send appointment cancellation email to {facility_data.get('name', 'facility')}")
                return {
                    "success": False,
                    "message": f"Failed to send appointment cancellation email to {facility_data.get('name', 'facility')}",
                    "facility_name": facility_data.get('name', 'Unknown'),
                    "facility_type": facility_type
                }
                
        except Exception as e:
            Logger.error(f"Error in send_appointment_cancellation_email: {e}")
            return {
                "success": False,
                "message": f"Error sending appointment cancellation email: {str(e)}",
                "facility_name": facility_data.get('name', 'Unknown'),
                "facility_type": facility_type
            }
    
    # Return the tool configuration
    return {
        "type": "function",
        "function": {
            "name": "booking_email_tool",
            "description": "Send emails to facilities (police stations, healthcare facilities) for booking confirmations, reminders, and cancellations",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["send_confirmation", "send_reminder", "send_cancellation"],
                        "description": "The type of email to send"
                    },
                    "appointment_data": {
                        "type": "object",
                        "description": "Appointment information including patient details, date, time, etc.",
                        "properties": {
                            "appointment_id": {"type": "string"},
                            "user_id": {"type": "string"},
                            "facility_id": {"type": "integer"},
                            "facility_name": {"type": "string"},
                            "appointment_date": {"type": "string", "format": "date-time"},
                            "appointment_type": {"type": "string", "enum": ["consultation", "follow_up", "emergency", "routine_checkup", "specialist"]},
                            "status": {"type": "string", "enum": ["scheduled", "confirmed", "cancelled", "completed", "no_show"]},
                            "patient_name": {"type": "string"},
                            "patient_phone": {"type": "string"},
                            "patient_age": {"type": "integer"},
                            "reason_for_visit": {"type": "string"},
                            "notes": {"type": "string"},
                            "doctor_name": {"type": "string"},
                            "duration_minutes": {"type": "integer"}
                        },
                        "required": ["user_id", "facility_id", "facility_name", "appointment_date", "patient_name", "patient_phone"]
                    },
                    "facility_data": {
                        "type": "object",
                        "description": "Facility information including name, address, contact details",
                        "properties": {
                            "name": {"type": "string"},
                            "addr_full": {"type": "string"},
                            "contact_number": {"type": "string"},
                            "contact_email": {"type": "string"},
                            "email": {"type": "string"},
                            "amenity": {"type": "string"},
                            "speciality": {"type": "string"},
                            "jurisdiction": {"type": "string"}
                        },
                        "required": ["name"]
                    },
                    "facility_type": {
                        "type": "string",
                        "enum": ["healthcare", "police"],
                        "description": "Type of facility to send email to",
                        "default": "healthcare"
                    },
                    "cancellation_reason": {
                        "type": "string",
                        "description": "Reason for cancellation (only required for cancellation emails)",
                        "default": "Not specified"
                    }
                },
                "required": ["action", "appointment_data", "facility_data"]
            }
        },
        "handler": {
            "send_confirmation": send_booking_confirmation_email,
            "send_reminder": send_appointment_reminder_email,
            "send_cancellation": send_appointment_cancellation_email
        }
    }


# Standalone function for direct use
async def send_booking_email(
    action: str,
    appointment_data: Dict[str, Any],
    facility_data: Dict[str, Any],
    facility_type: str = "healthcare",
    cancellation_reason: str = "Not specified"
) -> Dict[str, Any]:
    """
    Standalone function to send booking emails
    
    Args:
        action: Type of email to send ("send_confirmation", "send_reminder", "send_cancellation")
        appointment_data: Appointment information
        facility_data: Facility information
        facility_type: Type of facility ("healthcare" or "police")
        cancellation_reason: Reason for cancellation (for cancellation emails)
    
    Returns:
        Dict containing success status and message
    """
    email_service = EmailService()
    
    try:
        # Create appointment object from data
        appointment = Appointment(**appointment_data)
        
        if action == "send_confirmation":
            success = await email_service.send_booking_confirmation_email(
                appointment=appointment,
                facility=facility_data,
                facility_type=facility_type
            )
        elif action == "send_reminder":
            success = await email_service.send_appointment_reminder_email(
                appointment=appointment,
                facility=facility_data,
                facility_type=facility_type
            )
        elif action == "send_cancellation":
            success = await email_service.send_appointment_cancellation_email(
                appointment=appointment,
                facility=facility_data,
                facility_type=facility_type,
                cancellation_reason=cancellation_reason
            )
        else:
            return {
                "success": False,
                "message": f"Unknown action: {action}",
                "facility_name": facility_data.get('name', 'Unknown'),
                "facility_type": facility_type
            }
        
        if success:
            Logger.success(f"✅ {action} email sent to {facility_data.get('name', 'facility')}")
            return {
                "success": True,
                "message": f"{action.replace('_', ' ').title()} email sent successfully to {facility_data.get('name', 'facility')}",
                "facility_name": facility_data.get('name', 'Unknown'),
                "facility_type": facility_type
            }
        else:
            Logger.error(f"❌ Failed to send {action} email to {facility_data.get('name', 'facility')}")
            return {
                "success": False,
                "message": f"Failed to send {action.replace('_', ' ').title()} email to {facility_data.get('name', 'facility')}",
                "facility_name": facility_data.get('name', 'Unknown'),
                "facility_type": facility_type
            }
            
    except Exception as e:
        Logger.error(f"Error in send_booking_email: {e}")
        return {
            "success": False,
            "message": f"Error sending {action.replace('_', ' ').title()} email: {str(e)}",
            "facility_name": facility_data.get('name', 'Unknown'),
            "facility_type": facility_type
        }
