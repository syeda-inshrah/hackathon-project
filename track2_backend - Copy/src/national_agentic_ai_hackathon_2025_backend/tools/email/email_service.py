"""
Email Service for Booking Agent
Handles sending emails to different types of facilities (police, healthcare, etc.)
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from national_agentic_ai_hackathon_2025_backend.utils.email_sender import send_email
from national_agentic_ai_hackathon_2025_backend._debug import Logger
from national_agentic_ai_hackathon_2025_backend.schemas.booking import Appointment
from national_agentic_ai_hackathon_2025_backend.schemas.police import PoliceFacility
from national_agentic_ai_hackathon_2025_backend.schemas.hospitals import HealthFacility


class EmailService:
    """Service for sending emails to various facilities"""
    
    def __init__(self):
        self.sender_name = "National Agentic AI Booking System"
    
    async def send_booking_confirmation_email(
        self, 
        appointment: Appointment, 
        facility: Dict[str, Any],
        facility_type: str = "healthcare"
    ) -> bool:
        """
        Send booking confirmation email to facility
        
        Args:
            appointment: The appointment details
            facility: Facility information (police or healthcare)
            facility_type: Type of facility ("healthcare" or "police")
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            if facility_type == "healthcare":
                return await self._send_healthcare_booking_email(appointment, facility)
            elif facility_type == "police":
                return await self._send_police_booking_email(appointment, facility)
            else:
                Logger.error(f"Unknown facility type: {facility_type}")
                return False
        except Exception as e:
            Logger.error(f"Error sending booking confirmation email: {e}")
            return False
    
    async def _send_healthcare_booking_email(
        self, 
        appointment: Appointment, 
        facility: Dict[str, Any]
    ) -> bool:
        """Send booking email to healthcare facility"""
        try:
            facility_email = facility.get('contact_email') or facility.get('email')
            if not facility_email:
                Logger.warning(f"No email found for healthcare facility: {facility.get('name', 'Unknown')}")
                return False
            
            subject = f"New Appointment Booking - {appointment.patient_name}"
            
            body = self._generate_healthcare_email_body(appointment, facility)
            
            Logger.info(f"Sending healthcare booking email to: {facility_email}")
            return send_email(facility_email, subject, body)
            
        except Exception as e:
            Logger.error(f"Error sending healthcare booking email: {e}")
            return False
    
    async def _send_police_booking_email(
        self, 
        appointment: Appointment, 
        facility: Dict[str, Any]
    ) -> bool:
        """Send booking email to police facility"""
        try:
            facility_email = facility.get('contact_email') or facility.get('email')
            if not facility_email:
                Logger.warning(f"No email found for police facility: {facility.get('name', 'Unknown')}")
                return False
            
            subject = f"New Service Request - {appointment.patient_name}"
            
            body = self._generate_police_email_body(appointment, facility)
            
            Logger.info(f"Sending police booking email to: {facility_email}")
            return send_email(facility_email, subject, body)
            
        except Exception as e:
            Logger.error(f"Error sending police booking email: {e}")
            return False
    
    def _generate_healthcare_email_body(
        self, 
        appointment: Appointment, 
        facility: Dict[str, Any]
    ) -> str:
        """Generate email body for healthcare facility"""
        facility_name = facility.get('name', 'Healthcare Facility')
        facility_address = facility.get('addr_full', 'Address not available')
        facility_phone = facility.get('contact_number', 'Phone not available')
        
        appointment_date = appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")
        
        body = f"""
Dear {facility_name} Team,

A new appointment has been booked through the National Agentic AI Booking System.

APPOINTMENT DETAILS:
===================
Patient Name: {appointment.patient_name}
Patient Phone: {appointment.patient_phone}
Patient Age: {appointment.patient_age or 'Not specified'}
Appointment Date & Time: {appointment_date}
Appointment Type: {appointment.appointment_type.value.title()}
Duration: {appointment.duration_minutes} minutes
Reason for Visit: {appointment.reason_for_visit or 'Not specified'}
Assigned Doctor: {appointment.doctor_name or 'To be assigned'}
Additional Notes: {appointment.notes or 'None'}

FACILITY INFORMATION:
====================
Facility Name: {facility_name}
Address: {facility_address}
Phone: {facility_phone}

BOOKING INFORMATION:
===================
Booking ID: {appointment.appointment_id or 'Pending'}
Status: {appointment.status.value.title()}
Created At: {appointment.created_at.strftime("%B %d, %Y at %I:%M %p") if appointment.created_at else 'Not available'}

Please confirm this appointment and contact the patient if any changes are needed.

Best regards,
{self.sender_name}
        """
        return body.strip()
    
    def _generate_police_email_body(
        self, 
        appointment: Appointment, 
        facility: Dict[str, Any]
    ) -> str:
        """Generate email body for police facility"""
        facility_name = facility.get('name', 'Police Station')
        facility_address = facility.get('addr_full', 'Address not available')
        facility_phone = facility.get('contact_number', 'Phone not available')
        jurisdiction = facility.get('jurisdiction', 'Not specified')
        
        appointment_date = appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")
        
        body = f"""
Dear {facility_name} Team,

A new service request has been submitted through the National Agentic AI Booking System.

SERVICE REQUEST DETAILS:
========================
Requestor Name: {appointment.patient_name}
Contact Phone: {appointment.patient_phone}
Request Date & Time: {appointment_date}
Service Type: {appointment.appointment_type.value.title()}
Duration: {appointment.duration_minutes} minutes
Reason for Request: {appointment.reason_for_visit or 'Not specified'}
Additional Notes: {appointment.notes or 'None'}

FACILITY INFORMATION:
====================
Station Name: {facility_name}
Jurisdiction: {jurisdiction}
Address: {facility_address}
Phone: {facility_phone}

REQUEST INFORMATION:
===================
Request ID: {appointment.appointment_id or 'Pending'}
Status: {appointment.status.value.title()}
Submitted At: {appointment.created_at.strftime("%B %d, %Y at %I:%M %p") if appointment.created_at else 'Not available'}

Please review this request and contact the requestor if any additional information is needed.

Best regards,
{self.sender_name}
        """
        return body.strip()
    
    async def send_appointment_reminder_email(
        self, 
        appointment: Appointment, 
        facility: Dict[str, Any],
        facility_type: str = "healthcare"
    ) -> bool:
        """
        Send appointment reminder email to facility
        
        Args:
            appointment: The appointment details
            facility: Facility information
            facility_type: Type of facility ("healthcare" or "police")
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            facility_email = facility.get('contact_email') or facility.get('email')
            if not facility_email:
                Logger.warning(f"No email found for facility: {facility.get('name', 'Unknown')}")
                return False
            
            subject = f"Appointment Reminder - {appointment.patient_name}"
            
            if facility_type == "healthcare":
                body = self._generate_healthcare_reminder_body(appointment, facility)
            else:
                body = self._generate_police_reminder_body(appointment, facility)
            
            Logger.info(f"Sending appointment reminder email to: {facility_email}")
            return send_email(facility_email, subject, body)
            
        except Exception as e:
            Logger.error(f"Error sending appointment reminder email: {e}")
            return False
    
    def _generate_healthcare_reminder_body(
        self, 
        appointment: Appointment, 
        facility: Dict[str, Any]
    ) -> str:
        """Generate reminder email body for healthcare facility"""
        facility_name = facility.get('name', 'Healthcare Facility')
        appointment_date = appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")
        
        body = f"""
