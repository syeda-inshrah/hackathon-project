# Booking System Documentation

## Overview

The booking system provides comprehensive appointment management functionality for healthcare facilities. It includes scheduling, rescheduling, cancellation, and availability checking capabilities.

## Architecture

### Components

1. **Schemas** (`schemas/booking.py`)
   - `Appointment`: Main appointment model
   - `AppointmentCreate`: Model for creating appointments
   - `AppointmentUpdate`: Model for updating appointments
   - `AppointmentStatus`: Enum for appointment statuses
   - `AppointmentType`: Enum for appointment types

2. **Database Layer** (`database/booking.py`)
   - `BookingDB`: Database operations for appointments
   - Conflict detection and resolution
   - Availability checking
   - CRUD operations

3. **Tools Layer** (`tools/booking.py`)
   - `BookingTools`: Main booking functionality
   - Business logic validation
   - Error handling and logging
   - Tool functions for agent integration

4. **Agent Integration** (`agents_workflow/booking_agent/`)
   - `BookingAgent`: AI agent for handling booking requests
   - Natural language processing for appointment management
   - Integration with other system tools

## Features

### Core Functionality

1. **Schedule Appointment**
   - Create new appointments
   - Validate business hours (Monday-Saturday, 09:00-18:00)
   - Check for time conflicts
   - Support multiple appointment types

2. **Cancel Appointment**
   - Cancel existing appointments
   - Validate user ownership
   - Prevent cancellation of completed appointments

3. **Reschedule Appointment**
   - Change appointment date/time
   - Validate new time slot availability
   - Maintain appointment history

4. **View Appointments**
   - Get user's appointments
   - Filter by status, date, facility
   - Search functionality

5. **Check Availability**
   - Get available time slots for a facility
   - Real-time conflict detection
   - Configurable duration support

### Validation Rules

- **Business Hours**: Appointments only available Monday-Saturday, 09:00-18:00
- **Past Dates**: Cannot schedule appointments in the past
- **Conflict Detection**: Prevents double-booking
- **User Ownership**: Users can only manage their own appointments
- **Status Validation**: Prevents invalid state transitions

## API Reference

### Schedule Appointment

```python
await schedule_appointment(
    user_id: str,
    facility_id: int,
    facility_name: str,
    appointment_date: str,  # ISO format
    patient_name: str,
    patient_phone: str,
    appointment_type: str = "consultation",
    patient_age: Optional[int] = None,
    reason_for_visit: Optional[str] = None,
    notes: Optional[str] = None,
    doctor_name: Optional[str] = None,
    duration_minutes: int = 30
) -> Dict[str, Any]
```

**Response:**
```json
{
    "success": true,
    "message": "Appointment scheduled successfully for John Doe on 2024-01-15 at 10:00",
    "appointment_id": "uuid-string",
    "appointment_details": { ... }
}
```

### Cancel Appointment

```python
await cancel_appointment(
    appointment_id: str,
    user_id: Optional[str] = None
) -> Dict[str, Any]
```

**Response:**
```json
{
    "success": true,
    "message": "Appointment for John Doe on 2024-01-15 at 10:00 has been cancelled successfully",
    "appointment_id": "uuid-string",
    "cancelled_at": "2024-01-14T15:30:00"
}
```

### Reschedule Appointment

```python
await change_appointment_time(
    appointment_id: str,
    new_appointment_date: str,  # ISO format
    user_id: Optional[str] = None,
    new_duration_minutes: Optional[int] = None
) -> Dict[str, Any]
```

**Response:**
```json
{
    "success": true,
    "message": "Appointment for John Doe has been rescheduled to 2024-01-16 at 14:00",
    "appointment_id": "uuid-string",
    "old_date": "2024-01-15T10:00:00",
    "new_date": "2024-01-16T14:00:00",
    "updated_appointment": { ... }
}
```

### Get User Appointments

```python
await get_user_appointments(
    user_id: str,
    limit: int = 50
) -> Dict[str, Any]
```

**Response:**
```json
{
    "success": true,
    "appointments": [ ... ],
    "total_count": 5,
    "message": "Found 5 appointments"
}
```

### Get Available Slots

```python
await get_available_slots(
    facility_id: int,
    date: str,  # YYYY-MM-DD format
    duration_minutes: int = 30
) -> Dict[str, Any]
```

**Response:**
```json
{
    "success": true,
    "available_slots": [
        {
            "start_time": "2024-01-15T09:00:00",
            "end_time": "2024-01-15T09:30:00",
            "duration_minutes": 30
        }
    ],
    "facility_id": 12345,
    "date": "2024-01-15",
    "duration_minutes": 30,
    "message": "Found 18 available slots"
}
```

## Appointment Types

- `consultation`: General medical consultation
- `follow_up`: Follow-up appointment
- `emergency`: Emergency appointment
- `routine_checkup`: Routine health checkup
- `specialist`: Specialist consultation

## Appointment Statuses

- `scheduled`: Newly created appointment
- `confirmed`: Confirmed by patient/facility
- `cancelled`: Cancelled appointment
- `completed`: Completed appointment
- `no_show`: Patient did not show up

## Error Handling

All functions return a standardized response format:

```json
{
    "success": false,
    "error": "Error message describing what went wrong"
}
```

### Common Error Messages

- "Invalid appointment date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS)"
- "Appointments are not available on Sundays. Please choose Monday-Saturday."
- "Appointments are only available between 09:00 and 18:00. Please choose a different time."
- "Cannot schedule appointments in the past. Please choose a future date and time."
- "Time slot not available. Conflicts with existing appointment from 10:00 to 10:30"
- "Appointment not found. Please check the appointment ID."
- "You can only cancel your own appointments."
- "Cannot reschedule a cancelled appointment. Please schedule a new appointment instead."

## Database Schema

The appointments table includes the following fields:

- `appointment_id`: Unique identifier (UUID)
- `user_id`: ID of the user who booked the appointment
- `facility_id`: OSM ID of the health facility
- `facility_name`: Name of the health facility
- `appointment_date`: Date and time of the appointment
- `appointment_type`: Type of appointment
- `status`: Current status of the appointment
- `patient_name`: Name of the patient
- `patient_phone`: Phone number of the patient
- `patient_age`: Age of the patient (optional)
- `reason_for_visit`: Reason for the appointment (optional)
- `notes`: Additional notes (optional)
- `created_at`: When the appointment was created
- `updated_at`: When the appointment was last updated
- `doctor_name`: Name of the assigned doctor (optional)
- `duration_minutes`: Duration of the appointment in minutes

## Testing

Run the test script to verify functionality:

```bash
python src/national_agentic_ai_hackathon_2025_backend/scripts/test_booking.py
```

The test script includes:
- Basic functionality tests
- Validation logic tests
- Error handling tests
- Edge case testing

## Integration with AI Agents

The booking system integrates seamlessly with the AI agent workflow:

1. **Booking Agent**: Handles natural language appointment requests
2. **Orchestrator Agent**: Routes booking-related queries to the booking agent
3. **Medical Agent**: Can also access booking tools for medical consultations

## Security Considerations

- User ownership validation for appointment management
- Input validation and sanitization
- SQL injection prevention through parameterized queries
- Rate limiting for appointment creation (can be implemented)

## Performance Considerations

- Efficient conflict detection using database queries
- Indexed fields for fast lookups
- Pagination support for large appointment lists
- Caching for frequently accessed data (can be implemented)

## Future Enhancements

- Email/SMS notifications for appointment reminders
- Recurring appointment support
- Waitlist functionality
- Integration with calendar systems
- Advanced reporting and analytics
- Multi-language support
- Mobile app integration
