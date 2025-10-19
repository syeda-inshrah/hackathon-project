"""
Test script for the booking email tool
Demonstrates how to use the email functionality for different facility types
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from national_agentic_ai_hackathon_2025_backend.tools.email.booking_email_tool import send_booking_email
from national_agentic_ai_hackathon_2025_backend._debug import Logger


async def test_healthcare_booking_email():
    """Test sending booking confirmation email to healthcare facility"""
    Logger.info("Testing healthcare booking email...")
    
    # Sample appointment data
    appointment_data = {
        "user_id": "user_123",
        "facility_id": 12345,
        "facility_name": "Fatima Memorial Hospital",
        "appointment_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "appointment_type": "consultation",
        "status": "scheduled",
        "patient_name": "John Doe",
        "patient_phone": "+92-300-1234567",
        "patient_age": 35,
        "reason_for_visit": "Regular checkup",
        "notes": "Patient prefers morning appointments",
        "doctor_name": "Dr. Sarah Ahmed",
        "duration_minutes": 30,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Sample healthcare facility data
    facility_data = {
        "name": "Fatima Memorial Hospital",
        "addr_full": "Shadman, Lahore, Pakistan",
        "contact_number": "+92-42-111-123456",
        "contact_email": "appointments@fatimahospital.com",
        "amenity": "hospital",
        "speciality": "General Medicine"
    }
    
    # Send booking confirmation email
    result = await send_booking_email(
        action="send_confirmation",
        appointment_data=appointment_data,
        facility_data=facility_data,
        facility_type="healthcare"
    )
    
    Logger.info(f"Healthcare booking email result: {result}")
    return result


async def test_police_booking_email():
    """Test sending booking confirmation email to police station"""
    Logger.info("Testing police booking email...")
    
    # Sample appointment data for police service
    appointment_data = {
        "user_id": "user_456",
        "facility_id": 67890,
        "facility_name": "Gulshan-e-Iqbal Police Station",
        "appointment_date": (datetime.now() + timedelta(days=2)).isoformat(),
        "appointment_type": "consultation",
        "status": "scheduled",
        "patient_name": "Ahmed Ali",
        "patient_phone": "+92-300-9876543",
        "patient_age": 28,
        "reason_for_visit": "Report filing assistance",
        "notes": "Need help with filing a complaint",
        "doctor_name": None,  # Not applicable for police
        "duration_minutes": 45,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Sample police facility data
    facility_data = {
        "name": "Gulshan-e-Iqbal Police Station",
        "addr_full": "Gulshan-e-Iqbal, Karachi, Pakistan",
        "contact_number": "+92-21-12345678",
        "contact_email": "info@gulshanpolice.gov.pk",
        "amenity": "police",
        "jurisdiction": "Gulshan-e-Iqbal and surrounding areas"
    }
    
    # Send booking confirmation email
    result = await send_booking_email(
        action="send_confirmation",
        appointment_data=appointment_data,
        facility_data=facility_data,
        facility_type="police"
    )
    
    Logger.info(f"Police booking email result: {result}")
    return result


async def test_reminder_email():
    """Test sending reminder email"""
    Logger.info("Testing reminder email...")
    
    # Sample appointment data
    appointment_data = {
        "user_id": "user_789",
        "facility_id": 11111,
        "facility_name": "Aga Khan Hospital",
        "appointment_date": (datetime.now() + timedelta(hours=2)).isoformat(),
        "appointment_type": "emergency",
        "status": "confirmed",
        "patient_name": "Maria Khan",
        "patient_phone": "+92-300-5555555",
        "patient_age": 42,
        "reason_for_visit": "Emergency consultation",
        "notes": "Urgent medical attention required",
        "doctor_name": "Dr. Hassan Ali",
        "duration_minutes": 60,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Sample healthcare facility data
    facility_data = {
        "name": "Aga Khan Hospital",
        "addr_full": "Stadium Road, Karachi, Pakistan",
        "contact_number": "+92-21-111-911911",
        "contact_email": "emergency@agakhankh.org",
        "amenity": "hospital",
        "speciality": "Emergency Medicine"
    }
    
    # Send reminder email
    result = await send_booking_email(
        action="send_reminder",
        appointment_data=appointment_data,
        facility_data=facility_data,
        facility_type="healthcare"
    )
    
    Logger.info(f"Reminder email result: {result}")
    return result


async def test_cancellation_email():
    """Test sending cancellation email"""
    Logger.info("Testing cancellation email...")
    
    # Sample appointment data
    appointment_data = {
        "user_id": "user_999",
        "facility_id": 22222,
        "facility_name": "Lahore General Hospital",
        "appointment_date": (datetime.now() + timedelta(days=3)).isoformat(),
        "appointment_type": "routine_checkup",
        "status": "cancelled",
        "patient_name": "Fatima Sheikh",
        "patient_phone": "+92-300-7777777",
        "patient_age": 55,
        "reason_for_visit": "Annual checkup",
        "notes": "Patient cancelled due to personal reasons",
        "doctor_name": "Dr. Amina Khan",
        "duration_minutes": 30,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Sample healthcare facility data
    facility_data = {
        "name": "Lahore General Hospital",
        "addr_full": "Lahore, Punjab, Pakistan",
        "contact_number": "+92-42-12345678",
        "contact_email": "appointments@lahoregeneral.com",
        "amenity": "hospital",
        "speciality": "General Medicine"
    }
    
    # Send cancellation email
    result = await send_booking_email(
        action="send_cancellation",
        appointment_data=appointment_data,
        facility_data=facility_data,
        facility_type="healthcare",
        cancellation_reason="Patient requested cancellation due to personal reasons"
    )
    
    Logger.info(f"Cancellation email result: {result}")
    return result


async def main():
    """Run all email tests"""
    Logger.info("Starting email tool tests...")
    
    # Check if email configuration is available
    from national_agentic_ai_hackathon_2025_backend.config import Config
    
    if not Config.sender_email or not Config.app_password:
        Logger.error("❌ Email configuration not found. Please set SENDER_EMAIL and APP_PASSWORD environment variables.")
        Logger.info("To test email functionality:")
        Logger.info("1. Set up a Gmail account")
        Logger.info("2. Enable 2-factor authentication")
        Logger.info("3. Generate an app password")
        Logger.info("4. Set environment variables:")
        Logger.info("   export SENDER_EMAIL='your-email@gmail.com'")
        Logger.info("   export APP_PASSWORD='your-app-password'")
        return
    
    Logger.info("✅ Email configuration found. Running tests...")
    
    # Run tests
    try:
        # Test healthcare booking email
        await test_healthcare_booking_email()
        await asyncio.sleep(1)  # Small delay between emails
        
        # Test police booking email
        await test_police_booking_email()
        await asyncio.sleep(1)
        
        # Test reminder email
        await test_reminder_email()
        await asyncio.sleep(1)
        
        # Test cancellation email
        await test_cancellation_email()
        
        Logger.success("✅ All email tests completed!")
        
    except Exception as e:
        Logger.error(f"❌ Error during email tests: {e}")


if __name__ == "__main__":
    asyncio.run(main())