Dear {facility_name} Team,

This is a reminder for an upcoming appointment.

APPOINTMENT REMINDER:
====================
Patient Name: {appointment.patient_name}
Patient Phone: {appointment.patient_phone}
Appointment Date & Time: {appointment_date}
Appointment Type: {appointment.appointment_type.value.title()}
Duration: {appointment.duration_minutes} minutes
Reason for Visit: {appointment.reason_for_visit or 'Not specified'}
Assigned Doctor: {appointment.doctor_name or 'To be assigned'}

Please ensure all necessary preparations are made for this appointment.

Best regards,
{self.sender_name}
        """
        return body.strip()
    
    def _generate_police_reminder_body(
        self, 
        appointment: Appointment, 
        facility: Dict[str, Any]
    ) -> str:
        """Generate reminder email body for police facility"""
        facility_name = facility.get('name', 'Police Station')
        appointment_date = appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")
        
        body = f"""
Dear {facility_name} Team,

This is a reminder for an upcoming service request.

SERVICE REQUEST REMINDER:
========================
Requestor Name: {appointment.patient_name}
Contact Phone: {appointment.patient_phone}
Request Date & Time: {appointment_date}
Service Type: {appointment.appointment_type.value.title()}
Duration: {appointment.duration_minutes} minutes
Reason for Request: {appointment.reason_for_visit or 'Not specified'}

