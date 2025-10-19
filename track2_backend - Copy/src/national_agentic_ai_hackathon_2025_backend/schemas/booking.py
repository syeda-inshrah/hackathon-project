from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class AppointmentStatus(str, Enum):
    """Appointment status enumeration"""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class AppointmentType(str, Enum):
    """Appointment type enumeration"""
    CONSULTATION = "consultation"
    FOLLOW_UP = "follow_up"
    EMERGENCY = "emergency"
    ROUTINE_CHECKUP = "routine_checkup"
    SPECIALIST = "specialist"


class Appointment(BaseModel):
    """Appointment booking model"""
    appointment_id: Optional[str] = None
    user_id: str = Field(..., description="ID of the user booking the appointment")
    facility_id: int = Field(..., description="OSM ID of the health facility")
    facility_name: str = Field(..., description="Name of the health facility")
    appointment_date: datetime = Field(..., description="Date and time of the appointment")
    appointment_type: AppointmentType = Field(default=AppointmentType.CONSULTATION, description="Type of appointment")
    status: AppointmentStatus = Field(default=AppointmentStatus.SCHEDULED, description="Current status of the appointment")
    patient_name: str = Field(..., description="Name of the patient")
    patient_phone: str = Field(..., description="Phone number of the patient")
    patient_age: Optional[int] = Field(None, description="Age of the patient")
    reason_for_visit: Optional[str] = Field(None, description="Reason for the appointment")
    notes: Optional[str] = Field(None, description="Additional notes for the appointment")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="When the appointment was created")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, description="When the appointment was last updated")
    doctor_name: Optional[str] = Field(None, description="Name of the assigned doctor")
    duration_minutes: int = Field(default=30, description="Duration of the appointment in minutes")


class AppointmentCreate(BaseModel):
    """Model for creating a new appointment"""
    user_id: str
    facility_id: int
    facility_name: str
    appointment_date: datetime
    appointment_type: AppointmentType = AppointmentType.CONSULTATION
    patient_name: str
    patient_phone: str
    patient_age: Optional[int] = None
    reason_for_visit: Optional[str] = None
    notes: Optional[str] = None
    doctor_name: Optional[str] = None
    duration_minutes: int = 30


class AppointmentUpdate(BaseModel):
    """Model for updating an existing appointment"""
    appointment_date: Optional[datetime] = None
    appointment_type: Optional[AppointmentType] = None
    status: Optional[AppointmentStatus] = None
    patient_name: Optional[str] = None
    patient_phone: Optional[str] = None
    patient_age: Optional[int] = None
    reason_for_visit: Optional[str] = None
    notes: Optional[str] = None
    doctor_name: Optional[str] = None
    duration_minutes: Optional[int] = None


class AppointmentResponse(BaseModel):
    """Response model for appointment operations"""
    success: bool
    message: str
    appointment: Optional[Appointment] = None
    error: Optional[str] = None


class AppointmentListResponse(BaseModel):
    """Response model for listing appointments"""
    success: bool
    appointments: list[Appointment] = []
    total_count: int = 0
    error: Optional[str] = None
