"""
Example script demonstrating how to use the booking agent with email functionality
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from national_agentic_ai_hackathon_2025_backend.agents_workflow.booking_agent.agent import BookingAgent
from national_agentic_ai_hackathon_2025_backend.context.global_context import GlobalContext
from national_agentic_ai_hackathon_2025_backend.context.user import User
from national_agentic_ai_hackathon_2025_backend._debug import Logger


async def example_healthcare_booking():
    """Example of booking a healthcare appointment with email notification"""
    Logger.info("=== Healthcare Booking Example ===")
    
    # Create context
    user = User(
        user_id="user_123",
        name="John Doe",
        phone="+92-300-1234567",
        location="Lahore, Pakistan"
    )
    
    context = GlobalContext(user=user)
    
    # Create booking agent
    booking_agent = BookingAgent(context)
    
    # Example booking message
    booking_message = """
    I need to book an appointment at Fatima Memorial Hospital for a regular checkup. 
    My name is John Doe, phone number is +92-300-1234567, and I'm 35 years old. 
    I prefer morning appointments and need to see a general physician. 
    Please book it for tomorrow at 10:00 AM.
    """
    
    try:
        # Process booking request
        Logger.info("Processing healthcare booking request...")
        result = await booking_agent.run(booking_message)
        Logger.info(f"Booking result: {result}")
        
        # The booking agent will automatically use the email tool to send
        # confirmation emails to the healthcare facility
        
    except Exception as e:
        Logger.error(f"Error in healthcare booking: {e}")


async def example_police_booking():
    """Example of booking a police service with email notification"""
    Logger.info("=== Police Service Booking Example ===")
    
    # Create context
    user = User(
        user_id="user_456",
        name="Ahmed Ali",
        phone="+92-300-9876543",
        location="Karachi, Pakistan"
    )
    
    context = GlobalContext(user=user)
    
    # Create booking agent
    booking_agent = BookingAgent(context)
    
    # Example police service request
    police_message = """
    I need to visit Gulshan-e-Iqbal Police Station to file a complaint. 
    My name is Ahmed Ali, phone number is +92-300-9876543, and I'm 28 years old. 
    I need help with filing a complaint about a property dispute. 
    Please book an appointment for the day after tomorrow at 2:00 PM.
    """
    
    try:
        # Process police service request
        Logger.info("Processing police service request...")
        result = await booking_agent.run(police_message)
        Logger.info(f"Police service result: {result}")
        
        # The booking agent will automatically use the email tool to send
        # confirmation emails to the police station
        
    except Exception as e:
        Logger.error(f"Error in police service booking: {e}")


async def example_emergency_booking():
    """Example of booking an emergency appointment with email notification"""
    Logger.info("=== Emergency Booking Example ===")
    
    # Create context
    user = User(
        user_id="user_789",
        name="Maria Khan",
        phone="+92-300-5555555",
        location="Karachi, Pakistan"
    )
    
    context = GlobalContext(user=user)
    
    # Create booking agent
    booking_agent = BookingAgent(context)
    
    # Example emergency booking
    emergency_message = """
    I need an emergency appointment at Aga Khan Hospital immediately. 
    My name is Maria Khan, phone number is +92-300-5555555, and I'm 42 years old. 
    I'm experiencing severe chest pain and need urgent medical attention. 
    Please book an emergency appointment as soon as possible.
    """
    
    try:
        # Process emergency booking
        Logger.info("Processing emergency booking request...")
        result = await booking_agent.run(emergency_message)
        Logger.info(f"Emergency booking result: {result}")
        
        # The booking agent will automatically use the email tool to send
        # confirmation emails to the healthcare facility
        
    except Exception as e:
        Logger.error(f"Error in emergency booking: {e}")


async def main():
    """Run all booking examples"""
    Logger.info("Starting booking agent examples with email functionality...")
    
    # Check if email configuration is available
    from national_agentic_ai_hackathon_2025_backend.config import Config
    
    if not Config.sender_email or not Config.app_password:
        Logger.warning("⚠️ Email configuration not found. Emails will not be sent.")
        Logger.info("To enable email functionality:")
        Logger.info("1. Set up Gmail with 2-factor authentication")
        Logger.info("2. Generate an app password")
        Logger.info("3. Set environment variables:")
        Logger.info("   export SENDER_EMAIL='your-email@gmail.com'")
        Logger.info("   export APP_PASSWORD='your-app-password'")
        Logger.info("")
        Logger.info("Continuing with examples (emails will be simulated)...")
    else:
        Logger.success("✅ Email configuration found. Emails will be sent to facilities.")
    
    try:
        # Run examples
        await example_healthcare_booking()
        await asyncio.sleep(2)
        
        await example_police_booking()
        await asyncio.sleep(2)
        
        await example_emergency_booking()
        
        Logger.success("✅ All booking examples completed!")
        
    except Exception as e:
        Logger.error(f"❌ Error during examples: {e}")


if __name__ == "__main__":
    asyncio.run(main())