Please ensure all necessary preparations are made for this service request.

Best regards,
{self.sender_name}
        """
        return body.strip()
    
    async def send_appointment_cancellation_email(
        self, 
        appointment: Appointment, 
        facility: Dict[str, Any],
        facility_type: str = "healthcare",
        cancellation_reason: str = "Not specified"
    ) -> bool:
        """
        Send appointment cancellation email to facility
        
        Args:
            appointment: The appointment details
            facility: Facility information
            facility_type: Type of facility ("healthcare" or "police")
            cancellation_reason: Reason for cancellation
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            facility_email = facility.get('contact_email') or facility.get('email')
            if not facility_email:
                Logger.warning(f"No email found for facility: {facility.get('name', 'Unknown')}")
                return False
            
            subject = f"Appointment Cancellation - {appointment.patient_name}"
            
            if facility_type == "healthcare":
                body = self._generate_healthcare_cancellation_body(appointment, facility, cancellation_reason)
            else:
                body = self._generate_police_cancellation_body(appointment, facility, cancellation_reason)
            
            Logger.info(f"Sending appointment cancellation email to: {facility_email}")
            return send_email(facility_email, subject, body)
            
        except Exception as e:
            Logger.error(f"Error sending appointment cancellation email: {e}")
            return False
    
    def _generate_healthcare_cancellation_body(
        self, 
        appointment: Appointment, 
        facility: Dict[str, Any],
        cancellation_reason: str
    ) -> str:
        """Generate cancellation email body for healthcare facility"""
        facility_name = facility.get('name', 'Healthcare Facility')
        appointment_date = appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")
        
        body = f"""
Dear {facility_name} Team,

An appointment has been cancelled.

CANCELLED APPOINTMENT DETAILS:
=============================
Patient Name: {appointment.patient_name}
Patient Phone: {appointment.patient_phone}
Original Appointment Date & Time: {appointment_date}
Appointment Type: {appointment.appointment_type.value.title()}
Cancellation Reason: {cancellation_reason}
Cancelled At: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

Please update your records accordingly.

Best regards,
{self.sender_name}
        """
        return body.strip()
    
    def _generate_police_cancellation_body(
        self, 
        appointment: Appointment, 
        facility: Dict[str, Any],
        cancellation_reason: str
    ) -> str:
        """Generate cancellation email body for police facility"""
        facility_name = facility.get('name', 'Police Station')
        appointment_date = appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")
        
        body = f"""
Dear {facility_name} Team,

A service request has been cancelled.

CANCELLED SERVICE REQUEST DETAILS:
==================================
Requestor Name: {appointment.patient_name}
Contact Phone: {appointment.patient_phone}
Original Request Date & Time: {appointment_date}
Service Type: {appointment.appointment_type.value.title()}
Cancellation Reason: {cancellation_reason}
Cancelled At: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

Please update your records accordingly.

Best regards,
{self.sender_name}
        """
        return body.strip()
