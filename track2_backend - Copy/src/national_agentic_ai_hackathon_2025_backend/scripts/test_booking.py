#!/usr/bin/env python3
"""
Test script for booking functionality
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from national_agentic_ai_hackathon_2025_backend.tools.booking import (
    schedule_appointment,
    cancel_appointment,
    change_appointment_time,
    get_user_appointments,
    get_available_slots
)


async def test_booking_functionality():
    """Test the booking tools functionality"""
    print("🧪 Testing Booking Functionality")
    print("=" * 50)
    
    # Test data
    test_user_id = "test_user_123"
    test_facility_id = 12345
    test_facility_name = "Test Medical Center"
    test_patient_name = "John Doe"
    test_patient_phone = "+1234567890"
    
    # Test 1: Schedule an appointment
    print("\n1. Testing schedule_appointment...")
    future_date = (datetime.now() + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
    appointment_date = future_date.isoformat()
    
    result = await schedule_appointment(
        user_id=test_user_id,
        facility_id=test_facility_id,
        facility_name=test_facility_name,
        appointment_date=appointment_date,
        patient_name=test_patient_name,
        patient_phone=test_patient_phone,
        appointment_type="consultation",
        patient_age=30,
        reason_for_visit="General checkup",
        notes="First time patient"
    )
    
    print(f"Schedule result: {result}")
    
    if result["success"]:
        appointment_id = result["appointment_id"]
        print(f"✅ Appointment scheduled successfully! ID: {appointment_id}")
        
        # Test 2: Get user appointments
        print("\n2. Testing get_user_appointments...")
        appointments_result = await get_user_appointments(test_user_id)
        print(f"User appointments: {appointments_result}")
        
        # Test 3: Reschedule appointment
        print("\n3. Testing change_appointment_time...")
        new_date = (datetime.now() + timedelta(days=2)).replace(hour=14, minute=0, second=0, microsecond=0)
        new_appointment_date = new_date.isoformat()
        
        reschedule_result = await change_appointment_time(
            appointment_id=appointment_id,
            new_appointment_date=new_appointment_date,
            user_id=test_user_id
        )
        print(f"Reschedule result: {reschedule_result}")
        
        # Test 4: Get available slots
        print("\n4. Testing get_available_slots...")
        test_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        slots_result = await get_available_slots(
            facility_id=test_facility_id,
            date=test_date,
            duration_minutes=30
        )
        print(f"Available slots: {slots_result}")
        
        # Test 5: Cancel appointment
        print("\n5. Testing cancel_appointment...")
        cancel_result = await cancel_appointment(
            appointment_id=appointment_id,
            user_id=test_user_id
        )
        print(f"Cancel result: {cancel_result}")
        
    else:
        print(f"❌ Failed to schedule appointment: {result['error']}")
    
    print("\n" + "=" * 50)
    print("✅ Booking functionality test completed!")


async def test_validation():
    """Test validation logic"""
    print("\n🔍 Testing Validation Logic")
    print("=" * 50)
    
    test_user_id = "test_user_456"
    test_facility_id = 67890
    test_facility_name = "Test Hospital"
    test_patient_name = "Jane Smith"
    test_patient_phone = "+1234567891"
    
    # Test 1: Past date validation
    print("\n1. Testing past date validation...")
    past_date = (datetime.now() - timedelta(days=1)).isoformat()
    result = await schedule_appointment(
        user_id=test_user_id,
        facility_id=test_facility_id,
        facility_name=test_facility_name,
        appointment_date=past_date,
        patient_name=test_patient_name,
        patient_phone=test_patient_phone
    )
    print(f"Past date result: {result}")
    
    # Test 2: Sunday validation
    print("\n2. Testing Sunday validation...")
    # Find next Sunday
    days_ahead = 6 - datetime.now().weekday()  # Sunday is 6
    if days_ahead <= 0:
        days_ahead += 7
    sunday = datetime.now() + timedelta(days=days_ahead)
    sunday = sunday.replace(hour=10, minute=0, second=0, microsecond=0)
    
    result = await schedule_appointment(
        user_id=test_user_id,
        facility_id=test_facility_id,
        facility_name=test_facility_name,
        appointment_date=sunday.isoformat(),
        patient_name=test_patient_name,
        patient_phone=test_patient_phone
    )
    print(f"Sunday result: {result}")
    
    # Test 3: Outside business hours validation
    print("\n3. Testing outside business hours validation...")
    future_date = (datetime.now() + timedelta(days=1)).replace(hour=20, minute=0, second=0, microsecond=0)
    
    result = await schedule_appointment(
        user_id=test_user_id,
        facility_id=test_facility_id,
        facility_name=test_facility_name,
        appointment_date=future_date.isoformat(),
        patient_name=test_patient_name,
        patient_phone=test_patient_phone
    )
    print(f"Outside hours result: {result}")
    
    # Test 4: Invalid appointment type validation
    print("\n4. Testing invalid appointment type validation...")
    future_date = (datetime.now() + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
    
    result = await schedule_appointment(
        user_id=test_user_id,
        facility_id=test_facility_id,
        facility_name=test_facility_name,
        appointment_date=future_date.isoformat(),
        patient_name=test_patient_name,
        patient_phone=test_patient_phone,
        appointment_type="invalid_type"
    )
    print(f"Invalid type result: {result}")
    
    print("\n" + "=" * 50)
    print("✅ Validation test completed!")


if __name__ == "__main__":
    print("🚀 Starting Booking System Tests")
    print("=" * 60)
    
    # Run tests
    asyncio.run(test_booking_functionality())
    asyncio.run(test_validation())
    
    print("\n🎉 All tests completed!")
