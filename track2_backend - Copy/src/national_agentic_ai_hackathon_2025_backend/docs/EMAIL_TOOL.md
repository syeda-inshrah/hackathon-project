# Email Tool for Booking Agent

This document describes the email functionality integrated with the booking agent for sending notifications to police stations, healthcare facilities, and other organizations.

## Overview

The email tool provides comprehensive email functionality for the booking agent, allowing it to send various types of emails to different facilities:

- **Booking Confirmation Emails**: Sent when a new appointment is booked
- **Appointment Reminder Emails**: Sent as reminders for upcoming appointments
- **Cancellation Emails**: Sent when appointments are cancelled

## Features

### Supported Facility Types

1. **Healthcare Facilities**
   - Hospitals
   - Clinics
   - Pharmacies
   - Medical centers

2. **Police Facilities**
   - Police stations
   - Checkpoints
   - Law enforcement offices

### Email Types

1. **Booking Confirmation**
   - Patient/requestor details
   - Appointment/service details
   - Facility information
   - Contact information

2. **Appointment Reminders**
   - Upcoming appointment details
   - Patient/requestor information
   - Facility contact information

3. **Cancellation Notifications**
   - Cancelled appointment details
   - Cancellation reason
   - Facility contact information

## Configuration

### Environment Variables

Set the following environment variables for email functionality:

```bash
export SENDER_EMAIL="your-email@gmail.com"
export APP_PASSWORD="your-gmail-app-password"
```

### Gmail Setup

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this password as `APP_PASSWORD`

## Usage

### Integration with Booking Agent

The email tool is automatically integrated with the booking agent and can be used through the agent's tool system.

### Direct Usage

```python
from national_agentic_ai_hackathon_2025_backend.tools.email.booking_email_tool import send_booking_email

# Send booking confirmation email
result = await send_booking_email(
    action="send_confirmation",
    appointment_data={
        "user_id": "user_123",
        "facility_id": 12345,
        "facility_name": "Hospital Name",
        "appointment_date": "2024-01-15T10:00:00",
        "patient_name": "John Doe",
        "patient_phone": "+92-300-1234567",
        # ... other appointment details
    },
    facility_data={
        "name": "Hospital Name",
        "contact_email": "appointments@hospital.com",
        "addr_full": "Hospital Address",
        # ... other facility details
    },
    facility_type="healthcare"
)
```

### Tool Parameters

#### Action Types
- `send_confirmation`: Send booking confirmation email
- `send_reminder`: Send appointment reminder email
- `send_cancellation`: Send cancellation email

#### Appointment Data
```python
appointment_data = {
    "user_id": str,                    # Required: User ID
    "facility_id": int,                # Required: Facility OSM ID
    "facility_name": str,              # Required: Facility name
    "appointment_date": str,           # Required: ISO datetime string
    "patient_name": str,               # Required: Patient/requestor name
    "patient_phone": str,              # Required: Contact phone
    "patient_age": int,                # Optional: Patient age
    "appointment_type": str,           # Optional: consultation, follow_up, emergency, etc.
    "status": str,                     # Optional: scheduled, confirmed, cancelled, etc.
    "reason_for_visit": str,           # Optional: Reason for appointment
    "notes": str,                      # Optional: Additional notes
    "doctor_name": str,                # Optional: Assigned doctor
    "duration_minutes": int,           # Optional: Appointment duration
    "created_at": str,                 # Optional: Creation timestamp
    "updated_at": str                  # Optional: Last update timestamp
}
```

#### Facility Data
```python
facility_data = {
    "name": str,                       # Required: Facility name
    "contact_email": str,              # Optional: Primary email
    "email": str,                      # Optional: Alternative email
    "addr_full": str,                  # Optional: Full address
    "contact_number": str,             # Optional: Phone number
    "amenity": str,                    # Optional: Facility type
    "speciality": str,                 # Optional: Medical speciality
    "jurisdiction": str                # Optional: Police jurisdiction
}
```

## Email Templates

### Healthcare Facility Templates

#### Booking Confirmation
- Professional medical appointment format
- Patient details and medical information
- Doctor assignment and appointment specifics
- Facility contact information

#### Reminder
- Upcoming appointment details
- Patient information
- Preparation instructions

#### Cancellation
- Cancelled appointment details
- Cancellation reason
- Rescheduling information

### Police Facility Templates

#### Service Request Confirmation
- Service request details
- Requestor information
- Station jurisdiction and contact info
- Request type and urgency

#### Reminder
- Upcoming service request details
- Requestor information
- Station contact information

#### Cancellation
- Cancelled service request details
- Cancellation reason
- Alternative contact information

## Error Handling

The email tool includes comprehensive error handling:

- **Configuration Validation**: Checks for required email settings
- **Data Validation**: Validates appointment and facility data
- **Email Delivery**: Handles SMTP errors and delivery failures
- **Logging**: Detailed logging for debugging and monitoring

## Testing

### Test Script

Run the test script to verify email functionality:

```bash
cd src/national_agentic_ai_hackathon_2025_backend
python scripts/test_email_tool.py
```

### Test Scenarios

The test script includes:

1. **Healthcare Booking Email**: Tests medical appointment confirmation
2. **Police Booking Email**: Tests police service request confirmation
3. **Reminder Email**: Tests appointment reminder functionality
4. **Cancellation Email**: Tests cancellation notification

## Security Considerations

1. **App Passwords**: Use Gmail app passwords instead of regular passwords
2. **Environment Variables**: Store credentials in environment variables
3. **Email Validation**: Validate email addresses before sending
4. **Rate Limiting**: Implement rate limiting for bulk emails
5. **Data Privacy**: Ensure patient data is handled securely

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify Gmail app password is correct
   - Ensure 2-factor authentication is enabled
   - Check SENDER_EMAIL format

2. **Email Not Delivered**
   - Check recipient email address
   - Verify SMTP settings
   - Check spam folder

3. **Configuration Errors**
   - Verify environment variables are set
   - Check email configuration in config.py
   - Ensure all required fields are provided

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
from national_agentic_ai_hackathon_2025_backend._debug import Logger
Logger.set_level("DEBUG")
```

## Future Enhancements

1. **Email Templates**: Customizable email templates
2. **Bulk Emails**: Support for sending multiple emails
3. **Email Scheduling**: Schedule emails for future delivery
4. **Email Tracking**: Track email delivery and read status
5. **Multi-language Support**: Support for multiple languages
6. **Attachment Support**: Support for email attachments
7. **Email Analytics**: Track email performance and metrics

## API Reference

### EmailService Class

Main service class for email operations.

#### Methods

- `send_booking_confirmation_email()`: Send booking confirmation
- `send_appointment_reminder_email()`: Send appointment reminder
- `send_appointment_cancellation_email()`: Send cancellation notification

### BookingEmailTool

Tool wrapper for agent integration.

#### Functions

- `create_booking_email_tool()`: Create tool for agent
- `send_booking_email()`: Standalone email function

## Support

For issues or questions regarding the email tool:

1. Check the troubleshooting section
2. Review the test script for examples
3. Check the logs for error messages
4. Verify email configuration
