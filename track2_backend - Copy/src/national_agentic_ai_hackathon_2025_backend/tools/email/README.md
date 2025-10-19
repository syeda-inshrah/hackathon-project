# Email Tools for Booking Agent

This directory contains email functionality for the National Agentic AI Hackathon 2025 Backend booking system.

## Files

- `email_service.py` - Core email service class with templates and functionality
- `booking_email_tool.py` - Tool wrapper for agent integration
- `police.py` - (Existing) Police-specific email functionality
- `README.md` - This documentation file

## Quick Start

### 1. Configuration

Set up your email credentials:

```bash
export SENDER_EMAIL="your-email@gmail.com"
export APP_PASSWORD="your-gmail-app-password"
```

### 2. Basic Usage

```python
from national_agentic_ai_hackathon_2025_backend.tools.email.booking_email_tool import send_booking_email

# Send a booking confirmation email
result = await send_booking_email(
    action="send_confirmation",
    appointment_data={
        "user_id": "user_123",
        "facility_id": 12345,
        "facility_name": "Hospital Name",
        "appointment_date": "2024-01-15T10:00:00",
        "patient_name": "John Doe",
        "patient_phone": "+92-300-1234567"
    },
    facility_data={
        "name": "Hospital Name",
        "contact_email": "appointments@hospital.com"
    },
    facility_type="healthcare"
)
```

### 3. Integration with Booking Agent

The email tool is automatically integrated with the booking agent. When you use the booking agent, it will automatically send appropriate emails to facilities.

## Features

- ✅ **Healthcare Facility Emails**: Send emails to hospitals, clinics, pharmacies
- ✅ **Police Facility Emails**: Send emails to police stations, checkpoints
- ✅ **Multiple Email Types**: Confirmations, reminders, cancellations
- ✅ **Professional Templates**: Facility-specific email templates
- ✅ **Error Handling**: Comprehensive error handling and logging
- ✅ **Agent Integration**: Seamless integration with booking agent

## Email Types

1. **Booking Confirmation** (`send_confirmation`)
   - Sent when a new appointment is booked
   - Includes patient details and appointment information

2. **Appointment Reminder** (`send_reminder`)
   - Sent as a reminder for upcoming appointments
   - Includes appointment details and contact information

3. **Cancellation Notification** (`send_cancellation`)
   - Sent when appointments are cancelled
   - Includes cancellation reason and details

## Supported Facilities

### Healthcare Facilities
- Hospitals
- Clinics
- Pharmacies
- Medical centers
- Specialized medical facilities

### Police Facilities
- Police stations
- Checkpoints
- Law enforcement offices
- Security facilities

## Testing

Run the test script to verify functionality:

```bash
python scripts/test_email_tool.py
```

Run the booking examples:

```bash
python scripts/example_booking_with_email.py
```

## Configuration

### Gmail Setup

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this password as `APP_PASSWORD`

### Environment Variables

```bash
# Required
export SENDER_EMAIL="your-email@gmail.com"
export APP_PASSWORD="your-gmail-app-password"

# Optional (for testing)
export DEBUG_EMAIL="true"
```

## API Reference

### EmailService Class

Main service class for email operations.

```python
from national_agentic_ai_hackathon_2025_backend.tools.email.email_service import EmailService

email_service = EmailService()

# Send booking confirmation
await email_service.send_booking_confirmation_email(
    appointment=appointment_object,
    facility=facility_dict,
    facility_type="healthcare"
)
```

### BookingEmailTool

Tool wrapper for agent integration.

```python
from national_agentic_ai_hackathon_2025_backend.tools.email.booking_email_tool import create_booking_email_tool

# Create tool for agent
email_tool = create_booking_email_tool(context)
```

## Error Handling

The email tool includes comprehensive error handling:

- **Configuration Validation**: Checks for required email settings
- **Data Validation**: Validates appointment and facility data
- **SMTP Error Handling**: Handles email delivery errors
- **Logging**: Detailed logging for debugging

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

### Debug Mode

Enable debug logging:

```python
from national_agentic_ai_hackathon_2025_backend._debug import Logger
Logger.set_level("DEBUG")
```

## Security

- Use Gmail app passwords instead of regular passwords
- Store credentials in environment variables
- Validate email addresses before sending
- Handle patient data securely

## Future Enhancements

- [ ] Customizable email templates
- [ ] Bulk email support
- [ ] Email scheduling
- [ ] Email tracking
- [ ] Multi-language support
- [ ] Attachment support
- [ ] Email analytics

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review the test script for examples
3. Check the logs for error messages
4. Verify email configuration

## License

This email tool is part of the National Agentic AI Hackathon 2025 Backend project.
